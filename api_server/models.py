import uuid
from datetime import datetime

class Node:
    def __init__(self, cpu_cores, memory_gb):
        self.node_id = str(uuid.uuid4())
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.pods = []
        self.last_heartbeat = datetime.utcnow()
        self.status = "Healthy"

    def to_dict(self):
        return {
            "node_id": self.node_id,
            "cpu_cores": self.cpu_cores,
            "memory_gb": self.memory_gb,
            "pods": [pod.to_dict() for pod in self.pods],
            "last_heartbeat": self.last_heartbeat.isoformat(),
            "status": self.status
        }

class Pod:
    def __init__(self, cpu_cores, memory_gb):
        self.pod_id = str(uuid.uuid4())
        self.cpu_cores = cpu_cores
        self.memory_gb = memory_gb
        self.node_id = None

    def to_dict(self):
        return {
            "pod_id": self.pod_id,
            "cpu_cores": self.cpu_cores,
            "memory_gb": self.memory_gb,
            "node_id": self.node_id
        }

