from data_manager import *

# data yang disimpan sementara quiz berjalan (Temporary Data)
username = ""

Judul_quiz = ""
Jumlah_soal = -1
Total_waktu = -1
Waktu_digunakan = -1

Nomor_soal = -1 # quiz belum dimulai memiliki nilai Nomor_soal -1
# variabel soal menyimpan dictionary berisi deskripsi_soal, jawaban dan list pilihan
Soal = None
Riwayat_jawaban = None

Jumlah_benar = 0
Jumlah_salah = 0
Skor = 0


def simpan_nama_pemain(NAMA):
    global username
    username = NAMA
    print(f"Nama pemain disimpan: {username}")

def muat_quiz(JUDUL):
    global Judul_quiz, Jumlah_soal, Soal, Nomor_soal, Total_waktu, Riwayat_jawaban
    Soal = load_quiz_soal(JUDUL)
    if Soal == None:
        print("Pertanyaan tidak ditemukan!")
        return 

    Judul_quiz = JUDUL
    Jumlah_soal, Total_waktu = load_quiz_jumlah_time(JUDUL)
    
    Nomor_soal = 0
    Riwayat_jawaban = []
    
    
def ambil_rasio_progressbar():
    return (Nomor_soal+1) / Jumlah_soal

def simpan_jawaban_soal(index_jawaban):
    global Nomor_soal, Riwayat_jawaban
    if Riwayat_jawaban is None:
        Riwayat_jawaban = []
    Riwayat_jawaban.append(int(index_jawaban))
    
    Nomor_soal += 1
    return
    
def hitung_skor(sisa_waktu):
    '''Menghitung jumlah benar dan salah, persentase skor, serta menghitung waktu yang digunakan'''
    global Jumlah_benar, Jumlah_salah, Skor, Waktu_digunakan, Riwayat_jawaban, Jumlah_soal, Judul_quiz, Soal
    
    # Menghitung jumlah jawaban benar dan salah
    try:
        for i in range(Jumlah_soal):
            jawaban = Soal[i]['jawaban']
            print(type(jawaban), '==' if type(jawaban) == type(Riwayat_jawaban[i]) else '!=' ,type(Riwayat_jawaban[i]))
            if Riwayat_jawaban[i] == jawaban:
                Jumlah_benar += 1
                print(f"Riwayat_jawaban {Riwayat_jawaban[i]} == jawaban {jawaban} (Benar)")
            else:
                Jumlah_salah += 1
                print(f"Riwayat_jawaban {Riwayat_jawaban[i]} != jawaban {jawaban} (Salah)")
        # Menghitung persentase skor
        Skor = int((Jumlah_benar / Jumlah_soal) * 100)
        print(f"Jumlah Benar: {Jumlah_benar:<5}Jumlah Salah: {Jumlah_salah:<5}Skor: {f"{Skor:.2f}":<7}")
        # Menghitung waktu yang digunakan
        Waktu_digunakan = Total_waktu - sisa_waktu

        save_hasil_quiz(username, Judul_quiz, Skor, Jumlah_benar, Jumlah_salah, Waktu_digunakan)
    except IndexError:
        return IndexError

def format_waktu(SISA_DETIK):
    '''
    Mengambil sisa waktu dalam detik dan mengembalikannya dalam format MM:SS.
    '''
    menit = SISA_DETIK // 60
    detik = SISA_DETIK % 60
    return f"{menit:02d}:{detik:02d}"


def reset_data():
    global username, Judul_quiz, Total_waktu, Sisa_waktu, Nomor_soal, Soal, Riwayat_jawaban, Jumlah_benar, Jumlah_salah, Skor
    username = ""
    Judul_quiz = ""
    Total_waktu = -1
    Sisa_waktu = -1
    Nomor_soal = -1 # quiz belum dimulai memiliki nilai Nomor_soal -1
    Soal = None
    Riwayat_jawaban = None
    Jumlah_benar = 0
    Jumlah_salah = 0
    Skor = 0
    
    print("Temporary Data sudah di reset!")
    
def sort_user_history(data, judul=None):
    '''
    Mengembalikan data_user_history yang telah di sort berdasarkan nilai yang di ambil dari quiz yang sama, kemudian berdasarkan tanggal dan waktu pengerjaan
    '''
    result_data = []
    if judul != None:
        for item in data:
            if item['judul_quiz'] == judul:
                result_data.append(item)
    else:
        result_data = data
    
    
    return sorted(
        result_data,
        key=lambda x: (x['judul_quiz'], -int(x['skor']), x['waktu_digunakan'])
    )

Deskripsi = ""

def simpan_kepala_quiz(judul, deskripsi, jumlah, waktu):
    global Judul_quiz, Deskripsi, Jumlah_soal, Total_waktu, Nomor_soal, Soal
    
    Judul_quiz = judul
    Deskripsi = deskripsi
    Jumlah_soal = int(jumlah)
    Total_waktu = int(waktu)
    Nomor_soal = 0
    # inisialisasi Soal sebagai list ketika awal pembuatan
    if Soal == None:
        print("[Soal] belum pernah di inisialisasi!")
        Soal = []
        for _ in range(Jumlah_soal):
            Soal.append(None)
    elif len(Soal) != Jumlah_soal: # menyesuaikan panjang Soal setelah inisialisasi
        panjang_soal = len(Soal)
        print(f"[Soal] pernah di inisialisasi dengan panjang {panjang_soal} soal")
        if panjang_soal > Jumlah_soal:
            for _ in range(len(Soal)-Jumlah_soal):
                Soal.pop()
        elif panjang_soal < Jumlah_soal:
            for _ in range(Jumlah_soal-panjang_soal):
                Soal.append(None)
            
        
        print(f"Berhasil menyimpan\nJudul_quiz: {Judul_quiz}\nDeskripsi: {Deskripsi}\nJumlah_soal: {Jumlah_soal:<7}Waktu: {Total_waktu}")
    
def simpan_soal(index, deskripsi_soal, opsi_a, opsi_b, opsi_c, opsi_d, jawaban_benar, penjelasan):
    global Soal
    if index != Nomor_soal:
        print(f"index:{index}\t\tNomor_soal:{Nomor_soal}")
        return False
    opsi = [opsi_a, opsi_b, opsi_c, opsi_d]
    Soal[index] = {'deskripsi_soal': deskripsi_soal, 'opsi': opsi, 'jawaban': jawaban_benar, 'penjelasan':penjelasan}
    return True

def ambil_soal(index):
    global Soal
    print(f"Isi Soal:\n{Soal}")
    for i, soal in enumerate(Soal):
        if i == index:
            if soal == None:
                return ("", '','','','', 0, 'Tuliskan penjelasan anda di sini...')
            opsi_a, opsi_b, opsi_c, opsi_d = tuple(soal['opsi'])
            return (soal['deskripsi_soal'], opsi_a, opsi_b, opsi_c, opsi_d, soal['jawaban'], soal['penjelasan'])
    return None

def simpan_quiz():
    global Judul_quiz, Deskripsi, Total_waktu, Jumlah_soal, Soal # Menyimpan menggunakan data global di logika.py
    return save_buat_quiz(Judul_quiz, Deskripsi, Total_waktu, Jumlah_soal, Soal)