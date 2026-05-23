import tkinter as tk
from tkinter import ttk
import time

quizData = [
    ("What is the capital of France?", ["London", "Paris", "Moscow", "Berlin"], "B"),
    ("What is 2 + 2?", ["3", "4", "5", "6"], "B"),
    ("Who wrote Romeo and Juliet?", ["Charles Dickens", "William Shakespeare", "Jane Austen", "Mark Twain"], "B"),
    ("What is the largest planet in our solar system?", ["Earth", "Mars", "Jupiter", "Saturn"], "C"),
    ("What color is the sky on a clear day?", ["Red", "Blue", "Green", "Yellow"], "B"),
    ("How many continents are there?", ["5", "6", "7", "8"], "C"),
    ("What is the capital of Japan?", ["Beijing", "Seoul", "Tokyo", "Bangkok"], "C"),
    ("What is the square root of 16?", ["2", "3", "4", "5"], "C"),
    ("Who painted the Mona Lisa?", ["Vincent van Gogh", "Pablo Picasso", "Leonardo da Vinci", "Michelangelo"], "C"),
    ("What is the chemical symbol for water?", ["H2O", "CO2", "O2", "NaCl"], "A"),
    ("What is the capital of Germany?", ["Vienna", "Berlin", "Prague", "Warsaw"], "B"),
    ("What is 5 * 6?", ["25", "30", "35", "40"], "B"),
    ("Who discovered penicillin?", ["Alexander Fleming", "Louis Pasteur", "Jonas Salk", "Edward Jenner"], "A"),
    ("What is the smallest country in the world?", ["Monaco", "Vatican City", "San Marino", "Liechtenstein"], "B"),
    ("In what year did World War II end?", ["1944", "1945", "1946", "1947"], "B")
]

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cool Quiz with Animations!")
        self.root.geometry("600x500")
        self.root.configure(bg="#2E3440")

        self.currentQuestion = 0
        self.score = 0
        self.quizData = quizData

        # Title
        self.title_label = tk.Label(root, text="Welcome to the Quiz!", font=("Arial", 24, "bold"), bg="#2E3440", fg="#88C0D0")
        self.title_label.pack(pady=20)

        # Question label
        self.question_label = tk.Label(root, text="", font=("Arial", 18), bg="#2E3440", fg="#ECEFF4", wraplength=500)
        self.question_label.pack(pady=20)

        # Options frame
        self.options_frame = tk.Frame(root, bg="#2E3440")
        self.options_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(4):
            btn = tk.Button(self.options_frame, text="", font=("Arial", 14, "bold"), width=25, height=2,
                            bg="#88C0D0", fg="#2E3440", activebackground="#81A1C1", activeforeground="#ECEFF4",
                            relief="raised", bd=3, command=lambda idx=i: self.check_answer(chr(65 + idx)))
            btn.grid(row=i//2, column=i%2, padx=10, pady=5)
            self.option_buttons.append(btn)

        # Feedback label
        self.feedback_label = tk.Label(root, text="", font=("Arial", 16, "bold"), bg="#2E3440", fg="#ECEFF4")
        self.feedback_label.pack(pady=10)

        # Score label
        self.score_label = tk.Label(root, text=f"Score: {self.score}/{len(self.quizData)}", font=("Arial", 14), bg="#2E3440", fg="#8FBCBB")
        self.score_label.pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)
        self.progress['maximum'] = len(self.quizData)

        self.show_question()

    def show_question(self):
        if self.currentQuestion < len(self.quizData):
            question, options, _ = self.quizData[self.currentQuestion]
            self.question_label.config(text="")
            self.fade_in_text(self.question_label, question, 0)
            for i, option in enumerate(options):
                self.option_buttons[i].config(text=f"{chr(65+i)}) {option}", state="normal")
            self.feedback_label.config(text="")
            self.progress['value'] = self.currentQuestion
        else:
            self.end_quiz()

    def fade_in_text(self, label, text, index):
        if index < len(text):
            label.config(text=text[:index+1])
            self.root.after(50, self.fade_in_text, label, text, index+1)

    def check_answer(self, answer):
        _, _, correct = self.quizData[self.currentQuestion]
        if answer == correct:
            self.score += 1
            self.animate_feedback("Correct! 🎉", "#A3BE8C")
        else:
            self.animate_feedback("Incorrect! 😞", "#BF616A")
        self.score_label.config(text=f"Score: {self.score}/{len(self.quizData)}")
        for btn in self.option_buttons:
            btn.config(state="disabled")
        self.root.after(2000, self.next_question)

    def animate_feedback(self, text, color):
        self.feedback_label.config(text=text, fg=color)
        self.flash_feedback(color, 5)

    def flash_feedback(self, color, count):
        if count > 0:
            current_color = "#A3BE8C" if color == "#BF616A" else "#BF616A"
            self.feedback_label.config(fg=current_color)
            self.root.after(200, lambda: self.feedback_label.config(fg=color))
            self.root.after(400, self.flash_feedback, color, count-1)

    def next_question(self):
        self.currentQuestion += 1
        self.show_question()

    def end_quiz(self):
        self.question_label.config(text=f"Quiz Complete! Final Score: {self.score}/{len(self.quizData)}")
        for btn in self.option_buttons:
            btn.pack_forget()
        self.feedback_label.config(text="")
        self.progress.pack_forget()
        # ASCII art
        ascii_art = """#####
#   #
#   #
#####
  ###
#   #
 # #
  ###
"""
        self.ascii_label = tk.Label(self.root, text=ascii_art, font=("Courier", 12), bg="#2E3440", fg="#88C0D0")
        self.ascii_label.pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()