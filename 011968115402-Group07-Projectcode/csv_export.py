import csv
import os


class CSVLogger:
    def __init__(self, core):
        self.core = core
        self.step = 0

        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, "output")
        os.makedirs(output_dir, exist_ok=True)

        self.output_path = os.path.join(output_dir, "result.csv")

        with open(self.output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "Step",
                "Process",
                "Action",
                "Resource",
                "Holding",
                "Waiting_For",
                "Deadlock"
            ])

    def log_step(self, process_name, action, resource_name):
        self.step += 1

        p = self.core.processes[process_name]

        holding = ",".join([r.name for r in p.holding]) or "None"
        waiting = p.waiting_for.name if p.waiting_for else "None"

        cycle = self.core.detect_deadlock()
        deadlock = " -> ".join(cycle) if cycle else "No"

        with open(self.output_path, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                self.step,
                process_name,
                action,
                resource_name,
                holding,
                waiting,
                deadlock
            ])
