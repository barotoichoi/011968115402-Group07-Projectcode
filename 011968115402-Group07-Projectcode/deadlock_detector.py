from collections import defaultdict

class DeadlockDetector:
    def __init__(self, core):
        self.core = core
    
    def build_wait_for_graph(self):
        """Build wait-for graph: node A -> node B means A waits for B"""
        graph = defaultdict(list)

        # Sort process names để đảm bảo thứ tự nhất quán
        for process_name in sorted(self.core.processes.keys()):
            process = self.core.processes[process_name]
            if process.waiting_for:
                holder = process.waiting_for.allocated_to
                if holder:
                    graph[process.name].append(holder.name)

        return graph

    def detect_deadlock(self):
        """Detect cycle in wait-for graph using DFS"""
        graph = self.build_wait_for_graph()

        visited = set()
        rec_stack = set()  # Recursion stack để track cycle
        cycle_nodes = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in sorted(graph[node]):  # Sort để đảm bảo thứ tự nhất quán
                if neighbor not in visited:
                    if dfs(neighbor):
                        cycle_nodes.add(node)
                        return True
                elif neighbor in rec_stack:
                    # Found cycle
                    cycle_nodes.add(node)
                    return True

            rec_stack.remove(node)
            return False

        # Xử lý các node theo thứ tự nhất quán
        for node in sorted(graph.keys()):
            if node not in visited:
                if dfs(node):
                    return True, sorted(list(cycle_nodes))

        return False, []
