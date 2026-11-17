from data_manager import *

# data yang disimpan sementara quiz berjalan (Temporary Data)
username = ""

Judul_quiz = ""
Jumlah_soal = -1
Total_waktu = -1
Waktu_digunakan = -1

Nomor_soal = -1 # quiz belum dimulai memiliki nilai Nomor_soal -1
# variabel soal menyimpan dictionary yang berisi deskripsi_soal dan list pilihan
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
    
def lanjut_quiz(PILIHAN):
    '''
    Menyimpan pilihan yang telah dibuat di soal ini
    '''
    Nomor_soal += 1
    
def ambil_rasio_progressbar():
    return (Nomor_soal+1) / Jumlah_soal

def simpan_jawaban_soal(index_jawaban):
    global Nomor_soal, Riwayat_jawaban
    if Riwayat_jawaban is None:
        Riwayat_jawaban = []
    Riwayat_jawaban.append(index_jawaban)
    

    Nomor_soal += 1
    return
    
def hitung_skor(sisa_waktu):
    '''Menghitung jumlah benar dan salah, persentase skor, serta menghitung waktu yang digunakan'''
    global Jumlah_benar, Jumlah_salah, Skor, Waktu_digunakan, Riwayat_jawaban, Jumlah_soal, Judul_quiz
    jawaban = load_quiz_jawaban(Judul_quiz)
    # Menghitung jumlah jawaban benar dan salah
    try:
        for i in range(Jumlah_soal):
            if Riwayat_jawaban[i] == jawaban[i]:
                Jumlah_benar += 1
                print(f"Riwayat_jawaban {Riwayat_jawaban[i]} == jawaban {jawaban[i]} (Benar)")
            else:
                Jumlah_salah += 1
                print(f"Riwayat_jawaban {Riwayat_jawaban[i]} != jawaban {jawaban[i]} (Salah)")
        # Menghitung persentase skor
        Skor = int((Jumlah_benar / Jumlah_soal) * 100)
        print(f"Jumlah Benar: {Jumlah_benar:<5}Jumlah Salah: {Jumlah_salah:<5}Skor: {f"{Skor:.2f}":<7}")
        # Menghitung waktu yang digunakan
        Waktu_digunakan = Total_waktu - sisa_waktu

        simpan_hasil_quiz(username, Judul_quiz, Skor, Jumlah_benar, Jumlah_salah, Waktu_digunakan)
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
    