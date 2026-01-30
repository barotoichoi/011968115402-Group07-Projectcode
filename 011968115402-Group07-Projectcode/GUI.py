import tkinter as tk
from tkinter import ttk, messagebox

from deadlock_core import DeadlockCore
from csv_loader import load_csv


class DeadlockVisualizer:
    def __init__(self, core):
        self.core = core

        self.root = tk.Tk()
        self.root.title("Deadlock Visualization")
        self.root.geometry("800x500")

        self._build_ui()
        self._refresh_views()

    def _build_ui(self):
        # ===== MAIN FRAMES =====
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # ===== PROCESS VIEW =====
        ttk.Label(left_frame, text="Processes", font=("Arial", 12, "bold")).pack(anchor=tk.W)

        self.process_list = tk.Listbox(left_frame, height=12)
        self.process_list.pack(fill=tk.BOTH, expand=True, pady=5)

        # ===== RESOURCE VIEW =====
        ttk.Label(left_frame, text="Resources", font=("Arial", 12, "bold")).pack(anchor=tk.W)

        self.resource_list = tk.Listbox(left_frame, height=12)
        self.resource_list.pack(fill=tk.BOTH, expand=True, pady=5)

        # ===== DEADLOCK PANEL =====
        ttk.Label(right_frame, text="Deadlock Status", font=("Arial", 12, "bold")).pack(anchor=tk.W)

        self.deadlock_text = tk.Text(
            right_frame,
            height=10,
            state=tk.DISABLED,
            background="#f5f5f5"
        )
        self.deadlock_text.pack(fill=tk.BOTH, expand=True, pady=5)

        detect_btn = ttk.Button(
            right_frame,
            text="Detect Deadlock",
            command=self._detect_deadlock
        )
        detect_btn.pack(pady=10)

        refresh_btn = ttk.Button(
            right_frame,
            text="Refresh View",
            command=self._refresh_views
        )
        refresh_btn.pack()

    # ===== UPDATE UI =====
    def _refresh_views(self):
        self.process_list.delete(0, tk.END)
        self.resource_list.delete(0, tk.END)

        for p in self.core.processes.values():
            holding = ", ".join(r.name for r in p.holding) or "None"
            waiting = p.waiting_for.name if p.waiting_for else "None"
            self.process_list.insert(
                tk.END,
                f"{p.name} | Holding: {holding} | Waiting: {waiting}"
            )

        for r in self.core.resources.values():
            allocated = r.allocated_to.name if r.allocated_to else "None"
            self.resource_list.insert(
                tk.END,
                f"{r.name} | Allocated to: {allocated}"
            )

        self._update_deadlock_panel(None)

    def _detect_deadlock(self):
        cycle = self.core.detect_deadlock()
        self._update_deadlock_panel(cycle)

        if cycle:
            messagebox.showwarning(
                "Deadlock Detected",
                "Deadlock cycle:\n" + " -> ".join(cycle)
            )
        else:
            messagebox.showinfo("Deadlock Status", "No deadlock detected.")

    def _update_deadlock_panel(self, cycle):
        self.deadlock_text.config(state=tk.NORMAL)
        self.deadlock_text.delete("1.0", tk.END)

        if cycle:
            self.deadlock_text.insert(
                tk.END,
                "DEADLOCK DETECTED\n\n"
            )
            self.deadlock_text.insert(
                tk.END,
                "Cycle:\n" + " -> ".join(cycle)
            )
        else:
            self.deadlock_text.insert(
                tk.END,
                "No deadlock detected."
            )

        self.deadlock_text.config(state=tk.DISABLED)

    def run(self):
        self.root.mainloop()


def _apply_operations(core, operations):
    """Apply operations (list of dicts) to a DeadlockCore instance.
    """
    for op in operations:
        process = op["process"]
        action = op["action"]
        resource = op["resource"]

        # ensure existence
        if process not in core.processes:
            core.create_process(process)
        if resource not in core.resources:
            core.create_resource(resource)

        if action in ("request", "hold"):
            core.request_resource(process, resource)
        elif action == "release":
            # perform release without relying on core.release_resource
            r = core.resources[resource]
            p = core.processes[process]
            if r in p.holding:
                p.holding.remove(r)
            if r.allocated_to == p:
                r.allocated_to = None
            # clear waiting_for for any processes waiting for this resource
            for proc in core.processes.values():
                if proc.waiting_for == r:
                    proc.waiting_for = None


if __name__ == "__main__":
    # Run standalone GUI using input CSV
    core = DeadlockCore()
    try:
        ops = load_csv("input/input.csv")
    except Exception as e:
        print("CSV load error:", e)
        ops = []

    if ops:
        _apply_operations(core, ops)

    app = DeadlockVisualizer(core)
    app.run()