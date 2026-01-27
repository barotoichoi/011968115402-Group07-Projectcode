from state import State

class ResourceManager:
    def request(self, process, resource):
        # Resource rảnh → cấp
        if resource.is_free():
            process.add_resource(resource)
            process.state = State.RUNNING
        else:
            # Resource bận → block
            process.state = State.BLOCKED

    def release_all(self, process):
        process.release_resources()
