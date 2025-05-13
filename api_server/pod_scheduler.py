# api_server/pod_scheduler.py
import uuid

class PodScheduler:
    def __init__(self, node_manager):
        self.node_manager = node_manager
    
    def launch_pod(self, cpu_cores, algorithm='first_fit'):
        """Launch a pod with specified CPU cores using the chosen scheduling algorithm.
        
        Args:
            cpu_cores (int): Number of CPU cores required by the pod
            algorithm (str): Scheduling algorithm to use. Options:
                - 'first_fit': Selects first available node (default)
                - 'worst_fit': Selects node with most available resources
                - 'best_fit': Selects node with least available resources that can fit the pod
        
        Returns:
            dict: Contains pod_id and node_id if successful, or error message if failed
        """
        if algorithm not in ['first_fit', 'worst_fit', 'best_fit']:
            return {'error': 'Invalid scheduling algorithm. Must be one of: first_fit, worst_fit, best_fit'}
            
        available_node = self._find_available_node(cpu_cores, algorithm)
        if available_node:
            pod_id = str(uuid.uuid4())
            available_node['pods'].append(pod_id)
            return {'pod_id': pod_id, 'node_id': available_node['node_id']}
        else:
            return {'error': 'No sufficient resources available'}
    
    def _find_available_node(self, cpu_cores, algorithm):
        """Find an available node based on the selected scheduling algorithm."""
        if algorithm == 'first_fit':
            return self._first_fit(cpu_cores)
        elif algorithm == 'worst_fit':
            return self._worst_fit(cpu_cores)
        elif algorithm == 'best_fit':
            return self._best_fit(cpu_cores)
    
    def _first_fit(self, cpu_cores):
        """First Fit algorithm: Selects the first node that has sufficient resources."""
        for node in self.node_manager.values():
            if node['status'] == 'Healthy' and self._get_available_cores(node) >= cpu_cores:
                return node
        return None
    
    def _worst_fit(self, cpu_cores):
        """Worst Fit algorithm: Selects the node with the most available resources."""
        worst_fit_node = None
        max_available_cores = 0
        
        for node in self.node_manager.values():
            if node['status'] == 'Healthy':
                available_cores = self._get_available_cores(node)
                if available_cores >= cpu_cores and available_cores > max_available_cores:
                    max_available_cores = available_cores
                    worst_fit_node = node
        
        return worst_fit_node
    
    def _best_fit(self, cpu_cores):
        """Best Fit algorithm: Selects the node with the least available resources that can still accommodate the pod."""
        best_fit_node = None
        min_available_cores = float('inf')
        
        for node in self.node_manager.values():
            if node['status'] == 'Healthy':
                available_cores = self._get_available_cores(node)
                if available_cores >= cpu_cores and available_cores < min_available_cores:
                    min_available_cores = available_cores
                    best_fit_node = node
        
        return best_fit_node
    
    def _get_available_cores(self, node):
        """Calculate available CPU cores for a node."""
        # Each pod uses 1 CPU core in our system
        used_cores = len(node['pods'])
        return node['cpu_cores'] - used_cores

