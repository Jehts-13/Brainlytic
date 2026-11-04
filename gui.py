# File: gui.py
import tkinter as tk

def halaman_homescreen(root):
    # 2. Membuat Widget Label untuk Judul
    judul = tk.Label(root, text="Brainlytic", font=("Helvetica", 32, "bold"), fg="#5C3A21", bg="#F4EFE6")
    judul.pack(pady=(40, 5))

    sub_judul = tk.Label(root, text="Uji pengetahuanmu, satu soal setiap kali", font=("Helvetica", 12), fg="#5C3A21", bg="#F4EFE6")
    sub_judul.pack(pady=(0, 20))

    # 3. Frame Input Nama
    frame_nama = tk.Frame(root, bg="#F4EFE6")
    frame_nama.pack(pady=10)

    label_nama = tk.Label(frame_nama, text="Nama pemain", font=("Helvetica", 10, "bold"), fg="#5C3A21", bg="#F4EFE6")
    label_nama.pack(anchor="w")

    input_nama = tk.Entry(frame_nama, width=50, font=("Helvetica", 12))
    input_nama.insert(0, "Ketik namamu...")
    input_nama.pack(ipady=5)

    # 4. Frame Menu (Tombol Kerjakan Quiz & Buat Quiz Baru)
    frame_menu = tk.Frame(root, bg="#F4EFE6")
    frame_menu.pack(pady=30)

    btn_kerjakan = tk.Button(frame_menu, text="Kerjakan Quiz\n\nPilih dari daftar quiz yang\ntersedia", 
                             bg="#A06A42", fg="white", font=("Helvetica", 10, "bold"), width=25, height=5,
                             command=lambda: halaman_pilih_quiz(root)) # Tambahkan bagian ini
    btn_kerjakan.grid(row=0, column=0, padx=10)

    btn_buat = tk.Button(frame_menu, text="Buat Quiz Baru\n\nSusun soal dan jawabanmu\nsendiri", 
                         bg="#A06A42", fg="white", font=("Helvetica", 10, "bold"), width=25, height=5)
    btn_buat.grid(row=0, column=1, padx=10)

    # 5. Link Papan Skor
    link_skor = tk.Label(root, text="Lihat papan skor", font=("Helvetica", 10), fg="#A06A42", bg="#F4EFE6", cursor="hand2")
    link_skor.pack(pady=10)

    # Memulai perulangan aplikasi
    root.mainloop()

def bersihkan_layar(root):
    """Menghapus semua widget di dalam root window untuk mengganti halaman."""
    for widget in root.winfo_children():
        widget.destroy()

def halaman_pilih_quiz(root):
    bersihkan_layar(root) # Bersihkan Home Screen sebelumnya
    
    root.configure(bg="#F4EFE6")

    # 1. Bilah Atas (Top Bar)
    top_bar = tk.Frame(root, bg="#A0B084", height=25) # Warna hijau zaitun pudar
    top_bar.pack(fill="x")
    
    label_top = tk.Label(top_bar, text="QuizPy | Kerjakan Quiz", bg="#A0B084", fg="#4A2C11", font=("Helvetica", 9, "bold"))
    label_top.pack(side="left", padx=10, pady=2)

    # 2. Area Judul & Pencarian
    header_frame = tk.Frame(root, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=20, pady=(20, 10))

    judul = tk.Label(header_frame, text="Pilih Quiz", font=("Helvetica", 24, "bold"), fg="#4A2C11", bg="#F4EFE6")
    judul.pack(side="left")

    cari_entry = tk.Entry(header_frame, font=("Helvetica", 10), width=25)
    cari_entry.insert(0, "Cari quiz...")
    cari_entry.pack(side="right", ipady=5)

    # 3. Daftar Quiz
    list_frame = tk.Frame(root, bg="#F4EFE6")
    list_frame.pack(fill="both", expand=True, padx=20)

    def buat_item_quiz(parent, judul_quiz, deskripsi):
        # Menggunakan tombol agar daftar kuis bisa diklik
        teks_tombol = f"{judul_quiz}\n{deskripsi}"
        btn = tk.Button(parent, text=teks_tombol, bg="white", fg="#4A2C11", 
                        font=("Helvetica", 9), justify="left", anchor="w", relief="solid", bd=1)
        btn.pack(fill="x", pady=5, ipady=8, padx=2)
        return btn

    # Item Kuis sesuai desain screenshot
    buat_item_quiz(list_frame, "Dasar Python", "Tipe data, variabel, dan operator. 10 soal, 5 menit") # Item aktif
    buat_item_quiz(list_frame, "Struktur Kontrol", "If, for, while, dan logika program. 8 soal, 4 menit")

    # 4. Tombol Navigasi Bawah
    bottom_frame = tk.Frame(root, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=20, pady=20)

    btn_kembali = tk.Button(bottom_frame, text="Kembali", bg="white", fg="#4A2C11", 
                            font=("Helvetica", 10, "bold"), width=15, relief="solid", bd=1,
                            command=lambda: {
                                bersihkan_layar(root),  # Bersihkan halaman 
                                halaman_homescreen(root)  # Kembali ke Home Screen
                            }) 
    btn_kembali.pack(side="left", ipady=5)

    btn_mulai = tk.Button(bottom_frame, text="Mulai Quiz", bg="#4A2C11", fg="white", 
                        font=("Helvetica", 10, "bold"), width=15,
                        command=lambda: {
                            bersihkan_layar(root),  # Bersihkan halaman 
                            halaman_soal_quiz(root) # Pindah ke halaman soal quiz
                        }) 
    btn_mulai.pack(side="right", ipady=5)

def halaman_soal_quiz(root):
    bersihkan_layar(root)
    root.configure(bg="#F4EFE6")

    # 1. Bilah Atas (Top Bar)
    top_bar = tk.Frame(root, bg="#A0B084", height=25)
    top_bar.pack(fill="x")
    
    label_top = tk.Label(top_bar, text="QuizPy | Kategori: Python", bg="#A0B084", fg="#4A2C11", font=("Helvetica", 9, "bold"))
    label_top.pack(side="left", padx=10, pady=2)

    # 2. Header Info (Indikator Soal & Waktu)
    header_frame = tk.Frame(root, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=20, pady=(15, 5))

    label_soal = tk.Label(header_frame, text="Soal 3 dari 10", font=("Helvetica", 10, "bold"), fg="#4A2C11", bg="#F4EFE6")
    label_soal.pack(side="left")

    label_waktu = tk.Label(header_frame, text="Waktu: 00:15", font=("Helvetica", 10, "bold"), fg="white", bg="#A06A42", width=12, pady=3)
    label_waktu.pack(side="right")

    # 3. Bilah Progres (Progress Bar Manual menggunakan Frame)
    progress_bg = tk.Frame(root, bg="#A0B084", height=10) # Latar belakang progres (hijau pudar)
    progress_bg.pack(fill="x", padx=20, pady=(0, 15))
    
    progress_fill = tk.Frame(progress_bg, bg="#4A2C11", width=150, height=10) # Bagian yang terisi (coklat tua)
    progress_fill.pack(side="left")
    progress_bg.pack_propagate(False) # Mencegah frame bg mengecil mengikuti isi

    # 4. Kotak Pertanyaan
    pertanyaan_frame = tk.Frame(root, bg="white", highlightbackground="#A0B084", highlightthickness=2)
    pertanyaan_frame.pack(fill="x", padx=20, pady=10)
    
    teks_pertanyaan = tk.Label(pertanyaan_frame, text="Apa output dari print(type([]))?", font=("Helvetica", 14, "bold"), fg="#4A2C11", bg="white")
    teks_pertanyaan.pack(pady=20)

    # 5. Pilihan Ganda (Grid 2x2)
    opsi_frame = tk.Frame(root, bg="#F4EFE6")
    opsi_frame.pack(fill="x", padx=20, pady=5)
    
    # Konfigurasi grid agar seimbang
    opsi_frame.columnconfigure(0, weight=1)
    opsi_frame.columnconfigure(1, weight=1)

    # Membuat tombol pilihan (Opsi B dibuat aktif sesuai screenshot)
    btn_a = tk.Button(opsi_frame, text="A.", bg="white", fg="#4A2C11", font=("Helvetica", 10), relief="solid", bd=1)
    btn_a.grid(row=0, column=0, sticky="ew", padx=(0, 5), pady=5, ipady=8)

    btn_b = tk.Button(opsi_frame, text="B.", bg="#A06A42", fg="white", font=("Helvetica", 10), relief="solid", bd=1) # Opsi terpilih
    btn_b.grid(row=0, column=1, sticky="ew", padx=(5, 0), pady=5, ipady=8)

    btn_c = tk.Button(opsi_frame, text="C.", bg="white", fg="#4A2C11", font=("Helvetica", 10), relief="solid", bd=1)
    btn_c.grid(row=1, column=0, sticky="ew", padx=(0, 5), pady=5, ipady=8)

    btn_d = tk.Button(opsi_frame, text="D.", bg="white", fg="#4A2C11", font=("Helvetica", 10), relief="solid", bd=1)
    btn_d.grid(row=1, column=1, sticky="ew", padx=(5, 0), pady=5, ipady=8)

    # 6. Umpan Balik (Feedback Box)
    feedback_label = tk.Label(root, text="Benar! List ditulis dengan tanda kurung siku.", bg="#A0B084", fg="#4A2C11", font=("Helvetica", 9, "bold"))
    feedback_label.pack(fill="x", padx=20, pady=(15, 10), ipady=8)

    # 7. Tombol Navigasi Bawah
    bottom_frame = tk.Frame(root, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=20, pady=10)

    btn_keluar = tk.Button(bottom_frame, text="Keluar", bg="white", fg="#4A2C11", font=("Helvetica", 10), relief="solid", bd=1, width=12)
    btn_keluar.pack(side="left", ipady=5)

    label_skor = tk.Label(bottom_frame, text="Skor: 20", font=("Helvetica", 10), fg="#4A2C11", bg="#F4EFE6")
    label_skor.pack(side="left", expand=True)

    btn_berikutnya = tk.Button(bottom_frame, text="Berikutnya", bg="#4A2C11", fg="white", font=("Helvetica", 10, "bold"), width=12)
    btn_berikutnya.pack(side="right", ipady=5)