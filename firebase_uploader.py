import sys
import csv
import os
import json
import firebase_admin
from firebase_admin import credentials, db
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QFileDialog, QTableWidget, QTableWidgetItem
from PySide2.QtGui import QColor, QPixmap
from PySide2.QtCore import Qt, QStandardPaths

class QuestionBankApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Question Bank App")
        self.setGeometry(100, 100, 800, 600)

        self.initialize_firebase()
        
        self.initUI()
        
        self.load_question_bank_from_json()
        

    def initUI(self):

        
        layout = QVBoxLayout()

        self.import_button = QPushButton("Import CSV")
        self.import_button.clicked.connect(self.import_csv)
        layout.addWidget(self.import_button)

        self.grid_widget = QTableWidget()
        self.grid_widget.setColumnCount(9)  # Number of columns including the status column
        self.grid_widget.setHorizontalHeaderLabels(["ID", "Date", "Question", "Answer A", "Answer B", "Answer C", "Answer D", "Correct", "Status"])
      
        
        layout.addWidget(self.grid_widget)
        for row_idx in range(10):  # Adjust the range according to your data
            self.grid_widget.setItem(row_idx, 9, QTableWidgetItem("X"))  # Initialize status column



        self.upload_button = QPushButton("Upload")
        self.upload_button.clicked.connect(self.upload_to_firebase)
        layout.addWidget(self.upload_button)

        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.clicked.connect(self.refresh_status)
        layout.addWidget(self.refresh_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.question_bank = {}
        self.load_question_bank_from_json()
        if not self.question_bank:
            # If the question_bank is empty or not loaded from JSON, display data from CSV
            self.display_data()
        else:
            # If question_bank is loaded from JSON, display that data
            self.display_data()
            self.refresh_status()

    def initialize_firebase(self):
        cred = credentials.Certificate("credentials.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://danieledu-9cd63-default-rtdb.firebaseio.com'
        })

    def import_csv(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Import CSV File", "", "CSV Files (*.csv);;All Files (*)")

        if file_name:
            if file_name.lower().endswith('.csv'):
                self.read_csv(file_name)
            else:
                print("Not a CSV file.")




    def read_csv(self, file_path):
        with open(file_path, 'r') as csvfile:
            csvreader = csv.DictReader(csvfile)
            for row in csvreader:
                self.question_bank[row["ID"]] = row

        self.display_data()
        self.save_question_bank_to_json()

    def load_question_bank_from_json(self):
        json_file_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation), 'shsat_vcb_prefs.json')
        if os.path.exists(json_file_path):
            with open(json_file_path, 'r') as jsonfile:
                self.question_bank = json.load(jsonfile)

    def save_question_bank_to_json(self):
        json_file_path = os.path.join(QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation), 'shsat_vcb_prefs.json')
        with open(json_file_path, 'w') as jsonfile:
            json.dump(self.question_bank, jsonfile, indent=4)

    def display_data(self):
        self.grid_widget.setRowCount(0)

        for row_idx, (id, data) in enumerate(self.question_bank.items()):
            self.grid_widget.insertRow(row_idx)
            for col_idx, key in enumerate(data.keys()):
                item = QTableWidgetItem(data[key])
                self.grid_widget.setItem(row_idx, col_idx, item)

            # Add a status item at the end of the row
            status_item = QTableWidgetItem("O")
            status_item.setForeground(QColor(Qt.yellow))
            self.grid_widget.setItem(row_idx, len(data.keys()), status_item)





    def upload_to_firebase(self):
        ref = db.reference('question_bank')
        ref.set(self.question_bank)
        print("Uploaded to Firebase")


    def refresh_status(self):
        ref = db.reference('question_bank')
        for row_idx in range(self.grid_widget.rowCount()):
            id_item = self.grid_widget.item(row_idx, 0)
            if id_item:
                question_id = id_item.text()
                status_item = self.grid_widget.item(row_idx, len(self.question_bank))  # Index for "Status" column

                if question_id in ref.get():
                    status_item = QTableWidgetItem("O")
                    status_item.setForeground(QColor(Qt.green))
                    self.grid_widget.setItem(row_idx, 8, status_item)
                    status_item.setToolTip("Uploaded to Firebase")
                        
                else:
                    status_item = QTableWidgetItem("O")
                    status_item.setForeground(QColor(Qt.red))
                    self.grid_widget.setItem(row_idx, 8, status_item)
                    status_item.setToolTip("Uploaded to Firebase")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QuestionBankApp()
    window.show()
    sys.exit(app.exec_())
