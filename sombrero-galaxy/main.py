import sys
import numpy as np
from scipy.io import wavfile

from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QMainWindow,
    QLabel,
    QVBoxLayout,
    QGridLayout,
    QFormLayout,
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

import pyqtgraph as pg

class MainWindow(QMainWindow):
    ds = 1

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sombrero Galaxy")

        widget = QWidget()

        layout = QGridLayout()
        audio_wave_layout = QVBoxLayout()
        audio_wave_settings_layout = QFormLayout()

        layout.addLayout(audio_wave_layout, 1, 1)

        self.audio_wave_graph = pg.PlotWidget()
        self.audio_wave_graph.setTitle("Waveform")

        ax_x = self.audio_wave_graph.getAxis("bottom")
        ax_x.setLabel(text="time", units="s")

        ax_y = self.audio_wave_graph.getAxis("left")
        ax_y.setLabel(text="Amplitude")

        load_file_button = QAction("Load File", self)
        load_file_button.triggered.connect(self.open_file_dialog)

        menu = self.menuBar()

        file_menu = menu.addMenu("File")
        file_menu.addAction(load_file_button)

        self.downscale_field = QLineEdit(str(self.ds))
        self.downscale_field.returnPressed.connect(self.downscale_change)

        downscale_field_label = QLabel("downscale factor")

        audio_wave_layout.addWidget(self.audio_wave_graph)
        audio_wave_layout.addLayout(audio_wave_settings_layout)

        audio_wave_settings_layout.addRow(downscale_field_label, self.downscale_field)

        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def downscale_change(self):
        self.ds = int(self.downscale_field.text())
        self.update_plot()

    def open_file_dialog(self):
        file = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "./",
            ""
        )

        self.samplerate, self.data = wavfile.read(file[0])

        self.update_plot()
    
    def update_plot(self):
        time = np.linspace(0., self.data.shape[0] / self.samplerate, self.data.shape[0])
        time = time[::self.ds]

        self.audio_wave_graph.clear()

        self.audio_wave_graph.plot(
            time, 
            self.data[::self.ds, 0], 
            pen=pg.mkPen('b', width=1.0)
        ).setSkipFiniteCheck(skipFiniteCheck=True)
        self.audio_wave_graph.plot(
            time,
            self.data[::self.ds, 1], 
            pen=pg.mkPen('g', width=1.0)
        ).setSkipFiniteCheck(skipFiniteCheck=True)
        
        self.audio_wave_graph.setDownsampling(auto=True)

def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
