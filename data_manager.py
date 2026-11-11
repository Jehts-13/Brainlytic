import csv
import os
from logika import format_waktu

def load_daftar_quiz(filepath="data/daftar_quiz.csv"):
    if not os.path.exists(filepath):
        return []  # Return an empty list if the file doesn't exist

    daftar_quiz = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        # Menggunakan DictReader agar lebih aman dari koma di dalam teks
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # Sesuaikan dengan header kolom CSV Anda
            nama = row.get('nama_quiz', 'Tanpa Nama')
            deskripsi_dasar = row.get('deskripsi', 'Tidak ada deskripsi')
            waktu = row.get('batas_waktu', 0)
            jumlah_soal = row.get('jumlah_soal', 0)
            
            teks_deskripsi = f"{deskripsi_dasar}. {jumlah_soal} soal, {format_waktu(int(waktu))} menit."
            
            daftar_quiz.append({
                "judul": nama,
                "deskripsi": teks_deskripsi
            })
            
    return daftar_quiz


# Fungsi untuk mengambil dan mengirim jumlah soal dan batas waktu dari daftar_quiz.csv
def load_quiz_details(judul_quiz, filepath="data/daftar_quiz.csv"):
    if not os.path.exists(filepath):
        return None  # Return None if the file doesn't exist

    with open(filepath, mode='r', encoding='utf-8') as file:
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            if row.get('nama_quiz') == judul_quiz:
                jumlah_soal = int(row.get('jumlah_soal', 0))
                batas_waktu = int(row.get('batas_waktu', 0))
                return jumlah_soal, batas_waktu

    return None  # Return None if the quiz is not found

def save_hasil_quiz():
    # Implementasikan logika untuk menyimpan hasil quiz ke file 
    pass