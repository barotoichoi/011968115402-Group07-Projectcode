import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
from pathlib import Path

from deadlock_core import DeadlockCore
from csv_loader import load_csv

# Get the directory where this script is located
SCRIPT_DIR = Path(__file__).parent
INPUT_DIR = SCRIPT_DIR / "input"


class DeadlockVisualizer:
    def __init__(self, core, file_path=None):
        self.core = core
        self.file_path = file_path

        self.root = tk.Tk()
        self.root.title("Deadlock Visualization")
        self.root.geometry("800x500")

        self._build_ui()
        self._refresh_views()

    def _build_ui(self):
        
        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Load CSV File", padding=10)
        file_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            file_frame,
            text="Choose from Input Folder",
            command=self._load_from_input
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            file_frame,
            text="Choose from Computer",
            command=self._load_from_computer
        ).pack(side=tk.LEFT, padx=5)

        self.file_label = ttk.Label(file_frame, text="No file loaded", foreground="gray")
        self.file_label.pack(side=tk.LEFT, padx=20)

        # Separator
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)

        left_frame = ttk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        right_frame = ttk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        
        ttk.Label(left_frame, text="Processes", font=("Arial", 12, "bold")).pack(anchor=tk.W)

        self.process_list = tk.Listbox(left_frame, height=12)
        self.process_list.pack(fill=tk.BOTH, expand=True, pady=5)

      
        ttk.Label(left_frame, text="Resources", font=("Arial", 12, "bold")).pack(anchor=tk.W)

        self.resource_list = tk.Listbox(left_frame, height=12)
        self.resource_list.pack(fill=tk.BOTH, expand=True, pady=5)

        
        ttk.Label(right_frame, text="Deadlock Status", font=("Arial", 12, "bold")).pack(anchor=tk.W)

        self.deadlock_text = tk.Text(
            right_frame,
            height=10,
            state=tk.DISABLED,
            background="#f5f5f5"
        )
        self.deadlock_text.pack(fill=tk.BOTH, expand=True, pady=5)

        # Button frame
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(pady=10)

        detect_btn = ttk.Button(
            button_frame,
            text="Detect Deadlock",
            command=self._detect_deadlock
        )
        detect_btn.pack(side=tk.LEFT, padx=5)

        export_btn = ttk.Button(
            button_frame,
            text="Export Result",
            command=self._export_result
        )
        export_btn.pack(side=tk.LEFT, padx=5)

        refresh_btn = ttk.Button(
            right_frame,
            text="Refresh View",
            command=self._refresh_views
        )
        refresh_btn.pack()

    
    def _load_from_input(self):
        """Load CSV file from input folder"""
        
        if not INPUT_DIR.exists():
            messagebox.showerror("Error", f"Input folder not found at {INPUT_DIR}")
            return
        
        csv_files = list(INPUT_DIR.glob("*.csv"))
        
        if not csv_files:
            messagebox.showwarning("No Files", "No CSV files found in input folder")
            return
        
        # Create selection window
        select_window = tk.Toplevel(self.root)
        select_window.title("Select Case")
        select_window.geometry("400x300")
        
        ttk.Label(select_window, text="Available Cases:", font=("Arial", 11, "bold")).pack(pady=10)
        
        listbox = tk.Listbox(select_window, height=10)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        file_names = [f.name for f in csv_files]
        for name in sorted(file_names):
            listbox.insert(tk.END, name)
        
        def load_selected():
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a file")
                return
            
            selected_file = sorted(file_names)[selection[0]]
            file_path = INPUT_DIR / selected_file
            self._load_csv_file(str(file_path))
            select_window.destroy()
        
        ttk.Button(select_window, text="Load", command=load_selected).pack(pady=10)

    def _load_from_computer(self):
        """Load CSV file from computer using file dialog"""
        file_path = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if file_path:
            self._load_csv_file(file_path)

    def _load_csv_file(self, file_path):
        """Load and apply CSV file"""
        try:
            ops = load_csv(file_path)
            
            if not ops:
                messagebox.showwarning("Empty File", "CSV file is empty or invalid")
                return
            
            # Clear previous data
            self.core = DeadlockCore()
            
            # Apply operations
            _apply_operations(self.core, ops)
            
            # Update file label
            self.file_path = file_path
            file_name = Path(file_path).name
            self.file_label.config(text=f"Loaded: {file_name}", foreground="green")
            
            # Refresh UI
            self._refresh_views()
            
            messagebox.showinfo("Success", f"File loaded successfully: {file_name}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")

    def _export_result(self):
        """Export result.csv to a location chosen by user"""
        # Check if result.csv exists in output folder
        script_dir = Path(__file__).parent
        result_file = script_dir / "output" / "result.csv"
        
        if not result_file.exists():
            messagebox.showwarning("No Result", "No result.csv found. Please load a case first.")
            return
        
        # Ask user where to save
        save_path = filedialog.asksaveasfilename(
            title="Export Result CSV",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile="result.csv"
        )
        
        if save_path:
            try:
                shutil.copy(str(result_file), save_path)
                messagebox.showinfo("Success", f"Result exported to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export file:\n{str(e)}")

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

        
        if process not in core.processes:
            core.create_process(process)
        if resource not in core.resources:
            core.create_resource(resource)

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


if __name__ == "__main__":
   
    core = DeadlockCore()
    
    app = DeadlockVisualizer(core)
    app.run()