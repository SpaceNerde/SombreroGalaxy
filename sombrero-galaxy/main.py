import sys
import wave

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QFileDialog,
    QLineEdit,
    QToolBar
)

from PyQt6.QtCore import (
    Qt,
    QSize
)

from PyQt6.QtGui import (
    QAction
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sombrero Galaxy")

        layout = QVBoxLayout()
        widget = QWidget()

        load_file_button = QAction("Load File", self)
        load_file_button.triggered.connect(self.open_file_dialog)

        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        file_menu.addAction(load_file_button)
        
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def open_file_dialog(self):
        file = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "./",
            ""
        )
        
       #with wave.open(file[0]) as wav_file:
       #     wav_file.close()

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
