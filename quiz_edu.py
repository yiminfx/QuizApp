import sys
import os
import json
import random
from PySide2.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout,QVBoxLayout, QLabel, QPushButton, QRadioButton, QMessageBox, QInputDialog, QComboBox
import firebase_admin
from firebase_admin import credentials, db
import datetime

from PySide2.QtCore import Qt, QStandardPaths
class StartupWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

       
        
         # Initialize Firebase
        cred = credentials.Certificate("credentials.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://danieledu-9cd63-default-rtdb.firebaseio.com'
        })


    def initUI(self):
        layout = QVBoxLayout()
        self.setWindowTitle('Select Question Bank')
        
        self.question_bank_label = QLabel('Select Question Bank:')
        self.question_bank_combo = QComboBox()
        
        self.load_question_banks()  # Load available question banks
        
        layout.addWidget(self.question_bank_label)
        layout.addWidget(self.question_bank_combo)
        
        self.start_button = QPushButton('Start Quiz')
        self.start_button.clicked.connect(self.start_quiz)
        layout.addWidget(self.start_button)
        
        self.setLayout(layout)
        
    def load_question_banks(self):
        prefs_file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'shsat_vcb_prefs.json')

        if os.path.exists(prefs_file_path):
            with open(prefs_file_path, 'r') as prefs_file:
                prefs_data = json.load(prefs_file)
                question_banks = list(prefs_data.keys())
                self.question_bank_combo.addItems(question_banks)
        else:
            self.show_error_message('Question bank preferences file not found.')

    def start_quiz(self):
        selected_bank = self.question_bank_combo.currentText()
        self.quiz_app = QuizApp(selected_bank)
        self.quiz_app.show()
        self.close()

    def show_error_message(self, message):
        error_msg = QMessageBox(self)
        error_msg.setWindowTitle('Error')
        error_msg.setText(message)
        error_msg.setIcon(QMessageBox.Critical)
        error_msg.exec_()


class QuizApp(QMainWindow):
    def __init__(self, selected_bank):
        super().__init__()
        self.username = ''
        self.selected_bank = selected_bank
        #self.initUI()

        self.load_username()
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
            QLabel {
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
                color: #CCCCCC;
            }
        ''')

        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(QVBoxLayout())  # Set up central widget's layout

        # Load username from preferences or prompt user to create one
        self.load_username()

        # Display username label
        self.username_label = QLabel(f"Welcome {self.username}", self)
        self.username_label.setAlignment(Qt.AlignRight)
        self.username_label.setStyleSheet("color: white; font-size: 16px; padding-right: 20px;")
        self.central_widget.layout().addWidget(self.username_label)

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

    def upload_quiz_results(self, quiz_results):
        ref = db.reference('test_results')
        results_ref = ref.child(self.selected_bank).child(self.username)
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        results_ref.child(timestamp).set(quiz_results)

    def load_question_banks(self):
        prefs_file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'shsat_vcb_prefs.json')

        if os.path.exists(prefs_file_path):
            with open(prefs_file_path, 'r') as prefs_file:
                prefs_data = json.load(prefs_file)
                question_banks = list(prefs_data.keys())  # Convert to a list
                if question_banks:
                    self.question_bank_combo.addItems(question_banks)
                    self.question_bank_combo.setCurrentIndex(0)  # Select the first question bank
                else:
                    self.show_error_message('No question banks found.')
        else:
            self.show_error_message('Question bank preferences file not found.')


    def load_question_bank(self):
        selected_bank = self.selected_bank
        prefs_file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'shsat_vcb_prefs.json')

        if os.path.exists(prefs_file_path):
            with open(prefs_file_path, 'r') as prefs_file:
                prefs_data = json.load(prefs_file)
                if selected_bank in prefs_data:
                    self.question_bank = prefs_data[selected_bank]
                else:
                    self.show_error_message(f'Question bank "{selected_bank}" not found.')
        else:
            self.show_error_message('Question bank preferences file not found.')

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
            self.question_label.setWordWrap(True)

            font = self.font()
            font.setPointSize(14)  # Change this to the desired font size

            for idx, answer in enumerate(['Answer A', 'Answer B', 'Answer C', 'Answer D']):    
                answer_radio = QRadioButton(f'{chr(65 + idx)}: {question_data[answer]}')  # Add A:, B:, C:, D: labels
                answer_radio.toggled.connect(lambda state, a=f'{chr(65 + idx)}': self.select_answer(a, state))
                answer_radio.setFont(font)
                self.answers_radio_layout.addWidget(answer_radio)  # Add answer radio button to layout

            self.prev_button.setEnabled(self.current_question_index > 0)  # Enable/disable previous button
            self.next_button.setEnabled(self.current_question_index < len(self.selected_questions) - 1)  # Enable/disable next button
            self.submit_button.setEnabled(True)  # Enable submit button

            self.setWindowTitle(f'Quiz - Question {self.current_question_index + 1}/{len(self.selected_questions)}')
        else:
            self.show_result()

    def load_username(self):
        prefs_file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'shsat_quiz_prefs.json')

        if os.path.exists(prefs_file_path):
            with open(prefs_file_path, 'r') as prefs_file:
                prefs_data = json.load(prefs_file)
                if 'username' in prefs_data:
                    self.username = prefs_data['username']
                else:
                    self.prompt_for_username()
        else:
            self.prompt_for_username()
   
    def prompt_for_username(self):
        self.username, ok = QInputDialog.getText(self, 'Create Username', 'Please enter your username:')
        if ok and self.username:
            prefs_file_path = os.path.join(os.path.expanduser('~'), 'Documents', 'shsat_quiz_prefs.json')
            with open(prefs_file_path, 'w') as prefs_file:
                prefs_data = {'username': self.username}
                json.dump(prefs_data, prefs_file)

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
        print(self.selected_answers)
        score = sum(1 for selected, correct in zip(self.selected_answers, 
                                                   [self.question_bank[q]['Correct'] for q in self.selected_questions]) if selected == correct)
      

                # Upload quiz results to Firebase
        quiz_results = {
            'datetime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M'),
            'score': score,
            'correct': [q_id for q_id, selected, correct in zip(self.selected_questions, self.selected_answers,
                                                                [self.question_bank[q]['Correct'] for q in self.selected_questions]) if selected == correct],
            'incorrect': [q_id for q_id, selected, correct in zip(self.selected_questions, self.selected_answers,
                                                                [self.question_bank[q]['Correct'] for q in self.selected_questions]) if selected != correct]
        }
        
        self.upload_quiz_results(quiz_results)
        self.show_score(score)


    def show_score(self, score):
        score_message = f'Your score: {score} / {len(self.selected_questions)}'
        if score < len(self.selected_questions):
            score_message += '\n\nIncorrect answers:'
            for idx, (selected, correct) in enumerate(zip(self.selected_answers, 
                                                           [self.question_bank[q]['Correct'] for q in self.selected_questions]), start=1):
                if selected != correct:
                    question_text = self.question_bank[self.selected_questions[idx - 1]]['Question']
                    
                    user_answer = ''
                    if selected is not None:
                        user_answer = self.question_bank[self.selected_questions[idx - 1]][f'Answer {selected}']
                    
                    correct_answer = self.question_bank[self.selected_questions[idx - 1]][f'Answer {correct}']

                    score_message += f'\nQ{idx} {question_text}:\n\n You selected {selected} {user_answer} \t Correct answer: {correct} {correct_answer}\n'
        self.show_info_message(score_message)
        self.restart_quiz()

    def show_info_message(self, message):
        info_box = QMessageBox()
        info_box.setIcon(QMessageBox.Information)
        info_box.setText(message)
        info_box.setWindowTitle('Quiz Result')
        info_box.addButton('Restart Quiz', QMessageBox.AcceptRole)
        info_box.addButton('Quit', QMessageBox.RejectRole)
        info_box.setStyleSheet('''
        background-color: #2E2E2E;
        color: #FFFFFF;
        QPushButton {
            background-color: #555555;
            color: #FFFFFF;
        }
        QPushButton:hover {
            background-color: #666666;
        }
    ''')
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

'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWindow = QuizApp()
    mainWindow.show()
    sys.exit(app.exec_())
'''
if __name__ == '__main__':
    app = QApplication(sys.argv)
    startup_window = StartupWindow()
    startup_window.show()
    sys.exit(app.exec_())