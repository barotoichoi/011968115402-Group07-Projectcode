from collections import deque


class Resource:
    def __init__(self, resource_id: str):
        self.resource_id = resource_id
        self.owner = None
        self.waiting_queue = deque()

    def request(self, process_id: str) -> bool:
        if self.owner is None:
            self.owner = process_id
            print(f"[RESOURCE] {process_id} acquired {self.resource_id}")
            return True
        else:
            if process_id not in self.waiting_queue:
                self.waiting_queue.append(process_id)
                print(f"[RESOURCE] {process_id} waiting for {self.resource_id}")
            return False

    def release(self, process_id: str):
        if self.owner != process_id:
            print(f"[ERROR] {process_id} cannot release {self.resource_id}")
            return

        print(f"[RESOURCE] {process_id} released {self.resource_id}")

        if self.waiting_queue:
            next_process = self.waiting_queue.popleft()
            self.owner = next_process
            print(f"[RESOURCE] {self.resource_id} now assigned to {next_process}")
        else:
            self.owner = None

    def is_free(self) -> bool:
        return self.owner is None

    def status(self) -> dict:
        return {
            "resource_id": self.resource_id,
            "owner": self.owner,
            "waiting_queue": list(self.waiting_queue)
        }
