import os
import shutil
import sys
import cv2
import random
from datetime import datetime
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QComboBox, QSpinBox, QHBoxLayout, QCheckBox, QSizePolicy, QMessageBox
)
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt, QTimer
from qt_material import apply_stylesheet


class ImageSlideshow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Visualizador de Imagens e Vídeos")

        # Área de apresentação
        self.image_label = QLabel(alignment=Qt.AlignCenter)
        self.image_label.setStyleSheet("background-color: #202020; border: 1px solid #444;")
        self.image_label.setScaledContents(False)
        self.image_label.setMinimumSize(1, 1)
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Lista de ficheiros
        self.files = []
        self.index = 0
        self.fav_folder = None

        # Vídeo
        self.video_cap = None
        self.video_timer = QTimer()
        self.video_timer.timeout.connect(self.play_video_frame)

        # Timer slideshow
        self.timer = QTimer()
        self.timer.timeout.connect(self.next_file)

        # Timer countdown
        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.time_left = 0

        # Label countdown
        self.lbl_countdown = QLabel("Tempo restante: -- s")
        self.lbl_countdown.setAlignment(Qt.AlignRight)
        self.lbl_countdown.setStyleSheet("font-size: 12px; color: #AAA;")
        self.lbl_countdown.setMaximumHeight(12)
        
        # tempo total decorrido
        self.start_time = None
        self.elapsed_label = QLabel("Tempo decorrido: 00:00:00")
        self.elapsed_label.setStyleSheet("font-size: 12px; font-weight: bold; color: #D10000;")
        self.elapsed_label.setAlignment(Qt.AlignCenter)

        self.elapsed_timer = QTimer()
        self.elapsed_timer.timeout.connect(self.update_elapsed_time)

        
        # Label filename
        self.lbl_filename = QLabel("Caminho: ---")
        self.lbl_filename.setAlignment(Qt.AlignLeft)
        self.lbl_filename.setStyleSheet("font-size: 12px; color: #AAA;")
        self.lbl_filename.setMaximumHeight(30)
        self.lbl_filename.setTextInteractionFlags(
            Qt.TextSelectableByMouse | 
            Qt.LinksAccessibleByMouse
            )
        self.lbl_filename.setWordWrap(True)

        # Label filecount
        self.lbl_filecount = QLabel("Ficheiros: 0 ")
        self.lbl_filename.setAlignment(Qt.AlignLeft)
        self.lbl_filecount.setStyleSheet("font-size: 12px; color: #AAA;")
        self.lbl_filecount.setMaximumHeight(12)


        # Botões
        self.btn_folder = QPushButton("Escolher Pasta")
        self.btn_folder.clicked.connect(self.choose_folder)

        self.btn_prev = QPushButton("Anterior")
        self.btn_prev.clicked.connect(self.prev_file)

        self.btn_next = QPushButton("Próxima")
        self.btn_next.clicked.connect(self.next_file)

        self.btn_pause = QPushButton("Pausar")
        self.btn_pause.clicked.connect(self.toggle_pause)

        self.btn_delete = QPushButton("Eliminar")
        self.btn_delete.clicked.connect(self.delete_file)

        self.btn_fav = QPushButton("Favoritos")
        self.btn_fav.clicked.connect(self.fav_file)

        # Temporizador
        self.combo_time = QComboBox()
        self.combo_time.addItems(["30 segundos", 
                                  "60 segundos", 
                                  "90 segundos", 
                                  "120 segundos", 
                                  "Personalizado"
                                  ])

        self.spin_custom = QSpinBox()
        self.spin_custom.setRange(1, 3600)
        self.spin_custom.setValue(30)
        self.spin_custom.setEnabled(False)

        self.combo_time.currentIndexChanged.connect(self.update_timer_mode)

        # Subpastas + Random
        self.chk_subfolders = QCheckBox("Incluir subpastas")
        self.chk_random = QCheckBox("Randomizar ordem")
        self.chk_random.setChecked(True)

        # Iniciar slideshow
        self.btn_start = QPushButton("Iniciar Slideshow")
        self.btn_start.clicked.connect(self.start_from_btn)

        # Layouts
        time_layout = QHBoxLayout()
        time_layout.addWidget(self.combo_time)
        time_layout.addWidget(self.spin_custom)
        time_layout.addWidget(self.btn_start)

        options_layout = QHBoxLayout()
        options_layout.addWidget(self.chk_subfolders)
        options_layout.addWidget(self.chk_random)
        options_layout.addWidget(self.btn_folder)
        
        info_layout = QHBoxLayout()
        info_layout.addWidget(self.lbl_filecount)
        info_layout.addWidget(self.elapsed_label)
        info_layout.addWidget(self.lbl_countdown)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.btn_prev)
        nav_layout.addWidget(self.btn_pause)
        nav_layout.addWidget(self.btn_next)

        del_layout = QHBoxLayout()
        del_layout.addWidget(self.btn_delete)
        del_layout.addWidget(self.btn_fav)

        layout = QVBoxLayout()

        # Opções (subpastas + random)
        layout.addLayout(options_layout)
        # Temporizador
        layout.addLayout(time_layout)
        # Countdown
        layout.addWidget(self.lbl_filename)
        # File info
        layout.addLayout(info_layout)
        # Área de imagem
        layout.addWidget(self.image_label)
        # Navegação
        layout.addLayout(nav_layout)
        # Options
        layout.addLayout(del_layout)

        self.setLayout(layout)

    # -----------------------------
    #   FUNÇÕES DE TIMER
    # -----------------------------

    def update_timer_mode(self):
        self.spin_custom.setEnabled(self.combo_time.currentText() == "Personalizado")

    def start_slideshow(self):
        if not self.files:
            return

        # Determinar intervalo
        if self.combo_time.currentText() == "30 segundos":
            interval = 30
        elif self.combo_time.currentText() == "60 segundos":
            interval = 60
        if self.combo_time.currentText() == "90 segundos":
            interval = 90
        elif self.combo_time.currentText() == "120 segundos":
            interval = 120
        else:
            interval = self.spin_custom.value()

        # Reiniciar contador
        self.time_left = interval
        self.lbl_countdown.setText(f"Tempo restante: {self.time_left} s")
        
        # Iniciar timers
        self.timer.start(interval * 1000)
        self.countdown_timer.start(1000)
        if self.start_time is None:
             self.start_time = datetime.now()
        self.elapsed_timer.start(1000)  # atualiza a cada 1 segundo
        
        # update filename
        self.lbl_filename.setText(f"{self.get_filename()}")
        
    def update_countdown(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.lbl_countdown.setText(f"Tempo restante: {self.time_left} s")
        else:
            self.lbl_countdown.setText(f"A mudar... time_left {self.time_left}")
            self.start_slideshow()
    
    def start_from_btn(self):
        self.start_time = datetime.now()
        self.start_slideshow()
            
    def update_elapsed_time(self):
        if self.start_time is None:
            return

        delta = datetime.now() - self.start_time
        total_seconds = int(delta.total_seconds())

        horas = total_seconds // 3600
        minutos = (total_seconds % 3600) // 60
        segundos = total_seconds % 60

        self.elapsed_label.setText(
            f"Tempo decorrido: {horas:02d}:{minutos:02d}:{segundos:02d}"
        )

    def toggle_pause(self):
        if self.timer.isActive() or self.video_timer.isActive():
            self.timer.stop()
            self.video_timer.stop()
            self.countdown_timer.stop()
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
            print("Nenhum ficheiro encontrado.")
            return

        self.index = 0
        self.lbl_filename.setText(f"{self.get_filename()}")
        self.show_file()

    def scan_folder(self, folder, include_subfolders):
        valid_ext = (".png", ".jpg", ".jpeg", ".bmp", ".gif",
                     ".mp4", ".avi", ".mov", ".mkv")

        files = []

        if include_subfolders:
            for root, dirs, filenames in os.walk(folder):
                for name in filenames:
                    if name.lower().endswith(valid_ext):
                        full_path = os.path.join(root, name)
                        if os.path.isfile(full_path):
                            files.append(os.path.normpath(full_path))
        else:
            for name in os.listdir(folder):
                full_path = os.path.join(folder, name)
                if os.path.isfile(full_path) and name.lower().endswith(valid_ext):
                    files.append(os.path.normpath(full_path))
        # Randomizar ordem
        if self.chk_random.isChecked():
            random.shuffle(files)
        else:
            files = sorted(files)
         
        self.lbl_filecount.setText(f"Ficheiros: {len(files)}")
        return files

    def get_filename(self):
        if self.files:
            raw_filename = self.files[self.index]
            return raw_filename
    
    def delete_file(self):
        if not self.files:
            return
        file = self.files[self.index]
        save_index = self.index
        delete_file = QMessageBox.question(self,
                                           "Confirmar eliminação",
                                           "Tens a certeza que queres apagar esta imagem?", QMessageBox.Yes | QMessageBox.No
                                           )

        if delete_file == QMessageBox.Yes:
            try:
                os.remove(file)
                QMessageBox.information(self, "Apagado", "A imagem foi apagada com sucesso.")

                # remover da lista interna
                del self.files[save_index]
                
                # ajustar índice
                if save_index >= len(self.files):
                    self.index = 0

                # mostrar próxima imagem
                if self.files:
                    self.show_file()
                else:
                    self.image_label.clear()
                    
                # atualizar labels
                self.lbl_filecount.setText(f"Ficheiros: {len(self.files)}")
                self.lbl_filename.setText(f"{self.get_filename()}")
                

            except Exception as e:
                QMessageBox.critical(self, "Erro", f"Não foi possível apagar o ficheiro:\n{e}")

    
    def fav_file(self):
        if not self.files:
            return
        if self.fav_folder == None:
            if self.btn_pause.text() == "Pausar":
                self.toggle_pause()
            self.fav_folder = QFileDialog.getExistingDirectory(self, "Pasta Favoritos")
            self.btn_fav.setText(f"Favoritos\n {self.fav_folder}")
            
        origem = rf"{self.files[self.index]}"
        destino = os.path.join(self.fav_folder, os.path.basename(origem))
        if os.path.exists(destino):
            confirm_duplicate = QMessageBox.question(self, "Confirmar favorito duplicado", "Mesmo nome encontrado, continuaar com a copia?", QMessageBox.Yes | QMessageBox.No)
            if confirm_duplicate == QMessageBox.Yes:
                data = datetime.now()
                data_txt = data.strftime("_%d-%m-%Y_%H%M%S")
                destino = destino.split(".")
                data_txt += f".{destino[-1]}"
                destino = "".join(destino[:-1])
                destino += data_txt
            else:
                return
        
        shutil.copy2(origem, destino)
        QMessageBox.information(self, "Copia", "A imagem foi Copiada para os favoritos.")
    
    
    # -----------------------------
    #   NAVEGAÇÃO
    # -----------------------------

    def next_file(self):
        if not self.files:
            return
        self.index = (self.index + 1) % len(self.files)
        self.show_file()
        if self.btn_pause.text() == "Retomar":
            self.show_file()
            self.lbl_filename.setText(f"{self.get_filename()}")
        else:
            self.start_slideshow()
        

    def prev_file(self):
        if not self.files:
            return
        self.index = (self.index - 1) % len(self.files)
        self.show_file()
        if self.btn_pause.text() == "Retomar":
            self.show_file()
            self.lbl_filename.setText(f"{self.get_filename()}")
        else:
            self.start_slideshow()
        

    # -----------------------------
    #   APRESENTAÇÃO
    # -----------------------------

    def show_file(self):
        file = self.files[self.index]

        if file.lower().endswith((".mp4", ".avi", ".mov", ".mkv")):
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
    window.resize(500, 800)
    window.show()

    sys.exit(app.exec())