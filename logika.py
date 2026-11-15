from data_manager import *

# data yang disimpan sementara quiz berjalan
username = ""
Judul_quiz = ""
Jumlah_soal = -1
Total_waktu = -1
Sisa_waktu = -1
Nomor_soal = -1 # quiz belum dimulai memiliki nilai Nomor_soal -1
# variabel soal menyimpan dictionary yang berisi deskripsi_soal dan list pilihan
Soal = None
Riwayat_jawaban = None


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
    print(f"Jumlah soal:    {Jumlah_soal}\nTotal Waktu:    {Total_waktu}\n")
    
def lanjut_quiz(PILIHAN):
    '''
    Menyimpan pilihan yang telah dibuat di soal ini
    '''
    
    Nomor_soal += 1
    
def ambil_rasio_progressbar():
    return (Nomor_soal+1 / Jumlah_soal)






def format_waktu(SISA_DETIK):
    '''
    Mengambil sisa waktu dalam detik dan mengembalikannya dalam format MM:SS.
    '''
    menit = SISA_DETIK // 60
    detik = SISA_DETIK % 60
    return f"{menit:02d}:{detik:02d}"

def reset_data():
    global username, Judul_quiz, Total_waktu, Sisa_waktu, Nomor_soal, soal, pilihan, riwayat_jawaban
    username = ""
    Judul_quiz = ""
    Total_waktu = -1
    Sisa_waktu = -1
    Nomor_soal = -1 # quiz belum dimulai memiliki nilai Nomor_soal -1
    Soal = None
    Riwayat_jawaban = None
    
    print("Temporary Data sudah di reset!")