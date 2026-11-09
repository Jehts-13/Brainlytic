# File: gui.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from logika import *
from data_manager import *

def fungsi_dummy(teks):
    print(teks)

def halaman_homescreen(root):
    def batasi_input(*args):
        batas_maksimal = 20 # Ubah angka ini sesuai kebutuhan batas karakter Anda
        nilai_saat_ini = nama_var.get()
        
        # Jika panjang teks melebihi batas, potong teksnya
        if len(nilai_saat_ini) > batas_maksimal:
            nama_var.set(nilai_saat_ini[:batas_maksimal])

    def validasi_sebelum_lanjut():
        nama = nama_var.get()
        # Mengecek apakah input kosong atau mengandung karakter selain huruf/angka
        if not nama.isalnum():
            messagebox.showwarning("Input Tidak Valid", "Nama hanya boleh berisi huruf dan angka (tanpa spasi atau simbol)!")
            return # Menghentikan proses agar tidak pindah halaman
        
        # Jika lolos validasi, jalankan perintah asli
        simpan_nama_pemain(nama)
        bersihkan_layar(root)
        halaman_pilih_quiz(root)
    
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

    nama_var = tk.StringVar()
    nama_var.trace_add("write", batasi_input)
    input_nama = tk.Entry(frame_nama, width=50, font=("Helvetica", 12), textvariable=nama_var)
    input_nama.insert(0, "Ketik nama Anda di sini (maks. 20 karakter)")
    input_nama.pack(ipady=5)

    # 4. Frame Menu (Tombol Kerjakan Quiz & Buat Quiz Baru)
    frame_menu = tk.Frame(root, bg="#F4EFE6")
    frame_menu.pack(pady=30)

    btn_kerjakan = tk.Button(frame_menu, text="Kerjakan Quiz\n\nPilih dari daftar quiz yang\ntersedia", 
                             bg="#A06A42", fg="white", font=("Helvetica", 10, "bold"), width=25, height=5,
                             command=lambda: validasi_sebelum_lanjut())  
    btn_kerjakan.grid(row=0, column=0, padx=10)

    btn_buat = tk.Button(frame_menu, text="Buat Quiz Baru\n\nSusun soal dan jawabanmu\nsendiri", 
                         bg="#A06A42", fg="white", font=("Helvetica", 10, "bold"), width=25, height=5)
    btn_buat.grid(row=0, column=1, padx=10)

    # 5. Link Papan Skor
    link_skor = tk.Label(root, text="Lihat papan skor", font=("Helvetica", 10), fg="#A06A42", bg="#F4EFE6", cursor="hand2",) 
    link_skor.bind("<Button-1>", lambda: halaman_papan_skor(root))
    link_skor.pack(pady=10)

    # Memulai perulangan aplikasi
    root.mainloop()

def bersihkan_layar(root):
    """Menghapus semua widget di dalam root window untuk mengganti halaman."""
    for widget in root.winfo_children():
        widget.destroy()

def halaman_pilih_quiz(root):
    quiz_dipilih = None  # Variabel global untuk menyimpan quiz yang dipilih
    
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

    # 3. Tombol Navigasi 
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

    # --- AREA SCROLL UNTUK DAFTAR KUIS ---
    # 1. Buat kontainer utama untuk Canvas dan Scrollbar
    scroll_container = tk.Frame(root, bg="#F4EFE6")
    scroll_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

    # 2. Buat Canvas
    canvas = tk.Canvas(scroll_container, bg="#F4EFE6", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # 3. Buat Scrollbar dan pasangkan dengan Canvas
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 4. Buat Frame di dalam Canvas untuk menampung tombol kuis
    list_frame = tk.Frame(canvas, bg="#F4EFE6")
    
    # 5. Masukkan list_frame ke dalam Canvas
    canvas_window = canvas.create_window((0, 0), window=list_frame, anchor="nw")

    # 6. Fungsi untuk memperbarui area scroll (dipanggil setiap kali isi list_frame berubah)
    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        # Menyesuaikan lebar list_frame agar sama dengan lebar canvas
        canvas.itemconfig(canvas_window, width=event.width)
        
    canvas.bind("<Configure>", on_configure)

    # 7. Fungsi untuk mengaktifkan scroll menggunakan mouse wheel
    def _on_mousewheel(event):
        # Untuk Windows/Mac (event.delta biasanya kelipatan 120)
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    # Bind scroll event saat kursor berada di dalam canvas
    canvas.bind_all("<MouseWheel>", _on_mousewheel) # Windows & Mac
    # Untuk Linux: canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    # Untuk Linux: canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # Pastikan untuk menghapus bind_all saat frame ini ditutup/dihancurkan
    # agar tidak mengganggu scroll di halaman lain
    def unbind_scroll(event):
        canvas.unbind_all("<MouseWheel>")
    list_frame.bind("<Destroy>", unbind_scroll)

    # Fungsi untuk membuat satu item (tombol) kuis
    def buat_item_quiz(parent, judul_quiz, deskripsi):
        teks_tombol = f"{judul_quiz}\n{deskripsi}"
        btn = tk.Button(parent, text=teks_tombol, bg="white", fg="#4A2C11", 
                        font=("Helvetica", 9), justify="left", anchor="w", relief="solid", bd=1,
                        command=lambda: mulai_kuis_terpilih(judul_quiz))
        btn.pack(fill="x", pady=5, ipady=8, padx=2)
        return btn

    def mulai_kuis_terpilih(judul_quiz):
        # Logika pemanggilan muat_soal(judul_quiz) nanti diletakkan di sini
        pass

    # --- MEMUAT DATA DARI data_manager.py ---
    daftar_quiz = load_daftar_quiz()

    # Mengecek apakah daftar kuis memiliki isi atau tidak
    if not daftar_quiz:
        pesan_kosong = tk.Label(list_frame, text="Belum ada kuis yang tersedia.", bg="#F4EFE6", fg="#4A2C11")
        pesan_kosong.pack(pady=20)
    else:
        # Looping data dari dictionary dan membuatkan tombolnya secara otomatis
        for quiz in daftar_quiz:
            buat_item_quiz(list_frame, quiz["judul"], quiz["deskripsi"])



    

def halaman_soal_quiz(root):
    root.configure(bg="#F4EFE6")

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

def halaman_hasil_quiz(root, nama_pemain="Budi", skor=80, benar=8, salah=2, waktu="02:45"):
    # Membersihkan layar dari widget sebelumnya
    for widget in root.winfo_children():
        widget.destroy()
        
    root.configure(bg="#F4EFE6")

    # Kontainer Utama untuk menengahkan konten
    main_frame = tk.Frame(root, bg="#F4EFE6")
    main_frame.pack(expand=True)

    # Judul / Header[cite: 5]
    judul = tk.Label(main_frame, text=f"Kuis selesai, {nama_pemain}!", font=("Helvetica", 24, "bold"), fg="#4A2C11", bg="#F4EFE6")
    judul.pack(pady=(0, 20))

    # Tampilan Skor dengan Lingkaran (menggunakan Canvas)[cite: 5]
    canvas = tk.Canvas(main_frame, width=160, height=160, bg="#F4EFE6", highlightthickness=0)
    canvas.pack(pady=10)
    
    # Gambar background lingkaran cokelat[cite: 5]
    canvas.create_oval(10, 10, 150, 150, fill="#A06A42", outline="#A06A42")
    # Teks angka skor di tengah lingkaran[cite: 5]
    canvas.create_text(80, 80, text=f"{skor}/100", font=("Helvetica", 24, "bold"), fill="white")

    # Frame untuk deretan Statistik (Benar, Salah, Waktu)[cite: 5]
    stats_frame = tk.Frame(main_frame, bg="#F4EFE6")
    stats_frame.pack(pady=20)

    # Kotak Jawaban Benar (Background Hijau)[cite: 5]
    box_benar = tk.Label(stats_frame, text=f"Benar: {benar}", font=("Helvetica", 11, "bold"), bg="#A0B084", fg="#4A2C11", width=15, height=2)
    box_benar.grid(row=0, column=0, padx=10)

    # Kotak Jawaban Salah (Background Putih, Border Cokelat)[cite: 5]
    box_salah = tk.Label(stats_frame, text=f"Salah: {salah}", font=("Helvetica", 11, "bold"), bg="white", fg="#A06A42", width=15, height=2, relief="solid", bd=1)
    box_salah.grid(row=0, column=1, padx=10)

    # Kotak Waktu (Background Putih, Border Cokelat)[cite: 5]
    box_waktu = tk.Label(stats_frame, text=f"Waktu: {waktu}", font=("Helvetica", 11, "bold"), bg="white", fg="#4A2C11", width=15, height=2, relief="solid", bd=1)
    box_waktu.grid(row=0, column=2, padx=10)

    # Frame untuk Navigasi Tombol Bawah[cite: 5]
    btn_frame = tk.Frame(main_frame, bg="#F4EFE6")
    btn_frame.pack(pady=20)

    # Tombol Tinjau Jawaban[cite: 5]
    btn_tinjau = tk.Button(btn_frame, text="Tinjau Jawaban", bg="white", fg="#4A2C11", font=("Helvetica", 10), width=15, relief="solid", bd=1)
    btn_tinjau.grid(row=0, column=0, padx=10, ipady=5)

    # Tombol Papan Skor[cite: 5]
    btn_papan = tk.Button(btn_frame, text="Papan Skor", bg="white", fg="#4A2C11", font=("Helvetica", 10), width=15, relief="solid", bd=1)
    btn_papan.grid(row=0, column=1, padx=10, ipady=5)

    # Tombol Main Lagi[cite: 5]
    btn_main = tk.Button(btn_frame, text="Main Lagi", bg="#4A2C11", fg="white", font=("Helvetica", 10, "bold"), width=15,
                        command=lambda: {
                            bersihkan_layar(root),  # Bersihkan halaman 
                            halaman_homescreen(root)  # Kembali ke Home Screen
                        })
    btn_main.grid(row=0, column=2, padx=10, ipady=5)

def halaman_papan_skor(root):
    # Membersihkan layar dari widget sebelumnya[cite: 3]
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#F4EFE6")

    # Bilah Atas[cite: 1]
    top_bar = tk.Frame(root, bg="#A0B084", height=25)
    top_bar.pack(fill="x")
    
    label_top = tk.Label(top_bar, text="QuizPy | Papan Skor", bg="#A0B084", fg="#4A2C11", font=("Helvetica", 9, "bold"))
    label_top.pack(side="left", padx=10, pady=2)

    # Kontainer Utama
    main_frame = tk.Frame(root, bg="#F4EFE6")
    main_frame.pack(expand=True, fill="both", padx=40, pady=20)

    # Header Frame (Judul & Filter Kategori)[cite: 1]
    header_frame = tk.Frame(main_frame, bg="#F4EFE6")
    header_frame.pack(fill="x", pady=(10, 20))

    judul = tk.Label(header_frame, text="10 Skor Tertinggi", font=("Helvetica", 24, "bold"), fg="#4A2C11", bg="#F4EFE6")
    judul.pack(side="left")

    btn_filter = tk.Button(header_frame, text="Semua kategori", bg="white", fg="#4A2C11", font=("Helvetica", 10), relief="solid", bd=1, padx=15)
    btn_filter.pack(side="right", ipady=2)

    # Tabel Frame[cite: 1]
    tabel_frame = tk.Frame(main_frame, bg="#F4EFE6")
    tabel_frame.pack(fill="x")

    # Header Tabel (Background Cokelat)[cite: 1]
    header_bg = "#4A2C11"
    header_fg = "white"
    row_header = tk.Frame(tabel_frame, bg=header_bg)
    row_header.pack(fill="x", pady=(0, 10), ipady=5)

    tk.Label(row_header, text="#", bg=header_bg, fg=header_fg, font=("Helvetica", 10, "bold"), width=5, anchor="w").pack(side="left", padx=(15, 0))
    tk.Label(row_header, text="Nama", bg=header_bg, fg=header_fg, font=("Helvetica", 10, "bold"), width=25, anchor="w").pack(side="left")
    tk.Label(row_header, text="Kategori", bg=header_bg, fg=header_fg, font=("Helvetica", 10, "bold"), width=20, anchor="w").pack(side="left")
    tk.Label(row_header, text="Skor", bg=header_bg, fg=header_fg, font=("Helvetica", 10, "bold"), width=10, anchor="e").pack(side="left")

    # Data Dummy untuk Tabel (Bisa diganti dengan data dari data_manager.py)[cite: 1, 3]
    data_skor = [
        ("Sari", "Python", "100"),
        ("Budi", "Python", "80"),
        ("Andi", "Sains", "70"),
        ("", "", "")
    ]

    # Melakukan iterasi untuk membuat baris Tabel[cite: 1]
    for rank, data in enumerate(data_skor):
        row_frame = tk.Frame(tabel_frame, bg="white", relief="solid", bd=1)
        row_frame.pack(fill="x", pady=4, ipady=5)
        
        tk.Label(row_frame, text=rank+1, bg="white", fg="#4A2C11", font=("Helvetica", 10), width=5, anchor="w").pack(side="left", padx=(15, 0))
        tk.Label(row_frame, text=data[0], bg="white", fg="#4A2C11", font=("Helvetica", 10), width=25, anchor="w").pack(side="left")
        tk.Label(row_frame, text=data[1], bg="white", fg="#4A2C11", font=("Helvetica", 10), width=20, anchor="w").pack(side="left")
        tk.Label(row_frame, text=data[2], bg="white", fg="#4A2C11", font=("Helvetica", 10), width=10, anchor="e").pack(side="left")

    # Frame Pembatas untuk mendorong tombol ke dasar layar
    spacer = tk.Frame(main_frame, bg="#F4EFE6")
    spacer.pack(expand=True, fill="both")

    # Tombol Navigasi Bawah[cite: 1]
    bottom_frame = tk.Frame(main_frame, bg="#F4EFE6")
    bottom_frame.pack(fill="x", pady=(20, 10))

    btn_kembali = tk.Button(bottom_frame, text="Kembali", bg="white", fg="#4A2C11", font=("Helvetica", 10), width=15, relief="solid", bd=1)
    btn_kembali.pack(side="left", ipady=5)


def halaman_buat_kuis_soal(root):
    bersihkan_layar(root)
    root.configure(bg="#F4EFE6")

    # Kontainer Utama
    main_frame = tk.Frame(root, bg="#F4EFE6")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Panel Kiri (Daftar Soal)
    left_panel = tk.Frame(main_frame, bg="#A0B084", width=150)
    left_panel.pack(side="left", fill="y", padx=(0, 15))
    left_panel.pack_propagate(False) # Pertahankan lebar

    label_daftar = tk.Label(left_panel, text="Daftar soal (3)", font=("Helvetica", 9, "bold"), bg="#A0B084", fg="#4A2C11")
    label_daftar.pack(pady=(15, 10))

    soal_1 = tk.Button(left_panel, text="Soal 1", bg="white", fg="#4A2C11", relief="flat", anchor="w", padx=10)
    soal_1.pack(fill="x", padx=10, pady=5, ipady=3)
    
    soal_2 = tk.Button(left_panel, text="Soal 2", bg="white", fg="#4A2C11", relief="flat", anchor="w", padx=10)
    soal_2.pack(fill="x", padx=10, pady=5, ipady=3)
    
    soal_3 = tk.Button(left_panel, text="Soal 3 (sedang diedit)", bg="#A06A42", fg="white", relief="solid", bd=1, anchor="w", padx=10)
    soal_3.pack(fill="x", padx=10, pady=5, ipady=3)

    btn_tambah = tk.Button(left_panel, text="+ Tambah Soal", bg="#4A2C11", fg="white", font=("Helvetica", 9, "bold"))
    btn_tambah.pack(side="bottom", fill="x", padx=10, pady=15, ipady=5)

    # Panel Kanan (Form Input Soal)
    right_panel = tk.Frame(main_frame, bg="#F4EFE6")
    right_panel.pack(side="left", fill="both", expand=True)

    # Input Pertanyaan
    label_tanya = tk.Label(right_panel, text="Pertanyaan", font=("Helvetica", 10, "bold"), fg="#4A2C11", bg="#F4EFE6")
    label_tanya.pack(anchor="w", pady=(10, 5))
    
    entry_tanya = tk.Text(right_panel, font=("Helvetica", 10), height=3)
    entry_tanya.insert("1.0", "Apa output dari print(type([]))?")
    entry_tanya.pack(fill="x", pady=5)

    # Input Pilihan Jawaban
    label_pilih = tk.Label(right_panel, text="Pilihan jawaban (tandai yang benar)", font=("Helvetica", 10, "bold"), fg="#4A2C11", bg="#F4EFE6")
    label_pilih.pack(anchor="w", pady=(15, 5))

    # Opsi A
    frame_a = tk.Frame(right_panel, bg="#F4EFE6")
    frame_a.pack(fill="x", pady=2)
    tk.Radiobutton(frame_a, bg="#F4EFE6").pack(side="left")
    tk.Entry(frame_a, font=("Helvetica", 10)).pack(side="left", fill="x", expand=True, ipady=3)

    # Opsi B (Terpilih)
    frame_b = tk.Frame(right_panel, bg="#F4EFE6")
    frame_b.pack(fill="x", pady=2)
    tk.Radiobutton(frame_b, bg="#F4EFE6").pack(side="left")
    entry_b = tk.Entry(frame_b, font=("Helvetica", 10), bg="#A0B084")
    entry_b.insert(0, "B. (jawaban benar)")
    entry_b.pack(side="left", fill="x", expand=True, ipady=3)

    # Opsi C
    frame_c = tk.Frame(right_panel, bg="#F4EFE6")
    frame_c.pack(fill="x", pady=2)
    tk.Radiobutton(frame_c, bg="#F4EFE6").pack(side="left")
    tk.Entry(frame_c, font=("Helvetica", 10)).pack(side="left", fill="x", expand=True, ipady=3)

    # Opsi D
    frame_d = tk.Frame(right_panel, bg="#F4EFE6")
    frame_d.pack(fill="x", pady=2)
    tk.Radiobutton(frame_d, bg="#F4EFE6").pack(side="left")
    tk.Entry(frame_d, font=("Helvetica", 10)).pack(side="left", fill="x", expand=True, ipady=3)

    # Penjelasan
    entry_jelas = tk.Entry(right_panel, font=("Helvetica", 10))
    entry_jelas.insert(0, "Penjelasan (opsional): List ditulis dengan kurung siku.")
    entry_jelas.pack(fill="x", pady=(15, 5), ipady=5)

    # Tombol Navigasi Bawah
    bottom_frame = tk.Frame(root, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

    btn_kembali = tk.Button(bottom_frame, text="Kembali", bg="white", fg="#4A2C11", font=("Helvetica", 10, "bold"), width=15, relief="solid", bd=1, command=lambda: halaman_buat_kuis_info(root))
    btn_kembali.pack(side="left", ipady=5)

    btn_simpan = tk.Button(bottom_frame, text="Simpan Quiz", bg="#4A2C11", fg="white", font=("Helvetica", 10, "bold"), width=15)
    btn_simpan.pack(side="right", ipady=5)
    
    btn_hapus = tk.Button(bottom_frame, text="Hapus Soal", bg="white", fg="#4A2C11", font=("Helvetica", 10, "bold"), width=15, relief="solid", bd=1)
    btn_hapus.pack(side="right", padx=10, ipady=5)


def halaman_buat_kepala_kuis(root):
    # Membersihkan layar dari widget sebelumnya[cite: 1]
    for widget in root.winfo_children():
        widget.destroy()

    root.configure(bg="#F4EFE6")

    # Bilah Atas[cite: 3]
    top_bar = tk.Frame(root, bg="#A0B084", height=25)
    top_bar.pack(fill="x")
    
    label_top = tk.Label(top_bar, text="QuizPy | Buat Quiz Baru (Langkah 1 dari 2)", bg="#A0B084", fg="#4A2C11", font=("Helvetica", 9, "bold"))
    label_top.pack(side="left", padx=10, pady=2)

    # Header Judul Halaman[cite: 3]
    header_frame = tk.Frame(root, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=40, pady=(20, 10))

    judul = tk.Label(header_frame, text="Informasi Quiz", font=("Helvetica", 24, "bold"), fg="#4A2C11", bg="#F4EFE6")
    judul.pack(side="left")

    # Frame Kontainer Formulir[cite: 3]
    form_frame = tk.Frame(root, bg="#F4EFE6")
    form_frame.pack(fill="both", expand=True, padx=40)

    # Input Nama Quiz[cite: 3]
    label_nama = tk.Label(form_frame, text="Nama quiz", font=("Helvetica", 10, "bold"), fg="#4A2C11", bg="#F4EFE6")
    label_nama.grid(row=0, column=0, sticky="w", pady=(10, 5))
    
    entry_nama = tk.Entry(form_frame, font=("Helvetica", 10), width=60)
    entry_nama.insert(0, "Contoh: Dasar Python")
    entry_nama.grid(row=1, column=0, columnspan=2, sticky="we", ipady=5)

    # Input Deskripsi Quiz[cite: 3]
    label_deskripsi = tk.Label(form_frame, text="Deskripsi", font=("Helvetica", 10, "bold"), fg="#4A2C11", bg="#F4EFE6")
    label_deskripsi.grid(row=2, column=0, sticky="w", pady=(15, 5))
    
    entry_deskripsi = tk.Text(form_frame, font=("Helvetica", 10), height=4, width=60)
    entry_deskripsi.insert("1.0", "Jelaskan singkat isi quiz ini...")
    entry_deskripsi.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)

    # Input Kategori dan Batas Waktu (Bersebelahan)[cite: 3]
    label_kategori = tk.Label(form_frame, text="Kategori", font=("Helvetica", 10, "bold"), fg="#4A2C11", bg="#F4EFE6")
    label_kategori.grid(row=4, column=0, sticky="w", pady=(15, 5))
    
    entry_kategori = tk.Entry(form_frame, font=("Helvetica", 10))
    entry_kategori.insert(0, "Pilih kategori")
    entry_kategori.grid(row=5, column=0, sticky="we", padx=(0, 10), ipady=5)
    
    label_waktu = tk.Label(form_frame, text="Batas waktu (menit)", font=("Helvetica", 10, "bold"), fg="#4A2C11", bg="#F4EFE6")
    label_waktu.grid(row=4, column=1, sticky="w", pady=(15, 5))
    
    entry_waktu = tk.Entry(form_frame, font=("Helvetica", 10))
    entry_waktu.insert(0, "5")
    entry_waktu.grid(row=5, column=1, sticky="we", ipady=5)

    # Mengatur bobot kolom agar lebar grid proporsional
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=1)

    # Tombol Navigasi Bawah[cite: 3]
    bottom_frame = tk.Frame(root, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=40, pady=20)

    btn_batal = tk.Button(bottom_frame, text="Batal", bg="white", fg="#4A2C11", font=("Helvetica", 10, "bold"), width=15, relief="solid", bd=1)
    btn_batal.pack(side="left", ipady=5)

    btn_lanjut = tk.Button(bottom_frame, text="Lanjut: Tambah Soal", bg="#4A2C11", fg="white", font=("Helvetica", 10, "bold"), width=20)
    # Catatan: tambahkan command=lambda: halaman_buat_kuis_soal(root) pada btn_lanjut untuk menyambungkan navigasi
    btn_lanjut.pack(side="right", ipady=5)

