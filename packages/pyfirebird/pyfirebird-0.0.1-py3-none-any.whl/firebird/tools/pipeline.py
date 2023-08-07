#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from typing import Dict, Callable
import logging
import logging.config
import argparse
import importlib

from .zk_path import ZKNamespaces

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
}

# logging.config.dictConfig(LOG_CONFIG)
logger = logging.getLogger(__name__)

import json
from uuid import uuid4
import docker
from kazoo.client import KazooClient

from firebird.rabbitmq import get_connection, RabbitMQ

def main(config):
    parser = argparse.ArgumentParser(
        description='Pipeline Tool'
    )
    parser.add_argument(
        "action", type=str, help="Specify action",
        choices=['register', 'list', 'execute', 'stop'],
        nargs=1
    )
    parser.add_argument(
        "-pmn", "--pipeline-module-name", type=str, required=False,
        help="Pipeline module name"
    )
    parser.add_argument(
        "-pid", "--pipeline-id", type=str, required=False, help="pipeline ID"
    )
    parser.add_argument(
        "-wc", "--worker-count", type=int, default=1, required=False,
        help="Worker count"
    )
    parser.add_argument(
        "-dhn", "--docker-host-name", type=str, required=False,
        help="Docker host name"
    )
    parser.add_argument(
        "-dcn", "--docker-container-name", type=str, required=False,
        help="Docker container name"
    )
    parser.add_argument(
        "-eid", "--executor-id", type=str, required=False, help="Executor ID"
    )
    args = parser.parse_args()
    action = args.action[0]

    if action == "register":
        register_command(config, args.pipeline_module_name)
    elif action == "list":
        list_command(config)
    elif action == "execute":
        execute_command(config, args.docker_host_name, args.docker_container_name, args.pipeline_id, args.worker_count)
    elif action == "stop":
        stop_command(config, args.pipeline_id, args.executor_id)

def register_command(config, pipeline_module_name):
    pipeline = importlib.import_module(pipeline_module_name).get_pipeline(None)
    pipeline_info = pipeline.to_json()

    mq = RabbitMQ(
        connection = get_connection(**config["rabbitmq"]),
        topic = pipeline.id
    )
    mq.initialize()

    zk = KazooClient(**config['zookeeper'])
    zk_namespace = ZKNamespaces(zk)
    zk.start()
    try:
        zk_namespace.register_pipeline(pipeline.id, pipeline_module_name, pipeline_info)
    finally:
        zk.stop()

def list_command(config):
    zk = KazooClient(**config['zookeeper'])
    zk_namespace = ZKNamespaces(zk)
    zk.start()
    try:
        pipeline_dict = zk_namespace.get_pipelines()
        for pipeline_id, pipeline in pipeline_dict.items():
            print(f"{pipeline_id}:")
            print(f"    module: {pipeline['module']}")
            if len(pipeline["executors"]) == 0:
                print("    executors: None")
            else:
                print("    executors:")
                for executor_id, executor in pipeline["executors"].items():
                    executor_info = executor["info"]
                    print(f"        {executor_id}:")
                    print(f"            docker_host_name      = {executor_info['docker_host_name']}")
                    print(f"            docker_container_name = {executor_info['docker_container_name']}")
                    print(f"            worker_count          = {executor_info['worker_count']}")
                    print(f"            start_time            = {executor_info['start_time']}")
                    print(f"            pid                   = {executor_info['pid']}")
    finally:
        zk.stop()

def stop_command(config:dict, pipeline_id:str, executor_id:str):
    zk = KazooClient(**config['zookeeper'])
    zk_namespace = ZKNamespaces(zk)
    zk.start()
    try:
        zk_namespace.stop_executor(pipeline_id, executor_id)
    finally:
        zk.stop()

def execute_command(config:dict, docker_host_name:str, docker_container_name:str, pipeline_id:str, worker_count:int):
    docker_client = docker.DockerClient(base_url=f"ssh://{docker_host_name}:22", use_ssh_client=True)
    r = docker_client.containers.run(
        "pulse-streaming", 
        name=docker_container_name, 
        hostname=docker_container_name, 
        environment={
            "ENV_HOME": "/mnt/DATA_DISK/mordor"
        }, 
        volumes = {
            "/mnt/DATA_DISK": {
                "bind": "/mnt/DATA_DISK",
                "mode": "rw"
            },
        },
        network = "sfnet",
        detach = True,
        command=[
            "python", "-u",
            "executor.py",
            "-pid", pipeline_id,
            "-dhn", docker_host_name,
            "-dcn", docker_container_name
        ]
    )


if __name__ == '__main__':
    main()
