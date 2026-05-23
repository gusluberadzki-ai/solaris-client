import random
import tkinter as tk
import json
import os
import sys

# -------- SOUND (improved) --------
def play_sound(kind="type"):
    try:
        if sys.platform.startswith("win"):
            import winsound
            sounds = {
                "type": (400, 40),
                "correct": (700, 80),
                "present": (600, 80),
                "win": (900, 150),
                "lose": (200, 400)
            }
            freq, dur = sounds.get(kind, (500, 50))
            winsound.Beep(freq, dur)
        else:
            # fallback beep (mac/linux terminal bell)
            print("\a", end="", flush=True)
    except:
        pass

# -------- WORDS --------
words = []
with open("words.txt") as f:
    for line in f:
        w = line.strip().lower()
        if len(w) == 5:
            words.append(w)

# -------- STATS --------
STATS_FILE = "wordle_stats.json"
if os.path.exists(STATS_FILE):
    with open(STATS_FILE) as f:
        stats = json.load(f)
else:
    stats = {"wins": 0, "games": 0, "streak": 0, "best": 0}

# -------- GAME STATE --------
def new_game():
    return random.choice(words), 0, 0

TARGET, attempt, col = new_game()
MAX_ATTEMPTS = 6

# -------- COLORS --------
CORRECT = "#6aaa64"
PRESENT = "#c9b458"
ABSENT = "#787c7e"
EMPTY = "#3a3a3c"
BG = "#121213"
TEXT = "#ffffff"

# -------- UI --------
root = tk.Tk()
root.title("Wordle PRO")
root.configure(bg=BG)
root.geometry("440x780")

# Title
tk.Label(root, text="WORDLE", font=("Helvetica", 32, "bold"), bg=BG, fg=TEXT).pack()

# Stats label
stats_label = tk.Label(root, text="", font=("Helvetica", 11), bg=BG, fg=TEXT)
stats_label.pack()

# Update stats display
def update_stats_label():
    stats_label.config(text=f"Wins: {stats['wins']} | Games: {stats['games']} | Streak: {stats['streak']} | Best: {stats['best']}")

update_stats_label()

# Grid
grid = tk.Frame(root, bg=BG)
grid.pack(pady=10)

cells = []
for r in range(MAX_ATTEMPTS):
    row = []
    for c in range(5):
        lbl = tk.Label(grid, text="", width=4, height=2,
                       font=("Helvetica", 24, "bold"), bg=EMPTY, fg=TEXT, bd=2)
        lbl.grid(row=r, column=c, padx=5, pady=5)
        row.append(lbl)
    cells.append(row)

# Message
msg = tk.Label(root, text="", font=("Helvetica", 14), bg=BG, fg=TEXT)
msg.pack()

# Keyboard
kb = tk.Frame(root, bg=BG)
kb.pack(pady=10)
keys = {}
for line in ["qwertyuiop", "asdfghjkl", "zxcvbnm"]:
    row = tk.Frame(kb, bg=BG)
    row.pack()
    for ch in line:
        b = tk.Label(row, text=ch.upper(), width=3, height=2,
                     font=("Helvetica", 12, "bold"), bg=EMPTY, fg=TEXT)
        b.pack(side="left", padx=2, pady=2)
        keys[ch] = b

# Restart
def restart():
    global TARGET, attempt, col
    TARGET, attempt, col = new_game()
    msg.config(text="")
    for r in range(MAX_ATTEMPTS):
        for c in range(5):
            cells[r][c].config(text="", bg=EMPTY)
    for k in keys.values():
        k.config(bg=EMPTY)

# Save stats
def save_stats():
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

# Submit guess with delay animation
def submit():
    global attempt, col

    if col < 5:
        msg.config(text="Not enough letters")
        return

    guess = "".join(cells[attempt][i].cget("text").lower() for i in range(5))

    if guess not in words:
        msg.config(text="Not in word list")
        shake_row(attempt)
        return

    counts = {l: TARGET.count(l) for l in set(TARGET)}
    res = [""] * 5

    for i in range(5):
        if guess[i] == TARGET[i]:
            res[i] = "c"
            counts[guess[i]] -= 1

    for i in range(5):
        if res[i] == "":
            if guess[i] in TARGET and counts.get(guess[i], 0) > 0:
                res[i] = "p"
                counts[guess[i]] -= 1
            else:
                res[i] = "a"

    def animate(i=0):
        global attempt, col
        if i < 5:
            cell = cells[attempt][i]
            color = CORRECT if res[i]=="c" else PRESENT if res[i]=="p" else ABSENT
            cell.config(bg=color)
            keys[guess[i]].config(bg=color)
            play_sound("correct" if res[i]=="c" else "present")
            root.after(250, animate, i+1)
        else:
            finish_guess(guess)

    animate()

# Finish guess
def finish_guess(guess):
    global attempt, col

    attempt += 1
    col = 0

    if guess == TARGET:
        msg.config(text="🎉 YOU WIN!")
        stats["wins"] += 1
        stats["streak"] += 1
        stats["best"] = max(stats["best"], stats["streak"])
        stats["games"] += 1
        play_sound("win")
        save_stats()
        update_stats_label()
    elif attempt >= MAX_ATTEMPTS:
        msg.config(text=f"Game Over: {TARGET.upper()}")
        stats["streak"] = 0
        stats["games"] += 1
        play_sound("lose")
        save_stats()
        update_stats_label()

# Shake animation
def shake_row(r, offset=0):
    if offset < 6:
        for c in range(5):
            cells[r][c].grid_configure(padx=5 + (-1)**offset * 5)
        root.after(50, shake_row, r, offset+1)
    else:
        for c in range(5):
            cells[r][c].grid_configure(padx=5)

# Input
def key(e):
    global col

    if e.keysym == "Return":
        submit()
    elif e.keysym == "BackSpace":
        if col > 0:
            col -= 1
            cells[attempt][col].config(text="")
    elif e.char.isalpha():
        if col < 5:
            cells[attempt][col].config(text=e.char.upper())
            col += 1
            play_sound("type")

root.bind("<Key>", key)

# Restart button
tk.Button(root, text="Restart", command=restart).pack(pady=5)

root.mainloop()