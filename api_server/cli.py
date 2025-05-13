import requests
import json

def print_menu():
    print("\n=== Pod Scheduler CLI ===")
    print("1. First Fit Algorithm")
    print("2. Worst Fit Algorithm")
    print("3. Best Fit Algorithm")
    print("4. Exit")
    print("=======================")

def get_algorithm_choice():
    while True:
        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if 1 <= choice <= 4:
                return choice
            else:
                print("Invalid choice! Please enter a number between 1 and 4.")
        except ValueError:
            print("Invalid input! Please enter a number.")

def get_cpu_cores():
    while True:
        try:
            cores = int(input("Enter number of CPU cores needed: "))
            if cores > 0:
                return cores
            else:
                print("CPU cores must be a positive integer!")
        except ValueError:
            print("Invalid input! Please enter a number.")

def launch_pod(algorithm, cpu_cores):
    url = "http://localhost:5000/launch_pod"
    data = {
        "cpu_cores": cpu_cores,
        "algorithm": algorithm
    }
    
    try:
        response = requests.post(url, json=data)
        result = response.json()
        
        if response.status_code == 200:
            print("\nPod launched successfully!")
            print(f"Pod ID: {result['pod_id']}")
            print(f"Node ID: {result['node_id']}")
            print(f"Algorithm used: {result['algorithm_used']}")
        else:
            print(f"\nError: {result['message']}")
    except requests.exceptions.RequestException as e:
        print(f"\nError connecting to server: {e}")

def main():
    while True:
        print_menu()
        choice = get_algorithm_choice()
        
        if choice == 4:
            print("Exiting...")
            break
            
        algorithm_map = {
            1: "first_fit",
            2: "worst_fit",
            3: "best_fit"
        }
        
        algorithm = algorithm_map[choice]
        cpu_cores = get_cpu_cores()
        
        print(f"\nLaunching pod with {algorithm} algorithm...")
        launch_pod(algorithm, cpu_cores)

if __name__ == "__main__":
    main() 