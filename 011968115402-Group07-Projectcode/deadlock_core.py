class Resource:
    def __init__(self, name):
        self.name = name
        self.allocated_to = None  

    def __repr__(self):
        owner = self.allocated_to.name if self.allocated_to else None
        return f"Resource({self.name}, allocated_to={owner})"

class Process:
    def __init__(self, name):
        self.name = name
        self.holding = []         
        self.waiting_for = None   

    def __repr__(self):
        holding_names = [r.name for r in self.holding]
        waiting = self.waiting_for.name if self.waiting_for else None
        return f"Process({self.name}, holding={holding_names}, waiting_for={waiting})"

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

    def release_resource(self, process_name, resource_name):
        process = self.processes.get(process_name)
        resource = self.resources.get(resource_name)
        if not process or not resource:
            return

        if resource in process.holding:
            process.holding.remove(resource)

        if resource.allocated_to == process:
            resource.allocated_to = None

        # clear waiting_for for any processes waiting for this resource
        for proc in self.processes.values():
            if proc.waiting_for == resource:
                proc.waiting_for = None

    def detect_deadlock(self):
        try:
            from deadlock_detector import DeadlockDetector
        except Exception:
            return []

        detector = DeadlockDetector(self)
        has_deadlock, processes = detector.detect_deadlock()
        return processes if has_deadlock else []

    def show_state(self):
        print("\n PROCESS STATE ")
        for p in self.processes.values():
            print(p)

        print("\n RESOURCE STATE")
        for r in self.resources.values():
            print(r)

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

    core.show_state()
