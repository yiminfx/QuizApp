import sys
import os
from PySide2.QtCore import Qt, QTimer
from PySide2.QtGui import QImage, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QToolBar, QProgressBar

class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Image Sequence Viewer")
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Get the script's directory and join it with the folder name
        script_directory = os.path.dirname(os.path.abspath(__file__))
        self.image_sequence_folder = os.path.join(script_directory, 'src', 'BEN_Previs_1')

        self.total_images = len(os.listdir(self.image_sequence_folder))

        self.init_ui()
        self.current_image_index = 0

        # Set the desired frame rate (24 FPS)
        self.frame_rate = 24
        self.frame_interval = 1000 // self.frame_rate

        self.animation_timer = QTimer(self)
        self.animation_timer.timeout.connect(self.update_image)

        # Flag to keep track of mouse hover
        self.is_mouse_hovering = False

    def init_ui(self):
        layout = QVBoxLayout()

        self.view = QGraphicsView(self)
        layout.addWidget(self.view)
        self.scene = QGraphicsScene(self)
        self.view.setScene(self.scene)
        self.view.setAlignment(Qt.AlignCenter)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initialize the progress bar here
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setVisible(False)  # Initially, hide the progress bar
        layout.addWidget(self.progress_bar)

        self.load_image(0)

        # Create a custom toolbar stylesheet to set the background color to teal
        toolbar_stylesheet = """
            QToolBar {
                background-color: teal;
            }
        """

        # Apply the stylesheet to the toolbar
        self.toolbar = QToolBar(self)
        self.toolbar.setStyleSheet(toolbar_stylesheet)
        self.addToolBar(self.toolbar)

        # Add widgets and actions to the toolbar as needed

    def load_image(self, index):
        image_path = os.path.join(
            self.image_sequence_folder, f"thumbnail.{index:04d}.png"
        )
        if os.path.exists(image_path):
            image = QImage(image_path)
            pixmap = QPixmap.fromImage(image)
            self.scene.clear()
            self.scene.addPixmap(pixmap)

            # Calculate the progress based on the current image index
            progress = (index + 1) / self.total_images * 100
            self.progress_bar.setValue(progress)

    def update_image(self):
        if self.current_image_index < self.total_images - 1:
            self.current_image_index += 1
        else:
            self.current_image_index = 0

        self.load_image(self.current_image_index)

    def enterEvent(self, event):
        if not self.animation_timer.isActive():
            self.animation_timer.start(self.frame_interval)  # Adjust the interval for 24 FPS
        self.is_mouse_hovering = True
        self.progress_bar.setVisible(True)

    def leaveEvent(self, event):
        if self.animation_timer.isActive():
            self.animation_timer.stop()
        self.is_mouse_hovering = False
        self.progress_bar.setVisible(False)

def main():
    app = QApplication(sys.argv)
    viewer = ImageViewer()
    viewer.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
