class Resource:
    def __init__(self, name):
        self.name = name
        self.owner = None  # Process that currently owns the resource


class Process:
    def __init__(self, name):
        self.name = name
        self.held_resources = []
        self.waiting_for = None


class DeadlockSimulator:
    def __init__(
        self,
        mutual_exclusion=True,
        hold_and_wait=True,
        no_preemption=True,
        circular_wait=True
    ):
        self.mutual_exclusion = mutual_exclusion
        self.hold_and_wait = hold_and_wait
        self.no_preemption = no_preemption
        self.circular_wait = circular_wait

        self.p1 = Process("P1")
        self.p2 = Process("P2")

        self.r1 = Resource("R1")
        self.r2 = Resource("R2")

    def allocate(self, process, resource):
        # Resource is free
        if resource.owner is None:
            resource.owner = process
            process.held_resources.append(resource)
            print(f"{process.name} acquired {resource.name}")
            return True

        # Mutual Exclusion disabled → shared resource allowed
        if not self.mutual_exclusion:
            print(f"{process.name} shared {resource.name}")
            process.held_resources.append(resource)
            return True

        # Resource is busy
        print(f"{process.name} cannot acquire {resource.name} (already owned)")
        process.waiting_for = resource
        return False

    def simulate(self):
        print("\n=== START DEADLOCK SIMULATION ===")

        # Step 1: Initial allocation
        self.allocate(self.p1, self.r1)
        self.allocate(self.p2, self.r2)

        # Step 2: Hold and Wait condition
        if self.hold_and_wait:
            print("\n[Hold and Wait] ENABLED")
            self.allocate(self.p1, self.r2)
            self.allocate(self.p2, self.r1)
        else:
            print("\n[Hold and Wait] DISABLED")
            self.p1.held_resources.clear()
            self.p2.held_resources.clear()

        # Step 3: No Preemption condition
        if not self.no_preemption:
            print("\n[No Preemption] DISABLED → resources are preempted")
            self.r1.owner = None
            self.r2.owner = None

        
        deadlock = (
            self.mutual_exclusion
            and self.hold_and_wait
            and self.no_preemption
            and self.circular_wait
            and self.p1.waiting_for == self.r2
            and self.p2.waiting_for == self.r1
        )

        print("\n=== RESULT ===")
        if deadlock:
            print("DEADLOCK OCCURRED")
        else:
            print("NO DEADLOCK")

        return deadlock


def main():
    print("===== DEADLOCK CONDITION SIMULATOR =====")

    
    simulator = DeadlockSimulator(
        mutual_exclusion=True,
        hold_and_wait=True,
        no_preemption=True,
        circular_wait=True
    )

    simulator.simulate()


if __name__ == "__main__":
    main()
