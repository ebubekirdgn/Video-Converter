import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import threading
import os

def select_file():
    # .mov dosyasını seçmek için bir dosya diyalogu aç
    file_path.set(filedialog.askopenfilename(filetypes=[("MOV files", "*.mov")]))
    
def convert_to_mp4():
    mov_file_path = file_path.get()
    
    if not mov_file_path:
        messagebox.showerror("Hata", "Lütfen bir .mov dosyası seçin.")
        return
    
    def conversion_thread():
        try:
            # Masaüstü yolunu al
            desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop') if os.name == 'nt' else os.path.join(os.path.expanduser('~'), 'Desktop')
            # .mp4 dosya yolu
            mp4_file_path = os.path.join(desktop_path, 'ebubekir.mp4')
            
            # Video dosyasını dönüştür
            clip = VideoFileClip(mov_file_path)
            clip.write_videofile(mp4_file_path, codec='libx264')
            
            # Tamamlandığında kullanıcıyı bilgilendir
            messagebox.showinfo("Bilgi", f"Dönüştürme tamamlandı!\n{mp4_file_path}")
        except Exception as e:
            # Hata durumunda kullanıcıyı bilgilendir
            messagebox.showerror("Hata", f"Dönüştürme sırasında bir hata oluştu:\n{str(e)}")

    threading.Thread(target=conversion_thread).start()

# Ana pencereyi oluştur
root = tk.Tk()
root.title("MOV to MP4 Converter")
root.geometry("300x150")

file_path = tk.StringVar()

# Video Yükle butonu
load_button = tk.Button(root, text="Video Yükle", command=select_file)
load_button.pack(pady=10)

# Seçilen dosya yolunu göstermek için etiket
file_label = tk.Label(root, textvariable=file_path)
file_label.pack(pady=5)

# Dönüştür butonu
convert_button = tk.Button(root, text="Dönüştür", command=convert_to_mp4)
convert_button.pack(pady=10)

# Pencereyi çalıştır
root.mainloop()
