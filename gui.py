import tkinter as tk
from tkinter import messagebox
from rover import Rover
import datetime

rover = Rover()

def undo_move():
    status = rover.undo()
    update_status()
    log_command("UNDO", status)

def reset_rover():
    status = rover.reset()
    update_status()
    log_command("RESET", status)

def refresh_log():
    try:
        with open("logs/move_log.txt", "r", encoding="utf-8") as file:
            log_text.config(state=tk.NORMAL)
            log_text.delete(1.0, tk.END)
            log_text.insert(tk.END, file.read())
            log_text.see(tk.END)  # Auto-scroll to the bottom
            log_text.config(state=tk.DISABLED)
    except FileNotFoundError:
        log_text.config(state=tk.NORMAL)
        log_text.delete(1.0, tk.END)
        log_text.insert(tk.END, "No log file found.")
        log_text.config(state=tk.DISABLED)


def update_status():
    status_text.set(rover.status())
    draw_map()

def draw_map():
    canvas.delete("all")
    size = 60
    for y in range(rover.grid_height):
        for x in range(rover.grid_width):
            x1, y1 = x * size, y * size
            x2, y2 = x1 + size, y1 + size
            color = "#2e2e3e"
            if (x, y) in rover.terrain:
                color = "#444"
            if (x, y) == (rover.x, rover.y):
                color = "#39ff14"  # neon green
            canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="#888")
            if (x, y) == (rover.x, rover.y):
                canvas.create_text(x1 + size // 2, y1 + size // 2, text=rover.direction, fill="black", font=("Consolas", 16, "bold"))

def move_forward():
    status = rover.move()
    update_status()
    log_command("MOVE", status)

def turn_left():
    status = rover.turn_left()
    update_status()
    log_command("LEFT", status)

def turn_right():
    status = rover.turn_right()
    update_status()
    log_command("RIGHT", status)

def log_command(command, status):
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("logs/move_log.txt", "a", encoding="utf-8") as file:
        file.write(f"[{time}] Command: {command} | {status}\n")
    refresh_log()

# 🪐 Theme colors
bg_color = "#1e1e2f"
btn_color = "#3e3e5e"
text_color = "white"
log_bg = "#2b2b3d"

# GUI
window = tk.Tk()
window.title("🚀 Mars Rover Simulator")
window.configure(bg=bg_color)

status_text = tk.StringVar()
status_label = tk.Label(window, textvariable=status_text, font=("Consolas", 14), bg=bg_color, fg="#39ff14")
status_label.pack(pady=5)

canvas = tk.Canvas(window, width=300, height=300, bg="#1e1e2f", highlightthickness=0)
canvas.pack(padx=10, pady=10)

btn_frame = tk.Frame(window, bg=bg_color)
btn_frame.pack(pady=5)

def styled_button(master, text, cmd, r, c):
    tk.Button(master, text=text, command=cmd, width=10, bg=btn_color, fg=text_color,
              font=("Consolas", 10, "bold"), activebackground="#505070", relief="flat").grid(row=r, column=c, padx=5, pady=5)

log_label = tk.Label(window, text="📜 Command Log", font=("Consolas", 12), bg=bg_color, fg="lightgray")
log_label.pack()

# Frame to hold log_text and scrollbar side-by-side
log_frame = tk.Frame(window, bg=bg_color)
log_frame.pack(padx=10, pady=5)

log_text = tk.Text(log_frame, height=8, width=45, wrap="word",
                   bg=log_bg, fg="lightgray", font=("Consolas", 10))
log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(log_frame, command=log_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

log_text.config(yscrollcommand=scrollbar.set)
log_text.config(state=tk.DISABLED)

refresh_log()

styled_button(btn_frame, "⬅️ LEFT", turn_left, 0, 0)
styled_button(btn_frame, "⬆️ MOVE", move_forward, 0, 1)
styled_button(btn_frame, "➡️ RIGHT", turn_right, 0, 2)
styled_button(btn_frame, "↩️ UNDO", undo_move, 1, 0)
styled_button(btn_frame, "🔄 RESET", reset_rover, 1, 2)

update_status()
window.mainloop()
