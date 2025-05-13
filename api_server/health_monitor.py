# api_server/health_monitor.py

class HealthMonitor:
    def __init__(self, node_manager):
        self.node_manager = node_manager
    
    def check_health(self, node_id):
        for node in self.node_manager.list_nodes():
            if node['node_id'] == node_id:
                return node['status']
        return 'Node not found'

