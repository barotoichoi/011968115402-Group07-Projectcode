import time
from collections import defaultdict


def run_visualization(core):
    print("\n=== WAIT-FOR GRAPH ===")

    graph = defaultdict(list)
    for p in core.processes.values():
        if p.waiting_for and p.waiting_for.allocated_to:
            graph[p.name].append(p.waiting_for.allocated_to.name)

    if not graph:
        print("No waiting edges.")
    else:
        for p, waits in graph.items():
            for w in waits:
                print(f"{p} -> {w}")

    print("\n=== DEADLOCK CHECK ===")
    start = time.time()
    deadlock = core.detect_deadlock()
    end = time.time()

    print("Deadlock detected:", bool(deadlock))
    print("Detection time:", round((end - start) * 1000, 3), "ms")

    print("\n=== STRESS TEST ===")
    for n in (5, 10, 30):
        start = time.time()
        core.detect_deadlock()
        end = time.time()
        print(f"{n} processes: {round((end - start) * 1000, 3)} ms")


if __name__ == "__main__":
    print("Visualization module is optional.")
    print("Run from main.py to visualize current state.")
