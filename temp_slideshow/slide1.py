import os
import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QComboBox, QSpinBox, QHBoxLayout
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QTimer
from qt_material import apply_stylesheet


class ImageSlideshow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visualizador de Imagens - Slideshow")
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #202020; border: 1px solid #444;")

        # Lista de imagens
        self.images = []
        self.index = 0

        # Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_image)

        # Botão para escolher pasta
        self.btn_folder = QPushButton("Escolher Pasta")
        self.btn_folder.clicked.connect(self.choose_folder)

        # Temporizador
        self.combo_time = QComboBox()
        self.combo_time.addItems(["30 segundos", "1 minuto", "Personalizado"])

        self.spin_custom = QSpinBox()
        self.spin_custom.setRange(1, 3600)
        self.spin_custom.setValue(30)
        self.spin_custom.setEnabled(False)

        self.combo_time.currentIndexChanged.connect(self.update_timer_mode)

        # Botão iniciar
        self.btn_start = QPushButton("Iniciar Slideshow")
        self.btn_start.clicked.connect(self.start_slideshow)

        # Layout
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.combo_time)
        time_layout.addWidget(self.spin_custom)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_folder)
        layout.addLayout(time_layout)
        layout.addWidget(self.btn_start)

        self.setLayout(layout)

    def update_timer_mode(self):
        if self.combo_time.currentText() == "Personalizado":
            self.spin_custom.setEnabled(True)
        else:
            self.spin_custom.setEnabled(False)

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher Pasta de Imagens")
        if folder:
            self.images = [
                os.path.join(folder, f)
                for f in os.listdir(folder)
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif"))
            ]
            self.index = 0
            if self.images:
                self.show_image()

    def start_slideshow(self):
        if not self.images:
            return

        if self.combo_time.currentText() == "30 segundos":
            interval = 30
        elif self.combo_time.currentText() == "1 minuto":
            interval = 60
        else:
            interval = self.spin_custom.value()

        self.timer.start(interval * 1000)

    def next_image(self):
        if not self.images:
            return

        self.index = (self.index + 1) % len(self.images)
        self.show_image()

    def show_image(self):
        pixmap = QPixmap(self.images[self.index])

        # Redimensionar imagem ao tamanho da janela
        scaled = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        # Atualiza a imagem quando a janela é redimensionada
        if self.images:
            self.show_image()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Tema escuro moderno
    apply_stylesheet(app, theme="dark_teal.xml")

    window = ImageSlideshow()
    window.resize(900, 600)
    window.show()

    sys.exit(app.exec())
