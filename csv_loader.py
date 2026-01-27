import tkinter as tk
from tkinter import ttk
import random

class ProcessUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Monitor")
        self.running = False
        self.progress = 0

        ttk.Label(root, text="Process State:").grid(row=0, column=0, sticky="w")
        self.state_var = tk.StringVar(value="Stopped")
        ttk.Label(root, textvariable=self.state_var).grid(row=0, column=1, sticky="w")

        ttk.Label(root, text="CPU Usage (%):").grid(row=1, column=0, sticky="w")
        self.cpu_var = tk.StringVar(value="0")
        ttk.Label(root, textvariable=self.cpu_var).grid(row=1, column=1, sticky="w")

        ttk.Label(root, text="Memory Usage (MB):").grid(row=2, column=0, sticky="w")
        self.mem_var = tk.StringVar(value="0")
        ttk.Label(root, textvariable=self.mem_var).grid(row=2, column=1, sticky="w")

        self.progress_bar = ttk.Progressbar(root, length=200, maximum=100)
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(root, text="Start", command=self.start).grid(row=4, column=0, pady=5)
        ttk.Button(root, text="Pause", command=self.pause).grid(row=4, column=1, pady=5)
        ttk.Button(root, text="Reset", command=self.reset).grid(row=5, column=0, columnspan=2)

    def start(self):
        if not self.running:
            self.running = True
            self.state_var.set("Running")
            self.update_process()

    def pause(self):
        self.running = False
        self.state_var.set("Paused")

    def reset(self):
        self.running = False
        self.progress = 0
        self.progress_bar['value'] = 0
        self.cpu_var.set("0")
        self.mem_var.set("0")
        self.state_var.set("Stopped")

    def update_process(self):
        if self.running and self.progress < 100:
            self.progress += 1
            self.progress_bar['value'] = self.progress
            self.cpu_var.set(str(random.randint(10, 90)))
            self.mem_var.set(str(random.randint(100, 500)))
            self.root.after(200, self.update_process)
        elif self.progress >= 100:
            self.state_var.set("Completed")
            self.running = False


if __name__ == "__main__":
    root = tk.Tk()
    app = ProcessUI(root)
    root.mainloop()
