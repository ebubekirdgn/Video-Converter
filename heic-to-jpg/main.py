import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pillow_heif

# pillow-heif eklentisini Pillow'a entegre et
pillow_heif.register_heif_opener()

def convert_heic_to_jpg(folder_path):
    files = os.listdir(folder_path)
    heic_files = [f for f in files if f.lower().endswith(".heic")]

    if not heic_files:
        messagebox.showinfo("Bilgi", "Seçilen klasörde .heic dosyası bulunamadı.")
        return

    for file_name in heic_files:
        heic_path = os.path.join(folder_path, file_name)
        jpg_path = os.path.join(folder_path, f"{os.path.splitext(file_name)[0]}.jpg")

        image = Image.open(heic_path)
        image.save(jpg_path, "JPEG")

    messagebox.showinfo("Tamamlandı", "Tüm HEIC dosyaları JPG formatına dönüştürüldü.")

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        convert_heic_to_jpg(folder_selected)

root = tk.Tk()
root.title("HEIC to JPG Dönüştürücü")
root.geometry("300x150")

btn_select_folder = tk.Button(root, text="Klasör Seç ve Dönüştür", command=select_folder)
btn_select_folder.pack(pady=40)

root.mainloop()
