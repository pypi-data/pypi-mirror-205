#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from typing import Dict, Callable
import logging
import logging.config
import importlib
from uuid import uuid4
from firebird.rabbitmq import get_connection, RabbitMQ
from firebird import zkdb
import docker

logger = logging.getLogger(__name__)

def register_command(config:dict, pipeline_module_name:str):
    pipeline = importlib.import_module(pipeline_module_name).get_pipeline(None)
    pipeline_info = pipeline.to_json()

    mq = RabbitMQ(
        connection = get_connection(**config["rabbitmq"]),
        topic = pipeline.id
    )
    # create rabbitmq topic, etc
    mq.initialize()

    with zkdb(**config['zookeeper']) as db:
        db.register_pipeline(pipeline.id, pipeline_module_name, pipeline_info)

def list_command(config):
    with zkdb(**config['zookeeper']) as db:
        pipeline_dict = db.get_pipelines()

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

def stop_command(config:dict, pipeline_id:str, executor_id:str):
    with zkdb(**config['zookeeper']) as db:
        db.stop_executor(pipeline_id, executor_id)

def execute_command(config:dict, docker_host_name:str, docker_container_name:str, pipeline_id:str, worker_count:int):
    docker_client = docker.DockerClient(base_url=f"ssh://{docker_host_name}:22", use_ssh_client=True)
    try:
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
    finally:
        docker_client.close()
