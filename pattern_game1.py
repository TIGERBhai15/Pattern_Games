import sys
import random
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QGridLayout
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QFont

class LogicGame(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-Level Logic Pattern Game")
        self.resize(400, 400)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.info_label = QLabel("Memorize the pattern")
        self.info_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.info_label)

        self.grid_layout = QGridLayout()
        self.layout.addLayout(self.grid_layout)

        self.score_label = QLabel("Score: 0")
        self.layout.addWidget(self.score_label)

        self.level = 1
        self.score = 0
        self.pattern = []
        self.user_input = []
        self.buttons = []

        self.max_buttons = 9  # Maximum buttons on grid
        self.create_buttons()
        self.start_level()

    def create_buttons(self):
        for i in range(self.max_buttons):
            btn = QPushButton(str(i + 1))
            btn.setFont(QFont("Arial", 16))
            btn.setVisible(False)
            btn.clicked.connect(self.make_handler(i))
            self.buttons.append(btn)
            self.grid_layout.addWidget(btn, i // 3, i % 3)

    def make_handler(self, index):
        def handler():
            self.user_input.append(index)
            if self.user_input == self.pattern[:len(self.user_input)]:
                if len(self.user_input) == len(self.pattern):
                    self.score += 10
                    self.score_label.setText(f"Score: {self.score}")
                    self.level += 1
                    self.start_level()
            else:
                QMessageBox.warning(self, "Wrong!", "Wrong pattern! Try again.")
                self.level = 1
                self.score = 0
                self.score_label.setText("Score: 0")
                self.start_level()
        return handler

    def start_level(self):
        self.user_input = []
        btn_count = min(3 + self.level - 1, self.max_buttons)
        pattern_len = min(3 + self.level - 1, btn_count)
        delay_time = max(1000, 4000 - self.level * 250)  # Decrease delay

        for i, btn in enumerate(self.buttons):
            btn.setVisible(i < btn_count)

        self.pattern = [random.randint(0, btn_count - 1) for _ in range(pattern_len)]
        self.info_label.setText(f"Level {self.level}: Memorize the pattern")

        self.show_pattern(delay_time)

    def show_pattern(self, delay):
        def flash(i):
            if i < len(self.pattern):
                idx = self.pattern[i]
                self.buttons[idx].setStyleSheet("background-color: yellow")
                QTimer.singleShot(400, lambda: self.reset_button(idx))
                QTimer.singleShot(500, lambda: flash(i + 1))
            else:
                self.info_label.setText("Repeat the pattern")

        flash(0)

    def reset_button(self, idx):
        self.buttons[idx].setStyleSheet("")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = LogicGame()
    game.show()
    sys.exit(app.exec())
