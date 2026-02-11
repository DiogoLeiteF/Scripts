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

        # ---------------------------------------------------------
        # SUPER SAMPLING (melhor nitidez)
        # ---------------------------------------------------------
        crop = cv2.resize(crop, None, fx=1.3, fy=1.3, interpolation=cv2.INTER_CUBIC)

        # ---------------------------------------------------------
        # GARANTIR ALTURA MÍNIMA DE 500px
        # ---------------------------------------------------------
        ch, cw = crop.shape[:2]
        min_height = 1000
        if ch < min_height:
            scale = min_height / ch
            new_w = int(cw * scale)
            new_h = min_height
            crop = cv2.resize(crop, (new_w, new_h), interpolation=cv2.INTER_CUBIC)

        return crop, None

    except Exception as e:
        return None, str(e)

# ---------------------------------------------------------
# Função redimencionar a imagem para um maximo de 1700px lado maior
# ---------------------------------------------------------
def redimensionar_imagem(path_in, max_dim=1700):
    img = cv2.imread(path_in)
    if img is None:
        return None, "Erro ao abrir imagem"

    h, w = img.shape[:2]
    maior = max(w, h)

    # Se já for menor que o limite, não redimensiona
    if maior <= max_dim:
        return img, None

    escala = max_dim / maior
    new_w = int(w * escala)
    new_h = int(h * escala)

    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
    return resized, None



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
        self.lat_value = 60
        self.label_lat = ttk.Label(frame, text=f"Margem Lateral {self.lat_value}", font=("Segoe UI", 11))
        self.label_lat.pack()
        self.slider_lat = ttk.Scale(frame, from_=0, to=250, orient="horizontal", command=self.update_label_lat)
        self.slider_lat.set(self.lat_value)
        self.slider_lat.pack(fill="x", padx=20)
        
        self.top_value = 50
        self.label_top =ttk.Label(frame, text=f"Margem Superior {self.top_value}", font=("Segoe UI", 11))
        self.label_top.pack()
        self.slider_top = ttk.Scale(frame, from_=0, to=250, orient="horizontal", command=self.update_label_top)
        self.slider_top.set(self.top_value)
        self.slider_top.pack(fill="x", padx=20)

        self.bot_value = 100
        self.label_bot = ttk.Label(frame, text=f"Margem Inferior {self.bot_value}", font=("Segoe UI", 11))
        self.label_bot.pack()
        self.slider_bot = ttk.Scale(frame, from_=0, to=550, orient="horizontal", command=self.update_label_bot)
        self.slider_bot.set(self.bot_value)
        self.slider_bot.pack(fill="x", padx=20)

        # Escolher qualidade do jpeg
        self.jpeg_value = 60
        self.label_jpeg = ttk.Label(frame, text=f"Qualidade Jpeg {self.jpeg_value}%", font=("Segoe UI", 11))
        self.label_jpeg.pack()
        self.slider_jpeg = ttk.Scale(frame, from_=0, to=100, orient="horizontal", command=self.update_label_jpeg)
        self.slider_jpeg.set(60)
        self.slider_jpeg.pack(fill="x", padx=20)
        
        

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
    
    def update_label_lat(self, value):
        self.label_lat.config(text=f"Margem Lateral {float(value):.0f}")

    def update_label_top(self, value):
        self.label_top.config(text=f"Margem Superior {float(value):.0f}")

    def update_label_bot(self, value):
        self.label_bot.config(text=f"Margem Inferior {float(value):.0f}")

    def update_label_jpeg(self, value):
        self.label_jpeg.config(text=f"Qualidade Jpeg {float(value):.0f}%")


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
        m_jpeg = int(self.slider_jpeg.get())

        for i, img_nome in enumerate(imagens, start=1):
            caminho = os.path.join(pasta, img_nome)

            crop, erro = recortar_face(caminho, m_lat, m_top, m_bot)

            if erro or crop is None:
                falhadas.append((img_nome, erro))
            else:
                out_path = os.path.join(pasta_recortes, img_nome)
                cv2.imwrite(
                    out_path,
                    crop,
                    [
                        cv2.IMWRITE_JPEG_QUALITY, 100,
                        cv2.IMWRITE_JPEG_OPTIMIZE, 1
                    ]
                )


            self.progress["value"] = i
            self.root.update_idletasks()

        if falhadas:
            self.text_erros.insert(tk.END, "Imagens não processadas:\n\n")
            for nome, erro in falhadas:
                self.text_erros.insert(tk.END, f"{nome} → {erro}\n")
        else:
            self.text_erros.insert(tk.END, "Todas as imagens foram processadas com sucesso.\n")


        # ---------------------------------------------------------
        # SEGUNDA PASSAGEM: criar versões reduzidas (Resized)
        # ---------------------------------------------------------
        self.text_erros.insert(tk.END, "\n--- A criar versões reduzidas ---\n")

        pasta_resized = os.path.join(pasta, "Resized")
        os.makedirs(pasta_resized, exist_ok=True)

        # Reset da barra de progresso para a segunda fase
        self.progress["value"] = 0
        self.progress["maximum"] = total

        for i, img_nome in enumerate(imagens, start=1):
            caminho = os.path.join(pasta, img_nome)

            resized, erro = redimensionar_imagem(caminho, max_dim=1700)

            if erro or resized is None:
                self.text_erros.insert(tk.END, f"{img_nome} → {erro}\n")
                continue

            out_path = os.path.join(pasta_resized, img_nome)

            # Guardar com qualidade 60%
            cv2.imwrite(
                out_path,
                resized,
                [
                    cv2.IMWRITE_JPEG_QUALITY, m_jpeg,
                    cv2.IMWRITE_JPEG_OPTIMIZE, 1
                ]
            )

            self.progress["value"] = i
            self.root.update_idletasks()

        self.text_erros.insert(tk.END, "\nVersões reduzidas criadas com sucesso.\n")



        messagebox.showinfo("Concluído", "Processamento finalizado.")


# ---------------------------------------------------------
# Iniciar aplicação
# ---------------------------------------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()