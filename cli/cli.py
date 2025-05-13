import requests
import os
import sys
import json

API_URL = 'http://localhost:5000'

def check_api_connection():
    try:
        response = requests.get(f"{API_URL}/list_nodes")
        response.raise_for_status()  # Raises an exception for bad status codes
        return True
    except requests.exceptions.RequestException:
        print("\n❌ Error: Could not connect to the API server!")
        print("Please make sure the API server is running on http://localhost:5000")
        return False

def add_node():
    if not check_api_connection():
        return
        
    try:
        cpu_cores = int(input("Enter CPU cores: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
    
    try:
        # Send request to API Server to add the node
        response = requests.post(f"{API_URL}/add_node", json={"cpu_cores": cpu_cores})
        response.raise_for_status()
        data = response.json()
        
        node_id = data["node"]["node_id"]
        print(f"Node added successfully: {node_id}")
        
        # Start a Docker container for this node
        os.system(f"docker run -d --name node-{node_id} python:3.9-slim tail -f /dev/null")
    except requests.exceptions.RequestException as e:
        print(f"Failed to add node: {str(e)}")
    except KeyError:
        print("Invalid response from server")

def list_nodes():
    if not check_api_connection():
        return
        
    try:
        response = requests.get(f"{API_URL}/list_nodes")
        response.raise_for_status()
        data = response.json()
        print("\nCurrent Nodes:")
        for node_id, node in data.items():
            print(f"Node ID: {node_id}")
            print(f"Status: {node['status']}")
            print(f"CPU Cores: {node['cpu_cores']}")
            print(f"Pods: {len(node['pods'])}")
            print("---")
    except requests.exceptions.RequestException as e:
        print(f"Failed to list nodes: {str(e)}")

def get_algorithm_choice():
    print("\nSelect Scheduling Algorithm:")
    print("1. First Fit")
    print("2. Worst Fit")
    print("3. Best Fit")
    
    while True:
        try:
            choice = int(input("Enter choice (1-3): "))
            if 1 <= choice <= 3:
                algorithm_map = {
                    1: "first_fit",
                    2: "worst_fit",
                    3: "best_fit"
                }
                return algorithm_map[choice]
            else:
                print("Invalid choice! Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def launch_pod():
    if not check_api_connection():
        return
        
    try:
        cpu_cores = int(input("Enter CPU cores for pod: "))
    except ValueError:
        print("Invalid input! Please enter a number.")
        return
        
    algorithm = get_algorithm_choice()
    
    try:
        # Print the request data for debugging
        request_data = {
            'cpu_cores': cpu_cores,
            'algorithm': algorithm
        }
        print(f"\nSending request with data: {request_data}")
        
        response = requests.post(f"{API_URL}/launch_pod", 
                               json=request_data)
        
        # Print the response status and content for debugging
        print(f"Response Status: {response.status_code}")
        print(f"Response Content: {response.text}")
        
        response.raise_for_status()
        result = response.json()
        
        print("\nPod launched successfully!")
        print(f"Pod ID: {result['pod_id']}")
        print(f"Node ID: {result['node_id']}")
        print(f"Algorithm used: {result['algorithm_used']}")
    except requests.exceptions.HTTPError as e:
        print(f"\n❌ Failed to launch pod: HTTP {e.response.status_code}")
        print(f"Error message: {e.response.text}")
    except requests.exceptions.RequestException as e:
        print(f"\n❌ Failed to launch pod: {str(e)}")
    except KeyError:
        print("\n❌ Invalid response format from server")
    except json.JSONDecodeError:
        print("\n❌ Invalid JSON response from server")

def check_health(node_id):
    if not check_api_connection():
        return
        
    try:
        response = requests.post(f"{API_URL}/health_check", json={'node_id': node_id})
        response.raise_for_status()
        data = response.json()
        print(f"\nHealth Status for Node {node_id}:")
        print(f"Status: {data['node']['status']}")
        print(f"Last Heartbeat: {data['node']['last_heartbeat']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to check health: {str(e)}")

def update_health(node_id):
    if not check_api_connection():
        return
        
    try:
        # Send request to API Server to check the current health status
        response = requests.post(f"{API_URL}/health_check", json={'node_id': node_id})
        response.raise_for_status()
        data = response.json()

        if 'node' in data and 'status' in data['node']:
            if data['node']['status'] == 'Unhealthy':
                # Automatically update the health status to Healthy
                update_response = requests.post(f"{API_URL}/update_health", 
                                             json={'node_id': node_id, 'health_status': 'Healthy'})
                update_response.raise_for_status()
                print(f"Node {node_id} has been automatically updated to Healthy.")
            else:
                print(f"Node {node_id} is already Healthy.")
        else:
            print("Error: Invalid response format from server")
    except requests.exceptions.RequestException as e:
        print(f"Failed to update health: {str(e)}")

if __name__ == "__main__":
    print("\n=== Pod Scheduler CLI ===")
    print("Checking API connection...")
    
    if not check_api_connection():
        print("\nPlease start the API server first!")
        print("Run: python app.py in the api_server directory")
        sys.exit(1)
        
    while True:
        print("\n=== Pod Scheduler CLI ===")
        print("1️⃣ Add Node")
        print("2️⃣ List Nodes")
        print("3️⃣ Launch Pod")
        print("4️⃣ List Pods")
        print("5️⃣ Check Health")
        print("6️⃣ Update Health")
        print("7️⃣ Exit")
        print("=======================")
        
        choice = input("Enter choice: ")

        if choice == '1':
            add_node()
        elif choice == '2':
            list_nodes()
        elif choice == '3':
            launch_pod()
        elif choice == '4':
            list_nodes()  # Placeholder for pods listing
        elif choice == '5':
            node_id = input("Enter Node ID: ")
            check_health(node_id)
        elif choice == '6':
            node_id = input("Enter Node ID: ")
            update_health(node_id)
        elif choice == '7':
            print("Exiting...")
            break
        else:
            print("Invalid choice! Please enter a number between 1 and 7.")

