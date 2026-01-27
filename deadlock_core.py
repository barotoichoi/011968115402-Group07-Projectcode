from collections import defaultdict
class Resource:
    def __init__(self, name):
        self.name = name
        self.allocated_to = None  
    def __repr__(self):
        return f"Resource({self.name})"
class Process:
    def __init__(self, name):
        self.name = name
        self.holding = []         
        self.waiting_for = None   
    def __repr__(self):
        return f"Process({self.name})"
class DeadlockCore:
    def __init__(self):
        self.processes = {}
        self.resources = {}
    def create_process(self, name):
        self.processes[name] = Process(name)
    def create_resource(self, name):
        self.resources[name] = Resource(name)
    def request_resource(self, process_name, resource_name):
        process = self.processes[process_name]
        resource = self.resources[resource_name]
        if resource.allocated_to is None:
            resource.allocated_to = process
            process.holding.append(resource)
            print(f"{process.name} acquired {resource.name}")
        else:
            process.waiting_for = resource
            print(f"{process.name} is waiting for {resource.name}")
    def build_wait_for_graph(self):
        graph = defaultdict(list)
        for process in self.processes.values():
            if process.waiting_for:
                holder = process.waiting_for.allocated_to
                if holder:
                    graph[process.name].append(holder.name)
        return graph
    def detect_deadlock(self):
        graph = self.build_wait_for_graph()
        visited = set()
        rec_stack = set()

        def dfs(node):
            visited.add(node)
            rec_stack.add(node)

            for neighbor in graph[node]:
                if neighbor not in visited:
                    if dfs(neighbor):
                        return True
                elif neighbor in rec_stack:
                    return True

            rec_stack.remove(node)
            return False

        for process in self.processes:
            if process not in visited:
                if dfs(process):
                    return True

        return False
if __name__ == "__main__":
    core = DeadlockCore()
    core.create_process("P1")
    core.create_process("P2")
    core.create_resource("R1")
    core.create_resource("R2")
    core.request_resource("P1", "R1")
    core.request_resource("P2", "R2")
    core.request_resource("P1", "R2")  
    core.request_resource("P2", "R1")  
    if core.detect_deadlock():
        print("\n DEADLOCK DETECTED!")
    else:
        print("\n No deadlock.")