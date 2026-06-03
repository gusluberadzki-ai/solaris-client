# average grade calculator by Gustaw
import tkinter as tk
from tkinter import messagebox


GRADE_VALUES = {
    "A+": 14,
    "A": 13,
    "A-": 12,
    "B+": 11,
    "B": 10,
    "B-": 9,
    "C+": 8,
    "C": 7,
    "C-": 6,
    "D+": 5,
    "D": 4,
    "D-": 3,
    "E": 2,
    "F": 1,
}

VALUE_TO_GRADE = {value: grade for grade, value in GRADE_VALUES.items()}


class AverageGradeCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Average Grade Calculator")
        self.root.geometry("720x520")
        self.root.minsize(640, 460)
        self.root.configure(bg="#f4efe6")

        self.grades = []
        self.grade_var = tk.StringVar(value="A")
        self.average_var = tk.StringVar(value="Average grade: --")
        self.details_var = tk.StringVar(value="Add grades to calculate your average.")

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="Average Grade Calculator",
            font=("Avenir Next", 26, "bold"),
            bg="#f4efe6",
            fg="#3d2c1e",
        )
        title.pack(pady=(24, 8))

        subtitle = tk.Label(
            self.root,
            text="Add your grades one by one and see the average instantly.",
            font=("Avenir Next", 13),
            bg="#f4efe6",
            fg="#6a5848",
        )
        subtitle.pack(pady=(0, 18))

        card = tk.Frame(
            self.root,
            bg="#fffaf2",
            bd=0,
            highlightthickness=2,
            highlightbackground="#d7c4aa",
            padx=24,
            pady=24,
        )
        card.pack(fill="both", expand=True, padx=28, pady=(0, 28))

        controls = tk.Frame(card, bg="#fffaf2")
        controls.pack(fill="x", pady=(0, 18))

        grade_label = tk.Label(
            controls,
            text="Choose grade",
            font=("Avenir Next", 12, "bold"),
            bg="#fffaf2",
            fg="#3d2c1e",
        )
        grade_label.grid(row=0, column=0, sticky="w")

        grade_menu = tk.OptionMenu(controls, self.grade_var, *GRADE_VALUES.keys())
        grade_menu.config(
            font=("Avenir Next", 12),
            bg="#f1dfc4",
            fg="#2f241b",
            activebackground="#e5cda8",
            activeforeground="#2f241b",
            width=8,
            highlightthickness=0,
            bd=0,
        )
        grade_menu["menu"].config(font=("Avenir Next", 12), bg="#fffaf2", fg="#2f241b")
        grade_menu.grid(row=1, column=0, sticky="w", pady=(8, 0))

        add_button = tk.Button(
            controls,
            text="Add Grade",
            command=self.add_grade,
            font=("Avenir Next", 12, "bold"),
            bg="#bf7b30",
            fg="white",
            activebackground="#a5641f",
            activeforeground="white",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
        )
        add_button.grid(row=1, column=1, padx=14, pady=(8, 0))

        remove_button = tk.Button(
            controls,
            text="Remove Selected",
            command=self.remove_selected,
            font=("Avenir Next", 12),
            bg="#d8c5ad",
            fg="#2f241b",
            activebackground="#cbb394",
            activeforeground="#2f241b",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
        )
        remove_button.grid(row=1, column=2, padx=0, pady=(8, 0))

        clear_button = tk.Button(
            controls,
            text="Clear All",
            command=self.clear_grades,
            font=("Avenir Next", 12),
            bg="#efe5d6",
            fg="#5c4634",
            activebackground="#e2d2bc",
            activeforeground="#5c4634",
            relief="flat",
            padx=18,
            pady=10,
            cursor="hand2",
        )
        clear_button.grid(row=1, column=3, padx=14, pady=(8, 0))

        content = tk.Frame(card, bg="#fffaf2")
        content.pack(fill="both", expand=True)
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_rowconfigure(0, weight=1)

        list_frame = tk.Frame(content, bg="#f9f1e6", padx=16, pady=16)
        list_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        list_title = tk.Label(
            list_frame,
            text="Grades Entered",
            font=("Avenir Next", 14, "bold"),
            bg="#f9f1e6",
            fg="#3d2c1e",
        )
        list_title.pack(anchor="w")

        self.grade_listbox = tk.Listbox(
            list_frame,
            font=("Avenir Next", 13),
            bg="#fffdf9",
            fg="#2f241b",
            selectbackground="#bf7b30",
            selectforeground="white",
            relief="flat",
            bd=0,
            height=12,
        )
        self.grade_listbox.pack(fill="both", expand=True, pady=(12, 0))

        result_frame = tk.Frame(content, bg="#3f2c23", padx=20, pady=20)
        result_frame.grid(row=0, column=1, sticky="nsew", padx=(10, 0))

        result_title = tk.Label(
            result_frame,
            text="Result",
            font=("Avenir Next", 14, "bold"),
            bg="#3f2c23",
            fg="#f6e7cf",
        )
        result_title.pack(anchor="w")

        average_label = tk.Label(
            result_frame,
            textvariable=self.average_var,
            font=("Avenir Next", 24, "bold"),
            bg="#3f2c23",
            fg="#ffd28a",
        )
        average_label.pack(anchor="w", pady=(18, 12))

        details_label = tk.Label(
            result_frame,
            textvariable=self.details_var,
            font=("Avenir Next", 12),
            bg="#3f2c23",
            fg="#f5ddbb",
            justify="left",
            wraplength=260,
        )
        details_label.pack(anchor="w")

        hint_label = tk.Label(
            result_frame,
            text="Tip: select a grade on the left to remove it.",
            font=("Avenir Next", 11, "italic"),
            bg="#3f2c23",
            fg="#cfb28b",
        )
        hint_label.pack(anchor="w", pady=(22, 0))

    def add_grade(self):
        grade = self.grade_var.get()
        self.grades.append(grade)
        self.grade_listbox.insert(tk.END, grade)
        self.update_average()

    def remove_selected(self):
        selected_index = self.grade_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("No selection", "Select a grade to remove.")
            return

        index = selected_index[0]
        self.grade_listbox.delete(index)
        self.grades.pop(index)
        self.update_average()

    def clear_grades(self):
        self.grades.clear()
        self.grade_listbox.delete(0, tk.END)
        self.update_average()

    def update_average(self):
        if not self.grades:
            self.average_var.set("Average grade: --")
            self.details_var.set("Add grades to calculate your average.")
            return

        total = sum(GRADE_VALUES[grade] for grade in self.grades)
        count = len(self.grades)
        average_value = round(total / count)
        average_grade = VALUE_TO_GRADE[average_value]

        self.average_var.set(f"Average grade: {average_grade}")
        self.details_var.set(
            f"Total grades entered: {count}\n"
            f"Rounded score value: {average_value}\n"
            f"Current grade list: {', '.join(self.grades)}"
        )


def main():
    root = tk.Tk()
    app = AverageGradeCalculator(root)
    root.mainloop()


if __name__ == "__main__":
    main()
