import os

from deadlock_core import DeadlockCore          # Đức
from csv_loader import load_csv                 # Trọng
from deadlock_detector import DeadlockDetector  # Phát
from csv_export import CSVLogger                # Kiệt
from GUI import DeadlockVisualizer              # Huy
# visualization.py                              # Bảo


def main():
    # In thư mục chạy (debug đường dẫn)
    print("Current working directory:", os.getcwd())

    # Khởi tạo Core
    core = DeadlockCore()

    # Load CSV input
    try:
        operations = load_csv("input/input.csv")
    except Exception as e:
        print("CSV ERROR:", e)
        return

    # Khởi tạo Detector & Logger
    detector = DeadlockDetector(core)
    logger = CSVLogger(core)

    # Áp dụng từng thao tác + log
    for op in operations:
        process = op["process"]
        action = op["action"]
        resource = op["resource"]

        # Tạo process / resource nếu chưa tồn tại
        if process not in core.processes:
            core.create_process(process)
        if resource not in core.resources:
            core.create_resource(resource)

        # Thực hiện action
        if action in ("request", "hold"):
            core.request_resource(process, resource)
        elif action == "release":
            r = core.resources[resource]
            p = core.processes[process]

            if r in p.holding:
                p.holding.remove(r)
            if r.allocated_to == p:
                r.allocated_to = None

            for proc in core.processes.values():
                if proc.waiting_for == r:
                    proc.waiting_for = None

        # Log trạng thái sau mỗi bước
        logger.log_step(process, action, resource)

    # Detect deadlock
    has_deadlock, cycle = detector.detect_deadlock()

    print("\n=== DEADLOCK CHECK ===")
    if has_deadlock:
        print("DEADLOCK DETECTED:", " -> ".join(cycle))
    else:
        print("No deadlock detected.")

    # 6️⃣ Chạy GUI
    app = DeadlockVisualizer(core)
    app.run()

    from visualization import run_visualization

    viz = DeadlockVisualizer(core)
    run_visualization(core)

if __name__ == "__main__":
    main()
