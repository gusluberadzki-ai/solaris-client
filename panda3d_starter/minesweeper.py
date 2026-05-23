import tkinter as tk
from tkinter import ttk, messagebox
import random
import time
import threading

class MinesweeperApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Advanced Minesweeper")
        self.root.geometry("800x600")
        self.root.configure(bg="#1a1a1a")  # Dark military black

        # Game state
        self.current_screen = "loading"
        self.difficulty = None
        self.game_started = False

        # Difficulty settings
        self.difficulties = {
            "Easy": {"width": 9, "height": 9, "mines": 10, "cell_size": 50},
            "Medium": {"width": 16, "height": 16, "mines": 40, "cell_size": 35},
            "Hard": {"width": 30, "height": 16, "mines": 99, "cell_size": 25}
        }

        self.show_loading_screen()

    def show_loading_screen(self):
        self.clear_screen()

        # Loading screen
        loading_frame = tk.Frame(self.root, bg="#1a1a1a")
        loading_frame.pack(expand=True, fill="both")

        title = tk.Label(loading_frame, text="MILITARY MINESWEEPER", font=("Courier", 36, "bold"),
                        bg="#1a1a1a", fg="#00FF00")
        title.pack(pady=50)

        self.loading_text = tk.Label(loading_frame, text="Initializing tactical systems...", font=("Courier", 16),
                                   bg="#1a1a1a", fg="#FFFF00")
        self.loading_text.pack(pady=20)

        self.progress = ttk.Progressbar(loading_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=20)

        # Start loading animation
        self.loading_progress = 0
        self.animate_loading()

    def animate_loading(self):
        if self.loading_progress < 100:
            self.loading_progress += 2
            self.progress['value'] = self.loading_progress
            self.loading_text.config(text=f"Loading... {self.loading_progress}%")
            self.root.after(50, self.animate_loading)
        else:
            self.show_difficulty_screen()

    def show_difficulty_screen(self):
        self.clear_screen()
        self.current_screen = "difficulty"

        # Difficulty selection screen
        diff_frame = tk.Frame(self.root, bg="#1a1a1a")
        diff_frame.pack(expand=True, fill="both")

        title = tk.Label(diff_frame, text="SELECT COMBAT ZONE", font=("Courier", 32, "bold"),
                        bg="#1a1a1a", fg="#FF4500")
        title.pack(pady=40)

        button_frame = tk.Frame(diff_frame, bg="#1a1a1a")
        button_frame.pack(pady=30)

        for diff_name, settings in self.difficulties.items():
            threat_level = "LOW" if diff_name == "Easy" else "MEDIUM" if diff_name == "Medium" else "HIGH"
            btn = tk.Button(button_frame, text=f"{diff_name.upper()}\n{settings['width']}×{settings['height']} GRID\n{settings['mines']} MINES\nTHREAT: {threat_level}",
                           font=("Courier", 12, "bold"), width=20, height=4,
                           bg="#2F4F2F", fg="#00FF00", activebackground="#556B2F",
                           relief="raised", bd=4, command=lambda d=diff_name: self.start_game(d))
            btn.pack(pady=10)

        # Fullscreen toggle
        self.fullscreen_var = tk.BooleanVar()
        fullscreen_check = tk.Checkbutton(diff_frame, text="FULLSCREEN MODE", variable=self.fullscreen_var,
                                        font=("Courier", 12, "bold"), bg="#1a1a1a", fg="#FFFF00",
                                        selectcolor="#2F4F2F", activebackground="#1a1a1a",
                                        activeforeground="#FFFF00")
        fullscreen_check.pack(pady=20)

    def start_game(self, difficulty):
        self.difficulty = difficulty
        self.settings = self.difficulties[difficulty]

        if self.fullscreen_var.get():
            self.root.attributes('-fullscreen', True)
        else:
            # Calculate window size based on grid
            window_width = self.settings['width'] * self.settings['cell_size'] + 200
            window_height = self.settings['height'] * self.settings['cell_size'] + 150
            self.root.geometry(f"{window_width}x{window_height}")

        self.initialize_game()
        self.show_game_screen()

    def initialize_game(self):
        self.game_started = False
        self.game_over = False
        self.start_time = None

        # Initialize grids
        self.grid = [[0 for _ in range(self.settings['width'])] for _ in range(self.settings['height'])]
        self.revealed = [[False for _ in range(self.settings['width'])] for _ in range(self.settings['height'])]
        self.flagged = [[False for _ in range(self.settings['width'])] for _ in range(self.settings['height'])]

        # Place mines
        mines_placed = 0
        while mines_placed < self.settings['mines']:
            x = random.randint(0, self.settings['width'] - 1)
            y = random.randint(0, self.settings['height'] - 1)
            if self.grid[y][x] != -1:
                self.grid[y][x] = -1
                mines_placed += 1

        # Calculate numbers
        for y in range(self.settings['height']):
            for x in range(self.settings['width']):
                if self.grid[y][x] != -1:
                    self.grid[y][x] = self.count_adjacent_mines(x, y)

    def count_adjacent_mines(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.settings['width'] and
                    0 <= ny < self.settings['height'] and
                    self.grid[ny][nx] == -1):
                    count += 1
        return count

    def show_game_screen(self):
        self.clear_screen()
        self.current_screen = "game"

        # Main game frame
        self.game_frame = tk.Frame(self.root, bg="#1a1a1a")
        self.game_frame.pack(expand=True, fill="both")

        # Top panel
        top_frame = tk.Frame(self.game_frame, bg="#1a1a1a", height=60)
        top_frame.pack(fill="x", pady=10)
        top_frame.pack_propagate(False)

        self.mine_counter = tk.Label(top_frame, text=f"MINES: {self.settings['mines']}",
                                   font=("Courier", 14, "bold"), bg="#1a1a1a", fg="#FF0000")
        self.mine_counter.pack(side="left", padx=20)

        self.timer_label = tk.Label(top_frame, text="TIME: 0", font=("Courier", 14, "bold"),
                                  bg="#1a1a1a", fg="#00FF00")
        self.timer_label.pack(side="right", padx=20)

        self.restart_btn = tk.Button(top_frame, text="🔄 RESET", font=("Courier", 10, "bold"),
                                   bg="#2F4F2F", fg="#00FF00", activebackground="#556B2F",
                                   relief="raised", bd=3, command=self.restart_game)
        self.restart_btn.pack(side="top", pady=5)

        self.menu_btn = tk.Button(top_frame, text="⬅ MENU", font=("Courier", 10, "bold"),
                                bg="#2F4F2F", fg="#FFFF00", activebackground="#556B2F",
                                relief="raised", bd=3, command=self.back_to_menu)
        self.menu_btn.pack(side="top", pady=5)

        # Canvas for the game board
        canvas_width = self.settings['width'] * self.settings['cell_size']
        canvas_height = self.settings['height'] * self.settings['cell_size']

        self.canvas = tk.Canvas(self.game_frame, width=canvas_width, height=canvas_height,
                              bg="#2F4F2F", highlightthickness=2, highlightbackground="#00FF00")
        self.canvas.pack(pady=10)

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-2>", self.right_click)

        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        cell_size = self.settings['cell_size']

        for y in range(self.settings['height']):
            for x in range(self.settings['width']):
                x1 = x * cell_size
                y1 = y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                if self.revealed[y][x]:
                    if self.grid[y][x] == -1:
                        # Mine - red alert background
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#8B0000", outline="#4C566A", width=2)
                        self.canvas.create_text(x1 + cell_size//2, y1 + cell_size//2,
                                              text="💣", font=("Courier", cell_size//2))
                    else:
                        # Revealed cell - desert tan
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#D2B48C", outline="#4C566A", width=1)
                        if self.grid[y][x] > 0:
                            colors = ["#000000", "#0000FF", "#008000", "#FF0000", "#800080", "#FFA500", "#000080", "#800000"]
                            self.canvas.create_text(x1 + cell_size//2, y1 + cell_size//2,
                                                  text=str(self.grid[y][x]),
                                                  font=("Courier", cell_size//2, "bold"),
                                                  fill=colors[self.grid[y][x]-1] if self.grid[y][x] <= len(colors) else "#000000")
                else:
                    # Unrevealed cell - camouflage green
                    if self.flagged[y][x]:
                        self.canvas.create_rectangle(x1, y1, x2, y2, fill="#FF8C00", outline="#4C566A", width=2)
                        self.canvas.create_text(x1 + cell_size//2, y1 + cell_size//2,
                                              text="🚩", font=("Courier", cell_size//3))
                    else:
                        # 3D effect for unrevealed cells - military green
                        self.canvas.create_rectangle(x1+2, y1+2, x2, y2, fill="#2F4F2F", outline="#4C566A", width=1)
                        self.canvas.create_rectangle(x1, y1, x2-2, y2-2, fill="#556B2F", outline="#4C566A", width=1)

    def left_click(self, event):
        if self.game_over:
            return

        cell_size = self.settings['cell_size']
        x = event.x // cell_size
        y = event.y // cell_size

        if not (0 <= x < self.settings['width'] and 0 <= y < self.settings['height']):
            return

        if self.flagged[y][x] or self.revealed[y][x]:
            return

        # Start timer on first click
        if not self.game_started:
            self.game_started = True
            self.start_time = time.time()
            self.update_timer()

        self.revealed[y][x] = True

        if self.grid[y][x] == -1:
            self.game_over = True
            self.reveal_all_mines()
            self.show_game_over()
        elif self.grid[y][x] == 0:
            self.flood_fill(x, y)

        self.draw_board()
        self.update_mine_counter()

        if self.check_win():
            self.game_over = True
            self.show_win()

    def right_click(self, event):
        if self.game_over:
            return

        cell_size = self.settings['cell_size']
        x = event.x // cell_size
        y = event.y // cell_size

        if not (0 <= x < self.settings['width'] and 0 <= y < self.settings['height']):
            return

        if not self.revealed[y][x]:
            self.flagged[y][x] = not self.flagged[y][x]
            self.draw_board()
            self.update_mine_counter()

    def flood_fill(self, x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    nx, ny = cx + dx, cy + dy
                    if (0 <= nx < self.settings['width'] and
                        0 <= ny < self.settings['height'] and
                        not self.revealed[ny][nx] and
                        not self.flagged[ny][nx]):
                        self.revealed[ny][nx] = True
                        if self.grid[ny][nx] == 0:
                            stack.append((nx, ny))

    def reveal_all_mines(self):
        for y in range(self.settings['height']):
            for x in range(self.settings['width']):
                if self.grid[y][x] == -1:
                    self.revealed[y][x] = True

    def update_mine_counter(self):
        flagged_count = sum(sum(row) for row in self.flagged)
        remaining = self.settings['mines'] - flagged_count
        self.mine_counter.config(text=f"Mines: {remaining}")

    def update_timer(self):
        if self.game_started and not self.game_over:
            elapsed = int(time.time() - self.start_time)
            self.timer_label.config(text=f"Time: {elapsed}")
            self.root.after(1000, self.update_timer)

    def check_win(self):
        for y in range(self.settings['height']):
            for x in range(self.settings['width']):
                if self.grid[y][x] != -1 and not self.revealed[y][x]:
                    return False
        return True

    def show_game_over(self):
        self.canvas.create_rectangle(50, self.settings['height']*self.settings['cell_size']//2 - 30,
                                   self.settings['width']*self.settings['cell_size'] - 50,
                                   self.settings['height']*self.settings['cell_size']//2 + 30,
                                   fill="#BF616A", outline="#ECEFF4", width=3)
        self.canvas.create_text(self.settings['width']*self.settings['cell_size']//2,
                              self.settings['height']*self.settings['cell_size']//2,
                              text="💥 GAME OVER 💥", font=("Arial", 24, "bold"), fill="#ECEFF4")

    def show_win(self):
        self.canvas.create_rectangle(50, self.settings['height']*self.settings['cell_size']//2 - 30,
                                   self.settings['width']*self.settings['cell_size'] - 50,
                                   self.settings['height']*self.settings['cell_size']//2 + 30,
                                   fill="#A3BE8C", outline="#ECEFF4", width=3)
        self.canvas.create_text(self.settings['width']*self.settings['cell_size']//2,
                              self.settings['height']*self.settings['cell_size']//2,
                              text="🎉 YOU WIN! 🎉", font=("Arial", 24, "bold"), fill="#2E3440")

    def restart_game(self):
        self.initialize_game()
        self.game_over = False
        self.game_started = False
        self.start_time = None
        self.timer_label.config(text="Time: 0")
        self.draw_board()
        self.update_mine_counter()

    def back_to_menu(self):
        self.game_over = False
        self.game_started = False
        self.start_time = None
        self.show_difficulty_screen()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MinesweeperApp()
    app.run()