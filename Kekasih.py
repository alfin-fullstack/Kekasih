import csv
import os
from datetime import datetime

try:
    from tabulate import tabulate, tabulate_formats
except ImportError:
    print("Modul 'tabulate' belum terpasang. Jalankan dulu: pip install tabulate")
    raise SystemExit

FILE_USER = "data_user.csv"
FILE_DOMPET = "data_dompet.csv"
FILE_TRANSAKSI = "data_transaksi.csv"
FILE_KATEGORI = "data_kategori.csv"
FILE_SUMBER = "data_sumber.csv"
KOLOM_USER = ["username", "password", "role"]
KOLOM_DOMPET = ["pemilik", "dompet", "saldo_awal"]
KOLOM_TRANSAKSI = ["pemilik", "tanggal", "jenis", "dompet", "kategori", "jumlah"]
KOLOM_KATEGORI = ["pemilik", "kategori"]
KOLOM_SUMBER = ["pemilik", "sumber"]

FILE_DATA_PEMILIK = [
    [FILE_DOMPET, KOLOM_DOMPET],
    [FILE_TRANSAKSI, KOLOM_TRANSAKSI],
    [FILE_KATEGORI, KOLOM_KATEGORI],
    [FILE_SUMBER, KOLOM_SUMBER],
]

DAFTAR_DOMPET = ["GoPay", "Rekening Bank", "Tunai"]

KATEGORI_DEFAULT = ["Makan & Minum", "Transportasi", "Belanja", "Lainnya"]

SUMBER_PEMASUKAN = ["Kerja", "Uang saku", "Hadiah"]

ROLE_LABEL = {"admin": "orang tua", "user": "anak"}

MIN_PASSWORD = 6
LEBAR = 62

BATAS_NORMAL = 0.5
BATAS_BOROS = 0.8

if "rounded_grid" in tabulate_formats:
    FORMAT_TABEL = "rounded_grid"
elif "fancy_grid" in tabulate_formats:
    FORMAT_TABEL = "fancy_grid"
else:
    FORMAT_TABEL = "grid"

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"


def warna(teks, kode):
    return f"{kode}{teks}{RESET}"


def bersihkan():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def jeda():
    input(warna("\nTekan Enter untuk kembali...", DIM))


def banner(teks, subteks=""):
    print(warna("╔" + "═" * (LEBAR - 2) + "╗", CYAN))
    print(warna("║", CYAN) + warna(teks.center(LEBAR - 2), BOLD) + warna("║", CYAN))
    print(warna("╚" + "═" * (LEBAR - 2) + "╝", CYAN))
    if subteks != "":
        print(warna(subteks, DIM))


def judul(teks):
    print()
    print(warna("─" * LEBAR, DIM))
    print(warna(f" {teks}", BOLD + CYAN))
    print(warna("─" * LEBAR, DIM))
    print(warna("Ketik 'batal' kapan saja untuk kembali\n", DIM))


def sukses(teks):
    print(warna(teks, GREEN))


def gagal(teks):
    print(warna(teks, RED))


def info(teks):
    print(warna(f"• {teks}", YELLOW))


def tabel(baris, header, rata=None):
    header_warna = []
    for h in header:
        header_warna.append(warna(h, BOLD + CYAN))
    print(tabulate(baris, headers=header_warna, tablefmt=FORMAT_TABEL,
                   colalign=rata, disable_numparse=True))


def rupiah(angka):
    return f"Rp {float(angka):,.2f}"


def warna_jenis(jenis):
    if jenis == "Pemasukan":
        return warna(jenis, GREEN)
    return warna(jenis, RED)


def masukan(teks, strip=True):
    """input() biasa. Mengetik 'batal' mengembalikan None (= batal)."""
    nilai = input(teks)
    if nilai.strip().lower() == "batal":
        return None
    if strip:
        return nilai.strip()
    return nilai


def konfirmasi(teks):
    jawaban = input(f"{teks} (y/n): ").strip().lower()
    return jawaban == "y"


def pilih_index(teks, pilihan, batal="Kembali"):
    """Tampilkan pilihan bernomor + 0 untuk kembali.
    Mengembalikan index pilihan, atau None jika batal."""
    print(teks)
    baris = []
    for no in range(len(pilihan)):
        baris.append([no + 1, pilihan[no]])
    baris.append([0, warna(batal, DIM)])
    tabel(baris, ["No", "Pilihan"])
    while True:
        nomor = input("Pilih nomor: ").strip()
        if nomor == "0" or nomor.lower() == "batal":
            return None
        if nomor.isdigit() and 1 <= int(nomor) <= len(pilihan):
            return int(nomor) - 1
        gagal("Pilihan tidak valid!")


def pilih(teks, pilihan, batal="Kembali"):
    """Sama seperti pilih_index, tetapi mengembalikan ISI pilihan (None jika batal)."""
    index = pilih_index(teks, pilihan, batal)
    if index is None:
        return None
    return pilihan[index]


def tanggal_valid(tanggal):
    """True jika tanggal berformat DD-MM-YYYY dan benar-benar ada di kalender."""
    bagian = tanggal.split("-")
    if len(bagian) != 3:
        return False

    hari = bagian[0]
    bulan = bagian[1]
    tahun = bagian[2]
    if not (hari.isdigit() and bulan.isdigit() and tahun.isdigit()):
        return False
    if len(hari) > 2 or len(bulan) > 2 or len(tahun) != 4:
        return False

    hari = int(hari)
    bulan = int(bulan)
    tahun = int(tahun)
    if tahun < 1 or bulan < 1 or bulan > 12:
        return False

    hari_per_bulan = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    kabisat = (tahun % 4 == 0 and tahun % 100 != 0) or tahun % 400 == 0
    if kabisat:
        hari_per_bulan[1] = 29
    return 1 <= hari <= hari_per_bulan[bulan - 1]


def input_tanggal(teks="Tanggal (DD-MM-YYYY, kosongkan = hari ini): "):
    while True:
        tanggal = masukan(teks)
        if tanggal is None:
            return None
        if tanggal == "":
            tanggal = datetime.now().strftime("%d-%m-%Y")
            info(f"Memakai tanggal hari ini: {tanggal}")
            return tanggal
        if tanggal_valid(tanggal):
            return tanggal
        gagal("Format tanggal salah! Contoh: 25-12-2026")


def adalah_angka(teks):
    """True jika teks bisa diubah menjadi angka desimal (boleh diawali + atau -)."""
    if teks == "":
        return False
    angka = teks
    if angka[0] == "+" or angka[0] == "-":
        angka = angka[1:]
    return angka.count(".") <= 1 and angka.replace(".", "", 1).isdigit()


def input_jumlah(teks="Jumlah uang: ", boleh_nol=False):
    while True:
        isi = masukan(teks)
        if isi is None:
            return None
        if not adalah_angka(isi):
            gagal("Jumlah harus berupa angka!")
            continue
        jumlah = float(isi)
        if jumlah > 0 or (boleh_nol and jumlah == 0):
            return jumlah
        gagal("Jumlah tidak valid!")


def cek_password(password):
    """Return (valid, pesan). Wajib: min. 6 karakter, ada huruf besar dan angka."""
    ada_besar = False
    ada_angka = False
    for huruf in password:
        if huruf.isupper():
            ada_besar = True
        if huruf.isdigit():
            ada_angka = True

    if len(password) < MIN_PASSWORD:
        return False, f"Password minimal {MIN_PASSWORD} karakter!"
    if not ada_besar:
        return False, "Password harus mengandung minimal 1 huruf besar!"
    if not ada_angka:
        return False, "Password harus mengandung minimal 1 angka!"
    return True, ""


def input_password(teks="Password baru: ", boleh_kosong=False):
    """Minta password sampai valid.
    Return None jika batal, atau "" jika boleh_kosong dan dikosongkan."""
    pesan = f"Min. {MIN_PASSWORD} karakter, kombinasi huruf besar & angka"
    if boleh_kosong:
        pesan += " (kosongkan = tidak diubah)"
    info(pesan)
    while True:
        password = masukan(teks, strip=False)
        if password is None:
            return None
        if password == "" and boleh_kosong:
            return ""
        valid, pesan_error = cek_password(password)
        if valid:
            return password
        gagal(pesan_error)


def baca(file):
    """Membaca file CSV menjadi list of dictionary. File belum ada -> list kosong."""
    if not os.path.exists(file):
        return []
    with open(file, newline="") as f:
        return list(csv.DictReader(f))


def simpan(file, kolom, data):
    """Menulis ulang seluruh isi file CSV dari list of dictionary."""
    with open(file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=kolom)
        writer.writeheader()
        writer.writerows(data)


def pindah_data_pemilik(lama, baru):
    """Dipakai saat username berubah: dompet, transaksi, kategori, sumber ikut pindah."""
    for item in FILE_DATA_PEMILIK:
        file = item[0]
        kolom = item[1]
        data = baca(file)
        for row in data:
            if row["pemilik"] == lama:
                row["pemilik"] = baru
        simpan(file, kolom, data)


def ada_admin(users):
    for u in users:
        if u["role"] == "admin":
            return True
    return False


def username_ada(users, username):
    for u in users:
        if u["username"] == username:
            return True
    return False


def cari_nama(daftar, nama):
    """Cari nama di list tanpa membedakan huruf besar/kecil. None jika tidak ada."""
    for d in daftar:
        if d.lower() == nama.lower():
            return d
    return None


def setup_awal():
    """Jika belum ada akun orang tua (admin), buat akun pertama (ayah/ibu)."""
    users = baca(FILE_USER)
    if ada_admin(users):
        return

    bersihkan()
    banner("SETUP AWAL KEUANGAN KELUARGA")
    print("\nBelum ada akun orang tua. Buat akun pertama (ayah/ibu) sebagai admin.")
    print("Akun anak dan akun orang tua lainnya dibuat dari menu admin.\n")

    while True:
        username = input("Username: ").strip()
        if username == "":
            gagal("Username tidak boleh kosong!")
        elif username_ada(users, username):
            gagal("Username sudah dipakai!")
        else:
            break

    while True:
        password = input_password("Password: ")
        if password is None:
            gagal("Setup awal wajib diselesaikan.")
        else:
            break

    users.append({"username": username, "password": password, "role": "admin"})
    simpan(FILE_USER, KOLOM_USER, users)
    sukses(f"Akun orang tua {username} berhasil dibuat!")
    jeda()


def tambah_anggota(admin):
    """Orang tua membuat akun anggota keluarga (anak atau orang tua lain)."""
    judul("TAMBAH ANGGOTA KELUARGA")
    users = baca(FILE_USER)
    jenis = pilih("Jenis akun:", ["Anak", "Orang tua (admin)"])
    if jenis is None:
        return "batal"

    if jenis == "Anak":
        role = "user"
    else:
        role = "admin"

    username = masukan("Username: ")
    if username is None:
        return "batal"
    if username == "":
        gagal("Username tidak boleh kosong!")
        return
    if username_ada(users, username):
        gagal("Username sudah dipakai!")
        return

    password = input_password("Password: ")
    if password is None:
        return "batal"

    users.append({"username": username, "password": password, "role": role})
    simpan(FILE_USER, KOLOM_USER, users)
    sukses(f"Akun {username} ({ROLE_LABEL[role]}) berhasil dibuat!")


def login():
    """Return dictionary user jika berhasil, None jika 3x gagal, "batal" jika dibatalkan."""
    judul("LOGIN")
    users = baca(FILE_USER)

    for percobaan in range(3):
        username = masukan("Username: ")
        if username is None:
            return "batal"
        password = masukan("Password: ", strip=False)
        if password is None:
            return "batal"

        for u in users:
            if u["username"] == username and u["password"] == password:
                sukses(f"Login berhasil! Selamat datang, {username} ({ROLE_LABEL.get(u['role'], u['role'])}).")
                return u
        gagal("Username atau password salah!")

    gagal("Terlalu banyak percobaan.")
    return None


def ubah_username(user):
    """User/admin mengubah username miliknya sendiri."""
    judul("UBAH USERNAME")
    lama = user["username"]
    print(f"Username saat ini: {warna(lama, BOLD)}")
    baru = masukan("Username baru: ")

    if baru is None:
        return "batal"
    if baru == "":
        gagal("Username tidak boleh kosong!")
        return
    if baru == lama:
        info("Username sama dengan sebelumnya, tidak ada perubahan.")
        return

    users = baca(FILE_USER)
    if username_ada(users, baru):
        gagal("Username sudah dipakai!")
        return

    for u in users:
        if u["username"] == lama:
            u["username"] = baru
    simpan(FILE_USER, KOLOM_USER, users)
    pindah_data_pemilik(lama, baru)
    user["username"] = baru
    sukses(f"Username berhasil diubah menjadi {baru}!")


def ubah_password(user):
    """User/admin mengubah password miliknya sendiri (wajib konfirmasi password lama)."""
    judul("UBAH PASSWORD")
    lama = masukan("Password saat ini: ", strip=False)
    if lama is None:
        return "batal"
    if lama != user["password"]:
        gagal("Password saat ini salah!")
        return

    baru = input_password("Password baru: ")
    if baru is None:
        return "batal"
    if baru == lama:
        gagal("Password baru tidak boleh sama dengan password lama!")
        return

    users = baca(FILE_USER)
    for u in users:
        if u["username"] == user["username"]:
            u["password"] = baru
    simpan(FILE_USER, KOLOM_USER, users)
    user["password"] = baru
    sukses("Password berhasil diubah!")


def dompet_saya(user):
    hasil = []
    for d in baca(FILE_DOMPET):
        if d["pemilik"] == user["username"]:
            hasil.append(d)
    return hasil


def dompet_milik(user):
    nama = []
    for d in dompet_saya(user):
        nama.append(d["dompet"])
    return nama


def hitung_saldo(dompet, transaksi):
    """Saldo sekarang = saldo awal + pemasukan - pengeluaran."""
    saldo = float(dompet["saldo_awal"])
    for t in transaksi:
        if t["pemilik"] == dompet["pemilik"] and t["dompet"] == dompet["dompet"]:
            jumlah = float(t["jumlah"])
            if t["jenis"] == "Pemasukan":
                saldo += jumlah
            else:
                saldo -= jumlah
    return saldo


def ada_minus(transaksi, dompets):
    """True jika ada dompet yang saldonya jadi minus."""
    for d in dompets:
        if round(hitung_saldo(d, transaksi), 2) < 0:
            return True
    return False


def saldo_dompet(user, nama):
    """Saldo sekarang untuk satu dompet milik user (None jika dompet tidak ditemukan)."""
    transaksi = baca(FILE_TRANSAKSI)
    for d in dompet_saya(user):
        if d["dompet"] == nama:
            return hitung_saldo(d, transaksi)
    return None


def tampil_dompet(user):
    judul(f"DOMPET & SALDO ({user['username']})")
    dompets = dompet_saya(user)
    if len(dompets) == 0:
        info("Belum ada data dompet.")
        return

    transaksi = baca(FILE_TRANSAKSI)
    total = 0.0
    baris = []
    for d in dompets:
        sekarang = hitung_saldo(d, transaksi)
        total += sekarang
        baris.append([d["dompet"], rupiah(d["saldo_awal"]), rupiah(sekarang)])
    baris.append([warna("TOTAL", BOLD), "", warna(rupiah(total), BOLD)])
    tabel(baris, ["Dompet", "Saldo Awal", "Saldo Sekarang"], ("left", "right", "right"))


def tambah_dompet(user):
    judul("TAMBAH DOMPET")
    dompets = baca(FILE_DOMPET)
    milik = dompet_milik(user)

    nama = None
    saran = []
    for d in DAFTAR_DOMPET:
        if d not in milik:
            saran.append(d)

    if len(saran) > 0:
        lain = "Dompet lain (ketik nama sendiri)"
        pilihan = pilih("Pilih dompet:", saran + [lain])
        if pilihan is None:
            return "batal"
        if pilihan != lain:
            nama = pilihan

    if nama is None:
        nama = masukan("Nama dompet: ")
        if nama is None:
            return "batal"

    if nama == "":
        gagal("Nama dompet tidak boleh kosong!")
        return
    if cari_nama(milik, nama) is not None:
        gagal("Dompet tersebut sudah ada!")
        return

    saldo_awal = input_jumlah("Saldo awal: ", boleh_nol=True)
    if saldo_awal is None:
        return "batal"

    dompets.append({"pemilik": user["username"],
                    "dompet": nama,
                    "saldo_awal": saldo_awal})
    simpan(FILE_DOMPET, KOLOM_DOMPET, dompets)
    sukses(f"Dompet {nama} berhasil ditambahkan!")


def ubah_saldo_dompet(user):
    judul(f"UBAH SALDO AWAL DOMPET ({user['username']})")
    milik = dompet_milik(user)
    if len(milik) == 0:
        info("Belum ada dompet.")
        return

    nama = pilih("Pilih dompet:", milik)
    if nama is None:
        return "batal"

    dompets = baca(FILE_DOMPET)
    target = None
    for d in dompets:
        if d["pemilik"] == user["username"] and d["dompet"] == nama:
            target = d
    print(f"Saldo awal {nama} saat ini: {rupiah(target['saldo_awal'])}")

    saldo_baru = input_jumlah("Saldo awal baru: ", boleh_nol=True)
    if saldo_baru is None:
        return "batal"
    target["saldo_awal"] = saldo_baru

    if ada_minus(baca(FILE_TRANSAKSI), dompets):
        gagal("Gagal: saldo awal terlalu kecil, saldo dompet jadi minus!")
        return

    simpan(FILE_DOMPET, KOLOM_DOMPET, dompets)
    sukses("Saldo awal berhasil diubah!")


def hapus_dompet(user):
    judul(f"HAPUS DOMPET ({user['username']})")
    milik = dompet_milik(user)
    if len(milik) == 0:
        info("Belum ada dompet.")
        return

    nama = pilih("Pilih dompet yang dihapus:", milik)
    if nama is None:
        return "batal"

    transaksi = baca(FILE_TRANSAKSI)
    jumlah = 0
    for t in transaksi:
        if t["pemilik"] == user["username"] and t["dompet"] == nama:
            jumlah += 1

    if not konfirmasi(f"Hapus dompet {nama} beserta {jumlah} transaksinya?"):
        info("Penghapusan dibatalkan.")
        return

    dompet_sisa = []
    for d in baca(FILE_DOMPET):
        if not (d["pemilik"] == user["username"] and d["dompet"] == nama):
            dompet_sisa.append(d)
    simpan(FILE_DOMPET, KOLOM_DOMPET, dompet_sisa)

    transaksi_sisa = []
    for t in transaksi:
        if not (t["pemilik"] == user["username"] and t["dompet"] == nama):
            transaksi_sisa.append(t)
    simpan(FILE_TRANSAKSI, KOLOM_TRANSAKSI, transaksi_sisa)
    sukses(f"Dompet {nama} berhasil dihapus!")


def ambil_daftar(user, file, kolom, field, default):
    """Daftar pilihan milik user. User baru otomatis dapat daftar default."""
    data = baca(file)
    milik = []
    for r in data:
        if r["pemilik"] == user["username"]:
            milik.append(r[field])

    if len(milik) == 0:
        for d in default:
            data.append({"pemilik": user["username"], field: d})
            milik.append(d)
        simpan(file, kolom, data)
    return milik


def kategori_milik(user):
    return ambil_daftar(user, FILE_KATEGORI, KOLOM_KATEGORI, "kategori", KATEGORI_DEFAULT)


def sumber_milik(user):
    return ambil_daftar(user, FILE_SUMBER, KOLOM_SUMBER, "sumber", SUMBER_PEMASUKAN)


def pilih_kategori(user, jenis, dompet=None):
    """Pilih kategori pengeluaran / sumber pemasukan, atau tambah yang baru dari sini.
    Jika dompet diberikan, sisa saldo dompet itu ditampilkan dulu.
    Mengembalikan nama pilihan, atau None jika batal."""
    if jenis == "Pemasukan":
        file = FILE_SUMBER
        kolom = KOLOM_SUMBER
        field = "sumber"
        daftar = sumber_milik(user)
        teks = "\nSumber pemasukan:"
    else:
        file = FILE_KATEGORI
        kolom = KOLOM_KATEGORI
        field = "kategori"
        daftar = kategori_milik(user)
        teks = "\nKategori pengeluaran:"

    if dompet:
        saldo = saldo_dompet(user, dompet)
        if saldo is not None:
            print(f"\nSisa saldo {dompet}: {warna(rupiah(saldo), BOLD)}")

    tambah = warna("+ Tambah baru (ketik sendiri)", GREEN)
    pilihan = pilih(teks, daftar + [tambah])
    if pilihan is None:
        return None
    if pilihan != tambah:
        return pilihan

    while True:
        nama = masukan("Nama baru: ")
        if nama is None:
            return None
        if nama == "":
            gagal("Nama tidak boleh kosong!")
            continue

        ada = cari_nama(daftar, nama)
        if ada is not None:
            info(f"'{ada}' sudah ada, memakai yang sudah ada.")
            return ada

        data = baca(file)
        data.append({"pemilik": user["username"], field: nama})
        simpan(file, kolom, data)
        sukses(f"'{nama}' berhasil ditambahkan dan dipilih!")
        return nama


def transaksi_saya(user):
    """Daftar [index asli, transaksi] milik user."""
    semua = baca(FILE_TRANSAKSI)
    hasil = []
    for i in range(len(semua)):
        if semua[i]["pemilik"] == user["username"]:
            hasil.append([i, semua[i]])
    return hasil


def cetak(daftar):
    if len(daftar) == 0:
        info("Data tidak ditemukan.")
        return

    baris = []
    nomor = 1
    for item in daftar:
        t = item[1]
        baris.append([nomor, t["tanggal"], warna_jenis(t["jenis"]), t["dompet"],
                      t["kategori"], rupiah(t["jumlah"])])
        nomor += 1
    tabel(baris, ["No", "Tanggal", "Jenis", "Dompet", "Kategori / Sumber", "Jumlah"],
          ("right", "left", "left", "left", "left", "right"))


def cetak_dengan_saldo(user, daftar):
    """Seperti cetak(), tetapi ada kolom sisa saldo dompet setelah tiap transaksi
    (dihitung berurutan sesuai urutan data) dan total sisa saldo di bawah tabel."""
    if len(daftar) == 0:
        info("Data tidak ditemukan.")
        return

    saldo = {}
    for d in dompet_saya(user):
        saldo[d["dompet"]] = float(d["saldo_awal"])

    baris = []
    nomor = 1
    for item in daftar:
        t = item[1]
        nama = t["dompet"]
        if nama not in saldo:
            saldo[nama] = 0.0
        if t["jenis"] == "Pemasukan":
            saldo[nama] += float(t["jumlah"])
        else:
            saldo[nama] -= float(t["jumlah"])
        baris.append([nomor, t["tanggal"], warna_jenis(t["jenis"]), nama,
                      t["kategori"], rupiah(t["jumlah"]), rupiah(saldo[nama])])
        nomor += 1
    tabel(baris, ["No", "Tanggal", "Jenis", "Dompet", "Kategori / Sumber", "Jumlah", "Sisa Saldo"],
          ("right", "left", "left", "left", "left", "right", "right"))

    total = 0.0
    for nama in saldo:
        total += saldo[nama]
    print(f"\nTotal sisa saldo semua dompet: {warna(rupiah(total), BOLD)}")


def pilih_nomor(daftar, aksi):
    """Pilih nomor data dari tabel. 0 = kembali (None).
    Mengembalikan index ASLI di file."""
    while True:
        nomor = masukan(f"Nomor data yang ingin {aksi} (0 = kembali): ")
        if nomor is None or nomor == "0":
            return None
        if nomor.isdigit() and 1 <= int(nomor) <= len(daftar):
            return daftar[int(nomor) - 1][0]
        gagal("Nomor tidak valid!")


def pilih_jenis(user, transaksi):
    """Pilih jenis; kategori/sumber ikut menyesuaikan. Dipakai tambah & ubah transaksi.
    Return True jika selesai, False jika dibatalkan."""
    jenis_lama = transaksi.get("jenis")
    jenis = pilih("\nJenis transaksi:", ["Pemasukan", "Pengeluaran"])
    if jenis is None:
        return False

    transaksi["jenis"] = jenis
    if jenis == jenis_lama:
        return True

    kategori = pilih_kategori(user, jenis, transaksi.get("dompet"))
    if kategori is None:
        return False
    transaksi["kategori"] = kategori
    return True


def tambah_data(user):
    judul("TAMBAH TRANSAKSI")
    milik = dompet_milik(user)
    if len(milik) == 0:
        info("Anda belum punya dompet. Tambah dulu lewat menu Dompet > Tambah Dompet.")
        return

    transaksi = {"pemilik": user["username"]}

    dompet = pilih("\nPilih dompet:", milik)
    if dompet is None:
        return "batal"
    transaksi["dompet"] = dompet

    if not pilih_jenis(user, transaksi):
        return "batal"

    tanggal = input_tanggal()
    if tanggal is None:
        return "batal"
    transaksi["tanggal"] = tanggal

    jumlah = input_jumlah()
    if jumlah is None:
        return "batal"
    transaksi["jumlah"] = jumlah

    semua = baca(FILE_TRANSAKSI)
    semua.append(transaksi)
    if ada_minus(semua, baca(FILE_DOMPET)):
        gagal("Gagal: saldo dompet tidak cukup!")
        return

    simpan(FILE_TRANSAKSI, KOLOM_TRANSAKSI, semua)
    sukses("Transaksi berhasil ditambahkan!")


def tampilkan_data(user):
    judul("DAFTAR TRANSAKSI")
    cetak_dengan_saldo(user, transaksi_saya(user))


def cari_data(user):
    judul("CARI BERDASARKAN TANGGAL")
    tanggal = input_tanggal("Tanggal yang dicari (DD-MM-YYYY, kosongkan = hari ini): ")
    if tanggal is None:
        return "batal"

    hasil = []
    for item in transaksi_saya(user):
        if item[1]["tanggal"] == tanggal:
            hasil.append(item)
    cetak(hasil)


def ubah_data(user):
    judul("UBAH TRANSAKSI")
    daftar = transaksi_saya(user)
    cetak(daftar)
    if len(daftar) == 0:
        return

    index = pilih_nomor(daftar, "diubah")
    if index is None:
        return "batal"

    milik = dompet_milik(user)
    semua = baca(FILE_TRANSAKSI)
    asli = semua[index]
    baru = dict(asli)

    while True:
        bersihkan()
        judul("UBAH TRANSAKSI")
        print("Data saat ini:")
        cetak([[index, baru]])
        print()

        bagian = pilih("Apa yang ingin diubah?",
                       ["Tanggal", "Jenis", "Dompet", "Kategori / sumber", "Jumlah",
                        warna("Simpan perubahan", GREEN)],
                       batal="Batal (tanpa menyimpan)")
        if bagian is None:
            return "batal"

        match bagian:
            case "Tanggal":
                tanggal = input_tanggal()
                if tanggal is None:
                    return "batal"
                baru["tanggal"] = tanggal
            case "Jenis":
                if not pilih_jenis(user, baru):
                    return "batal"
            case "Dompet":
                dompet = pilih("\nPilih dompet:", milik)
                if dompet is None:
                    return "batal"
                baru["dompet"] = dompet
            case "Kategori / sumber":
                kategori = pilih_kategori(user, baru["jenis"], baru["dompet"])
                if kategori is None:
                    return "batal"
                baru["kategori"] = kategori
            case "Jumlah":
                jumlah = input_jumlah()
                if jumlah is None:
                    return "batal"
                baru["jumlah"] = jumlah
            case _:
                break

    bersihkan()
    judul("UBAH TRANSAKSI")
    if baru == asli:
        info("Tidak ada perubahan.")
        return

    semua[index] = baru
    if ada_minus(semua, baca(FILE_DOMPET)):
        gagal("Gagal: saldo dompet jadi minus!")
        return

    simpan(FILE_TRANSAKSI, KOLOM_TRANSAKSI, semua)
    sukses("Data berhasil diperbarui!")


def hapus_data(user):
    judul("HAPUS TRANSAKSI")
    daftar = transaksi_saya(user)
    cetak(daftar)
    if len(daftar) == 0:
        return

    index = pilih_nomor(daftar, "dihapus")
    if index is None:
        return "batal"

    semua = baca(FILE_TRANSAKSI)

    if not konfirmasi("Yakin menghapus?"):
        info("Penghapusan dibatalkan.")
        return

    semua.pop(index)

    if ada_minus(semua, baca(FILE_DOMPET)):
        gagal("Gagal: saldo dompet jadi minus jika data ini dihapus!")
        return

    simpan(FILE_TRANSAKSI, KOLOM_TRANSAKSI, semua)
    sukses("Data berhasil dihapus!")


def hitung_ringkasan(dompets, data):
    """Return (saldo awal, pemasukan, pengeluaran, saldo sekarang)."""
    awal = 0.0
    for d in dompets:
        awal += float(d["saldo_awal"])

    pemasukan = 0.0
    pengeluaran = 0.0
    for t in data:
        if t["jenis"] == "Pemasukan":
            pemasukan += float(t["jumlah"])
        elif t["jenis"] == "Pengeluaran":
            pengeluaran += float(t["jumlah"])

    return awal, pemasukan, pengeluaran, awal + pemasukan - pengeluaran


def urutkan_dari_terbesar(kamus):
    """Ubah dictionary {nama: jumlah} menjadi list [nama, jumlah]
    yang diurutkan dari jumlah terbesar (bubble sort)."""
    hasil = []
    for nama in kamus:
        hasil.append([nama, kamus[nama]])

    for i in range(len(hasil)):
        for j in range(len(hasil) - 1 - i):
            if hasil[j][1] < hasil[j + 1][1]:
                sementara = hasil[j]
                hasil[j] = hasil[j + 1]
                hasil[j + 1] = sementara
    return hasil


def cetak_status_pengeluaran(users, dompets, data):
    """Indikator hemat / normal / boros berdasarkan persen uang yang sudah terpakai."""
    print("\nStatus pengeluaran anak:")
    baris = []
    for u in users:
        nama = u["username"]

        d_user = []
        for d in dompets:
            if d["pemilik"] == nama:
                d_user.append(d)
        t_user = []
        for t in data:
            if t["pemilik"] == nama:
                t_user.append(t)

        awal, pemasukan, pengeluaran, saldo = hitung_ringkasan(d_user, t_user)
        dana = awal + pemasukan

        if dana <= 0:
            baris.append([nama, rupiah(dana), rupiah(pengeluaran), "-",
                          warna("Belum ada dana", DIM)])
            continue

        rasio = pengeluaran / dana
        if rasio >= BATAS_BOROS:
            status = warna("BOROS", RED)
        elif rasio >= BATAS_NORMAL:
            status = warna("NORMAL", YELLOW)
        else:
            status = warna("HEMAT", GREEN)
        baris.append([nama, rupiah(dana), rupiah(pengeluaran),
                      f"{rasio * 100:.1f}%", status])

    tabel(baris, ["Anak", "Total Dana", "Terpakai", "Persen", "Status"],
          ("left", "right", "right", "right", "left"))
    print(warna("Total dana = saldo awal + pemasukan. "
                "Hemat < 50% | Normal 50-79% | Boros >= 80%", DIM))


def cetak_laporan(dompets, data):
    """Tabel ringkasan + pemasukan per sumber + pengeluaran per kategori.
    Dipakai laporan user & admin."""
    awal, pemasukan, pengeluaran, saldo = hitung_ringkasan(dompets, data)

    tabel([["Total Saldo Awal", rupiah(awal)],
           ["Total Pemasukan", warna(rupiah(pemasukan), GREEN)],
           ["Total Pengeluaran", warna(rupiah(pengeluaran), RED)],
           [warna("Saldo Sekarang", BOLD), warna(rupiah(saldo), BOLD)]],
          ["Keterangan", "Jumlah"], ("left", "right"))

    per_kategori = {}
    per_sumber = {}
    for t in data:
        if t["jenis"] == "Pengeluaran":
            per_kategori[t["kategori"]] = per_kategori.get(t["kategori"], 0) + float(t["jumlah"])
        elif t["jenis"] == "Pemasukan":
            if t["kategori"] == "" or t["kategori"] == "-":
                sumber = "Tanpa sumber"
            else:
                sumber = t["kategori"]
            per_sumber[sumber] = per_sumber.get(sumber, 0) + float(t["jumlah"])

    print("\nPemasukan per sumber:")
    if len(per_sumber) == 0:
        info("Belum ada pemasukan.")
    else:
        baris = []
        for item in urutkan_dari_terbesar(per_sumber):
            baris.append([item[0], rupiah(item[1])])
        tabel(baris, ["Sumber", "Jumlah"], ("left", "right"))

    print("\nPengeluaran per kategori:")
    if len(per_kategori) == 0:
        info("Belum ada pengeluaran.")
        return
    baris = []
    for item in urutkan_dari_terbesar(per_kategori):
        baris.append([item[0], rupiah(item[1])])
    tabel(baris, ["Kategori", "Jumlah"], ("left", "right"))


def laporan(user):
    judul(f"LAPORAN KEUANGAN ({user['username']})")
    dompets = dompet_saya(user)
    data = []
    for item in transaksi_saya(user):
        data.append(item[1])
    cetak_laporan(dompets, data)
    cetak_status_pengeluaran([user], dompets, data)


def daftar_user(users):
    """Hanya akun anak (role 'user')."""
    anak = []
    for u in users:
        if u["role"] == "user":
            anak.append(u)
    return anak


def pilih_user(daftar, aksi):
    """Pilih anak dari tabel. None jika batal."""
    nama_anak = []
    for u in daftar:
        nama_anak.append(u["username"])

    nama = pilih(f"Pilih anak yang ingin {aksi}:", nama_anak)
    if nama is None:
        return None

    for u in daftar:
        if u["username"] == nama:
            return u


def statistik_user(user):
    judul("RINGKASAN AKTIVITAS ANAK")
    users = daftar_user(baca(FILE_USER))
    dompets = baca(FILE_DOMPET)
    transaksi = baca(FILE_TRANSAKSI)

    print(f"Jumlah anak      : {warna(len(users), BOLD)}")
    print(f"Jumlah transaksi : {warna(len(transaksi), BOLD)}")
    if len(users) == 0:
        return

    print("\nAktivitas per anak:")
    baris = []
    for u in users:
        n_dompet = 0
        for d in dompets:
            if d["pemilik"] == u["username"]:
                n_dompet += 1
        n_transaksi = 0
        for t in transaksi:
            if t["pemilik"] == u["username"]:
                n_transaksi += 1
        baris.append([u["username"], n_dompet, n_transaksi])
    tabel(baris, ["Username", "Dompet", "Transaksi"], ("left", "right", "right"))


def lihat_semua_akun(admin):
    """Admin melihat username dan password semua akun (anak dan orang tua)."""
    judul("DAFTAR SEMUA USERNAME & PASSWORD")
    users = baca(FILE_USER)
    if len(users) == 0:
        info("Belum ada akun.")
        return

    baris = []
    for no in range(len(users)):
        u = users[no]
        baris.append([no + 1, u["username"], u["password"],
                      ROLE_LABEL.get(u["role"], u["role"])])
    tabel(baris, ["No", "Username", "Password", "Peran"],
          ("right", "left", "left", "left"))
    print(warna("Data ini bersifat rahasia, jangan dilihat orang lain.", DIM))


def ubah_user(user):
    """Admin mengubah username dan/atau password anak."""
    judul("UBAH DATA ANAK")
    users = baca(FILE_USER)
    daftar = daftar_user(users)
    if len(daftar) == 0:
        info("Belum ada anak. Tambah dulu lewat menu Anggota Keluarga.")
        return

    target = pilih_user(daftar, "diubah")
    if target is None:
        return "batal"

    lama = target["username"]
    baru = masukan(f"Username baru (kosongkan = tetap '{lama}'): ")
    if baru is None:
        return "batal"
    if baru == "":
        baru = lama

    if baru != lama and username_ada(users, baru):
        gagal("Username sudah dipakai!")
        return

    password = input_password("Password baru: ", boleh_kosong=True)
    if password is None:
        return "batal"

    if baru == lama and password == "":
        info("Tidak ada perubahan.")
        return

    target["username"] = baru
    if password != "":
        target["password"] = password
    simpan(FILE_USER, KOLOM_USER, users)

    if baru != lama:
        pindah_data_pemilik(lama, baru)
    sukses("Data anak berhasil diubah!")


def hapus_user(user):
    judul("HAPUS AKUN ANAK")
    users = baca(FILE_USER)
    daftar = daftar_user(users)
    if len(daftar) == 0:
        info("Belum ada anak. Tambah dulu lewat menu Anggota Keluarga.")
        return

    target = pilih_user(daftar, "dihapus")
    if target is None:
        return "batal"
    username = target["username"]

    if konfirmasi(f"Hapus {username} beserta dompet, kategori, dan transaksinya?"):
        users.remove(target)
        simpan(FILE_USER, KOLOM_USER, users)

        for item in FILE_DATA_PEMILIK:
            file = item[0]
            kolom = item[1]
            sisa = []
            for r in baca(file):
                if r["pemilik"] != username:
                    sisa.append(r)
            simpan(file, kolom, sisa)
        sukses("Akun anak berhasil dihapus!")
    else:
        info("Penghapusan dibatalkan.")


def laporan_keseluruhan(admin):
    """Laporan gabungan semua anak + ringkasan per anak + status pengeluaran."""
    judul("LAPORAN KESELURUHAN ANAK")
    users = daftar_user(baca(FILE_USER))
    if len(users) == 0:
        info("Belum ada anak. Tambah dulu lewat menu Anggota Keluarga.")
        return

    nama_anak = []
    for u in users:
        nama_anak.append(u["username"])

    dompets = []
    for d in baca(FILE_DOMPET):
        if d["pemilik"] in nama_anak:
            dompets.append(d)
    data = []
    for t in baca(FILE_TRANSAKSI):
        if t["pemilik"] in nama_anak:
            data.append(t)

    print(f"Jumlah anak      : {warna(len(users), BOLD)}")
    print(f"Jumlah transaksi : {warna(len(data), BOLD)}\n")
    cetak_laporan(dompets, data)

    print("\nRingkasan per anak:")
    baris = []
    for u in users:
        d_user = []
        for d in dompets:
            if d["pemilik"] == u["username"]:
                d_user.append(d)
        t_user = []
        for t in data:
            if t["pemilik"] == u["username"]:
                t_user.append(t)

        awal, pemasukan, pengeluaran, saldo = hitung_ringkasan(d_user, t_user)
        baris.append([u["username"], rupiah(pemasukan), rupiah(pengeluaran), rupiah(saldo)])
    tabel(baris, ["Username", "Pemasukan", "Pengeluaran", "Saldo Sekarang"],
          ("left", "right", "right", "right"))

    cetak_status_pengeluaran(users, dompets, data)


def tampil_menu(jejak, user, daftar_menu, tombol_keluar="Kembali"):
    """Cetak banner + tabel menu, lalu kembalikan pilihan user (teks)."""
    bersihkan()
    banner(jejak.upper(), f"Masuk sebagai: {user['username']} ({ROLE_LABEL.get(user['role'], user['role'])})")
    print()
    baris = []
    for no in range(len(daftar_menu)):
        baris.append([no + 1, daftar_menu[no]])
    baris.append([0, warna(tombol_keluar, DIM)])
    tabel(baris, ["No", "Menu"])
    return input("Pilih menu: ").strip()


def selesai_fitur(hasil):
    """Tunggu Enter setelah fitur selesai, kecuali fitur dibatalkan."""
    if hasil != "batal":
        jeda()


def menu_dompet(user, jejak):
    while True:
        pilihan = tampil_menu(jejak, user,
                              ["Dompet & Saldo", "Tambah Dompet",
                               "Ubah Saldo Awal Dompet", "Hapus Dompet"])
        match pilihan:
            case "0":
                break
            case "1":
                bersihkan()
                selesai_fitur(tampil_dompet(user))
            case "2":
                bersihkan()
                selesai_fitur(tambah_dompet(user))
            case "3":
                bersihkan()
                selesai_fitur(ubah_saldo_dompet(user))
            case "4":
                bersihkan()
                selesai_fitur(hapus_dompet(user))
            case _:
                gagal("Pilihan tidak valid!")
                jeda()


def menu_transaksi(user, jejak):
    while True:
        pilihan = tampil_menu(jejak, user,
                              ["Tambah Transaksi", "Tampilkan Transaksi",
                               "Cari Berdasarkan Tanggal", "Ubah Transaksi",
                               "Hapus Transaksi"])
        match pilihan:
            case "0":
                break
            case "1":
                bersihkan()
                selesai_fitur(tambah_data(user))
            case "2":
                bersihkan()
                selesai_fitur(tampilkan_data(user))
            case "3":
                bersihkan()
                selesai_fitur(cari_data(user))
            case "4":
                bersihkan()
                selesai_fitur(ubah_data(user))
            case "5":
                bersihkan()
                selesai_fitur(hapus_data(user))
            case _:
                gagal("Pilihan tidak valid!")
                jeda()


def menu_akun(user, jejak):
    while True:
        pilihan = tampil_menu(jejak, user, ["Ubah Username", "Ubah Password"])
        match pilihan:
            case "0":
                break
            case "1":
                bersihkan()
                selesai_fitur(ubah_username(user))
            case "2":
                bersihkan()
                selesai_fitur(ubah_password(user))
            case _:
                gagal("Pilihan tidak valid!")
                jeda()


def menu_anggota(user, jejak):
    while True:
        pilihan = tampil_menu(jejak, user,
                              ["Ringkasan Aktivitas Anak", "Tambah Anggota",
                               "Ubah Data Anak (username/password)", "Hapus Akun Anak",
                               "Lihat Semua Username & Password"])
        match pilihan:
            case "0":
                break
            case "1":
                bersihkan()
                selesai_fitur(statistik_user(user))
            case "2":
                bersihkan()
                selesai_fitur(tambah_anggota(user))
            case "3":
                bersihkan()
                selesai_fitur(ubah_user(user))
            case "4":
                bersihkan()
                selesai_fitur(hapus_user(user))
            case "5":
                bersihkan()
                selesai_fitur(lihat_semua_akun(user))
            case _:
                gagal("Pilihan tidak valid!")
                jeda()


def menu_anak(user):
    """Menu utama untuk anak (role 'user')."""
    jejak = "Menu Utama"
    while True:
        pilihan = tampil_menu(jejak, user,
                              ["Dompet", "Transaksi", "Laporan", "Akun Saya"],
                              "Logout")
        match pilihan:
            case "0":
                break
            case "1":
                menu_dompet(user, jejak + " > Dompet")
            case "2":
                menu_transaksi(user, jejak + " > Transaksi")
            case "3":
                bersihkan()
                selesai_fitur(laporan(user))
            case "4":
                menu_akun(user, jejak + " > Akun Saya")
            case _:
                gagal("Pilihan tidak valid!")
                jeda()


def menu_admin(user):
    """Menu utama untuk orang tua (role 'admin')."""
    jejak = "Menu Utama"
    while True:
        pilihan = tampil_menu(jejak, user,
                              ["Anggota Keluarga", "Laporan", "Akun Saya"],
                              "Logout")
        match pilihan:
            case "0":
                break
            case "1":
                menu_anggota(user, jejak + " > Anggota Keluarga")
            case "2":
                bersihkan()
                selesai_fitur(laporan_keseluruhan(user))
            case "3":
                menu_akun(user, jejak + " > Akun Saya")
            case _:
                gagal("Pilihan tidak valid!")
                jeda()


def menu_user(user):
    if user["role"] == "admin":
        menu_admin(user)
    else:
        menu_anak(user)


def main():
    os.system("")
    setup_awal()

    while True:
        bersihkan()
        banner("KEUANGAN KELUARGA", datetime.now().strftime("Hari ini: %d-%m-%Y"))
        print()
        tabel([[1, "Login"], [0, warna("Keluar", DIM)]], ["No", "Menu"])

        pilihan = input("Pilih menu: ").strip()

        match pilihan:
            case "1":
                bersihkan()
                user = login()
                if user == "batal":
                    continue
                jeda()
                if user is not None:
                    menu_user(user)
            case "0":
                print("Terima kasih!")
                break
            case _:
                gagal("Pilihan tidak valid!")
                jeda()


if __name__ == "__main__":
    main()