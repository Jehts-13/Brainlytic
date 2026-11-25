import time
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import logika
from data_manager import *

username_var = None

# Variabel pembuatan quiz
judul_var = None
deskripsi = None
jumlah_soal_var = None
batas_waktu_var = None


def reset_username():
    username_var.set("")


def reset_pembuatan_quiz():
    global judul_var, deskripsi, jumlah_soal_var, batas_waktu_var
    judul_var = deskripsi = jumlah_soal_var = batas_waktu_var = None


def bersihkan_layar(ROOT):
    for widget in ROOT.winfo_children():
        widget.destroy()


def halaman_homescreen(ROOT):
    def batasi_input(*args):
        batas_maksimal = 20
        nama = username_var.get()
        if len(nama) > batas_maksimal:
            username_var.set(nama[:batas_maksimal])

    def validasi_sebelum_lanjut():
        global username_var
        nama = username_var.get()
        if not nama.isalnum():
            messagebox.showwarning(
                "Input Tidak Valid",
                "Nama hanya boleh berisi huruf dan angka (tanpa spasi atau simbol)!",
            )
            return

        logika.username = nama
        print(f"Nama pemain disimpan: {logika.username}")

        bersihkan_layar(ROOT)
        halaman_pilih_quiz(ROOT)

    judul = tk.Label(
        ROOT,
        text="Brainlytic",
        font=("Helvetica", 32, "bold"),
        fg="#5C3A21",
        bg="#F4EFE6",
    )
    judul.pack(pady=(40, 5))

    sub_judul = tk.Label(
        ROOT,
        text="Uji pengetahuanmu, satu soal setiap kali",
        font=("Helvetica", 12),
        fg="#5C3A21",
        bg="#F4EFE6",
    )
    sub_judul.pack(pady=(0, 20))

    frame_nama = tk.Frame(ROOT, bg="#F4EFE6")
    frame_nama.pack(pady=10)

    label_judul = tk.Label(
        frame_nama,
        text="Nama pemain",
        font=("Helvetica", 10, "bold"),
        fg="#5C3A21",
        bg="#F4EFE6",
    )
    label_judul.pack(anchor="w")

    global username_var
    if username_var is None:
        username_var = tk.StringVar(value="")
        username_var.trace_add("write", batasi_input)

    input_nama = tk.Entry(
        frame_nama, width=50, font=("Helvetica", 12), textvariable=username_var
    )
    input_nama.pack(ipady=5)

    frame_menu = tk.Frame(ROOT, bg="#F4EFE6")
    frame_menu.pack(pady=30)

    btn_kerjakan = tk.Button(
        frame_menu,
        text="Kerjakan Quiz\n\nPilih dari daftar quiz yang\ntersedia",
        bg="#A06A42",
        fg="white",
        font=("Helvetica", 10, "bold"),
        width=25,
        height=5,
        command=validasi_sebelum_lanjut,
    )
    btn_kerjakan.grid(row=0, column=0, padx=10)

    btn_buat = tk.Button(
        frame_menu,
        text="Buat Quiz Baru\n\nSusun soal dan jawabanmu\nsendiri",
        bg="#A06A42",
        fg="white",
        font=("Helvetica", 10, "bold"),
        width=25,
        height=5,
        command=lambda: [bersihkan_layar(ROOT), halaman_buat_kepala_quiz(ROOT)],
    )
    btn_buat.grid(row=0, column=1, padx=10)

    link_skor = tk.Label(
        ROOT,
        text="Lihat papan skor",
        font=("Helvetica", 10),
        fg="#A06A42",
        bg="#F4EFE6",
        cursor="hand2",
    )
    link_skor.bind("<Button-1>", lambda event: halaman_papan_skor(ROOT=ROOT))
    link_skor.pack(pady=10)

    ROOT.mainloop()


def halaman_pilih_quiz(ROOT):
    ROOT.configure(bg="#F4EFE6")

    top_bar = tk.Frame(ROOT, bg="#A0B084", height=25)
    top_bar.pack(fill="x")

    label_top = tk.Label(
        top_bar,
        text="QuizPy | Kerjakan Quiz",
        bg="#A0B084",
        fg="#4E220F",
        font=("Helvetica", 9, "bold"),
    )
    label_top.pack(side="left", padx=10, pady=2)

    header_frame = tk.Frame(ROOT, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=20, pady=(20, 10))

    judul = tk.Label(
        header_frame,
        text="Pilih Quiz",
        font=("Helvetica", 24, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    judul.pack(side="left")

    cari_entry = tk.Entry(header_frame, font=("Helvetica", 10), width=25)
    cari_entry.insert(0, "Cari quiz...")
    cari_entry.pack(side="right", ipady=5)

    bottom_frame = tk.Frame(ROOT, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=20, pady=20)

    btn_kembali = tk.Button(
        bottom_frame,
        text="Kembali",
        bg="white",
        fg="#4E220F",
        font=("Helvetica", 10, "bold"),
        width=15,
        relief="solid",
        bd=1,
        command=lambda: [bersihkan_layar(ROOT), halaman_homescreen(ROOT)],
    )
    btn_kembali.pack(side="left", ipady=5)

    btn_mulai = tk.Button(
        bottom_frame,
        text="Mulai Quiz",
        bg="#4E220F",
        fg="white",
        font=("Helvetica", 10, "bold"),
        width=15,
        command=lambda: aksi_mulai_kuis(),
    )
    btn_mulai.pack(side="right", ipady=5)

    scroll_container = tk.Frame(ROOT, bg="#F4EFE6")
    scroll_container.pack(fill="both", expand=True, padx=40, pady=(0, 20))

    canvas = tk.Canvas(scroll_container, bg="#F4EFE6", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        scroll_container, orient="vertical", command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    list_frame = tk.Frame(canvas, bg="#F4EFE6")
    canvas_window = canvas.create_window((0, 0), window=list_frame, anchor="nw")

    def on_configure(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", on_configure)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def unbind_scroll(event):
        canvas.unbind_all("<MouseWheel>")

    list_frame.bind("<Destroy>", unbind_scroll)

    kuis_terpilih = tk.StringVar(value="")
    tombol_kuis_dict = {}

    def pilih_kuis(judul_quiz):
        kuis_terpilih.set(judul_quiz)
        for nama, tombol in tombol_kuis_dict.items():
            if nama == judul_quiz:
                tombol.configure(bg="#A06A42", fg="white")
            else:
                tombol.configure(bg="white", fg="#4E220F")

    def buat_item_quiz(parent, judul_quiz, deskripsi):
        teks_tombol = f"{judul_quiz}\n{deskripsi}"
        btn = tk.Button(
            parent,
            text=teks_tombol,
            bg="white",
            fg="#4E220F",
            font=("Helvetica", 9),
            justify="left",
            anchor="w",
            relief="solid",
            bd=1,
        )
        tombol_kuis_dict[judul_quiz] = btn
        btn.configure(command=lambda q=judul_quiz: pilih_kuis(q))
        btn.pack(fill="x", pady=5, ipady=8, padx=2)
        return btn

    def aksi_mulai_kuis():
        judul = kuis_terpilih.get()
        if not judul:
            messagebox.showwarning(
                "Peringatan", "Silakan pilih salah satu kuis terlebih dahulu!"
            )
            return

        print(f"Kuis yang akan dimainkan: {judul}")
        logika.muat_soal_quiz(judul)
        time.sleep(0.5)
        bersihkan_layar(ROOT)
        halaman_soal_quiz(ROOT)

    daftar_quiz = load_daftar_quiz()

    if not daftar_quiz:
        print("Belum ada kuis yang tersedia.")
        tk.Label(
            list_frame,
            text="Belum ada kuis yang tersedia.",
            bg="#F4EFE6",
            fg="#4E220F",
        ).pack(pady=20)
    else:
        for quiz in daftar_quiz:
            buat_item_quiz(list_frame, quiz["judul"], quiz["deskripsi"])


def halaman_soal_quiz(ROOT):
    jawaban = tk.StringVar(value="")
    jumlah_soal = logika.Jumlah_soal
    batas_waktu = logika.Total_waktu
    sisa_waktu = batas_waktu
    nomor_soal = logika.Nomor_soal
    print(f"batas waktu:\t{batas_waktu}")

    ROOT.configure(bg="#F4EFE6")

    header_frame = tk.Frame(ROOT, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=20, pady=(15, 5))

    def text_indikator_soal():
        nonlocal nomor_soal, jumlah_soal
        return f"Soal {nomor_soal + 1} dari {jumlah_soal}"

    label_soal = tk.Label(
        header_frame,
        text=text_indikator_soal(),
        font=("Helvetica", 10, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    label_soal.pack(side="left")

    label_waktu = tk.Label(
        header_frame,
        text=f"Waktu: {logika.format_waktu(sisa_waktu)}",
        font=("Helvetica", 10, "bold"),
        fg="white",
        bg="#A06A42",
        width=12,
        pady=3,
    )
    label_waktu.pack(side="right")

    timer_id = None

    def update_timer():
        nonlocal sisa_waktu, timer_id
        if not label_waktu.winfo_exists():
            return

        if sisa_waktu > 0:
            sisa_waktu -= 1
            text_waktu = logika.format_waktu(sisa_waktu)
            label_waktu.configure(text=f"Waktu: {text_waktu}")
            timer_id = ROOT.after(1000, update_timer)
        else:
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

    progress_bg = tk.Frame(ROOT, bg="#A0B084", height=10)
    progress_bg.pack(fill="x", padx=20, pady=(0, 15))

    panjang_progres = logika.ambil_rasio_progressbar()

    progress_fill = tk.Frame(progress_bg, bg="#4E220F", height=10)
    progress_fill.pack(side="left")
    progress_fill.place(x=0, y=0, relheight=1.0, relwidth=0.0)
    progress_bg.pack_propagate(False)

    def update_progressbar():
        label_soal.configure(text=text_indikator_soal())
        progress_fill.place(x=0, y=0, relheight=1.0, relwidth=panjang_progres)

    update_progressbar()

    pertanyaan_frame = tk.Frame(
        ROOT, bg="white", highlightbackground="#A0B084", highlightthickness=2
    )
    pertanyaan_frame.pack(fill="x", padx=20, pady=10)

    pertanyaan = logika.Soal[nomor_soal]["deskripsi"]
    teks_pertanyaan_frame = tk.Label(
        pertanyaan_frame,
        text=pertanyaan,
        font=("Helvetica", 14, "bold"),
        fg="#4E220F",
        bg="white",
        wraplength=500,
    )
    teks_pertanyaan_frame.pack(pady=20)

    opsi_frame = tk.Frame(ROOT, bg="#F4EFE6")
    opsi_frame.pack(fill="x", padx=20, pady=5)
    opsi_frame.columnconfigure(0, weight=1)
    opsi_frame.columnconfigure(1, weight=1)

    teks_pilihan = logika.Soal[nomor_soal]["pilihan"]
    tombol_pilihan_dict = {}

    def pilih_opsi(jawabanIndex):
        jawaban.set(jawabanIndex)
        for index, btn in tombol_pilihan_dict.items():
            if index == jawabanIndex:
                btn.configure(bg="#A06A42", fg="white")
                print(f"\n@@ Pilihan ke-{index + 1} terpilih!")
            else:
                btn.configure(bg="white", fg="#4E220F")

    def reset_opsi():
        for btn in tombol_pilihan_dict.values():
            btn.configure(bg="white", fg="#4E220F")
        jawaban.set(value="")

    def buat_item_opsi(parent, nomor_index, baris, kolom):
        nonlocal teks_pilihan
        btn = tk.Button(
            parent,
            text=teks_pilihan[nomor_index],
            bg="white",
            fg="#4E220F",
            font=("Helvetica", 10),
            relief="solid",
            bd=1,
            wraplength=200,
        )
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

    btn_keluar = tk.Button(
        bottom_frame,
        text="Keluar",
        bg="white",
        fg="#4E220F",
        font=("Helvetica", 10),
        relief="solid",
        bd=1,
        width=12,
        command=keluar_quiz,
    )
    btn_keluar.pack(side="left", ipady=5)

    label_reset = tk.Button(
        bottom_frame,
        text="Reset Jawaban",
        font=("Helvetica", 10),
        fg="#4E220F",
        bg="#F4EFE6",
        relief="sunken",
        bd=1,
        width=16,
        command=reset_opsi,
    )
    label_reset.pack(side="left", expand=True)

    def load_berikutnya():
        try:
            nonlocal nomor_soal
            logika.simpan_jawaban_soal(jawaban.get() if jawaban.get() != "" else None)

            if jumlah_soal == nomor_soal + 1:
                logika.hitung_skor(sisa_waktu)
                time.sleep(0.5)
                halaman_hasil_quiz(ROOT)
                return

            reset_opsi()
            print(f"Jawaban {nomor_soal} disimpan, nomor_soal bertambah 1")
            nomor_soal += 1

            nonlocal panjang_progres, pertanyaan, teks_pilihan
            panjang_progres = logika.ambil_rasio_progressbar()
            update_progressbar()
            pertanyaan = logika.Soal[nomor_soal]["deskripsi"]
            teks_pertanyaan_frame.configure(text=pertanyaan)
            teks_pilihan = logika.Soal[nomor_soal]["pilihan"]
            update_pilihan()

        except IndexError:
            print(f"{nomor_soal} index is not in the list!")

    btn_berikutnya = tk.Button(
        bottom_frame,
        text="Berikutnya",
        bg="#4E220F",
        fg="white",
        font=("Helvetica", 10, "bold"),
        width=12,
        command=load_berikutnya,
    )
    btn_berikutnya.pack(side="right", ipady=5)


def halaman_hasil_quiz(ROOT):
    jumlah_benar = logika.Jumlah_benar
    jumlah_salah = logika.Jumlah_salah
    skor = logika.Skor
    waktu = logika.Waktu_digunakan
    print(
        f"Jumlah Benar: {jumlah_benar:<5}\nJumlah Salah: {jumlah_salah:<5}\nSkor: {skor:<5}Waktu: {waktu:<5}"
    )

    bersihkan_layar(ROOT)
    ROOT.configure(bg="#F4EFE6")

    main_frame = tk.Frame(ROOT, bg="#F4EFE6")
    main_frame.pack(expand=True)

    judul = tk.Label(
        main_frame,
        text=f"quiz selesai, {username_var.get()}!",
        font=("Helvetica", 24, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    judul.pack(pady=(0, 20))

    canvas = tk.Canvas(
        main_frame, width=160, height=160, bg="#F4EFE6", highlightthickness=0
    )
    canvas.pack(pady=10)
    canvas.create_oval(10, 10, 150, 150, fill="#A06A42", outline="#A06A42")
    canvas.create_text(
        80, 80, text=f"{skor}/100", font=("Helvetica", 24, "bold"), fill="white"
    )

    stats_frame = tk.Frame(main_frame, bg="#F4EFE6")
    stats_frame.pack(pady=20)

    box_benar = tk.Label(
        stats_frame,
        text=f"Benar: {jumlah_benar}",
        font=("Helvetica", 11, "bold"),
        bg="#A0B084",
        fg="#4E220F",
        width=15,
        height=2,
    )
    box_benar.grid(row=0, column=0, padx=10)

    box_salah = tk.Label(
        stats_frame,
        text=f"Salah: {jumlah_salah}",
        font=("Helvetica", 11, "bold"),
        bg="white",
        fg="#A06A42",
        width=15,
        height=2,
        relief="solid",
        bd=1,
    )
    box_salah.grid(row=0, column=1, padx=10)

    box_waktu = tk.Label(
        stats_frame,
        text=f"Waktu: {logika.format_waktu(waktu)}",
        font=("Helvetica", 11, "bold"),
        bg="white",
        fg="#4E220F",
        width=15,
        height=2,
        relief="solid",
        bd=1,
    )
    box_waktu.grid(row=0, column=2, padx=10)

    btn_frame = tk.Frame(main_frame, bg="#F4EFE6")
    btn_frame.pack(pady=20)

    btn_papan = tk.Button(
        btn_frame,
        text="Papan Skor",
        bg="white",
        fg="#4E220F",
        font=("Helvetica", 10),
        width=15,
        relief="solid",
        bd=1,
        command=lambda: halaman_papan_skor(ROOT),
    )
    btn_papan.grid(row=0, column=1, padx=10, ipady=5)

    btn_main = tk.Button(
        btn_frame,
        text="Main Lagi",
        bg="#4E220F",
        fg="white",
        font=("Helvetica", 10, "bold"),
        width=15,
        command=lambda: [
            bersihkan_layar(ROOT),
            logika.reset_data(),
            halaman_homescreen(ROOT),
        ],
    )
    btn_main.grid(row=0, column=2, padx=10, ipady=5)


def halaman_papan_skor(ROOT):
    for widget in ROOT.winfo_children():
        widget.destroy()

    ROOT.configure(bg="#F4EFE6")

    top_bar = tk.Frame(ROOT, bg="#A0B084", height=25)
    top_bar.pack(fill="x")

    label_top = tk.Label(
        top_bar,
        text="QuizPy | Papan Skor",
        bg="#A0B084",
        fg="#4E220F",
        font=("Helvetica", 9, "bold"),
    )
    label_top.pack(side="left", padx=10, pady=2)

    main_frame = tk.Frame(ROOT, bg="#F4EFE6")
    main_frame.pack(expand=True, fill="both", padx=40, pady=20)

    header_frame = tk.Frame(main_frame, bg="#F4EFE6")
    header_frame.pack(fill="x", pady=(10, 20))

    judul = tk.Label(
        header_frame,
        text="10 Skor Tertinggi",
        font=("Helvetica", 24, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    judul.pack(side="left")

    btn_filter = tk.Button(
        header_frame,
        text="Semua kategori",
        bg="white",
        fg="#4E220F",
        font=("Helvetica", 10),
        relief="solid",
        bd=1,
        padx=15,
    )
    btn_filter.pack(side="right", ipady=2)

    table_container = tk.Frame(main_frame, bg="#F4EFE6")
    table_container.pack(fill="both", expand=True)

    table_canvas = tk.Canvas(table_container, bg="#F4EFE6", highlightthickness=0)
    table_canvas.pack(side="left", fill="both", expand=True)

    scrollbar = tk.Scrollbar(
        table_container, orient="vertical", command=table_canvas.yview
    )
    scrollbar.pack(side="right", fill="y")
    table_canvas.configure(yscrollcommand=scrollbar.set)

    tabel_frame = tk.Frame(table_canvas, bg="#F4EFE6")
    canvas_window = table_canvas.create_window((0, 0), window=tabel_frame, anchor="nw")

    def update_scroll_region(event):
        table_canvas.configure(scrollregion=table_canvas.bbox("all"))

    tabel_frame.bind("<Configure>", update_scroll_region)

    def update_canvas_width(event):
        table_canvas.itemconfig(canvas_window, width=event.width)

    table_canvas.bind("<Configure>", update_canvas_width)

    def on_mousewheel(event):
        table_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    table_canvas.bind_all("<MouseWheel>", on_mousewheel)
    table_canvas.bind_all(
        "<Button-4>", lambda event: table_canvas.yview_scroll(-1, "units")
    )
    table_canvas.bind_all(
        "<Button-5>", lambda event: table_canvas.yview_scroll(1, "units")
    )

    header_bg = "#4E220F"
    header_fg = "white"
    row_header = tk.Frame(tabel_frame, bg=header_bg)
    row_header.pack(fill="x", pady=(0, 10), ipady=5)

    tk.Label(
        row_header,
        text="#",
        bg=header_bg,
        fg=header_fg,
        font=("Helvetica", 10, "bold"),
        width=5,
        anchor="w",
    ).pack(side="left", padx=(15, 0))
    tk.Label(
        row_header,
        text="Nama",
        bg=header_bg,
        fg=header_fg,
        font=("Helvetica", 10, "bold"),
        width=25,
        anchor="w",
    ).pack(side="left")
    tk.Label(
        row_header,
        text="Kategori",
        bg=header_bg,
        fg=header_fg,
        font=("Helvetica", 10, "bold"),
        width=20,
        anchor="w",
    ).pack(side="left")
    tk.Label(
        row_header,
        text="Skor",
        bg=header_bg,
        fg=header_fg,
        font=("Helvetica", 10, "bold"),
        width=10,
        anchor="e",
    ).pack(side="left")

    data_peringkat_raw = load_user_history()
    data_peringkat = logika.sort_user_history(data_peringkat_raw)[:10]

    for rank, data in enumerate(data_peringkat):
        row_frame = tk.Frame(tabel_frame, bg="white", relief="solid", bd=1)
        row_frame.pack(fill="x", pady=4, ipady=5)

        tk.Label(
            row_frame,
            text=rank + 1,
            bg="white",
            fg="#4E220F",
            font=("Helvetica", 10),
            width=5,
            anchor="w",
        ).pack(side="left", padx=(15, 0))
        tk.Label(
            row_frame,
            text=data["username"],
            bg="white",
            fg="#4E220F",
            font=("Helvetica", 10),
            width=25,
            anchor="w",
        ).pack(side="left")
        tk.Label(
            row_frame,
            text=data["judul_quiz"],
            bg="white",
            fg="#4E220F",
            font=("Helvetica", 10),
            width=20,
            anchor="w",
        ).pack(side="left")
        tk.Label(
            row_frame,
            text=data["skor"],
            bg="white",
            fg="#4E220F",
            font=("Helvetica", 10),
            width=10,
            anchor="e",
        ).pack(side="left")

    spacer = tk.Frame(main_frame, bg="#F4EFE6", height=5)
    spacer.pack(fill="x")

    bottom_frame = tk.Frame(main_frame, bg="#F4EFE6")
    bottom_frame.pack(fill="x", pady=(20, 10))

    btn_kembali = tk.Button(
        bottom_frame,
        text="Kembali",
        bg="white",
        fg="#4E220F",
        font=("Helvetica", 10),
        width=15,
        relief="solid",
        bd=1,
        command=lambda: [
            logika.reset_data(),
            bersihkan_layar(ROOT),
            halaman_homescreen(ROOT),
        ],
    )
    btn_kembali.pack(side="left", ipady=5)


def halaman_buat_kepala_quiz(ROOT):
    global judul_var, deskripsi, jumlah_soal_var, batas_waktu_var
    if judul_var is None:
        judul_var = tk.StringVar(value="")
    if jumlah_soal_var is None:
        jumlah_soal_var = tk.StringVar(value="")
    if batas_waktu_var is None:
        batas_waktu_var = tk.StringVar(value="")
    if deskripsi is None:
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
            jumlah_soal_var.set(jumlah[: len(jumlah) - 1])
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
            batas_waktu_var.set(waktu[: len(waktu) - 1])
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

        if len(judul) == 0:
            messagebox.showwarning(
                "Judul belum ada", "Mohon isi terlebih dahulu Judul Quiz ini!"
            )
            return False
        if len(deskripsi) == 0:
            messagebox.showwarning(
                "Deskripsi belum ada", "Mohon isi terlebih dahulu Deskripsi Quiz ini!"
            )
            return False
        if len(jumlah) == 0:
            messagebox.showwarning(
                "Jumlah soal belum ada", "Mohon isi terlebih dahulu Jumlah Soal!"
            )
            return False
        if len(waktu) == 0:
            messagebox.showwarning(
                "Batas Waktu belum ada", "Mohon isi terlebih dahulu Batas Waktu Quiz!"
            )
            return False

        daftar_quiz = load_daftar_quiz()
        for quiz in daftar_quiz:
            if judul == quiz["judul"]:
                messagebox.showwarning(
                    "Judul duplikat!",
                    "Judul telah terdaftar dalam list Quiz aplikasi! Mohon masukkan Judul Quiz yang berbeda",
                )
                return False
        return True

    def lanjut_pembuatan_soal():
        if not validasi_kepala_quiz():
            return

        logika.simpan_kepala_quiz(
            judul_var.get(),
            entry_deskripsi.get("1.0", "end-1c"),
            jumlah_soal_var.get(),
            batas_waktu_var.get(),
        )
        bersihkan_layar(ROOT)
        halaman_buat_quiz_soal(ROOT)

    ROOT.configure(bg="#F4EFE6")

    top_bar = tk.Frame(ROOT, bg="#A0B084", height=25)
    top_bar.pack(fill="x")

    label_top = tk.Label(
        top_bar,
        text="QuizPy | Buat Quiz Baru (Langkah 1 dari 2)",
        bg="#A0B084",
        fg="#4E220F",
        font=("Helvetica", 9, "bold"),
    )
    label_top.pack(side="left", padx=10, pady=2)

    header_frame = tk.Frame(ROOT, bg="#F4EFE6")
    header_frame.pack(fill="x", padx=40, pady=(20, 10))

    label_judul = tk.Label(
        header_frame,
        text="Informasi Quiz",
        font=("Helvetica", 24, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    label_judul.pack(side="left")

    form_frame = tk.Frame(ROOT, bg="#F4EFE6")
    form_frame.pack(fill="both", expand=True, padx=40)

    label_judul = tk.Label(
        form_frame,
        text="Judul quiz",
        font=("Helvetica", 14, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    label_judul.grid(row=0, column=0, sticky="w", pady=(10, 5))

    judul_var.trace_add("write", batasan_judul)
    entry_judul = tk.Entry(
        form_frame, font=("Helvetica", 14), width=60, textvariable=judul_var
    )
    entry_judul.grid(row=1, column=0, columnspan=2, sticky="we", ipady=5)

    label_deskripsi = tk.Label(
        form_frame,
        text="Deskripsi",
        font=("Helvetica", 14, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    label_deskripsi.grid(row=2, column=0, sticky="w", pady=(15, 5))

    label_deskripsi_cnt = tk.Label(
        form_frame,
        text=f"{len(deskripsi)}/55 karakter",
        font=("Helvetica", 10, "bold"),
        fg="#A06A42",
        bg="#F4EFE6",
    )
    label_deskripsi_cnt.grid(row=2, column=1, sticky="e", pady=(15, 5))

    entry_deskripsi = tk.Text(form_frame, font=("Helvetica", 14), height=4, width=60)
    entry_deskripsi.bind("<KeyRelease>", batasan_deskripsi)
    entry_deskripsi.insert("1.0", deskripsi)
    entry_deskripsi.grid(row=3, column=0, columnspan=2, sticky="we", pady=5)

    label_jumlah_soal = tk.Label(
        form_frame,
        text="Jumlah soal (maks. 25)",
        font=("Helvetica", 14, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    label_jumlah_soal.grid(row=4, column=0, sticky="w", pady=(15, 5))

    jumlah_soal_var.trace_add("write", batasan_soal)
    entry_jumlah_soal = tk.Entry(
        form_frame, font=("Helvetica", 14), textvariable=jumlah_soal_var
    )
    entry_jumlah_soal.grid(row=5, column=0, sticky="we", padx=(0, 10), ipady=5)

    label_waktu = tk.Label(
        form_frame,
        text="Batas waktu (menit)",
        font=("Helvetica", 14, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    label_waktu.grid(row=4, column=1, sticky="w", pady=(15, 5))

    batas_waktu_var.trace_add("write", batasan_waktu)
    entry_waktu = tk.Entry(
        form_frame, font=("Helvetica", 14), textvariable=batas_waktu_var
    )
    entry_waktu.grid(row=5, column=1, sticky="we", ipady=5)

    form_frame.columnconfigure(0, weight=1)
    form_frame.columnconfigure(1, weight=1)

    bottom_frame = tk.Frame(ROOT, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=40, pady=20)

    btn_batal = tk.Button(
        bottom_frame,
        text="Batal",
        bg="white",
        fg="#4E220F",
        font=("Helvetica", 10, "bold"),
        width=15,
        relief="solid",
        bd=1,
        command=lambda: [
            reset_pembuatan_quiz(),
            logika.reset_data(),
            bersihkan_layar(ROOT),
            halaman_homescreen(ROOT),
        ],
    )
    btn_batal.pack(side="left", ipady=5)

    btn_lanjut = tk.Button(
        bottom_frame,
        text="Lanjut: Tambah Soal",
        bg="#4E220F",
        fg="white",
        font=("Helvetica", 10, "bold"),
        width=20,
        command=lanjut_pembuatan_soal,
    )
    btn_lanjut.pack(side="right", ipady=5)


def halaman_buat_quiz_soal(ROOT):
    ROOT.configure(bg="#F4EFE6")
    nomor_pertanyaan_var = tk.IntVar(value=0)
    deskripsi_soal = ""
    jawaban_a_var = tk.StringVar(value="")
    jawaban_b_var = tk.StringVar(value="")
    jawaban_c_var = tk.StringVar(value="")
    jawaban_d_var = tk.StringVar(value="")
    jawaban_benar_var = tk.IntVar(value=0)
    penjelasan_var = tk.StringVar(value="")

    def batasan_deskripsi_soal(*args):
        nonlocal deskripsi_soal
        teks = entry_deskripsi_soal.get("1.0", "end-1c")
        if len(teks) > 90:
            teks = teks[:90]
            entry_deskripsi_soal.delete("1.0", "end")
            entry_deskripsi_soal.insert("1.0", teks)
        deskripsi_soal = teks

    top_bar = tk.Frame(ROOT, bg="#A0B084", height=25)
    top_bar.pack(fill="x")

    label_top = tk.Label(
        top_bar,
        text="QuizPy | Buat Quiz Baru (Langkah 2 dari 2)",
        bg="#A0B084",
        fg="#4E220F",
        font=("Helvetica", 9, "bold"),
    )
    label_top.pack(side="left", padx=10, pady=2)

    main_frame = tk.Frame(ROOT, bg="#F4EFE6")
    main_frame.pack(fill="both", expand=True, padx=20, pady=10)

    left_panel = tk.Frame(main_frame, bg="#A0B084", width=150)
    left_panel.pack(side="left", fill="y", padx=(0, 15))
    left_panel.pack_propagate(False)

    label_daftar = tk.Label(
        left_panel,
        text=f"Daftar soal ({jumlah_soal_var.get()})",
        font=("Helvetica", 9, "bold"),
        bg="#A0B084",
        fg="#4E220F",
    )
    label_daftar.pack(pady=(15, 10))

    scroll_container = tk.Frame(left_panel, bg="#A0B084")
    scroll_container.pack(fill="both", expand=True, padx=5, pady=5)

    canvas = tk.Canvas(scroll_container, bg="#A0B084", highlightthickness=0)
    canvas.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(
        scroll_container, orient="vertical", command=canvas.yview
    )
    scrollbar.pack(side="right", fill="y")
    canvas.configure(yscrollcommand=scrollbar.set)

    list_frame = tk.Frame(canvas, bg="#A0B084")
    canvas_window = canvas.create_window((0, 0), window=list_frame, anchor="nw")

    def update_scroll(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    list_frame.bind("<Configure>", update_scroll)

    def resize_canvas(event):
        canvas.itemconfig(canvas_window, width=event.width)

    canvas.bind("<Configure>", resize_canvas)

    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    canvas.bind_all("<MouseWheel>", _on_mousewheel)

    def unbind_scroll(event):
        canvas.unbind_all("<MouseWheel>")

    list_frame.bind("<Destroy>", unbind_scroll)

    tombol_soal_list = {}

    def simpan_input_soal():
        nonlocal deskripsi_soal
        deskripsi_soal = entry_deskripsi_soal.get("1.0", "end-1c")
        jawaban_a = jawaban_a_var.get()
        jawaban_b = jawaban_b_var.get()
        jawaban_c = jawaban_c_var.get()
        jawaban_d = jawaban_d_var.get()
        jawaban_benar = jawaban_benar_var.get()
        penjelasan = penjelasan_var.get()

        return logika.simpan_soal(
            logika.Nomor_soal,
            deskripsi_soal,
            jawaban_a,
            jawaban_b,
            jawaban_c,
            jawaban_d,
            jawaban_benar,
            penjelasan,
        )

    def muat_input_soal(indeks):
        nonlocal deskripsi_soal
        data = logika.ambil_soal(indeks)
        (
            deskripsi_soal,
            jawaban_a,
            jawaban_b,
            jawaban_c,
            jawaban_d,
            jawaban_benar,
            penjelasan,
        ) = data

        entry_deskripsi_soal.delete("1.0", "end")
        entry_deskripsi_soal.insert("1.0", deskripsi_soal)

        jawaban_a_var.set(jawaban_a)
        jawaban_b_var.set(jawaban_b)
        jawaban_c_var.set(jawaban_c)
        jawaban_d_var.set(jawaban_d)
        jawaban_benar_var.set(jawaban_benar)
        penjelasan_var.set(penjelasan)

        pilih_jawaban(jawaban_benar)

    def pilih_soal(indeks, simpan_sebelumnya=True):
        if simpan_sebelumnya:
            if not simpan_input_soal():
                print("Gagal menyimpan soal sebelumnya!")
                return

        logika.Nomor_soal = indeks
        nomor_pertanyaan_var.set(indeks)
        muat_input_soal(indeks)

        for i, tombol in tombol_soal_list.items():
            if i == indeks:
                tombol.configure(bg="#A06A42", fg="white")
            else:
                tombol.configure(bg="white", fg="#4E220F")

    def buat_item_soal(parent, indeks):
        btn = tk.Button(
            parent,
            text=f"Soal {indeks + 1}",
            bg="white",
            fg="#4E220F",
            relief="flat",
            anchor="w",
            padx=10,
        )
        tombol_soal_list[indeks] = btn
        btn.configure(command=lambda q=indeks: pilih_soal(q))
        btn.pack(fill="x", padx=10, pady=5, ipady=3)
        return btn

    opsi_entry_list = []

    def pilih_jawaban(val):
        print(f"kunci jawaban: {val}")
        for i, entry in enumerate(opsi_entry_list):
            if i == val:
                entry.configure(bg="#A0B084")
            else:
                entry.configure(bg="white")

    for i in range(logika.Jumlah_soal):
        buat_item_soal(list_frame, i)

    right_panel = tk.Frame(main_frame, bg="#F4EFE6")
    right_panel.pack(side="left", fill="both", expand=True)

    label_tanya = tk.Label(
        right_panel,
        text="Pertanyaan",
        font=("Helvetica", 10, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    label_tanya.pack(anchor="w", pady=(10, 5))

    entry_deskripsi_soal = tk.Text(right_panel, font=("Helvetica", 10), height=3)
    entry_deskripsi_soal.bind("<KeyRelease>", batasan_deskripsi_soal)
    entry_deskripsi_soal.pack(fill="x", pady=5)

    label_pilih = tk.Label(
        right_panel,
        text="Pilihan jawaban (tandai yang benar)",
        font=("Helvetica", 10, "bold"),
        fg="#4E220F",
        bg="#F4EFE6",
    )
    label_pilih.pack(anchor="w", pady=(15, 5))

    frame_a = tk.Frame(right_panel, bg="#F4EFE6")
    frame_a.pack(fill="x", pady=2)
    tk.Radiobutton(
        frame_a,
        bg="#F4EFE6",
        variable=jawaban_benar_var,
        value=0,
        command=lambda: pilih_jawaban(0),
    ).pack(side="left")
    entry_a = tk.Entry(frame_a, font=("Helvetica", 10), textvariable=jawaban_a_var)
    entry_a.pack(side="left", fill="x", expand=True, ipady=3)
    opsi_entry_list.append(entry_a)

    frame_b = tk.Frame(right_panel, bg="#F4EFE6")
    frame_b.pack(fill="x", pady=2)
    tk.Radiobutton(
        frame_b,
        bg="#F4EFE6",
        variable=jawaban_benar_var,
        value=1,
        command=lambda: pilih_jawaban(1),
    ).pack(side="left")
    entry_b = tk.Entry(frame_b, font=("Helvetica", 10), textvariable=jawaban_b_var)
    entry_b.pack(side="left", fill="x", expand=True, ipady=3)
    opsi_entry_list.append(entry_b)

    frame_c = tk.Frame(right_panel, bg="#F4EFE6")
    frame_c.pack(fill="x", pady=2)
    tk.Radiobutton(
        frame_c,
        bg="#F4EFE6",
        variable=jawaban_benar_var,
        value=2,
        command=lambda: pilih_jawaban(2),
    ).pack(side="left")
    entry_c = tk.Entry(frame_c, font=("Helvetica", 10), textvariable=jawaban_c_var)
    entry_c.pack(side="left", fill="x", expand=True, ipady=3)
    opsi_entry_list.append(entry_c)

    frame_d = tk.Frame(right_panel, bg="#F4EFE6")
    frame_d.pack(fill="x", pady=2)
    tk.Radiobutton(
        frame_d,
        bg="#F4EFE6",
        variable=jawaban_benar_var,
        value=3,
        command=lambda: pilih_jawaban(3),
    ).pack(side="left")
    entry_d = tk.Entry(frame_d, font=("Helvetica", 10), textvariable=jawaban_d_var)
    entry_d.pack(side="left", fill="x", expand=True, ipady=3)
    opsi_entry_list.append(entry_d)

    entry_jelas = tk.Entry(right_panel, font=("Helvetica", 10), textvariable=penjelasan_var)
    entry_jelas.pack(fill="x", pady=(15, 5), ipady=5)

    bottom_frame = tk.Frame(ROOT, bg="#F4EFE6")
    bottom_frame.pack(fill="x", padx=20, pady=(0, 20))

    btn_kembali = tk.Button(
        bottom_frame,
        text="Kembali",
        bg="white",
        fg="#4E220F",
        font=("Helvetica", 10, "bold"),
        width=15,
        relief="solid",
        bd=1,
        command=lambda: [
            simpan_input_soal(),
            bersihkan_layar(ROOT),
            halaman_buat_kepala_quiz(ROOT),
        ],
    )
    btn_kembali.pack(side="left", ipady=5)

    def simpan_semua_quiz():
        if not simpan_input_soal():
            return

        if not logika.simpan_quiz():
            messagebox.showerror("Penyimpanan Error", "Quiz tidak tersimpan!")
            return

        reset_pembuatan_quiz()
        bersihkan_layar(ROOT)
        halaman_homescreen(ROOT)

    btn_simpan = tk.Button(
        bottom_frame,
        text="Simpan Quiz",
        bg="#4E220F",
        fg="white",
        font=("Helvetica", 10, "bold"),
        width=15,
        command=simpan_semua_quiz,
    )
    btn_simpan.pack(side="right", ipady=5)

    pilih_soal(0, False)