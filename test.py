import tkinter as tk

from gui import *

# --- Blok untuk menguji (Testing) fungsi secara terpisah ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplikasi Kuis Interaktif")
    root.geometry("800x600")
    halaman_buat_kepala_kuis(root)
    root.mainloop()