import os
import threading
import cv2
import numpy as np
import insightface
from insightface.app import FaceAnalysis
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from ttkbootstrap import Style


# ---------------------------------------------------------
# Inicializar SCRFD (InsightFace)
# ---------------------------------------------------------
app_face = FaceAnalysis(name="buffalo_l")
app_face.prepare(ctx_id=0, det_size=(640, 640))


# ---------------------------------------------------------
# Função de deteção e recorte da face
# ---------------------------------------------------------
def recortar_face(path_in, m_lat, m_top, m_bot):
    try:
        img = cv2.imread(path_in)
        if img is None:
            return None, "Erro ao abrir imagem"

        h, w, _ = img.shape

        faces = app_face.get(img)

        if not faces:
            return None, "Nenhuma face encontrada"

        # Usar a face com maior área
        faces = sorted(faces, key=lambda f: (f.bbox[2] - f.bbox[0]) * (f.bbox[3] - f.bbox[1]), reverse=True)
        face = faces[0]

        x1, y1, x2, y2 = map(int, face.bbox)
        bw = x2 - x1
        bh = y2 - y1

        # Margens ajustáveis
        margem_lateral = int(bw * (m_lat / 100))
        margem_topo = int(bh * (m_top / 100))
        margem_baixo = int(bh * (m_bot / 100))

        x1 = max(0, x1 - margem_lateral)
        y1 = max(0, y1 - margem_topo)
        x2 = min(w, x2 + margem_lateral)
        y2 = min(h, y2 + margem_baixo)

        crop = img[y1:y2, x1:x2]

        if crop.size == 0:
            return None, "Recorte vazio"

        # Melhorar qualidade da imagem
        crop = cv2.resize(crop, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)

        return crop, None

    except Exception as e:
        return None, str(e)


# ---------------------------------------------------------
# Interface Gráfica
# ---------------------------------------------------------
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Extrator Automático de Faces")
        self.root.geometry("900x800")

        style = Style(theme="darkly")

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill="both", expand=True)

        ttk.Label(frame, text="Extrator Automático de Faces", font=("Segoe UI", 20, "bold")).pack(pady=10)

        # Escolher pasta
        self.btn_escolher = ttk.Button(frame, text="Escolher Pasta de Imagens", command=self.escolher_pasta)
        self.btn_escolher.pack(pady=10)

        # Sliders de margens
        ttk.Label(frame, text="Margem Lateral (%)", font=("Segoe UI", 11)).pack()
        self.slider_lat = ttk.Scale(frame, from_=0, to=80, orient="horizontal")
        self.slider_lat.set(30)
        self.slider_lat.pack(fill="x", padx=20)

        ttk.Label(frame, text="Margem Superior (%)", font=("Segoe UI", 11)).pack()
        self.slider_top = ttk.Scale(frame, from_=0, to=100, orient="horizontal")
        self.slider_top.set(60)
        self.slider_top.pack(fill="x", padx=20)

        ttk.Label(frame, text="Margem Inferior (%)", font=("Segoe UI", 11)).pack()
        self.slider_bot = ttk.Scale(frame, from_=0, to=150, orient="horizontal")
        self.slider_bot.set(120)
        self.slider_bot.pack(fill="x", padx=20)

        # Botão iniciar
        self.btn_processar = ttk.Button(frame, text="Iniciar Processamento", command=self.iniciar_processamento, bootstyle="primary")
        self.btn_processar.pack(pady=15)

        # Contador total
        self.label_total = ttk.Label(frame, text="Total de imagens: 0", font=("Segoe UI", 12))
        self.label_total.pack(pady=5)

        # Barra de progresso
        self.progress = ttk.Progressbar(frame, length=600, mode="determinate")
        self.progress.pack(pady=10)

        # Área de erros
        ttk.Label(frame, text="Erros / Imagens não processadas:", font=("Segoe UI", 12)).pack(pady=5)

        text_frame = ttk.Frame(frame)
        text_frame.pack(fill="both", expand=True)

        self.text_erros = tk.Text(text_frame, height=20, wrap="word", bg="#1e1e1e", fg="white", insertbackground="white")
        self.text_erros.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(text_frame, command=self.text_erros.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_erros.config(yscrollcommand=scrollbar.set)

        self.pasta = None

    def escolher_pasta(self):
        self.pasta = filedialog.askdirectory()
        if self.pasta:
            messagebox.showinfo("Pasta selecionada", f"Pasta escolhida:\n{self.pasta}")

    def iniciar_processamento(self):
        if not self.pasta:
            messagebox.showwarning("Aviso", "Escolhe primeiro uma pasta.")
            return
        threading.Thread(target=self.processar_pasta, daemon=True).start()

    def processar_pasta(self):
        pasta = self.pasta
        self.text_erros.delete("1.0", tk.END)

        pasta_recortes = os.path.join(pasta, "Recortes")
        os.makedirs(pasta_recortes, exist_ok=True)

        imagens = [f for f in os.listdir(pasta) if f.lower().endswith((".jpg", ".jpeg", ".png"))]

        total = len(imagens)
        if total == 0:
            messagebox.showinfo("Aviso", "Nenhuma imagem encontrada na pasta.")
            return

        self.label_total.config(text=f"Total de imagens: {total}")

        self.progress["value"] = 0
        self.progress["maximum"] = total

        falhadas = []

        # Ler margens do GUI
        m_lat = self.slider_lat.get()
        m_top = self.slider_top.get()
        m_bot = self.slider_bot.get()

        for i, img_nome in enumerate(imagens, start=1):
            caminho = os.path.join(pasta, img_nome)

            crop, erro = recortar_face(caminho, m_lat, m_top, m_bot)

            if erro or crop is None:
                falhadas.append((img_nome, erro))
            else:
                out_path = os.path.join(pasta_recortes, img_nome)
                cv2.imwrite(out_path, crop, [cv2.IMWRITE_JPEG_QUALITY, 98])

            self.progress["value"] = i
            self.root.update_idletasks()

        if falhadas:
            self.text_erros.insert(tk.END, "Imagens não processadas:\n\n")
            for nome, erro in falhadas:
                self.text_erros.insert(tk.END, f"{nome} → {erro}\n")
        else:
            self.text_erros.insert(tk.END, "Todas as imagens foram processadas com sucesso.\n")

        messagebox.showinfo("Concluído", "Processamento finalizado.")


# ---------------------------------------------------------
# Iniciar aplicação
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()