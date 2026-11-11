username = ""

def simpan_nama_pemain(nama):
    username = nama
    print(f"Nama pemain disimpan: {username}")

def ambil_nama_pemain():
    return username

def format_waktu(sisa_detik):
    '''
    Mengambil sisa waktu dalam detik dan mengembalikannya dalam format MM:SS.
    '''
    menit = sisa_detik // 60
    detik = sisa_detik % 60
    return f"{menit:02d}:{detik:02d}"