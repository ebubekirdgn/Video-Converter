import tkinter as tk
from tkinter import filedialog, messagebox
from moviepy.editor import VideoFileClip
import threading
import os

def select_file():
    # .mov dosyasını seçmek için bir dosya diyalogu aç
    file_path.set(filedialog.askopenfilename(filetypes=[("MOV files", "*.mov")]))
    
def select_folder():
    # Klasör seçimi için bir diyalog aç
    folder_path.set(filedialog.askdirectory())
    
def convert_to_mp4_single_file(mov_file_path, output_folder):
    try:
        # Dosya adını ve uzantısını al
        file_name = os.path.splitext(os.path.basename(mov_file_path))[0]
        mp4_file_path = os.path.join(output_folder, f'{file_name}.mp4')
        
        # Video dosyasını dönüştür
        clip = VideoFileClip(mov_file_path)
        clip.write_videofile(mp4_file_path, codec='libx264')
        
        return f"{mov_file_path} başarıyla {mp4_file_path} olarak dönüştürüldü."
    except Exception as e:
        return f"{mov_file_path} dönüştürülürken hata oluştu:\n{str(e)}"

def convert_all_in_folder():
    folder = folder_path.get()
    
    if not folder:
        messagebox.showerror("Hata", "Lütfen bir klasör seçin.")
        return
    
    def conversion_thread():
        try:
            # Seçilen klasördeki tüm .mov veya .MOV dosyalarını listele
            mov_files = [f for f in os.listdir(folder) if f.lower().endswith('.mov')]
            
            if not mov_files:
                messagebox.showinfo("Bilgi", "Seçilen klasörde .mov dosyası bulunamadı.")
                return
            
            output_folder = folder  # Aynı klasöre çıktı dosyalarını kaydetmek için

            results = []
            for mov_file in mov_files:
                # Her dosya için tam yol oluştur
                full_mov_path = os.path.join(folder, mov_file)
                result = convert_to_mp4_single_file(full_mov_path, output_folder)
                results.append(result)

            # Tamamlandığında kullanıcıya tüm sonuçları göster
            messagebox.showinfo("Dönüştürme Tamamlandı", "\n".join(results))
        except Exception as e:
            messagebox.showerror("Hata", f"Dönüştürme sırasında bir hata oluştu:\n{str(e)}")

    threading.Thread(target=conversion_thread).start()

# Ana pencereyi oluştur
root = tk.Tk()
root.title("MOV to MP4 Converter")
root.geometry("400x200")

file_path = tk.StringVar()
folder_path = tk.StringVar()

# Video Yükle butonu
load_button = tk.Button(root, text="Tek Video Yükle", command=select_file)
load_button.pack(pady=10)

# Seçilen dosya yolunu göstermek için etiket
file_label = tk.Label(root, textvariable=file_path)
file_label.pack(pady=5)

# Klasör Seç butonu
folder_button = tk.Button(root, text="Klasör Seç", command=select_folder)
folder_button.pack(pady=10)

# Seçilen klasörü göstermek için etiket
folder_label = tk.Label(root, textvariable=folder_path)
folder_label.pack(pady=5)

# Dönüştür butonu (Klasördeki tüm dosyalar)
convert_folder_button = tk.Button(root, text="Tüm .mov Dosyalarını Dönüştür", command=convert_all_in_folder)
convert_folder_button.pack(pady=10)

# Pencereyi çalıştır
root.mainloop()
