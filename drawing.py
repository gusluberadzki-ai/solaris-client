import tkinter as tk
from tkinter import simpledialog, colorchooser
import copy

root = tk.Tk()
root.title("Mini Photoshop PRO")
root.geometry("1100x700")
root.configure(bg="#2b2b2b")

# -------- STATE --------
objects = []
selected = None
tool = "draw"

current_color = "black"
brush_size = 6

history = []
redo_stack = []

scale = 1.0
last = None

# -------- CANVAS --------
canvas = tk.Canvas(root, bg="#f5f5f5", highlightthickness=0)
canvas.pack(fill="both", expand=True)

# -------- HISTORY --------
def save_state():
    history.append(copy.deepcopy(objects))
    redo_stack.clear()

def undo():
    if history:
        redo_stack.append(copy.deepcopy(objects))
        restore(history.pop())

def redo():
    if redo_stack:
        history.append(copy.deepcopy(objects))
        restore(redo_stack.pop())

def restore(state):
    global objects
    objects = state
    redraw()

# -------- REDRAW --------
def redraw():
    canvas.delete("all")
    for obj in objects:
        if not obj.get("visible", True):
            continue

        if obj["type"] == "oval":
            r = obj["size"]
            canvas.create_oval(
                obj["x"] - r, obj["y"] - r,
                obj["x"] + r, obj["y"] + r,
                fill=obj["color"],
                outline=""
            )

        elif obj["type"] == "text":
            canvas.create_text(
                obj["x"], obj["y"],
                text=obj["text"],
                fill=obj["color"],
                font=("Segoe UI", obj["size"]),
                anchor="nw"
            )

    # highlight selected
    if selected:
        canvas.create_rectangle(
            selected["x"] - 20, selected["y"] - 20,
            selected["x"] + 20, selected["y"] + 20,
            outline="blue", dash=(3, 2)
        )

# -------- OBJECT PICK --------
def find_object(x, y):
    for obj in reversed(objects):
        if obj["type"] == "text":
            if abs(obj["x"] - x) < 30 and abs(obj["y"] - y) < 30:
                return obj
    return None

# -------- MOUSE EVENTS --------
def click(event):
    global last, selected
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)

    if tool == "draw":
        save_state()
        last = (x, y)

    elif tool == "text":
        save_state()
        txt = simpledialog.askstring("Text", "Enter text:")
        if txt:
            objects.append({
                "type": "text",
                "x": x,
                "y": y,
                "text": txt,
                "color": current_color,
                "size": max(14, brush_size * 2),
                "visible": True
            })
            redraw()

    elif tool == "select":
        selected = find_object(x, y)
        redraw()

def drag(event):
    global last
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)

    # 🎨 Soft Brush
    if tool == "draw" and last:
        dx = x - last[0]
        dy = y - last[1]
        dist = int(max(abs(dx), abs(dy))) or 1

        for i in range(dist):
            px = last[0] + dx * i / dist
            py = last[1] + dy * i / dist

            objects.append({
                "type": "oval",
                "x": px,
                "y": py,
                "size": brush_size,
                "color": current_color,
                "visible": True
            })

        last = (x, y)
        redraw()

    # 🖱 Move
    elif tool == "move" and selected:
        selected["x"] = x
        selected["y"] = y
        redraw()

    # 🔎 Resize text
    elif tool == "resize" and selected and selected["type"] == "text":
        selected["size"] = max(5, int(abs(y - selected["y"])))
        redraw()

def release(event):
    global last
    last = None

canvas.bind("<Button-1>", click)
canvas.bind("<B1-Motion>", drag)
canvas.bind("<ButtonRelease-1>", release)

# -------- EDIT TEXT --------
def edit_text(event):
    x, y = canvas.canvasx(event.x), canvas.canvasy(event.y)
    obj = find_object(x, y)

    if obj and obj["type"] == "text":
        new = simpledialog.askstring("Edit Text", "Edit:", initialvalue=obj["text"])
        if new:
            save_state()
            obj["text"] = new
            redraw()

canvas.bind("<Double-1>", edit_text)

# -------- ZOOM --------
def zoom(event):
    global scale
    factor = 1.1 if event.delta > 0 else 0.9
    scale *= factor
    canvas.scale("all", 0, 0, factor, factor)

canvas.bind("<MouseWheel>", zoom)

# -------- PAN --------
def start_pan(event):
    canvas.scan_mark(event.x, event.y)

def pan(event):
    canvas.scan_dragto(event.x, event.y, gain=1)

canvas.bind("<Button-2>", start_pan)
canvas.bind("<B2-Motion>", pan)

# -------- RESET VIEW --------
def reset_view():
    global scale
    scale = 1.0
    canvas.scale("all", 0, 0, 1, 1)
    canvas.configure(scrollregion=canvas.bbox("all"))

# -------- TOOL WINDOW --------
tools = tk.Toplevel(root)
tools.title("Tools")
tools.geometry("260x550")
tools.configure(bg="#1e1e1e")
tools.attributes("-topmost", True)

container = tk.Frame(tools, bg="#1e1e1e")
container.pack(fill="both", expand=True, padx=10, pady=10)

btn = {
    "bg": "#2d2d2d",
    "fg": "white",
    "activebackground": "#3c3c3c",
    "activeforeground": "white",
    "relief": "flat",
    "bd": 0,
    "padx": 10,
    "pady": 8
}

def set_tool(t):
    global tool
    tool = t

tk.Label(container, text="Tools", bg="#1e1e1e", fg="white",
         font=("Segoe UI", 12, "bold")).pack(pady=(0,10))

tk.Button(container, text="Draw", command=lambda: set_tool("draw"), **btn).pack(fill="x", pady=3)
tk.Button(container, text="Text", command=lambda: set_tool("text"), **btn).pack(fill="x", pady=3)
tk.Button(container, text="Select", command=lambda: set_tool("select"), **btn).pack(fill="x", pady=3)
tk.Button(container, text="Move", command=lambda: set_tool("move"), **btn).pack(fill="x", pady=3)
tk.Button(container, text="Resize Text", command=lambda: set_tool("resize"), **btn).pack(fill="x", pady=3)

# COLOR
color_preview = tk.Label(container, bg=current_color, height=2)
color_preview.pack(fill="x", pady=5)

def pick_color():
    global current_color
    c = colorchooser.askcolor()[1]
    if c:
        current_color = c
        color_preview.config(bg=c)

tk.Button(container, text="Pick Color", command=pick_color, **btn).pack(fill="x", pady=5)

# BRUSH SIZE
def set_size(v):
    global brush_size
    brush_size = int(v)

tk.Scale(
    container,
    from_=1,
    to=50,
    orient="horizontal",
    command=set_size,
    bg="#1e1e1e",
    fg="white",
    troughcolor="#444",
    highlightthickness=0
).pack(fill="x", pady=10)

# VISIBILITY
def toggle_visibility():
    if selected:
        selected["visible"] = not selected.get("visible", True)
        redraw()

tk.Button(container, text="Toggle Visibility", command=toggle_visibility, **btn).pack(fill="x", pady=5)

# UNDO REDO
tk.Button(container, text="Undo", command=undo, **btn).pack(fill="x")
tk.Button(container, text="Redo", command=redo, **btn).pack(fill="x")

# RESET VIEW
tk.Button(container, text="Reset View", command=reset_view, **btn).pack(fill="x", pady=5)

# CLEAR
def clear():
    global objects
    save_state()
    objects = []
    redraw()

tk.Button(container, text="Clear", command=clear, **btn).pack(fill="x", pady=10)

root.mainloop()