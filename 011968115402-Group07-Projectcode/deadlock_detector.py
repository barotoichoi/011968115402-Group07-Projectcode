from collections import defaultdict

class DeadlockDetector:
    def __init__(self, core):
        self.core = core
    
    def build_wait_for_graph(self):
        graph = defaultdict(list)

        for process in self.core.processes.values():
            if process.waiting_for:
                holder = process.waiting_for.allocated_to
                if holder:
                    graph[process.name].append(holder.name)

        return graph

    def detect_deadlock(self):
        graph = self.build_wait_for_graph()

        visited = set()
        stack = set()
        deadlocked = []

        def dfs(node):
            visited.add(node)
            stack.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        deadlocked.append(node)
                        return True
                elif neighbor in stack:
                    deadlocked.append(node)
                    return True

            stack.remove(node)
            return False

        for node in graph:
            if node not in visited:
                if dfs(node):
                    return True, list(set(deadlocked))

        return False, []
