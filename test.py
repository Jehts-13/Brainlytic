import tkinter as tk

from gui import *

# --- Blok untuk menguji (Testing) fungsi secara terpisah ---
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplikasi quiz Interaktif")
    root.geometry("800x600")
    halaman_tinjau_jawaban(root)
    root.mainloop()