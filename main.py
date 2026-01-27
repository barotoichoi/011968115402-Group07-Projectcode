class DeadlockDetector:
    def __init__(self):
        self.graph = {}

    def add_edge(self, p1, p2):
        """Add edge p1 -> p2 (p1 waits for p2)"""
        if p1 not in self.graph:
            self.graph[p1] = []
        self.graph[p1].append(p2)

    def detect_deadlock(self):
        visited = set()
        rec_stack = set()

        for node in self.graph:
            if node not in visited:
                if self._dfs(node, visited, rec_stack):
                    return True
        return False

    def _dfs(self, node, visited, rec_stack):
        visited.add(node)
        rec_stack.add(node)

        for neighbor in self.graph.get(node, []):
            if neighbor not in visited:
                if self._dfs(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

if __name__ == "__main__":
    detector = DeadlockDetector()

    detector.add_edge("P1", "P2")
    detector.add_edge("P2", "P3")
    detector.add_edge("P3", "P1") 

    if detector.detect_deadlock():
        print("Deadlock detected!")
    else:
        print("No deadlock.")
