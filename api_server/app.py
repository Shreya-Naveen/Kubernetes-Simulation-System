from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import uuid
from pod_scheduler import PodScheduler

app = Flask(__name__)

# In-memory storage for nodes and pods
nodes = {}
pods = {}  # ✅ Added missing global dictionary for pods

# Initialize the pod scheduler
pod_scheduler = PodScheduler(nodes)

# Helper function to generate a unique Node ID
def generate_node_id():
    return str(uuid.uuid4())

# Route to add a new node
@app.route('/add_node', methods=['POST'])
def add_node():
    data = request.get_json()
    cpu_cores = data.get('cpu_cores')

    # ✅ Validate CPU cores input
    if not isinstance(cpu_cores, int) or cpu_cores <= 0:
        return jsonify({"message": "CPU cores must be a positive integer!"}), 400

    node_id = generate_node_id()
    last_heartbeat = datetime.now()
    node = {
        "node_id": node_id,
        "cpu_cores": cpu_cores,
        "last_heartbeat": last_heartbeat,
        "status": "Healthy",
        "pods": []
    }

    nodes[node_id] = node
    return jsonify({"message": "Node added successfully", "node": node}), 200

# Route to list all nodes and their health status
@app.route('/list_nodes', methods=['GET'])
def list_nodes():
    for node_id, node in nodes.items():
        # ✅ Correctly update health status based on last heartbeat
        if datetime.now() - node["last_heartbeat"] > timedelta(seconds=120):  
            node['status'] = 'Unhealthy'
        else:
            node['status'] = 'Healthy'
    
    return jsonify(nodes), 200

# Route to simulate a health check (updates heartbeat)
@app.route('/health_check', methods=['POST'])
def health_check():
    data = request.get_json()
    node_id = data.get('node_id')

    if node_id not in nodes:
        return jsonify({"message": "Node not found"}), 404

    node = nodes[node_id]
    node['last_heartbeat'] = datetime.now()

    return jsonify({"message": "Heartbeat received", "node": node}), 200

# Route to update the health status of a node manually
@app.route('/update_health', methods=['POST'])
def update_health():
    data = request.get_json()
    node_id = data.get('node_id')
    health_status = data.get('health_status')

    if node_id not in nodes:
        return jsonify({"message": "Node not found"}), 404

    if health_status not in ["Healthy", "Unhealthy"]:
        return jsonify({"message": "Invalid health status! Must be 'Healthy' or 'Unhealthy'."}), 400

    node = nodes[node_id]
    node['status'] = health_status

    return jsonify({"message": "Health status updated", "node": node}), 200

# Route to launch a pod
@app.route('/launch_pod', methods=['POST'])
def launch_pod():
    data = request.get_json()
    cpu_cores_needed = data.get("cpu_cores", 0)
    algorithm = data.get("algorithm", "first_fit")  # Default to first_fit if not specified

    if cpu_cores_needed <= 0:
        return jsonify({"message": "CPU cores must be a positive integer!"}), 400

    if algorithm not in ["first_fit", "worst_fit", "best_fit"]:
        return jsonify({"message": "Invalid scheduling algorithm! Must be one of: first_fit, worst_fit, best_fit"}), 400

    # Use the pod scheduler to find an appropriate node
    result = pod_scheduler.launch_pod(cpu_cores_needed, algorithm)
    
    if "error" in result:
        return jsonify({"message": result["error"]}), 400
    
    # Add the pod to our global pods dictionary
    pod_id = result["pod_id"]
    pods[pod_id] = {"cpu_cores": cpu_cores_needed, "node_id": result["node_id"]}
    
    return jsonify({
        "message": "Pod launched successfully",
        "node_id": result["node_id"],
        "pod_id": pod_id,
        "algorithm_used": algorithm
    }), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

