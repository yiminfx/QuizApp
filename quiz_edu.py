import sys
import os
import json
import random
from PySide2.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QRadioButton, QHBoxLayout, QMessageBox
from PySide2.QtCore import Qt, QStandardPaths

class QuizApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_question_bank()
        self.selected_questions = random.sample(list(self.question_bank.keys()), 10)
        self.current_question_index = 0
        self.selected_answers = [None] * len(self.selected_questions)
        self.show_question()

    def initUI(self):
        self.setWindowTitle('Quiz App')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet('''
            QMainWindow {
                background-color: #2E2E2E;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #555555;
                color: #FFFFFF;
                border: none;
                padding: 5px 10px;
            }
            QPushButton:hover {
                background-color: #666666;
            }
            QRadioButton {
                color: #FFFFFF;
            }
        ''')

        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(QVBoxLayout())  # Set up central widget's layout

        self.question_id_label = QLabel(self)
        #self.question_id_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        self.central_widget.layout().addWidget(self.question_id_label)  # Add question ID label to central widget's layout

        self.question_label = QLabel(self)
        self.central_widget.layout().addWidget(self.question_label)  # Add question label to central widget's layout

        self.answers_radio_layout = QVBoxLayout()  # Layout for answer choices
        self.central_widget.layout().addLayout(self.answers_radio_layout)  # Add answers layout to central widget's layout

         # Customize font size for question and answer choices
        font = self.font()
        font.setPointSize(24)  # Change this to the desired font size
        self.question_label.setFont(font)
        for idx in range(self.answers_radio_layout.count()):
            answer_radio = self.answers_radio_layout.itemAt(idx).widget()
            answer_radio.setFont(font)

        self.prev_button = QPushButton('Previous', self)
        self.prev_button.clicked.connect(self.prev_question)
        self.prev_button.setEnabled(False)  # Disable previous button initially
        self.next_button = QPushButton('Next', self)
        self.next_button.clicked.connect(self.next_question)
        self.submit_button = QPushButton('Submit', self)
        self.submit_button.clicked.connect(self.submit_quiz)
        self.submit_button.setEnabled(False)  # Disable submit button initially

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.prev_button)
        buttons_layout.addWidget(self.next_button)
        buttons_layout.addWidget(self.submit_button)
        self.central_widget.layout().addLayout(buttons_layout)  # Add buttons layout to central widget's layout

    def load_question_bank(self):
        prefs_file_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation), 'shsat_vcb_prefs.json')
        
        if not os.path.exists(prefs_file_path):
            self.fetch_data_from_firebase_and_create_prefs(prefs_file_path)
        
        with open(prefs_file_path, 'r') as prefs_file:
            self.question_bank = json.load(prefs_file)

    def fetch_data_from_firebase_and_create_prefs(self, prefs_file_path):
        # Fetch data from Firebase and populate self.question_bank
        self.question_bank = {}  # Replace with your code to fetch data

        with open(prefs_file_path, 'w') as prefs_file:
            json.dump(self.question_bank, prefs_file, indent=4)

    def show_question(self):
        if 0 <= self.current_question_index < len(self.selected_questions):
            question_id = self.selected_questions[self.current_question_index]
            question_data = self.question_bank[question_id]

            self.question_id_label.setText(f'Question ID: {question_id}')  # Update question ID label

            self.clear_layout(self.answers_radio_layout)  # Clear answer choices layout

            self.question_label.setText(question_data['Question'])  # Update question label

            for idx, answer in enumerate(['Answer A', 'Answer B', 'Answer C', 'Answer D']):
                answer_radio = QRadioButton(f'{chr(65 + idx)}: {question_data[answer]}')  # Add A:, B:, C:, D: labels
                answer_radio.toggled.connect(lambda state, a=answer: self.select_answer(a, state))
                self.answers_radio_layout.addWidget(answer_radio)  # Add answer radio button to layout

            self.prev_button.setEnabled(self.current_question_index > 0)  # Enable/disable previous button
            self.next_button.setEnabled(self.current_question_index < len(self.selected_questions) - 1)  # Enable/disable next button
            self.submit_button.setEnabled(True)  # Enable submit button

            self.setWindowTitle(f'Quiz - Question {self.current_question_index + 1}/{len(self.selected_questions)}')
        else:
            self.show_result()

    def next_question(self):
        if self.current_question_index < len(self.selected_questions) - 1:
            self.current_question_index += 1
            self.show_question()

    def prev_question(self):
        if self.current_question_index > 0:
            self.current_question_index -= 1
            self.show_question()

    def select_answer(self, answer, state):
        if state:
            self.selected_answers[self.current_question_index] = answer

    def submit_quiz(self):
        score = sum(1 for selected, correct in zip(self.selected_answers, 
                                                   [self.question_bank[q]['Correct'] for q in self.selected_questions]) if selected == correct)
        self.show_score(score)

    def show_score(self, score):
        score_message = f'Your score: {score} / {len(self.selected_questions)}'
        if score < len(self.selected_questions):
            score_message += '\n\nIncorrect answers:'
            for idx, (selected, correct) in enumerate(zip(self.selected_answers, 
                                                           [self.question_bank[q]['Correct'] for q in self.selected_questions]), start=1):
                if selected != correct:
                    score_message += f'\nQuestion {idx}: You selected {selected}, Correct answer: {correct}'
        self.show_info_message(score_message)
        self.restart_quiz()

    def show_info_message(self, message):
        info_box = QMessageBox()
        info_box.setIcon(QMessageBox.Information)
        info_box.setText(message)
        info_box.setWindowTitle('Quiz Result')
        info_box.addButton('Restart Quiz', QMessageBox.AcceptRole)
        info_box.addButton('Quit', QMessageBox.RejectRole)
        result = info_box.exec_()
        if result == 0:
            self.restart_quiz()
        else:
            self.close()

    def restart_quiz(self):
        self.current_question_index = 0
        self.selected_answers = [None] * len(self.selected_questions)
        self.show_question()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = QuizApp()
    mainWindow.show()
    sys.exit(app.exec_())
