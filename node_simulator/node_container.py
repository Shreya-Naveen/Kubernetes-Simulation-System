# node_simulator/node_container.py

import time
import requests
import os
from uuid import uuid4

node_id = os.environ['NODE_ID']
api_url = 'http://host.docker.internal:5000/health_check'  # Adjust for Docker network

def send_heartbeat():
    while True:
        response = requests.post(api_url, json={'node_id': node_id})
        print(f"Heartbeat sent. Status: {response.status_code}")
        time.sleep(10)

if __name__ == "__main__":
    send_heartbeat()

