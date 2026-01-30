import os

from deadlock_core import DeadlockCore
from csv_loader import load_csv
from deadlock_detector import DeadlockDetector
from GUI import DeadlockVisualizer
from visualization import DeadlockVisualizer as DeadlockVisualizer_Graph
from csv_export import CSVLogger

def main():
    # In thư mục hiện tại (rất hữu ích khi debug đường dẫn CSV)
    print("Current working directory:", os.getcwd())

    # 1. Khởi tạo core
    core = DeadlockCore()
    logger = CSVLogger(core)
    # 2. Load dữ liệu từ CSV
    try:
        operations = load_csv("input/input.csv")
    except Exception as e:
        print("CSV ERROR:", e)
        return

    # 3. Xử lý từng dòng trong CSV
    for op in operations:
        process = op["process"]
        action = op["action"]
        resource = op["resource"]

        # Tạo process / resource nếu chưa tồn tại
        if process not in core.processes:
            core.create_process(process)

        if resource not in core.resources:
            core.create_resource(resource)

        # Thực hiện hành động
        if action == "request":
            core.request_resource(process, resource)

        elif action == "release":
            core.release_resource(process, resource)

        elif action == "hold":
            # hold có thể xem như request (tuỳ thiết kế)
            core.request_resource(process, resource)
        logger.log_step(process, action, resource)
    # 4. Kiểm tra deadlock
    print("\n=== Checking deadlock ===")
    detector = DeadlockDetector(core)
    has_deadlock, processes = detector.detect_deadlock()
    
    if has_deadlock:
        print("DEADLOCK DETECTED!")
        print("Processes in deadlock:", processes)
    else:
        print("No deadlock.")

    # 5. Chạy GUI minh họa trước
    print("\n=== Running GUI ===")
    visualizer = DeadlockVisualizer(core)
    visualizer.run()
    
    # 6. Sau đó chạy visualization
    print("\n=== Running Visualization ===")
    visualizer_graph = DeadlockVisualizer_Graph(core)
    visualizer_graph.draw()
    visualizer_graph.window.mainloop()


if __name__ == "__main__":
    main()
