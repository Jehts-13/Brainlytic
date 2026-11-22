# File: gui.py
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import logika
from data_manager import *

username_var = None

# Variabel Pembuatan Quiz
judul_var = None
deskripsi = None
jumlah_soal_var = None
batas_waktu_var = None


def reset_username():
    username_var.set("")

def reset_pembuatan_quiz():
    global judul_var, deskripsi, jumlah_soal_var, batas_waktu_var 
    judul_var = deskripsi = jumlah_soal_var = batas_waktu_var = None

def halaman_homescreen(ROOT):
    def batasi_input(*args):
        batas_maksimal = 20 # Ubah angka ini sesuai kebutuhan batas karakter Anda
        nama = username_var.get()
        
        # Jika panjang teks melebihi batas, potong teksnya
        if len(nama) > batas_maksimal:
            username_var.set(nama[0:20])

    def validasi_sebelum_lanjut():
        global username_var
        nama = username_var.get()
        # Mengecek apakah input kosong atau mengandung karakter selain huruf/angka
        if not nama.isalnum():
            messagebox.showwarning("Input Tidak Valid", "Nama hanya boleh berisi huruf dan angka (tanpa spasi atau simbol)!")
            return # Menghentikan proses agar tidak pindah halaman
        
        # Jika lolos validasi, jalankan perintah asli
        logika.simpan_nama_pemain(nama)
        bersihkan_layar(ROOT)
        halaman_pilih_quiz(ROOT)
    
    # 2. Membuat Widget Label untuk Judul
    judul = tk.Label(ROOT, text="Brainlytic", font=("Helvetica", 32, "bold"), fg="#5C3A21", bg="#F4EFE6")
    judul.pack(pady=(40, 5))

    sub_judul = tk.Label(ROOT, text="Uji pengetahuanmu, satu soal setiap kali", font=("Helvetica", 12), fg="#5C3A21", bg="#F4EFE6")
    sub_judul.pack(pady=(0, 20))

    # 3. Frame Input Nama
    frame_nama = tk.Frame(ROOT, bg="#F4EFE6")
    frame_nama.pack(pady=10)

    label_judul = tk.Label(frame_nama, text="Nama pemain", font=("Helvetica", 10, "bold"), fg="#5C3A21", bg="#F4EFE6")
    label_judul.pack(anchor="w")

    global username_var
    if username_var is None:
        username_var = tk.StringVar(value="Nama")
    username_var.trace_add("write", batasi_input)
    input_nama = tk.Entry(frame_nama, width=50, font=("Helvetica", 12), textvariable=username_var)
    input_nama.pack(ipady=5)

    # 4. Frame Menu (Tombol Kerjakan Quiz & Buat Quiz Baru)
    frame_menu = tk.Frame(ROOT, bg="#F4EFE6")
    frame_menu.pack(pady=30)

    btn_kerjakan = tk.Button(frame_menu, text="Kerjakan Quiz\n\nPilih dari daftar quiz yang\ntersedia", 
                             bg="#A06A42", fg="white", font=("Helvetica", 10, "bold"), width=25, height=5,
                             command=lambda: validasi_sebelum_lanjut())  
    btn_kerjakan.grid(row=0, column=0, padx=10)

    btn_buat = tk.Button(frame_menu, text="Buat Quiz Baru\n\nSusun soal dan jawabanmu\nsendiri", 
                         bg="#A06A42", fg="white", font=("Helvetica", 10, "bold"), width=25, height=5,
                         command=lambda: {bersihkan_layar(ROOT),halaman_buat_kepala_quiz(ROOT)})
    btn_buat.grid(row=0, column=1, padx=10)

    # 5. Link Papan Skor
    link_skor = tk.Label(ROOT, text="Lihat papan skor", font=("Helvetica", 10), fg="#A06A42", bg="#F4EFE6", cursor="hand2",) 
    link_skor.bind("<Button-1>", lambda event: halaman_papan_skor(ROOT=ROOT))
    link_skor.pack(pady=10)

    # Memulai perulangan aplikasi
    ROOT.mainloop()

def bersihkan_layar(ROOT):
    """Menghapus semua widget di dalam ROOT window untuk mengganti halaman."""
    for widget in ROOT.winfo_children():
        widget.destroy()

def halaman_pilih_quiz(ROOT):
    quiz_dipilih = None  # Variabel global untuk menyimpan quiz yang dipilih
    
    ROOT.configure(bg="#F4EFE6")

    # 1. Bilah Atas (Top Bar)
    top_bar = tk.Frame(ROOT, bg="#A0B084", height=25) # Warna hijau zaitun pudar
    top_bar.pack(fill="x")
    
    label_top = tk.Label(top_bar, text="QuizPy | Kerjakan Quiz", bg="#A0B084", fg="#4E220F", font=("Helvetica", 9, "bold"))
    label_top.pack(side="left", padx=10, pady=2)

    # 2. Area Judul & Pencarian
    header_frame = tk.Frame(ROOT, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=20, pady=(20, 10))

    judul = tk.Label(header_frame, text="Pilih Quiz", font=("Helvetica", 24, "bold"), fg="#4E220F", bg="#F4EFE6")
    judul.pack(side="left")

    cari_entry = tk.Entry(header_frame, font=("Helvetica", 10), width=25)
    cari_entry.insert(0, "Cari quiz...")
    cari_entry.pack(side="right", ipady=5)

    # 3. Tombol Navigasi 
    bottom_frame = tk.Frame(ROOT, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=20, pady=20)

    btn_kembali = tk.Button(bottom_frame, text="Kembali", bg="white", fg="#4E220F", 
                            font=("Helvetica", 10, "bold"), width=15, relief="solid", bd=1,
                            command=lambda: {
                                bersihkan_layar(ROOT),  # Bersihkan halaman 
                                halaman_homescreen(ROOT)  # Kembali ke Home Screen
                            }) 
    btn_kembali.pack(side="left", ipady=5)

    btn_mulai = tk.Button(bottom_frame, text="Mulai Quiz", bg="#4E220F", fg="white", 
                        font=("Helvetica", 10, "bold"), width=15,
                        command=lambda: aksi_mulai_kuis()) 
    btn_mulai.pack(side="right", ipady=5)

    # --- AREA SCROLL UNTUK DAFTAR quiz ---
    # 1. Buat kontainer utama untuk Canvas dan Scrollbar
    scroll_container = tk.Frame(ROOT, bg="#F4EFE6")
    scroll_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

    # 2. Buat Canvas
    canvas = tk.Canvas(scroll_container, bg="#F4EFE6", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # 3. Buat Scrollbar dan pasangkan dengan Canvas
    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    # 4. Buat Frame di dalam Canvas untuk menampung tombol quiz
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
    canvas.bind_all("<MouseWheel>", _on_mousewheel)
    
    # Pastikan untuk menghapus bind_all saat frame ini ditutup/dihancurkan
    # agar tidak mengganggu scroll di halaman lain
    def unbind_scroll(event):
        canvas.unbind_all("<MouseWheel>")
    list_frame.bind("<Destroy>", unbind_scroll)
    
    #============================================================================================
    # 1. Variabel untuk menyimpan judul kuis yang dipilih
    kuis_terpilih = tk.StringVar(value="")
    
    # 2. Dictionary untuk menyimpan referensi widget tombol
    tombol_kuis_dict = {}

    # --- FUNGSI PEMILIHAN WARNA DAN PENYIMPANAN ---
    def pilih_kuis(judul_quiz):
        # Menyimpan nama kuis ke variabel
        kuis_terpilih.set(judul_quiz)
        
        # Iterasi semua tombol di dalam dictionary
        for nama, tombol in tombol_kuis_dict.items():
            if nama == judul_quiz:
                # Ubah tombol yang dipilih menjadi cokelat dengan teks putih
                tombol.configure(bg="#A06A42", fg="white")
            else:
                # Reset tombol lainnya kembali ke putih
                tombol.configure(bg="white", fg="#4E220F")

    # --- FUNGSI MEMBUAT TOMBOL ---
    def buat_item_quiz(parent, judul_quiz, deskripsi):
        teks_tombol = f"{judul_quiz}\n{deskripsi}"
        btn = tk.Button(parent, text=teks_tombol, bg="white", fg="#4E220F", 
                        font=("Helvetica", 9), justify="left", anchor="w", relief="solid", bd=1)
        
        # Simpan widget tombol ke dalam dictionary berdasarkan judulnya
        tombol_kuis_dict[judul_quiz] = btn
        
        # Pasang perintah yang memanggil pilih_kuis saat diklik
        btn.configure(command=lambda q=judul_quiz: pilih_kuis(q))
        
        btn.pack(fill="x", pady=5, ipady=8, padx=2)
        return btn

    # --- FUNGSI TOMBOL "MULAI QUIZ" ---
    def aksi_mulai_kuis():
        judul = kuis_terpilih.get()
        if not judul:
            # Cegah user lanjut jika belum ada frame yang diklik
            messagebox.showwarning("Peringatan", "Silakan pilih salah satu kuis terlebih dahulu!")
            return
            
        print(f"Kuis yang akan dimainkan: {judul}")
        # Lanjutkan ke logika pemanggilan muat_soal(judul) di sini
        # halaman_soal_quiz(ROOT, judul)
        logika.muat_quiz(judul)
        time.sleep(1)
        bersihkan_layar(ROOT)
        halaman_soal_quiz(ROOT)  # Panggil halaman soal quiz dengan judul yang dipilih
        return

    # [Kode pembuatan canvas, scrollbar, on_configure, _on_mousewheel tetap sama...]

    # --- MEMUAT DATA ---
    daftar_quiz = load_daftar_quiz()
    
    if not daftar_quiz:
        print("Belum ada kuis yang tersedia.")
        tk.Label(list_frame, text="Belum ada kuis yang tersedia.", bg="#F4EFE6", fg="#4E220F").pack(pady=20)
    else:
        for quiz in daftar_quiz:
            buat_item_quiz(list_frame, quiz["judul"], quiz["deskripsi"])

    # btn_mulai.configure(command=aksi_mulai_kuis)



    

def halaman_soal_quiz(ROOT):
    # VARIABEL: jumlah soal, dan batas waktu (detik)
    jawaban = tk.StringVar(value="")
    jumlah_soal = logika.Jumlah_soal 
    batas_waktu = logika.Total_waktu
    sisa_waktu = batas_waktu
    nomor_soal = logika.Nomor_soal
    print(f"batas waktu:\t{batas_waktu}")

    ROOT.configure(bg="#F4EFE6")

    # Header Info (Indikator Soal & Waktu)
    header_frame = tk.Frame(ROOT, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=20, pady=(15, 5))

    # text indikator soal
    def text_indikator_soal():
        nonlocal nomor_soal, jumlah_soal
        return f"Soal {nomor_soal+1} dari {jumlah_soal}" 

    label_soal = tk.Label(header_frame, text=text_indikator_soal(), font=("Helvetica", 10, "bold"), fg="#4E220F", bg="#F4EFE6")
    label_soal.pack(side="left")

    
    # Indikator Timer 
    label_waktu = tk.Label(header_frame, text=f"Waktu: {logika.format_waktu(sisa_waktu)}", font=("Helvetica", 10, "bold"), fg="white", bg="#A06A42", width=12, pady=3)
    label_waktu.pack(side="right")
    
    # Variabel untuk menyimpan ID jadwal timer agar bisa dibatalkan kapan saja
    timer_id = None

    def update_timer():
        nonlocal sisa_waktu, timer_id
        # 1. Cek terlebih dahulu apakah widget label_waktu masih ada di layar
        # Jika pemain sudah pindah halaman (misal klik Keluar/Selesai), hentikan fungsi
        if not label_waktu.winfo_exists():
            return

        # 2. Cek apakah waktu masih tersisa
        if sisa_waktu > 0:
            sisa_waktu -= 1
            text_waktu = logika.format_waktu(sisa_waktu)
            label_waktu.configure(text=f"Waktu: {text_waktu}")
            
            # Jadwalkan 1 detik berikutnya dan simpan ID-nya
            timer_id = ROOT.after(1000, update_timer)
        else:
            # 3. Jika waktu habis, proses selesai tanpa menjadwalkan .after() lagi
            try:
                logika.simpan_jawaban_soal(None)
                logika.hitung_skor(0)
            except IndexError:
                print("The Quiz has encountered an error!\t# Cannot continue the process!")
                print("Cancelling the quiz...")
                logika.reset_data()
                bersihkan_layar(ROOT)
                halaman_homescreen(ROOT)
                return
            bersihkan_layar(ROOT)
            halaman_hasil_quiz(ROOT)

    timer_id = ROOT.after(1000, update_timer)



    # 3. Bilah Progres (Progress Bar Manual menggunakan Frame)
    progress_bg = tk.Frame(ROOT, bg="#A0B084", height=10) # Latar belakang progres (hijau pudar)
    progress_bg.pack(fill="x", padx=20, pady=(0, 15))

    # Panjang total progress bar
    panjang_progres = logika.ambil_rasio_progressbar()

    progress_fill = tk.Frame(progress_bg, bg="#4E220F", height=10) # Bagian yang terisi (coklat tua)
    progress_fill.pack(side="left")
    progress_fill.place(x=0, y=0, relheight=1.0, relwidth=0.0)
    progress_bg.pack_propagate(False) # Mencegah frame bg mengecil mengikuti isi
    
    def update_progressbar():
        label_soal.configure(text=text_indikator_soal())
        progress_fill.place(x=0,y=0, relheight=1.0, relwidth=panjang_progres)
    
    # Mengupdate progress_bar di awal
    update_progressbar()

    # 4. Kotak Pertanyaan
    pertanyaan_frame = tk.Frame(ROOT, bg="white", highlightbackground="#A0B084", highlightthickness=2)
    pertanyaan_frame.pack(fill="x", padx=20, pady=10)
    
    pertanyaan = logika.Soal[nomor_soal]['deskripsi']
    teks_pertanyaan_frame = tk.Label(pertanyaan_frame, text=pertanyaan, font=("Helvetica", 14, "bold"), fg="#4E220F", bg="white", wraplength=500)
    teks_pertanyaan_frame.pack(pady=20)

    # 5. Pilihan Ganda (Grid 2x2)
    opsi_frame = tk.Frame(ROOT, bg="#F4EFE6")
    opsi_frame.pack(fill="x", padx=20, pady=5)
    
    # Konfigurasi grid agar seimbang
    opsi_frame.columnconfigure(0, weight=1)
    opsi_frame.columnconfigure(1, weight=1)

    teks_pilihan = logika.Soal[nomor_soal]['pilihan']
    tombol_pilihan_dict = {}
    
    def pilih_opsi(jawabanIndex):
        jawaban.set(jawabanIndex)
        
        for index, btn in tombol_pilihan_dict.items():
            if index == jawabanIndex:
                btn.configure(bg="#A06A42", fg="white")
                print(f"\n@@ Pilihan ke-{index+1} terpilih!")
            else:
                btn.configure(bg="white", fg="#4E220F")

    def reset_opsi():
        for btn in tombol_pilihan_dict.values():
            btn.configure(bg="white", fg="#4E220F")
            
        jawaban.set(value="")
        # print("\n@@ Jawaban telah di reset!")
    
    def buat_item_opsi(parent, nomor_index, baris, kolom):
        nonlocal teks_pilihan
        btn = tk.Button(parent, text=teks_pilihan[nomor_index], bg="white", fg="#4E220F", font=("Helvetica", 10), relief="solid", bd=1, wraplength=200)
        btn.grid(row=baris, column=kolom, sticky="ew", padx=(0, 5), pady=5, ipady=8)
        tombol_pilihan_dict[nomor_index] = btn
        btn.configure(command=lambda opsi=nomor_index: pilih_opsi(opsi))
        
    def update_pilihan():
        nonlocal teks_pilihan
        for index, btn in tombol_pilihan_dict.items():
            btn.configure(text=teks_pilihan[index])
    
    buat_item_opsi(opsi_frame, 0, 0, 0)
    buat_item_opsi(opsi_frame, 1, 0, 1)
    buat_item_opsi(opsi_frame, 2, 1, 0)
    buat_item_opsi(opsi_frame, 3, 1, 1)
        
    update_pilihan()

    # 6. Tombol Navigasi Bawah
    bottom_frame = tk.Frame(ROOT, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=20, pady=10)
    
    def keluar_quiz():
        nonlocal timer_id
        
        if timer_id is not None:
            ROOT.after_cancel(timer_id)
            timer_id = None
            
        logika.reset_data()
        bersihkan_layar(ROOT)
        halaman_homescreen(ROOT)

    btn_keluar = tk.Button(bottom_frame, text="Keluar", bg="white", fg="#4E220F", 
                           font=("Helvetica", 10), relief="solid", bd=1, width=12,
                           command=lambda: keluar_quiz())
    btn_keluar.pack(side="left", ipady=5)

    label_reset = tk.Button(bottom_frame, text="Reset Jawaban", font=("Helvetica", 10), fg="#4E220F", bg="#F4EFE6",  
                            relief="sunken", bd=1, width=16,
                            command=lambda:reset_opsi())
    label_reset.pack(side="left", expand=True)

    def load_berikutnya():
        try:
            # Menyimpan jawaban ke penyimpanan sementara
            nonlocal nomor_soal 
            logika.simpan_jawaban_soal(jawaban.get() if jawaban.get() != "" else None)
            
            # Jika jumlah_soal == nomor_soal+1, lanjut ke hasil quiz
            if jumlah_soal == nomor_soal + 1:
                logika.hitung_skor(sisa_waktu)
                time.sleep(0.5)
                halaman_hasil_quiz(ROOT)
                return
            
            
            # selain itu, update nomor_soal untuk lanjut ke soal berikutnya
            reset_opsi()
            print(f"Jawaban {nomor_soal} disimpan, nomor_soal bertambah 1")
            nomor_soal += 1
            
            nonlocal panjang_progres, pertanyaan, teks_pilihan
            # mengupdate progressbar
            panjang_progres = logika.ambil_rasio_progressbar()
            update_progressbar()
            # load soal yang baru
            pertanyaan = logika.Soal[nomor_soal]['deskripsi']
            teks_pertanyaan_frame.configure(text=pertanyaan)
            # load pilihan yang baru
            teks_pilihan = logika.Soal[nomor_soal]['pilihan']
            update_pilihan()
            
        except IndexError:
            print(f"{nomor_soal} index is not in the list!")

    btn_berikutnya = tk.Button(bottom_frame, text="Berikutnya", bg="#4E220F", fg="white", font=("Helvetica", 10, "bold"), width=12,
                               command=lambda: {
                                   load_berikutnya()
                               })
    btn_berikutnya.pack(side="right", ipady=5)

def halaman_hasil_quiz(ROOT):
    
    # VARIABEL: 
    jumlah_benar = logika.Jumlah_benar
    jumlah_salah = logika.Jumlah_salah
    skor = logika.Skor
    waktu = logika.Waktu_digunakan
    print(f"Jumlah Benar: {jumlah_benar:<5}\nJumlah Salah: {jumlah_salah:<5}\nSkor: {skor:<5}Waktu: {waktu:<5}")
    # Membersihkan layar dari widget sebelumnya
    bersihkan_layar(ROOT)
    ROOT.configure(bg="#F4EFE6") 

    # Kontainer Utama untuk menengahkan konten
    main_frame = tk.Frame(ROOT, bg="#F4EFE6")
    main_frame.pack(expand=True)

    # Judul / Header
    judul = tk.Label(main_frame, text=f"quiz selesai, {username_var.get()}!", font=("Helvetica", 24, "bold"), fg="#4E220F", bg="#F4EFE6")
    judul.pack(pady=(0, 20))

    # Tampilan Skor dengan Lingkaran (menggunakan Canvas)
    canvas = tk.Canvas(main_frame, width=160, height=160, bg="#F4EFE6", highlightthickness=0)
    canvas.pack(pady=10)
    
    # Gambar background lingkaran cokelat
    canvas.create_oval(10, 10, 150, 150, fill="#A06A42", outline="#A06A42")
    # Teks angka skor di tengah lingkaran
    canvas.create_text(80, 80, text=f"{skor}/100", font=("Helvetica", 24, "bold"), fill="white")

    # Frame untuk deretan Statistik (Benar, Salah, Waktu)
    stats_frame = tk.Frame(main_frame, bg="#F4EFE6")
    stats_frame.pack(pady=20)

    # Kotak Jawaban Benar (Background Hijau)
    box_benar = tk.Label(stats_frame, text=f"Benar: {jumlah_benar}", font=("Helvetica", 11, "bold"), bg="#A0B084", fg="#4E220F", width=15, height=2)
    box_benar.grid(row=0, column=0, padx=10)

    # Kotak Jawaban Salah (Background Putih, Border Cokelat)
    box_salah = tk.Label(stats_frame, text=f"Salah: {jumlah_salah}", font=("Helvetica", 11, "bold"), bg="white", fg="#A06A42", width=15, height=2, relief="solid", bd=1)
    box_salah.grid(row=0, column=1, padx=10)

    # Kotak Waktu (Background Putih, Border Cokelat)
    box_waktu = tk.Label(stats_frame, text=f"Waktu: {logika.format_waktu(waktu)}", font=("Helvetica", 11, "bold"), bg="white", fg="#4E220F", width=15, height=2, relief="solid", bd=1)
    box_waktu.grid(row=0, column=2, padx=10)

    # Frame untuk Navigasi Tombol Bawah
    btn_frame = tk.Frame(main_frame, bg="#F4EFE6")
    btn_frame.pack(pady=20)

    # Tombol Tinjau Jawaban
    btn_tinjau = tk.Button(btn_frame, text="Tinjau Jawaban", bg="white", fg="#4E220F", font=("Helvetica", 10), width=15, relief="solid", bd=1)
    btn_tinjau.grid(row=0, column=0, padx=10, ipady=5)

    # Tombol Papan Skor
    btn_papan = tk.Button(btn_frame, text="Papan Skor", bg="white", fg="#4E220F", font=("Helvetica", 10), width=15, relief="solid", bd=1,
                          command=lambda: halaman_papan_skor(ROOT))
    btn_papan.grid(row=0, column=1, padx=10, ipady=5)

    # Tombol Main Lagi
    btn_main = tk.Button(btn_frame, text="Main Lagi", bg="#4E220F", fg="white", font=("Helvetica", 10, "bold"), width=15,
                        command=lambda: {
                            bersihkan_layar(ROOT),  # Bersihkan halaman 
                            logika.reset_data(),
                            halaman_homescreen(ROOT)  # Kembali ke Home Screen
                        })
    btn_main.grid(row=0, column=2, padx=10, ipady=5)

def halaman_papan_skor(ROOT):
    # Membersihkan layar dari widget sebelumnya
    for widget in ROOT.winfo_children():
        widget.destroy()

    ROOT.configure(bg="#F4EFE6")

    # Bilah Atas
    top_bar = tk.Frame(ROOT, bg="#A0B084", height=25)
    top_bar.pack(fill="x")
    
    label_top = tk.Label(top_bar, text="QuizPy | Papan Skor", bg="#A0B084", fg="#4E220F", font=("Helvetica", 9, "bold"))
    label_top.pack(side="left", padx=10, pady=2)

    # Kontainer Utama
    main_frame = tk.Frame(ROOT, bg="#F4EFE6")
    main_frame.pack(expand=True, fill="both", padx=40, pady=20)

    # Header Frame (Judul & Filter Kategori)
    header_frame = tk.Frame(main_frame, bg="#F4EFE6")
    header_frame.pack(fill="x", pady=(10, 20))

    judul = tk.Label(header_frame, text="10 Skor Tertinggi", font=("Helvetica", 24, "bold"), fg="#4E220F", bg="#F4EFE6")
    judul.pack(side="left")

    btn_filter = tk.Button(header_frame, text="Semua kategori", bg="white", fg="#4E220F", font=("Helvetica", 10), relief="solid", bd=1, padx=15)
    btn_filter.pack(side="right", ipady=2)

    # Tabel Frame Container
    table_container = tk.Frame(main_frame, bg="#F4EFE6")
    table_container.pack(fill="both", expand=True)

    # Canvas untuk scrolling
    table_canvas = tk.Canvas(
        table_container,
        bg="#F4EFE6",
        highlightthickness=0
    )
    table_canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar
    scrollbar = tk.Scrollbar(
        table_container,
        orient="vertical",
        command=table_canvas.yview
    )
    scrollbar.pack(side="right", fill="y")

    table_canvas.configure(yscrollcommand=scrollbar.set)

    # Frame untuk isi tabel
    tabel_frame = tk.Frame(table_canvas, bg="#F4EFE6")

    canvas_window = table_canvas.create_window(
        (0, 0),
        window=tabel_frame,
        anchor="nw"
    )

    # Update scroll region ketika ukuran tabel berubah
    def update_scroll_region(event):
        table_canvas.configure(
            scrollregion=table_canvas.bbox("all")
        )

    tabel_frame.bind("<Configure>", update_scroll_region)

    # Menyesuaikan lebar tabel dengan canvas
    def update_canvas_width(event):
        table_canvas.itemconfig(
            canvas_window,
            width=event.width
        )

    table_canvas.bind("<Configure>", update_canvas_width)

    def on_mousewheel(event):
        table_canvas.yview_scroll(
            int(-1 * (event.delta / 120)),
            "units"
        )

    table_canvas.bind_all("<MouseWheel>", on_mousewheel)

    # Linux support
    table_canvas.bind_all(
        "<Button-4>",
        lambda event: table_canvas.yview_scroll(-1, "units")
    )

    table_canvas.bind_all(
        "<Button-5>",
        lambda event: table_canvas.yview_scroll(1, "units")
    )

    # Header Tabel (Background Cokelat)
    header_bg = "#4E220F"
    header_fg = "white"
    row_header = tk.Frame(tabel_frame, bg=header_bg)
    row_header.pack(fill="x", pady=(0, 10), ipady=5)

    tk.Label(row_header, text="#", bg=header_bg, fg=header_fg, font=("Helvetica", 10, "bold"), width=5, anchor="w").pack(side="left", padx=(15, 0))
    tk.Label(row_header, text="Nama", bg=header_bg, fg=header_fg, font=("Helvetica", 10, "bold"), width=25, anchor="w").pack(side="left")
    tk.Label(row_header, text="Kategori", bg=header_bg, fg=header_fg, font=("Helvetica", 10, "bold"), width=20, anchor="w").pack(side="left")
    tk.Label(row_header, text="Skor", bg=header_bg, fg=header_fg, font=("Helvetica", 10, "bold"), width=10, anchor="e").pack(side="left")

    data_peringkat_raw = load_user_history()
    data_peringkat = logika.sort_user_history(data_peringkat_raw)[:10]

    # Debugging Papan Peringkat
    print("PAPAN_PERINGKAT_RAW")
    for data in data_peringkat_raw:
        print(data)
    print('='*40,"\nPAPAN_PERINGKAT_SORTED")
    for data in data_peringkat:
        print(data)

    # Melakukan iterasi untuk membuat baris Tabel
    for rank, data in enumerate(data_peringkat):
        row_frame = tk.Frame(tabel_frame, bg="white", relief="solid", bd=1)
        row_frame.pack(fill="x", pady=4, ipady=5)
        
        tk.Label(row_frame, text=rank+1, bg="white", fg="#4E220F", font=("Helvetica", 10), width=5, anchor="w").pack(side="left", padx=(15, 0))
        tk.Label(row_frame, text=data['username'], bg="white", fg="#4E220F", font=("Helvetica", 10), width=25, anchor="w").pack(side="left")
        tk.Label(row_frame, text=data['judul_quiz'], bg="white", fg="#4E220F", font=("Helvetica", 10), width=20, anchor="w").pack(side="left")
        tk.Label(row_frame, text=data['skor'], bg="white", fg="#4E220F", font=("Helvetica", 10), width=10, anchor="e").pack(side="left")

    # Frame Pembatas untuk mendorong tombol ke dasar layar
    spacer = tk.Frame(main_frame, bg="#F4EFE6", height=5)
    spacer.pack(fill="x")

    # Tombol Navigasi Bawah
    bottom_frame = tk.Frame(main_frame, bg="#F4EFE6")
    bottom_frame.pack(fill="x", pady=(20, 10))

    btn_kembali = tk.Button(bottom_frame, text="Kembali", bg="white", fg="#4E220F", font=("Helvetica", 10), width=15, relief="solid", bd=1,
                            command=lambda: {logika.reset_data(),bersihkan_layar(ROOT), halaman_homescreen(ROOT)})
    btn_kembali.pack(side="left", ipady=5)

def halaman_buat_kepala_quiz(ROOT):
    global judul_var, deskripsi, jumlah_soal_var, batas_waktu_var
    if judul_var == None:
        judul_var = tk.StringVar(value="")
    if jumlah_soal_var == None:
        jumlah_soal_var = tk.StringVar(value="")
    if batas_waktu_var == None:
        batas_waktu_var = tk.StringVar(value="")
    if deskripsi == None:
        deskripsi = ""
    
    def batasan_judul(*args):
        global judul_var
        if len(judul_var.get()) > 28:
            judul_var.set(judul_var.get()[:28])

    def batasan_deskripsi(*args):
        nonlocal entry_deskripsi
        global deskripsi
        deskripsi = entry_deskripsi.get("1.0", "end-1c")
        if len(deskripsi) > 55:
            entry_deskripsi.delete("1.0", "end")
            entry_deskripsi.insert("1.0", deskripsi[:55])
            deskripsi = deskripsi[:55]
        label_deskripsi_cnt.configure(text=f"{len(deskripsi)}/55 karakter")
    
    def batasan_soal(*args):
        global jumlah_soal_var
        jumlah = jumlah_soal_var.get() 
        if not jumlah.isdigit():
            jumlah_soal_var.set(jumlah[:len(jumlah)-1])
        else:
            jumlah = int(jumlah)
            if jumlah > 25:
                jumlah_soal_var.set("25")
            else:
                jumlah_soal_var.set(f"{jumlah}")

    def batasan_waktu(*args):
        global batas_waktu_var
        waktu = batas_waktu_var.get() 
        if not waktu.isdigit():
            batas_waktu_var.set(waktu[:len(waktu)-1])
        else:
            waktu = int(waktu)
            if waktu > 125:
                batas_waktu_var.set("125")
            else:
                batas_waktu_var.set(f"{waktu}")

    def validasi_kepala_quiz():
        judul = judul_var.get()
        deskripsi = entry_deskripsi.get("1.0", "end-1c")
        jumlah = jumlah_soal_var.get()
        waktu = batas_waktu_var.get()

        # Check jika ada Input yang masih kosong
        if len(judul) == 0:
            messagebox.showwarning("Judul belum ada", "Mohon isi terlebih dahulu Judul Quiz ini!")
            return False
        if len(deskripsi) == 0:
            messagebox.showwarning("Deskripsi belum ada", "Mohon isi terlebih dahulu Deskripsi Quiz ini!")
            return False
        if len(jumlah) == 0:
            messagebox.showwarning("Jumlah soal belum ada", "Mohon isi terlebih dahulu Jumlah Soal!")
            return False
        if len(waktu) == 0:
            messagebox.showwarning("Batas Waktu belum ada", "Mohon isi terlebih dahulu Batas Waktu Quiz!")
            return False

        # Check jika judul yang sama telah ada di daftar quiz
        daftar_quiz = load_daftar_quiz()
        for quiz in daftar_quiz:
            if judul == quiz['judul']:
                messagebox.showwarning("Judul duplikat!", "Judul telah terdaftar dalam list Quiz aplikasi! Mohon masukkan Judul Quiz yang berbeda",)
                return False
        return True
        
    def lanjut_pembuatan_soal():
        valid = validasi_kepala_quiz()
        
        if not valid:
            return
        
        logika.simpan_kepala_quiz(judul_var.get(), entry_deskripsi.get("1.0", "end-1c"), jumlah_soal_var.get(), batas_waktu_var.get())
        bersihkan_layar(ROOT)
        halaman_buat_quiz_soal(ROOT)


    ROOT.configure(bg="#F4EFE6")

    # Bilah Atas
    top_bar = tk.Frame(ROOT, bg="#A0B084", height=25)
    top_bar.pack(fill="x")
    
    label_top = tk.Label(top_bar, text="QuizPy | Buat Quiz Baru (Langkah 1 dari 2)", bg="#A0B084", fg="#4E220F", font=("Helvetica", 9, "bold"))
    label_top.pack(side="left", padx=10, pady=2)

    # Header Judul Halaman
    header_frame = tk.Frame(ROOT, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=40, pady=(20, 10))

    label_judul = tk.Label(header_frame, text="Informasi Quiz", font=("Helvetica", 24, "bold"), fg="#4E220F", bg="#F4EFE6")
    label_judul.pack(side="left")

    # Frame Kontainer Formulir
    form_frame = tk.Frame(ROOT, bg="#F4EFE6")
    form_frame.pack(fill="both", expand=True, padx=40)

    # Input Judul Quiz
    label_judul = tk.Label(form_frame, text="Judul quiz", font=("Helvetica", 14, "bold"), fg="#4E220F", bg="#F4EFE6")
    label_judul.grid(row=0, column=0, sticky="w", pady=(10, 5))
    
    judul_var.trace_add("write", batasan_judul)
    entry_judul = tk.Entry(form_frame, font=("Helvetica", 14), width=60, textvariable=judul_var)
    entry_judul.insert(0,"judul_admin") #! dev test
    entry_judul.grid(row=1, column=0, columnspan=2, sticky="we", ipady=5)

    # Input Deskripsi Quiz
    label_deskripsi = tk.Label(form_frame, text="Deskripsi", font=("Helvetica", 14, "bold"), fg="#4E220F", bg="#F4EFE6")
    label_deskripsi.grid(row=2, column=0, sticky="w", pady=(15, 5))

    label_deskripsi_cnt = tk.Label(form_frame, text="0/55 karakter", font=("Helvetica", 10, "bold"), fg="#A06A42", bg="#F4EFE6")
    label_deskripsi_cnt.grid(row=2, column=1, sticky="e", pady=(15, 5))
    
    entry_deskripsi = tk.Text(form_frame, font=("Helvetica", 14), height=4, width=60)
    entry_deskripsi.bind("<KeyRelease>", batasan_deskripsi)
    deskripsi = "test_deskripsi_admin" #! dev test
    entry_deskripsi.insert("1.0", deskripsi)
    entry_deskripsi.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)

    # Input Jumlah Soal dan Batas Waktu (Bersebelahan)
    label_jumlah_soal = tk.Label(form_frame, text="Jumlah soal (maks. 25)", font=("Helvetica", 14, "bold"), fg="#4E220F", bg="#F4EFE6")
    label_jumlah_soal.grid(row=4, column=0, sticky="w", pady=(15, 5))
    
    jumlah_soal_var.trace_add("write", batasan_soal)
    entry_jumlah_soal = tk.Entry(form_frame, font=("Helvetica", 14), textvariable=jumlah_soal_var)
    entry_jumlah_soal.insert(0,"23")
    entry_jumlah_soal.grid(row=5, column=0, sticky="we", padx=(0, 10), ipady=5)
    
    label_waktu = tk.Label(form_frame, text="Batas waktu (menit)", font=("Helvetica", 14, "bold"), fg="#4E220F", bg="#F4EFE6")
    label_waktu.grid(row=4, column=1, sticky="w", pady=(15, 5))
    
    batas_waktu_var.trace_add("write", batasan_waktu)
    entry_waktu = tk.Entry(form_frame, font=("Helvetica", 14), textvariable=batas_waktu_var)
    entry_waktu.insert(0, "50")
    entry_waktu.grid(row=5, column=1, sticky="we", ipady=5)

    # Mengatur bobot kolom agar lebar grid proporsional
    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=1)

    # Tombol Navigasi Bawah
    bottom_frame = tk.Frame(ROOT, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=40, pady=20)

    btn_batal = tk.Button(bottom_frame, text="Batal", bg="white", fg="#4E220F", font=("Helvetica", 10, "bold"), width=15, relief="solid", bd=1,
                          command=lambda:{
                              reset_pembuatan_quiz(),
                              logika.reset_data(),
                              bersihkan_layar(ROOT),
                              halaman_homescreen(ROOT)
                          })
    btn_batal.pack(side="left", ipady=5)

    btn_lanjut = tk.Button(bottom_frame, text="Lanjut: Tambah Soal", bg="#4E220F", fg="white", font=("Helvetica", 10, "bold"), width=20,
                           command= lambda: lanjut_pembuatan_soal())
    btn_lanjut.pack(side="right", ipady=5)

def halaman_buat_quiz_soal(ROOT):
    ROOT.configure(bg="#F4EFE6")
    nomor_pertanyaan_var = tk.IntVar(value=None)
    deskripsi_soal = ""
    jawaban_a_var = tk.StringVar(value="")
    jawaban_b_var = tk.StringVar(value="")
    jawaban_c_var = tk.StringVar(value="")
    jawaban_d_var = tk.StringVar(value="")
    jawaban_benar_var = tk.IntVar()
    penjelasan_var = tk.StringVar(value="")
    
    def reset_data_soal():
        nonlocal deskripsi_soal, nomor_pertanyaan_var, jawaban_a_var, jawaban_b_var, jawaban_c_var, jawaban_d_var, jawaban_benar_var, penjelasan_var
        deskripsi_soal = ""
        nomor_pertanyaan_var.set(0)
        jawaban_a_var.set("")
        jawaban_b_var.set("")
        jawaban_c_var.set("")
        jawaban_d_var.set("")
        jawaban_benar_var.set(None)
        penjelasan_var.set("")

    def batasan_deskripsi_soal(*args):
        nonlocal deskripsi_soal

        teks = entry_deskripsi_soal.get("1.0", "end-1c")

        if len(teks) > 90:
            teks = teks[:90]

            entry_deskripsi_soal.delete("1.0", "end")
            entry_deskripsi_soal.insert("1.0", teks)

        deskripsi_soal = teks

    # Kontainer Utama
    main_frame = tk.Frame(ROOT, bg="#F4EFE6")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Panel Kiri (Daftar Soal)
    left_panel = tk.Frame(main_frame, bg="#A0B084", width=150)
    left_panel.pack(side="left", fill="y", padx=(0, 15))
    left_panel.pack_propagate(False) # Pertahankan lebar

    label_daftar = tk.Label(left_panel, text=f"Daftar soal ({jumlah_soal_var.get()})", font=("Helvetica", 9, "bold"), bg="#A0B084", fg="#4E220F")
    label_daftar.pack(pady=(15, 10))
    
    # --- AREA SCROLL UNTUK DAFTAR QUIZ ---
    # Container untuk Canvas dan Scrollbar
    scroll_container = tk.Frame(left_panel, bg="#A0B084")
    scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

    # Canvas
    canvas = tk.Canvas(scroll_container, bg="#A0B084", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    # Scrollbar di sebelah kanan Canvas
    scrollbar = ttk.Scrollbar( scroll_container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")

    canvas.configure(yscrollcommand=scrollbar.set)

    # Frame untuk tombol-tombol soal
    list_frame = tk.Frame(canvas, bg="#A0B084")

    canvas_window = canvas.create_window((0, 0), window=list_frame, anchor="nw")

    # Update scroll region ketika ukuran list berubah
    def update_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    list_frame.bind("<Configure>", update_scroll)

    # Sesuaikan lebar frame dengan Canvas
    def resize_canvas(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    # Mouse wheel scrolling
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def unbind_scroll(event):
        canvas.unbind_all("<MouseWheel>")

    list_frame.bind("<Destroy>", unbind_scroll)

    tombol_soal_list = {}
    
    def simpan_input_soal():
        nonlocal deskripsi_soal

        # Read directly from the widgets
        deskripsi_soal = entry_deskripsi_soal.get("1.0", "end-1c")

        jawaban_a = jawaban_a_var.get()
        jawaban_b = jawaban_b_var.get()
        jawaban_c = jawaban_c_var.get()
        jawaban_d = jawaban_d_var.get()

        jawaban_benar = jawaban_benar_var.get()
        penjelasan = penjelasan_var.get()

        # Save into your logic module
        tersimpan = logika.simpan_soal(
            logika.Nomor_soal,
            deskripsi_soal,
            jawaban_a,
            jawaban_b,
            jawaban_c,
            jawaban_d,
            jawaban_benar,
            penjelasan
        )

        return tersimpan

    def muat_input_soal(indeks):
        nonlocal deskripsi_soal

        # Get data from logic module
        data = logika.ambil_soal(indeks)

        (
            deskripsi_soal,
            jawaban_a,
            jawaban_b,
            jawaban_c,
            jawaban_d,
            jawaban_benar,
            penjelasan
        ) = data

        # Update question description
        entry_deskripsi_soal.delete("1.0", "end")
        entry_deskripsi_soal.insert("1.0", deskripsi_soal)

        # Update answer choices
        jawaban_a_var.set(jawaban_a)
        jawaban_b_var.set(jawaban_b)
        jawaban_c_var.set(jawaban_c)
        jawaban_d_var.set(jawaban_d)

        # Update correct answer
        jawaban_benar_var.set(jawaban_benar)

        # Update explanation
        penjelasan_var.set(penjelasan)

        # Update correct-answer highlighting
        pilih_jawaban(jawaban_benar)

    def pilih_soal(indeks):
        #TODO: Deskripsi Soal, Pilihan A-D (0-3), Jawaban Benar, serta Penjelasan
        # Menyimpan, membersihkan, Mengisi
            
        # 1. Menyimpan informasi dari soal saat ini
        if not simpan_input_soal():
            print("Gagal menyimpan soal sebelumnya!")
            return
        
        # 2. Mengupdate Nomor soal
        logika.Nomor_soal = indeks
        nomor_pertanyaan_var.set(indeks)
        
        # 3. Mengisi entry point dari data yang ada
        muat_input_soal(indeks)
        
        # 4. Update button appearances
        for i, tombol in tombol_soal_list.items():
            if i == indeks:
                tombol.configure(bg="#A06A42", fg="white")
            else:
                tombol.configure(bg="white", fg="#4E220F")    
        

    def buat_item_soal(parent, indeks):
        btn = tk.Button(parent, text=f"Soal {indeks+1}", bg="white", fg="#4E220F", relief="flat", anchor="w", padx=10)
        tombol_soal_list[indeks] = btn
        
        btn.configure(command=lambda q=indeks: pilih_soal(q))
        
        btn.pack(fill="x", padx=10, pady=5, ipady=3)
        return btn
    
    opsi_entry_list = [] # Menyimpan tombol widget entry A-D
    
    def pilih_jawaban(val):
        print(f"kunci jawaban: {val}")
        for i,entry in enumerate(opsi_entry_list):
            if i == val:
                entry.configure(bg="#A0B084")
            else:
                entry.configure(bg="white")
        
    for i in range(logika.Jumlah_soal):
        buat_item_soal(list_frame, i)
        

    # Panel Kanan (Form Input Soal)
    right_panel = tk.Frame(main_frame, bg="#F4EFE6")
    right_panel.pack(side="left", fill="both", expand=True)

    # Input Deskripsi Soal
    label_tanya = tk.Label(right_panel, text="Pertanyaan", font=("Helvetica", 10, "bold"), fg="#4E220F", bg="#F4EFE6")
    label_tanya.pack(anchor="w", pady=(10, 5))
    
    entry_deskripsi_soal = tk.Text(right_panel, font=("Helvetica", 10), height=3)
    entry_deskripsi_soal.bind("<KeyRelease>", batasan_deskripsi_soal)
    entry_deskripsi_soal.pack(fill="x", pady=5)

    # Input Pilihan Jawaban
    label_pilih = tk.Label(right_panel, text="Pilihan jawaban (tandai yang benar)", font=("Helvetica", 10, "bold"), fg="#4E220F", bg="#F4EFE6")
    label_pilih.pack(anchor="w", pady=(15, 5))

    # Opsi A
    frame_a = tk.Frame(right_panel, bg="#F4EFE6")
    frame_a.pack(fill="x", pady=2)
    tk.Radiobutton(frame_a, bg="#F4EFE6", variable=jawaban_benar_var, value=0, command=lambda: pilih_jawaban(0)).pack(side="left")
    entry_a = tk.Entry(frame_a, font=("Helvetica", 10), textvariable=jawaban_a_var)
    entry_a.pack(side="left", fill="x", expand=True, ipady=3)
    opsi_entry_list.append(entry_a)

    # Opsi B (Terpilih)
    frame_b = tk.Frame(right_panel, bg="#F4EFE6")
    frame_b.pack(fill="x", pady=2)
    tk.Radiobutton(frame_b, bg="#F4EFE6", variable=jawaban_benar_var, value=1, command=lambda: pilih_jawaban(1)).pack(side="left")
    entry_b = tk.Entry(frame_b, font=("Helvetica", 10), textvariable=jawaban_b_var)
    entry_b.pack(side="left", fill="x", expand=True, ipady=3)
    opsi_entry_list.append(entry_b)

    # Opsi C
    frame_c = tk.Frame(right_panel, bg="#F4EFE6")
    frame_c.pack(fill="x", pady=2)
    tk.Radiobutton(frame_c, bg="#F4EFE6", variable=jawaban_benar_var, value=2, command=lambda: pilih_jawaban(2)).pack(side="left")
    entry_c = tk.Entry(frame_c, font=("Helvetica", 10), textvariable=jawaban_c_var)
    entry_c.pack(side="left", fill="x", expand=True, ipady=3)
    opsi_entry_list.append(entry_c)

    # Opsi D
    frame_d = tk.Frame(right_panel, bg="#F4EFE6")
    frame_d.pack(fill="x", pady=2)
    tk.Radiobutton(frame_d, bg="#F4EFE6", variable=jawaban_benar_var, value=3, command=lambda: pilih_jawaban(3)).pack(side="left")
    entry_d = tk.Entry(frame_d, font=("Helvetica", 10), textvariable=jawaban_d_var)
    entry_d.pack(side="left", fill="x", expand=True, ipady=3)
    opsi_entry_list.append(entry_d)

    # Penjelasan
    entry_jelas = tk.Entry(right_panel, font=("Helvetica", 10), textvariable=penjelasan_var)
    entry_jelas.insert(0, "Tuliskan penjelasan anda di sini..")
    entry_jelas.pack(fill="x", pady=(15, 5), ipady=5)

    
    # Tombol Navigasi Bawah
    bottom_frame = tk.Frame(ROOT, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

    btn_kembali = tk.Button(bottom_frame, text="Kembali", bg="white", fg="#4E220F", font=("Helvetica", 10, "bold"), width=15, relief="solid", bd=1, 
                            command=lambda: {
                                bersihkan_layar(ROOT), 
                                halaman_buat_kepala_quiz(ROOT)
                            })
    btn_kembali.pack(side="left", ipady=5)

    def simpan_semua_quiz():
        # Simpan informasi soal saat ini
        if not simpan_input_soal():
            
            return # tidak berubah jika tidak tersimpan
        
        # Simpan seluruh quiz melalui logika.py 
        if not logika.simpan_quiz():
            messagebox.showerror("Penyimpanan Error", "Quiz tidak tersimpan!")
        
        # Continue with your quiz-saving process
        bersihkan_layar(ROOT)
        halaman_homescreen(ROOT)
    
    btn_simpan = tk.Button(bottom_frame, text="Simpan Quiz", bg="#4E220F", fg="white", font=("Helvetica", 10, "bold"), width=15,
                           command=lambda: simpan_semua_quiz())
    btn_simpan.pack(side="right", ipady=5)
    
    pilih_soal(0)

def halaman_tinjau_jawaban(ROOT, data_tinjauan=None):
    # Membersihkan layar dari widget sebelumnya
    for widget in ROOT.winfo_children():
        widget.destroy()

    ROOT.configure(bg="#F4EFE6")

    # Bilah Atas
    top_bar = tk.Frame(ROOT, bg="#A0B084", height=25)
    top_bar.pack(fill="x")
    
    label_top = tk.Label(top_bar, text="QuizPy | Tinjauan Jawaban", bg="#A0B084", fg="#4E220F", font=("Helvetica", 9, "bold"))
    label_top.pack(side="left", padx=10, pady=2)

    # Header Judul
    header_frame = tk.Frame(ROOT, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=40, pady=(20, 10))

    judul = tk.Label(header_frame, text="Tinjauan Jawaban", font=("Helvetica", 24, "bold"), fg="#4E220F", bg="#F4EFE6")
    judul.pack(side="left")

    # Data Dummy jika tidak ada data yang dilemparkan dari fungsi sebelumnya
    if data_tinjauan is None:
        data_tinjauan = [
            {
                "pertanyaan": "Apa output dari print(type([]))?",
                "jawaban_pemain": "List",
                "jawaban_benar": "<class 'list'>",
                "status": "Salah",
                "penjelasan": "List ditulis dengan kurung siku."
            },
            {
                "pertanyaan": "Tipe data untuk teks adalah?",
                "jawaban_pemain": "String",
                "jawaban_benar": "String",
                "status": "Benar",
                "penjelasan": "String digunakan untuk teks."
            }
        ]

    # --- AREA SCROLL UNTUK DAFTAR TINJAUAN ---
    scroll_container = tk.Frame(ROOT, bg="#F4EFE6")
    scroll_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

    canvas = tk.Canvas(scroll_container, bg="#F4EFE6", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(scroll_container, orient="vertical", command=canvas.yview)
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    list_frame = tk.Frame(canvas, bg="#F4EFE6")
    canvas_window = canvas.create_window((0, 0), window=list_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=event.width)
        
    canvas.bind("<Configure>", on_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def unbind_scroll(event):
        canvas.unbind_all("<MouseWheel>")
    list_frame.bind("<Destroy>", unbind_scroll)

    # --- MEMUAT KOTAK TINJAUAN UNTUK SETIAP SOAL ---
    for i, item in enumerate(data_tinjauan, start=1):
        # Frame untuk setiap soal
        soal_frame = tk.Frame(list_frame, bg="white", relief="solid", bd=1)
        soal_frame.pack(fill="x", pady=10, ipady=10, padx=5)

        # Pertanyaan
        lbl_tanya = tk.Label(soal_frame, text=f"Soal {i}: {item['pertanyaan']}", font=("Helvetica", 11, "bold"), fg="#4E220F", bg="white", anchor="w")
        lbl_tanya.pack(fill="x", padx=15, pady=(5, 10))

        # Menentukan warna teks berdasarkan status benar/salah
        warna_status = "#A0B084" if item["status"] == "Benar" else "#A06A42"

        # Menampilkan jawaban pemain
        lbl_jwbn_pemain = tk.Label(soal_frame, text=f"Jawaban Anda: {item['jawaban_pemain']} ({item['status']})", font=("Helvetica", 10), fg=warna_status, bg="white", anchor="w")
        lbl_jwbn_pemain.pack(fill="x", padx=15, pady=2)

        # Jika salah, tampilkan jawaban yang benar
        if item["status"] == "Salah":
            lbl_jwbn_benar = tk.Label(soal_frame, text=f"Jawaban Benar: {item['jawaban_benar']}", font=("Helvetica", 10, "bold"), fg="#4E220F", bg="white", anchor="w")
            lbl_jwbn_benar.pack(fill="x", padx=15, pady=2)
        else: # Jika benar, tampilkan penambahan poin dari pertanyaan (Placeholder)
            lbl_penambahan_poin = tk.Label(soal_frame, text= "+Placeholder points", font=("Helvetica", 10, "bold"),fg="#F4EFE6", bg="#4E220F")

        # Penjelasan tambahan
        if item.get("penjelasan"):
            lbl_jelas = tk.Label(soal_frame, text=f"Penjelasan: {item['penjelasan']}", font=("Helvetica", 9, "italic"), fg="#4E220F", bg="white", anchor="w")
            lbl_jelas.pack(fill="x", padx=15, pady=(5, 5))
            
    # Total poin pemain (Placeholder)

    totalpoin = tk.Label(header_frame, text=f"Total: {logika.Skor}/{logika.Perfect_Skor}",font=("Helvetica", 15, "bold"), fg="#F4EFE6", bg="#4E220F" )
    totalpoin.place(relx= 1.0, y=23, anchor="e")
    
    # --- TOMBOL NAVIGASI BAWAH ---
    bottom_frame = tk.Frame(ROOT, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=40, pady=20)

    # Tombol Kembali ke Hasil Kuis (Bisa disesuaikan command-nya untuk memanggil halaman_hasil_quiz)
    btn_kembali = tk.Button(bottom_frame, text="Kembali ke Hasil", bg="white", fg="#4E220F", font=("Helvetica", 10, "bold"), width=20, relief="solid", bd=1)
    btn_kembali.pack(side="left", ipady=5)
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Aplikasi quiz Interaktif")
    root.geometry("800x600")
    halaman_buat_quiz_soal(root)
    root.mainloop()
