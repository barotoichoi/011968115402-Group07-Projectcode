import os
print("Current working directory:", os.getcwd())
from csv_loader import load_csv, CSVFormatError
from deadlock_core import DeadlockCore


def main():
    core = DeadlockCore()

    try:
        operations = load_csv("input/input.csv")
    except (FileNotFoundError, CSVFormatError) as e:
        print("CSV ERROR:", e)
        return

    print("=== Loading operations from CSV ===")

    for op in operations:
        process = op["process"]
        action = op["action"]
        resource = op["resource"]

        # Tạo process & resource nếu chưa tồn tại
        if process not in core.processes:
            core.create_process(process)

        if resource not in core.resources:
            core.create_resource(resource)

        # Xử lý action
        if action == "hold":
            core.request_resource(process, resource)

        elif action == "request":
            core.request_resource(process, resource)

        elif action == "release":
            res = core.resources[resource]
            proc = core.processes[process]

            if res in proc.holding:
                proc.holding.remove(res)
                res.allocated_to = None
                print(f"{process} released {resource}")
            else:
                print(f"{process} cannot release {resource} (not holding)")

    print("\n=== Checking deadlock ===")
    if core.detect_deadlock():
        print("DEADLOCK DETECTED!")
    else:
        print("No deadlock detected.")


if __name__ == "__main__":
    main()
