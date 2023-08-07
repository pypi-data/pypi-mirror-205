import json
import socket
import os
from datetime import datetime

class ZKNamespaces:
    def __init__(self, zk):
        self.zk = zk
    
    def register_pipeline(self, pipeline_id, pipeline_module_name, pipeline_info):
        self.zk.ensure_path("/pipelines")
        pipeline_path = f"/pipelines/{pipeline_id}"
        if self.zk.exists(pipeline_path):
            raise Exception(f"Pipeline {pipeline_id} is already registered!")
        
        self.zk.ensure_path(pipeline_path)
        self.zk.create(f"{pipeline_path}/info", json.dumps(pipeline_info).encode("utf-8"))
        self.zk.create(f"{pipeline_path}/module", pipeline_module_name.encode("utf-8"))
    
    def get_pipelines(self):
        if not self.zk.exists("/pipelines"):
            return {}
        pipeline_dict = {}
        for pipeline_id in self.zk.get_children("/pipelines"):
            pipeline_dict[pipeline_id] = self.get_pipeline(pipeline_id)
        return pipeline_dict

    def get_executor(self, pipeline_id, executor_id):
        executor_path = f"/pipelines/{pipeline_id}/executors/{executor_id}"
        if not self.zk.exists(executor_path):
            return None
        v, _ = self.zk.get(f"{executor_path}/info")
        executor_info = json.loads(v.decode("utf-8"))
        v, _ = self.zk.get(f"{executor_path}/stop")
        stop = v == b'1'
        return {
            "info": executor_info,
            "stop": stop
        }

    def get_executor_stop(self, pipeline_id, executor_id):
        executor_path = f"/pipelines/{pipeline_id}/executors/{executor_id}"
        v, _ = self.zk.get(f"{executor_path}/stop")
        return v == b'1'

    def get_pipeline(self, pipeline_id):
        pipeline_path = f"/pipelines/{pipeline_id}"
        if not self.zk.exists(pipeline_path):
            return None

        v, _ = self.zk.get(f"{pipeline_path}/info")
        pipeline_info = json.loads(v.decode("utf-8"))
        v, _ = self.zk.get(f"{pipeline_path}/module")
        module = v.decode("utf-8")

        executor_ids_path = f"/pipelines/{pipeline_id}/executors"
        executors = {}
        if self.zk.exists(executor_ids_path):
            for executor_id in self.zk.get_children(executor_ids_path):
                executors[executor_id] = self.get_executor(pipeline_id, executor_id)
        
        return {
            "info": pipeline_info,
            "module": module,
            "executors": executors
        }


    def register_executor(self, pipeline_id, executor_id, *, docker_host_name, docker_container_name, worker_count):
        if not self.zk.exists(f"/pipelines/{pipeline_id}"):
            raise Exception(f"Pipeline {pipeline_id} does not exist!")
    
        executors_path = f"/pipelines/{pipeline_id}/executors"
        self.zk.ensure_path(executors_path)

        executor_path = f"{executors_path}/{executor_id}"
        if self.zk.exists(executor_path):
            raise Exception(f"Executor {executor_id} already exist!")
        
        self.zk.ensure_path(executor_path)

        executor_info = {
            "docker_host_name": docker_host_name,
            "docker_container_name": docker_container_name,
            "worker_count": worker_count,
            "start_time": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "pid": os.getpid(),
        }
        self.zk.create(f"{executor_path}/info", json.dumps(executor_info).encode("utf-8"))
        self.zk.create(f"{executor_path}/stop", b'0')

    def watch_executor(self, pipeline_id, executor_id, callback):
        _, _ = self.zk.get(f"/pipelines/{pipeline_id}/executors/{executor_id}/stop", callback)

    def unregister_executor(self, pipeline_id, executor_id):
        executor_path = f"/pipelines/{pipeline_id}/executors/{executor_id}"
        if not self.zk.exists(executor_path):
            raise Exception(f"Executor {executor_id} does not exist!")
        self.zk.delete(executor_path, recursive=True)

    def stop_executor(self, pipeline_id, executor_id):
        executor_path = f"/pipelines/{pipeline_id}/executors/{executor_id}"
        if not self.zk.exists(executor_path):
            raise Exception(f"Executor {executor_id} does not exist!")
    
        self.zk.set(f"{executor_path}/stop", b'1')
