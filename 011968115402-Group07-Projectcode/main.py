import os
import sys
from pathlib import Path

from deadlock_core import DeadlockCore          # Đức
from csv_loader import load_csv                 # Trọng
from deadlock_detector import DeadlockDetector  # Phát
from csv_export import CSVLogger                # Kiệt
from GUI import DeadlockVisualizer              # Huy
# visualization.py                              # Bảo


def select_csv_file():
    """Let user select a CSV file from input folder"""
    script_dir = Path(__file__).parent
    input_dir = script_dir / "input"
    
    # Get all CSV files
    csv_files = sorted([f for f in input_dir.glob("*.csv") if f.is_file()])
    
    if not csv_files:
        print("No CSV files found in input folder!")
        return None
    
    # Display menu
    print("\n" + "="*50)
    print("Available Cases:")
    print("="*50)
    for idx, file in enumerate(csv_files, 1):
        print(f"{idx}. {file.name}")
    print(f"0. Exit")
    print("="*50)
    
    while True:
        try:
            choice = input("\nSelect a case (enter number): ").strip()
            
            if choice == "0":
                print("Exiting...")
                return None
            
            idx = int(choice) - 1
            if 0 <= idx < len(csv_files):
                selected = csv_files[idx]
                print(f"\nSelected: {selected.name}")
                return str(selected)
            else:
                print(f"Invalid choice. Please enter a number between 1 and {len(csv_files)}")
        except ValueError:
            print(f"Invalid input. Please enter a number between 1 and {len(csv_files)}")


def main():
    # In thư mục chạy (debug đường dẫn)
    print("Current working directory:", os.getcwd())

    # Khởi tạo Core
    core = DeadlockCore()

    # Load CSV input - with selection menu
    csv_file = None
    
    # If a command line argument is provided, use it
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        # Otherwise, let user select
        csv_file = select_csv_file()
    
    if not csv_file:
        return

    try:
        operations = load_csv(csv_file)
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

    # Print visualization statistics
    from visualization import run_visualization
    run_visualization(core)
    
    # Run GUI (this will block)
    print("\nLaunching GUI...")
    app = DeadlockVisualizer(core)
    app.run()

if __name__ == "__main__":
    main()
