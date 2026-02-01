import os
import sys
import cv2
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QComboBox, QSpinBox, QHBoxLayout, QCheckBox, QSizePolicy
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTimer
from qt_material import apply_stylesheet


class ImageSlideshow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visualizador de Imagens e Vídeos - Slideshow Moderno")

        # Área de apresentação
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #202020; border: 1px solid #444;")
        self.image_label.setScaledContents(False)
        self.image_label.setMinimumSize(1, 1)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Lista de ficheiros
        self.files = []
        self.index = 0

        # Vídeo
        self.video_cap = None
        self.video_timer = QTimer()
        self.video_timer.timeout.connect(self.play_video_frame)

        # Timer slideshow
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_file)

        # Botões
        self.btn_folder = QPushButton("Escolher Pasta")
        self.btn_folder.clicked.connect(self.choose_folder)

        self.btn_prev = QPushButton("Anterior")
        self.btn_prev.clicked.connect(self.prev_file)

        self.btn_next = QPushButton("Próxima")
        self.btn_next.clicked.connect(self.next_file)

        self.btn_pause = QPushButton("Pausar")
        self.btn_pause.clicked.connect(self.toggle_pause)

        # Temporizador
        self.combo_time = QComboBox()
        self.combo_time.addItems(["30 segundos", "1 minuto", "Personalizado"])

        self.spin_custom = QSpinBox()
        self.spin_custom.setRange(1, 3600)
        self.spin_custom.setValue(30)
        self.spin_custom.setEnabled(False)

        self.combo_time.currentIndexChanged.connect(self.update_timer_mode)

        # Subpastas
        self.chk_subfolders = QCheckBox("Incluir subpastas")

        # Iniciar slideshow
        self.btn_start = QPushButton("Iniciar Slideshow")
        self.btn_start.clicked.connect(self.start_slideshow)

        # Layouts
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.combo_time)
        time_layout.addWidget(self.spin_custom)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_pause)
        nav_layout.addWidget(self.btn_next)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.btn_folder)
        layout.addWidget(self.chk_subfolders)
        layout.addLayout(time_layout)
        layout.addWidget(self.btn_start)
        layout.addLayout(nav_layout)

        self.setLayout(layout)

    # -----------------------------
    #   FUNÇÕES DE TIMER
    # -----------------------------

    def update_timer_mode(self):
        self.spin_custom.setEnabled(self.combo_time.currentText() == "Personalizado")

    def start_slideshow(self):
        if not self.files:
            return

        if self.combo_time.currentText() == "30 segundos":
            interval = 30
        elif self.combo_time.currentText() == "1 minuto":
            interval = 60
        else:
            interval = self.spin_custom.value()

        self.timer.start(interval * 1000)

    def toggle_pause(self):
        if self.timer.isActive() or self.video_timer.isActive():
            self.timer.stop()
            self.video_timer.stop()
            self.btn_pause.setText("Retomar")
        else:
            self.btn_pause.setText("Pausar")
            self.start_slideshow()

    # -----------------------------
    #   FUNÇÕES DE FICHEIROS
    # -----------------------------

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Escolher Pasta")
        if not folder:
            return

        include_sub = self.chk_subfolders.isChecked()

        self.files = self.scan_folder(folder, include_sub)

        if not self.files:
            print("Nenhum ficheiro encontrado. Verifica extensões e subpastas.")
            return

        self.index = 0
        self.show_file()



    def scan_folder(self, folder, include_subfolders):
        valid_ext = (".png", ".jpg", ".jpeg", ".bmp", ".gif",
                    ".mp4", ".avi", ".mov", ".mkv")

        files = []

        if include_subfolders:
            # Varre todas as subpastas
            for root, dirs, filenames in os.walk(folder):
                for name in filenames:
                    if name.lower().endswith(valid_ext):
                        full_path = os.path.join(root, name)
                        if os.path.isfile(full_path):
                            files.append(os.path.normpath(full_path))
        else:
            # Apenas a pasta principal
            for name in os.listdir(folder):
                full_path = os.path.join(folder, name)
                if os.path.isfile(full_path) and name.lower().endswith(valid_ext):
                    files.append(os.path.normpath(full_path))

        return sorted(files)




    # -----------------------------
    #   NAVEGAÇÃO
    # -----------------------------

    def next_file(self):
        if not self.files:
            return
        self.index = (self.index + 1) % len(self.files)
        self.show_file()

    def prev_file(self):
        if not self.files:
            return
        self.index = (self.index - 1) % len(self.files)
        self.show_file()

    # -----------------------------
    #   APRESENTAÇÃO
    # -----------------------------

    def show_file(self):
        file = self.files[self.index]

        # Se for vídeo
        if file.lower().endswith((".mp4", ".avi", ".mov")):
            self.start_video(file)
        else:
            self.stop_video()
            self.show_image(file)

    def show_image(self, path):
        pixmap = QPixmap(path)
        self.current_pixmap = pixmap
        self.update_display()

    # -----------------------------
    #   VÍDEO
    # -----------------------------

    def start_video(self, path):
        self.stop_video()
        self.video_cap = cv2.VideoCapture(path)
        self.video_timer.start(30)

    def play_video_frame(self):
        if not self.video_cap:
            return

        ret, frame = self.video_cap.read()
        if not ret:
            self.next_file()
            return

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        img = QImage(frame.data, w, h, ch * w, QImage.Format_RGB888)

        pixmap = QPixmap.fromImage(img)
        scaled = pixmap.scaled(
            self.image_label.size(),
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
        self.image_label.setPixmap(scaled)

    def stop_video(self):
        if self.video_cap:
            self.video_cap.release()
            self.video_cap = None
        self.video_timer.stop()

    # -----------------------------
    #   REDIMENSIONAMENTO
    # -----------------------------

    def resizeEvent(self, event):
        self.update_display()
        super().resizeEvent(event)

    def update_display(self):
        """Redimensiona a imagem atual sem recarregar ficheiros."""
        if hasattr(self, "current_pixmap") and self.current_pixmap:
            scaled = self.current_pixmap.scaled(
                self.image_label.size(),
                Qt.KeepAspectRatio,
                Qt.SmoothTransformation
            )
            self.image_label.setPixmap(scaled)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    apply_stylesheet(app, theme="dark_teal.xml")

    window = ImageSlideshow()
    window.resize(700, 500)
    window.show()

    sys.exit(app.exec())