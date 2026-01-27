class Resource:
    def __init__(self, name):
        self.name = name
        self.allocated_to = None  # Process đang giữ resource

    def is_free(self):
        return self.allocated_to is None

    def __str__(self):
        if self.is_free():
            return f"Resource {self.name} is free"
        return f"Resource {self.name} allocated to Process {self.allocated_to.pid}"
