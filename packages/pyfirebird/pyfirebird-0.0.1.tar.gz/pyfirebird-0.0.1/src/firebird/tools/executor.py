#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from typing import Dict, Callable
import logging
import logging.config
import argparse
import importlib

###################################################################
# the main process need to monitor child process
# - if main process got SIGTERM (killed), it will set quit_requested to True
#   this variable has been shared with child processes, so child process can check it and quit
#   accordingly
# - if a child process is terminated. The main process knows it
#   TODO: the main process can check the child process exit code and retry it if needed
# - if a child process got SIGTERM, it will quit.
###################################################################
LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(process)d - %(name)s - %(levelname)s - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "standard",
            "stream"  : "ext://sys.stdout"
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
    "loggers": {
        "pika": {
            "handlers": ["console"],
            "level":    "WARNING",
            "propagate": False
        },
        "kazoo": {
            "handlers": ["console"],
            "level":    "WARNING",
            "propagate": False
        }
    }
}

logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

import json
import signal
import time
from multiprocessing import Process, Value
from collections import deque
import socket
import os
from uuid import uuid4
from kazoo.client import KazooClient
from firebird.tools.zk_path import ZKNamespaces

from firebird.rabbitmq import get_connection, RabbitMQ

__APP_CONTEXT = {
    'quit_requested': Value('b', False)
}

__WORKER_CONTEXT = {
    'quit_requested': False
}
    
def __request_main_shutdown(signal_umber, frame):
    _, _ = signal_umber, frame
    __APP_CONTEXT['quit_requested'].value = True
    logger.info("main: Got SIGTERM")

def __request_worker_shutdown(signal_umber, frame):
    _, _ = signal_umber, frame
    __WORKER_CONTEXT['quit_requested'] = True
    logger.info("worker: Got SIGTERM")


def worker_main(config:dict, pipeline_module_name:str, pipeline_id:str, node_id, quit_requested):
    signal.signal(signal.SIGTERM, __request_worker_shutdown)  # regular kill command

    mq = RabbitMQ(
        connection = get_connection(**config["rabbitmq"]),
        topic = pipeline_id
    )
    pipeline = importlib.import_module(pipeline_module_name).get_pipeline(mq)
    
    if node_id is not None:
        # this is for generator
        generator = pipeline[node_id]
        generator.pump(quit_requested)
        return
    
    # otherwise, this is for message processing
    pipeline.message_loop(quit_requested)

def main(config):
    parser = argparse.ArgumentParser(
        description='Pipeline executor'
    )
    parser.add_argument(
        "-pid", "--pipeline-id", type=str, required=True, help="pipeline ID"
    )
    parser.add_argument(
        "-dhn", "--docker-host-name", type=str, required=True, help="docker host name"
    )
    parser.add_argument(
        "-dcn", "--docker-container-name", type=str, required=True, help="docker container name"
    )
    parser.add_argument(
        "-wc", "--worker-count", type=int, default=1, required=False,
        help="Worker count"
    )
    args = parser.parse_args()

    execute_pipeline(
        config, 
        pipeline_id=args.pipeline_id, 
        worker_count=args.worker_count, 
        docker_host_name=args.docker_host_name, 
        docker_container_name=args.docker_container_name
    )

def execute_pipeline(config:dict, *, pipeline_id:str, worker_count:int, docker_host_name:str, docker_container_name:str):
    logger.info(f"execute_pipeline: enter")
    logger.info(f"execute_pipeline: pipeline_id={pipeline_id}, worker_count={worker_count}, docker_host_name={docker_host_name}, docker_container_name={docker_container_name}")
    zk = KazooClient(**config['zookeeper'])
    zk_namespace = ZKNamespaces(zk)
    zk.start()
    try:
        pipeline = zk_namespace.get_pipeline(pipeline_id)
        pipeline_module_name = pipeline['module']
    finally:
        zk.stop()
    logger.info(f"execute_pipeline: pipeline_module_name={pipeline_module_name}")

    # try to import the pipeline
    pipeline = importlib.import_module(pipeline_module_name).get_pipeline(None)
    logger.info(f"execute_pipeline: pipeline acquired")

    executor_id = str(uuid4())
    logger.info(f"execute_pipeline: executor_id={executor_id}")
    zk.start()
    try:
        zk_namespace.register_executor(
            pipeline_id, 
            executor_id, 
            docker_host_name=docker_host_name, 
            docker_container_name=docker_container_name, 
            worker_count=worker_count
        )
    finally:
        zk.stop()
    logger.info(f"execute_pipeline: executor_id registered")

    active_processes = deque()
    terminated_processes = deque()
    signal.signal(signal.SIGTERM, __request_main_shutdown)  # regular kill command
    logger.info("Started")
    for node in pipeline.nodes:
        if node.is_generator():
            p = Process(
                target=worker_main,
                args=((config, pipeline_module_name, pipeline_id, node.id, __APP_CONTEXT['quit_requested']))
            )
            p.start()
            active_processes.append(p)
    for i in range(worker_count):
        p = Process(
            target=worker_main,
            args=((config, pipeline_module_name, pipeline_id, None, __APP_CONTEXT['quit_requested']))
        )
        p.start()
        active_processes.append(p)

    logger.info(f"execute_pipeline: all worker started")

    ctx = {
        "stop_requested": False
    }
    def watch_stop(event):
        if event.type == "CHANGED":
            stop = zk_namespace.get_executor_stop(pipeline_id, executor_id)
            if stop:
                logger.info(f"execute_pipeline: stop requested!")
                __APP_CONTEXT['quit_requested'].value = True
                ctx["stop_requested"] = True
            else:
                zk_namespace.watch_executor(pipeline_id, executor_id, watch_stop)
                logger.info(f"execute_pipeline: suspecious stop change!")
        else:
            # keep monitor if we encounter non CHANGED event
            zk_namespace.watch_executor(pipeline_id, executor_id, watch_stop)

    zk.start()
    zk_namespace.watch_executor(pipeline_id, executor_id, watch_stop)

    while True:
        if len(active_processes) == 0:
            break
        tmp = active_processes
        active_processes = deque()
        for p in tmp:
            if p.is_alive():
                active_processes.append(p)
            else:
                p.join()
                logger.info(f"execute_pipeline: pid={p.pid} is terminated!")
                terminated_processes.append(p)
        time.sleep(1)
    zk.stop()

    logger.info(f"execute_pipeline: all worker stopped")
    zk.start()
    try:
        zk_namespace.unregister_executor(pipeline_id, executor_id)
    finally:
        zk.stop()
    logger.info(f"execute_pipeline: executor {executor_id} unregistered")
    logger.info(f"execute_pipeline: exit")

if __name__ == '__main__':
    main()
