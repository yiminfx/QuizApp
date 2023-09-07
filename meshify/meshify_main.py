import sys
import os
import json
from PySide2.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, 
                               QGridLayout, QLabel, QFileDialog, QLineEdit, QScrollArea)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()
        self.loadPreferences()

    def initUI(self):
        # Main layout
        mainLayout = QVBoxLayout()

        # Top Shelf
        topLayout = QGridLayout()
        self.sourceImagesDir = QLineEdit(self)
        self.depthImagesDir = QLineEdit(self)
        self.exportDir = QLineEdit(self)
        topLayout.addWidget(QLabel('Source Images:'), 0, 0)
        topLayout.addWidget(self.sourceImagesDir, 0, 1)
        topLayout.addWidget(QPushButton('Browse', clicked=self.setSourceDirectory), 0, 2)
        topLayout.addWidget(QLabel('Depth Images:'), 1, 0)
        topLayout.addWidget(self.depthImagesDir, 1, 1)
        topLayout.addWidget(QPushButton('Browse', clicked=self.setDepthDirectory), 1, 2)
        topLayout.addWidget(QLabel('Export Directory:'), 2, 0)
        topLayout.addWidget(self.exportDir, 2, 1)
        topLayout.addWidget(QPushButton('Browse', clicked=self.setExportDirectory), 2, 2)
        populateButton = QPushButton('Populate Asset', clicked=self.populateGrid)
        topLayout.addWidget(populateButton, 3, 1, 1, 2)
        mainLayout.addLayout(topLayout)

        # Scroll Area for grid
        self.scrollArea = QScrollArea(self)
        self.scrollArea.setWidgetResizable(True)
        self.scrollWidget = QWidget()
        self.gridLayout = QGridLayout(self.scrollWidget)
        self.scrollArea.setWidget(self.scrollWidget)
        mainLayout.addWidget(self.scrollArea)

        # Bottom Shelf
        bottomLayout = QGridLayout()
        batchProcessButton = QPushButton('Batch Process All', clicked=self.batchProcess)
        saveAllButton = QPushButton('Save All', clicked=self.saveAllPreferences)
        bottomLayout.addWidget(batchProcessButton, 0, 0)
        bottomLayout.addWidget(saveAllButton, 0, 1)
        mainLayout.addLayout(bottomLayout)

        # Set central widget
        centralWidget = QWidget()
        centralWidget.setLayout(mainLayout)
        self.setCentralWidget(centralWidget)

    def setSourceDirectory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Source Images Directory")
        if dir_path:
            self.sourceImagesDir.setText(dir_path)

    def setDepthDirectory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Depth Images Directory")
        if dir_path:
            self.depthImagesDir.setText(dir_path)

    def setExportDirectory(self):
        dir_path = QFileDialog.getExistingDirectory(self, "Select Export Directory")
        if dir_path:
            self.exportDir.setText(dir_path)

    def loadPreferences(self):
        prefs_path = os.path.join(os.path.expanduser("~"), "Documents", "meshify_userpref.json")
        if os.path.exists(prefs_path):
            with open(prefs_path, 'r') as prefs_file:
                data = json.load(prefs_file)
                self.sourceImagesDir.setText(data.get('sourceImagesDir', ''))
                self.depthImagesDir.setText(data.get('depthImagesDir', ''))
                self.exportDir.setText(data.get('exportDir', ''))

    def saveAllPreferences(self):
        prefs_data = {
            'sourceImagesDir': self.sourceImagesDir.text(),
            'depthImagesDir': self.depthImagesDir.text(),
            'exportDir': self.exportDir.text()
        }

        prefs_path = os.path.join(os.path.expanduser("~"), "Documents", "meshify_userpref.json")
        with open(prefs_path, 'w') as prefs_file:
            json.dump(prefs_data, prefs_file, indent=4)

    def populateGrid(self):
        # Resetting the grid
        for i in reversed(range(self.gridLayout.count())):
            widget = self.gridLayout.itemAt(i).widget()
            widget.setParent(None)

        sourceDir = self.sourceImagesDir.text()
        if os.path.isdir(sourceDir):
            images = [f for f in os.listdir(sourceDir) if f.endswith('.png')]
            for row, image in enumerate(images):
                self.gridLayout.addWidget(QLabel(image), row, 0)
                processButton = QPushButton('Process')
                processButton.clicked.connect(lambda checked, img=image: self.processImage(img))
                self.gridLayout.addWidget(processButton, row, 1)
                self.gridLayout.addWidget(QLabel('Depth map exists'), row, 2)

    def processImage(self, imageName):
        # Placeholder for image processing logic
        print(f"Processing: {imageName}")

    def batchProcess(self):
        # Placeholder for batch processing logic
        print("Batch Processing All Images")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
