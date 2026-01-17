class Resource:
    def __init__(self, resource_id):
        self.resource_id = resource_id
        self.owner = None

    def acquire(self, process_id):
        if self.owner is None:
            self.owner = process_id
            return True
        return False

    def release(self, process_id):
        if self.owner == process_id:
            self.owner = None
            return True
        return False
#chua xong
