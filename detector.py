from state import State

class Process:
    def __init__(self, pid):
        self.pid = pid
        self.state = State.WAITING
        self.holding = []
        self.requesting = []

    def add_resource(self, resource):
        self.holding.append(resource)

    def request_resource(self, resource):
        self.requesting.append(resource)
        self.state = State.WAITING

    def block(self):
        self.state = State.BLOCKED

    def run(self):
        self.state = State.RUNNING

    def __str__(self):
        return f"Process {self.pid} | State: {self.state.value}"
