import sys
import random
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton,
    QVBoxLayout, QLineEdit, QMessageBox
)
from PyQt6.QtCore import QTimer


class LogicGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logic Game with Levels, Timer and Score")
        self.level = 1
        self.score = 0
        self.time_left = 30

        self.sequence = []
        self.answer = None
        self.logic = ""

        self.layout = QVBoxLayout()

        self.title_label = QLabel("Guess the Pattern")
        self.level_label = QLabel()
        self.sequence_label = QLabel()
        self.timer_label = QLabel("Time left: 30s")
        self.score_label = QLabel("Score: 0")
        self.input_line = QLineEdit()
        self.submit_button = QPushButton("Submit")
        self.next_button = QPushButton("Next Level")

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.level_label)
        self.layout.addWidget(self.sequence_label)
        self.layout.addWidget(self.timer_label)
        self.layout.addWidget(self.score_label)
        self.layout.addWidget(self.input_line)
        self.layout.addWidget(self.submit_button)
        self.layout.addWidget(self.next_button)

        self.setLayout(self.layout)

        self.submit_button.clicked.connect(self.check_answer)
        self.next_button.clicked.connect(self.next_level)
        self.next_button.setEnabled(False)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_timer)

        self.generate_question()

    def generate_question(self):
        self.input_line.clear()
        self.time_left = 30
        self.timer_label.setText(f"Time left: {self.time_left}s")
        self.timer.start(1000)

        patterns = [
            self.generate_add_pattern,
            self.generate_multiply_pattern,
            self.generate_fibonacci,
            self.generate_square,
            self.generate_alternating,
            self.generate_custom_mix
        ]

        if self.level > len(patterns):
            self.timer.stop()
            QMessageBox.information(
                self, "Finished",
                f"You completed all levels!\nFinal Score: {self.score}")
            self.close()
            return

        self.sequence, self.answer, self.logic = patterns[self.level - 1]()
        self.level_label.setText(f"Level {self.level}")
        self.sequence_label.setText(f"Sequence: {self.sequence}")

    def generate_add_pattern(self):
        start = random.randint(1, 10)
        step = random.randint(2, 6)
        sequence = [start + step * i for i in range(4)]
        return sequence, sequence[-1] + step, f"Add {step}"

    def generate_multiply_pattern(self):
        start = random.randint(1, 5)
        factor = random.randint(2, 3)
        sequence = [start * (factor ** i) for i in range(4)]
        return sequence, sequence[-1] * factor, f"Multiply by {factor}"

    def generate_fibonacci(self):
        a, b = random.randint(0, 3), random.randint(1, 4)
        sequence = []
        for _ in range(4):
            sequence.append(a)
            a, b = b, a + b
        return sequence, a, "Fibonacci sequence"

    def generate_square(self):
        base = random.randint(2, 6)
        sequence = [base + i for i in range(4)]
        squares = [x * x for x in sequence]
        return squares, (base + 4) ** 2, "Square of increasing numbers"

    def generate_alternating(self):
        start = random.randint(1, 10)
        add = random.randint(2, 5)
        sequence = []
        for i in range(4):
            start = start + add if i % 2 == 0 else start - add
            sequence.append(start)
        next_val = start + add if len(sequence) % 2 == 0 else start - add
        return sequence, next_val, "Alternating + and -"

    def generate_custom_mix(self):
        base = random.randint(2, 5)
        sequence = [base + i**2 for i in range(4)]
        return sequence, base + 16, "Mix of linear and square growth"

    def update_timer(self):
        self.time_left -= 1
        self.timer_label.setText(f"Time left: {self.time_left}s")
        if self.time_left == 0:
            self.timer.stop()
            QMessageBox.warning(self, "Time Up", "You ran out of time!")
            self.next_button.setEnabled(True)

    def check_answer(self):
        try:
            guess = int(self.input_line.text())
            if guess == self.answer:
                self.timer.stop()
                self.score += 10
                self.score_label.setText(f"Score: {self.score}")
                QMessageBox.information(self, "Correct", f"✅ Correct! Logic: {self.logic}")
                self.next_button.setEnabled(True)
            else:
                QMessageBox.warning(self, "Wrong", "❌ Wrong answer. Try again or wait for timeout.")
        except ValueError:
            QMessageBox.warning(self, "Invalid", "Please enter a valid number.")

    def next_level(self):
        self.level += 1
        self.next_button.setEnabled(False)
        self.generate_question()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = LogicGame()
    game.show()
    sys.exit(app.exec())
