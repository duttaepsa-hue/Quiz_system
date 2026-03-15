import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog

class Question:
    def __init__(self, question, options, answer):
        self.question = question
        self.options = options
        self.answer = answer

class Quiz:
    def __init__(self, questions):
        self.questions = questions
        self.score = 0
        self.current_question = 0

        # ------------------ WINDOW ------------------ #
        self.root = tk.Tk()
        self.root.title("Quiz Game by Ani")
        self.root.geometry("600x400")
        self.root.configure(bg="#2f4f7f")

        # ------------------ QUESTION LABEL ------------------ #
        self.question_label = tk.Label(
            self.root,
            text="",
            wraplength=500,
            bg="#2f4f7f",
            fg="white",
            font=("Arial", 18, "bold"),
        )
        self.question_label.pack(pady=20)

        # ------------------ OPTION BUTTONS ------------------ #
        self.option_buttons = []
        for i in range(4):
            button = tk.Button(
                self.root,
                text="",
                width=30,
                bg="#4f7f9f",
                fg="white",
                font=("Arial", 14),
                command=lambda i=i: self.check_answer(i),
            )
            button.pack(pady=8)
            self.option_buttons.append(button)

        # ------------------ RESULT LABEL ------------------ #
        self.result_label = tk.Label(
            self.root,
            text="",
            bg="#2f4f7f",
            fg="white",
            font=("Arial", 16),
        )
        self.result_label.pack(pady=20)

        self.display_question()

    # ------------------ DISPLAY QUESTION ------------------ #
    def display_question(self):
        q = self.questions[self.current_question]
        self.question_label.config(text=q.question)

        for i, option in enumerate(q.options):
            self.option_buttons[i].config(text=option, state="normal")

        self.result_label.config(text="")

    # ------------------ CHECK ANSWER ------------------ #
    def check_answer(self, i):
        q = self.questions[self.current_question]
        if q.options[i] == q.answer:
            self.score += 1
            self.result_label.config(text="Correct!", fg="lightgreen")
        else:
            self.result_label.config(
                text=f"Incorrect! Correct answer: {q.answer}", fg="red"
            )

        # Disable buttons
        for btn in self.option_buttons:
            btn.config(state="disabled")

        self.root.after(1500, self.next_question)

    # ------------------ NEXT QUESTION ------------------ #
    def next_question(self):
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.display_question()
        else:
            self.end_quiz()

    # ------------------ END QUIZ ------------------ #
    def end_quiz(self):
        self.question_label.config(
            text=f"Quiz Finished! You scored {self.score}/{len(self.questions)}"
        )

        for btn in self.option_buttons:
            btn.config(state="disabled")

        self.save_score()

    # ------------------ SAVE SCORE ------------------ #
    def save_score(self):
        name = simpledialog.askstring("Save Score", "Enter your name:")
        if not name:
            return

        if not os.path.exists("scores.json"):
            with open("scores.json", "w") as f:
                json.dump({}, f)

        with open("scores.json", "r+") as f:
            scores = json.load(f)
            scores[name] = self.score
            f.seek(0)
            json.dump(scores, f, indent=4)
            f.truncate()

        messagebox.showinfo("Score Saved", "Your score has been saved!")

    # ------------------ RUN APP ------------------ #
    def run(self):
        self.root.mainloop()

# ------------------ MAIN ------------------ #
def main():
    questions = [
        Question("What is the capital of France?", ["Berlin", "Paris", "London", "Rome"], "Paris"),
        Question("What is the largest planet in our Solar System?", ["Earth", "Saturn", "Jupiter", "Mars"], "Jupiter"),
        Question("Who painted the Mona Lisa?", ["Leonardo da Vinci", "Michelangelo", "Raphael", "Caravaggio"], "Leonardo da Vinci"),
    ]

    quiz = Quiz(questions)
    quiz.run()


if __name__ == "__main__":
    main()