class DeadlockDetector:
    def __init__(self):
        self.graph = {}

    def add_edge(self, p1, p2):
        if p1 not in self.graph:
            self.graph[p1] = []
        self.graph[p1].append(p2)

    def detect_deadlock(self):
        visited = set()
        stack = set()

        for p in self.graph:
            if p not in visited:
                if self.dfs(p, visited, stack):
                    return True
        return False

    def dfs(self, p, visited, stack):
        visited.add(p)
        stack.add(p)

        for neighbor in self.graph.get(p, []):
            if neighbor not in visited:
                if self.dfs(neighbor, visited, stack):
                    return True
            elif neighbor in stack:
                return True

        stack.remove(p)
        return False


if __name__ == "__main__":
    d = DeadlockDetector()
    d.add_edge("P1", "P2")
    d.add_edge("P2", "P3")
    d.add_edge("P3", "P1")

    if d.detect_deadlock():
        print("Deadlock detected")
    else:
        print("No deadlock")
