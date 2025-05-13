import requests

API_URL = 'http://localhost:5000'

def list_nodes():
    response = requests.get(f"{API_URL}/list_nodes")
    print(response.json())

if __name__ == "__main__":
    list_nodes()

