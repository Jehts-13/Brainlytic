# File: main.py
import gui
import tkinter as tk

# Blok ini memastikan kode hanya berjalan jika main.py dieksekusi langsung,
# bukan saat diimpor oleh file lain.
root = tk.Tk()
root.title("Aplikasi Kuis Interaktif")
root.geometry("600x450")
root.configure(bg="#F4EFE6")

if __name__ == "__main__":
    print("Memulai Aplikasi Kuis Interaktif...")
    gui.halaman_homescreen(root)