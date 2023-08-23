import sys
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PySide2.QtCore import QStandardPaths

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Generate TXT'
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        layout = QVBoxLayout()

        btn = QPushButton('Generate TXT', self)
        btn.clicked.connect(self.generate_txt_file)
        layout.addWidget(btn)

        self.setLayout(layout)
        self.show()

    def generate_txt_file(self):
        # Getting the path to the user's documents folder
        documents_path = QStandardPaths.writableLocation(QStandardPaths.DocumentsLocation)
        # Constructing the full path to the txt file
        file_path = documents_path + '/temp_delete.txt'

        # Writing the content to the file
        with open(file_path, 'w') as file:
            file.write('123')

        print(f"File saved to {file_path}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
