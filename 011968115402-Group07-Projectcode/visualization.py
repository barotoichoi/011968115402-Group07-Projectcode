# code test
import tkinter as tk

class DeadlockVisualizer:
    def __init__(self, core):
        self.core = core
        self.window = tk.Tk()
        self.window.title("Deadlock Visualization")
        self.canvas = tk.Canvas(self.window, width=800, height=500, bg="white")
        self.canvas.pack()

    def draw(self):
        self.canvas.delete("all")

        processes = list(self.core.processes.values())
        resources = list(self.core.resources.values())

        p_y = 100
        r_y = 300

        p_positions = {}
        r_positions = {}

        for i, p in enumerate(processes):
            x = 100 + i * 150
            self.canvas.create_rectangle(x, p_y, x + 80, p_y + 40, fill="#ADD8E6")
            self.canvas.create_text(x + 40, p_y + 20, text=p.name)
            p_positions[p.name] = (x + 40, p_y + 20)

        for i, r in enumerate(resources):
            x = 100 + i * 150
            self.canvas.create_oval(x, r_y, x + 60, r_y + 60, fill="#90EE90")
            self.canvas.create_text(x + 30, r_y + 30, text=r.name)
            r_positions[r.name] = (x + 30, r_y + 30)

        for r in resources:
            if r.allocated_to:
                x1, y1 = r_positions[r.name]
                x2, y2 = p_positions[r.allocated_to.name]
                self.canvas.create_line(
                    x1, y1 - 30, x2, y2 + 20,
                    arrow=tk.LAST, width=2, fill="green"
                )

        for p in processes:
            if p.waiting_for:
                x1, y1 = p_positions[p.name]
                x2, y2 = r_positions[p.waiting_for.name]
                self.canvas.create_line(
                    x1, y1 + 20, x2, y2 - 30,
                    arrow=tk.LAST, width=2, fill="red"
                )

        if self.core.detect_deadlock():
            self.canvas.create_text(
                400, 30,
                text="DEADLOCK DETECTED!",
                fill="red",
                font=("Arial", 20, "bold")
            )

    def run(self):
        self.draw()
        self.window.mainloop()