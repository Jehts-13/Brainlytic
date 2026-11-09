import csv
import os

def load_daftar_quiz(filepath="data/daftar_quiz.csv"):
    if not os.path.exists(filepath):
        return []  # Return an empty list if the file doesn't exist

    daftar_quiz = []
    with open(filepath, mode='r', encoding='utf-8') as file:
        # Menggunakan DictReader agar lebih aman dari koma di dalam teks
        csv_reader = csv.DictReader(file)
        
        for row in csv_reader:
            # Sesuaikan dengan header kolom CSV Anda
            nama = row.get('nama_kuis', 'Tanpa Nama')
            deskripsi_dasar = row.get('deskripsi', 'Tidak ada deskripsi')
            waktu = row.get('batas_waktu', 0)
            jumlah_soal = row.get('jumlah_soal', 0)
            
            teks_deskripsi = f"{deskripsi_dasar}. {jumlah_soal} soal, {waktu} menit"
            
            daftar_quiz.append({
                "judul": nama,
                "deskripsi": teks_deskripsi
            })
            
    return daftar_quiz