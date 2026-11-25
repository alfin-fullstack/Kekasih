##############################################################################
##############################################################################
##  BAGIAN 1 dari 4  -  FONDASI
##  Isi: import, konstanta, tampilan, input & validasi, file CSV, pencarian kecil
##############################################################################
##############################################################################
import csv  # modul bawaan Python untuk membaca/menulis file CSV
import os  # modul bawaan untuk perintah sistem (hapus layar, cek file ada/tidak)
from datetime import datetime  # untuk mengambil tanggal hari ini

try:  # coba jalankan blok ini dulu
    from tabulate import tabulate, tabulate_formats  # modul luar untuk menampilkan tabel rapi
except ImportError:  # jika modul tabulate belum dipasang, jalankan blok ini
    print("Modul 'tabulate' belum terpasang. Jalankan dulu: pip install tabulate")
    raise SystemExit  # hentikan program

# ---------- KONSTANTA (nilai tetap, ditulis HURUF BESAR) ----------
FILE_USER = "data_user.csv"  # nama file penyimpan akun
FILE_DOMPET = "data_dompet.csv"  # nama file penyimpan dompet
FILE_TRANSAKSI = "data_transaksi.csv"  # nama file penyimpan transaksi
FILE_KATEGORI = "data_kategori.csv"  # nama file penyimpan kategori pengeluaran
FILE_SUMBER = "data_sumber.csv"  # nama file penyimpan sumber pemasukan
KOLOM_USER = ["username", "password", "role"]  # judul kolom di file user
KOLOM_DOMPET = ["pemilik", "dompet", "saldo_awal"]  # judul kolom di file dompet
KOLOM_TRANSAKSI = ["pemilik", "tanggal", "jenis", "dompet", "kategori", "jumlah"]  # kolom file transaksi
KOLOM_KATEGORI = ["pemilik", "kategori"]  # kolom file kategori
KOLOM_SUMBER = ["pemilik", "sumber"]  # kolom file sumber

FILE_DATA_PEMILIK = [  # daftar [file, kolom] yang punya kolom "pemilik"
    [FILE_DOMPET, KOLOM_DOMPET],  # dipakai saat username diganti/dihapus supaya data ikut diproses
    [FILE_TRANSAKSI, KOLOM_TRANSAKSI],
    [FILE_KATEGORI, KOLOM_KATEGORI],
    [FILE_SUMBER, KOLOM_SUMBER],
]

DAFTAR_DOMPET = ["GoPay", "Rekening Bank", "Tunai"]  # saran dompet saat tambah dompet

KATEGORI_DEFAULT = ["Makan & Minum", "Transportasi", "Belanja", "Lainnya"]  # kategori awal user baru

SUMBER_PEMASUKAN = ["Kerja", "Uang saku", "Hadiah"]  # sumber pemasukan awal user baru

ROLE_LABEL = {"admin": "orang tua", "user": "anak"}  # dictionary: nama peran di file -> nama tampilan

MIN_PASSWORD = 6  # panjang minimal password
LEBAR = 30  # lebar garis/banner di layar

BATAS_NORMAL = 0.5  # pengeluaran >= 50% dari dana = NORMAL
BATAS_BOROS = 0.8  # pengeluaran >= 80% dari dana = BOROS

if "rounded_grid" in tabulate_formats:  # pilih gaya tabel terbaik yang didukung versi tabulate
    FORMAT_TABEL = "rounded_grid"
elif "fancy_grid" in tabulate_formats:
    FORMAT_TABEL = "fancy_grid"
else:
    FORMAT_TABEL = "grid"

RESET = "\033[0m"  # kode ANSI: kembalikan warna normal
BOLD = "\033[1m"  # kode ANSI: huruf tebal
DIM = "\033[2m"  # kode ANSI: huruf redup
CYAN = "\033[96m"  # kode ANSI: warna cyan
GREEN = "\033[92m"  # kode ANSI: warna hijau
RED = "\033[91m"  # kode ANSI: warna merah
YELLOW = "\033[93m"  # kode ANSI: warna kuning


# ---------- TAMPILAN ----------

# ARTI warna: membungkus teks dengan kode warna lalu RESET, supaya warna hanya berlaku di teks itu.
def warna(teks, kode):
    return f"{kode}{teks}{RESET}"


# ARTI bersihkan: menghapus isi layar terminal. "cls" untuk Windows, "clear" untuk Linux/Mac.
def bersihkan():
    if os.name == "nt":  # "nt" = Windows
        os.system("cls")
    else:
        os.system("clear")


# ARTI jeda: menahan layar sampai user menekan Enter, supaya hasil sempat dibaca.
def jeda():
    input(warna("\nTekan Enter untuk kembali...", DIM))


# ARTI banner: mencetak kotak judul besar (╔═╗) berisi teks di tengah, plus subteks redup di bawahnya.
def banner(teks, subteks=""):
    print(warna("╔" + "═" * (LEBAR - 2) + "╗", CYAN))  # garis atas
    print(warna("║", CYAN) + warna(teks.center(LEBAR - 2), BOLD) + warna("║", CYAN))  # teks rata tengah
    print(warna("╚" + "═" * (LEBAR - 2) + "╝", CYAN))  # garis bawah
    if subteks != "":  # subteks hanya dicetak kalau diisi
        print(warna(subteks, DIM))


# ARTI judul: mencetak judul bagian fitur diapit garis, dan pengingat bahwa 'batal' bisa diketik.
def judul(teks):
    print()
    print(warna("─" * LEBAR, DIM))
    print(warna(f" {teks}", BOLD + CYAN))
    print(warna("─" * LEBAR, DIM))
    print(warna("Ketik 'batal' kapan saja untuk kembali\n", DIM))


# ARTI sukses: mencetak pesan berhasil berwarna hijau.
def sukses(teks):
    print(warna(teks, GREEN))


# ARTI gagal: mencetak pesan error berwarna merah.
def gagal(teks):
    print(warna(teks, RED))


# ARTI info: mencetak pesan pemberitahuan berwarna kuning dengan tanda titik (•).
def info(teks):
    print(warna(f"• {teks}", YELLOW))


# ARTI tabel: mencetak data (list of list) sebagai tabel rapi memakai tabulate.
# baris = isi tabel, header = judul kolom, rata = rata kiri/kanan tiap kolom.
def tabel(baris, header, rata=None):
    header_warna = []
    for h in header:  # beri warna pada setiap judul kolom
        header_warna.append(warna(h, BOLD + CYAN))
    print(tabulate(baris, headers=header_warna, tablefmt=FORMAT_TABEL,
                   colalign=rata, disable_numparse=True))  # disable_numparse: angka tidak diubah-ubah


# ARTI rupiah: mengubah angka jadi tulisan uang, contoh 1500000 -> "Rp 1,500,000.00".
def rupiah(angka):
    return f"Rp {float(angka):,.2f}"  # ,.2f = pemisah ribuan + 2 angka desimal


# ARTI warna_jenis: "Pemasukan" diwarnai hijau, selain itu (Pengeluaran) merah.
def warna_jenis(jenis):
    if jenis == "Pemasukan":
        return warna(jenis, GREEN)
    return warna(jenis, RED)


# ---------- INPUT & VALIDASI ----------

# ARTI masukan: pengganti input() biasa. Jika user mengetik 'batal' hasilnya None (tanda batal).
# strip=True artinya spasi di awal/akhir dibuang (untuk password dipakai strip=False).
def masukan(teks, strip=True):
    """input() biasa. Mengetik 'batal' mengembalikan None (= batal)."""
    nilai = input(teks)
    if nilai.strip().lower() == "batal":  # lower() agar BATAL/Batal juga terbaca
        return None
    if strip:
        return nilai.strip()
    return nilai


# ARTI konfirmasi: bertanya y/n. Mengembalikan True hanya jika user mengetik "y".
def konfirmasi(teks):
    jawaban = input(f"{teks} (y/n): ").strip().lower()
    return jawaban == "y"


# ARTI pilih_index: menampilkan pilihan bernomor, lalu user memilih nomor.
# Mengembalikan posisi (index) pilihan, atau None jika user memilih 0 / mengetik batal.
def pilih_index(teks, pilihan, batal="Kembali"):
    """Tampilkan pilihan bernomor + 0 untuk kembali.
    Mengembalikan index pilihan, atau None jika batal."""
    print(teks)
    baris = []
    for no in range(len(pilihan)):
        baris.append([no + 1, pilihan[no]])  # nomor dimulai dari 1 agar enak dibaca
    baris.append([0, warna(batal, DIM)])  # nomor 0 selalu untuk kembali
    tabel(baris, ["No", "Pilihan"])
    while True:  # ulang terus sampai input valid
        nomor = input("Pilih nomor: ").strip()
        if nomor == "0" or nomor.lower() == "batal":
            return None
        if nomor.isdigit() and 1 <= int(nomor) <= len(pilihan):  # harus angka dan dalam rentang
            return int(nomor) - 1  # dikurangi 1 karena list dimulai dari 0
        gagal("Pilihan tidak valid!")


# ARTI pilih: sama seperti pilih_index, tetapi yang dikembalikan ISI pilihannya (teks), bukan nomornya.
def pilih(teks, pilihan, batal="Kembali"):
    """Sama seperti pilih_index, tetapi mengembalikan ISI pilihan (None jika batal)."""
    index = pilih_index(teks, pilihan, batal)
    if index is None:
        return None
    return pilihan[index]


# ARTI tanggal_valid: cek apakah teks tanggal berformat DD-MM-YYYY dan benar-benar ada di kalender
# (misal 30-02-2026 ditolak, 29-02 hanya valid di tahun kabisat).
def tanggal_valid(tanggal):
    """True jika tanggal berformat DD-MM-YYYY dan benar-benar ada di kalender."""
    bagian = tanggal.split("-")  # pecah "25-12-2026" menjadi ["25", "12", "2026"]
    if len(bagian) != 3:  # harus tepat 3 bagian
        return False

    hari = bagian[0]
    bulan = bagian[1]
    tahun = bagian[2]
    if not (hari.isdigit() and bulan.isdigit() and tahun.isdigit()):  # semua harus angka
        return False
    if len(hari) > 2 or len(bulan) > 2 or len(tahun) != 4:  # tahun harus 4 digit
        return False

    hari = int(hari)  # ubah teks menjadi angka bulat
    bulan = int(bulan)
    tahun = int(tahun)
    if tahun < 1 or bulan < 1 or bulan > 12:
        return False

    hari_per_bulan = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]  # jumlah hari tiap bulan
    kabisat = (tahun % 4 == 0 and tahun % 100 != 0) or tahun % 400 == 0  # rumus tahun kabisat
    if kabisat:
        hari_per_bulan[1] = 29  # Februari jadi 29 hari
    return 1 <= hari <= hari_per_bulan[bulan - 1]  # hari harus ada di bulan tersebut


# ARTI input_tanggal: meminta tanggal sampai valid. Dikosongkan = otomatis tanggal hari ini.
def input_tanggal(teks="Tanggal (DD-MM-YYYY, kosongkan = hari ini): "):
    while True:
        tanggal = masukan(teks)
        if tanggal is None:  # user batal
            return None
        if tanggal == "":  # kosong -> pakai tanggal hari ini
            tanggal = datetime.now().strftime("%d-%m-%Y")  # strftime = ubah tanggal jadi teks
            info(f"Memakai tanggal hari ini: {tanggal}")
            return tanggal
        if tanggal_valid(tanggal):
            return tanggal
        gagal("Format tanggal salah! Contoh: 25-12-2026")


# ARTI adalah_angka: True jika teks bisa dijadikan angka desimal (boleh diawali + atau -, satu titik).
def adalah_angka(teks):
    """True jika teks bisa diubah menjadi angka desimal (boleh diawali + atau -)."""
    if teks == "":
        return False
    angka = teks
    if angka[0] == "+" or angka[0] == "-":  # buang tanda di depan
        angka = angka[1:]
    # titik maksimal 1, dan sisanya harus digit semua
    return angka.count(".") <= 1 and angka.replace(".", "", 1).isdigit()


# ARTI input_jumlah: meminta nominal uang sampai valid (harus angka dan > 0).
# boleh_nol=True dipakai untuk saldo awal yang boleh 0.
def input_jumlah(teks="Jumlah uang: ", boleh_nol=False):
    while True:
        isi = masukan(teks)
        if isi is None:
            return None
        if not adalah_angka(isi):
            gagal("Jumlah harus berupa angka!")
            continue  # lompat ke putaran berikutnya (minta input lagi)
        jumlah = float(isi)  # float = angka desimal
        if jumlah > 0 or (boleh_nol and jumlah == 0):
            return jumlah
        gagal("Jumlah tidak valid!")


# ARTI cek_password: memeriksa aturan password (min 6 karakter, ada huruf besar, ada angka).
# Mengembalikan 2 nilai: (True/False, pesan error).
def cek_password(password):
    """Return (valid, pesan). Wajib: min. 6 karakter, ada huruf besar dan angka."""
    ada_besar = False  # penanda: sudah ketemu huruf besar?
    ada_angka = False  # penanda: sudah ketemu angka?
    for huruf in password:  # periksa karakter satu per satu
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


# ARTI input_password: meminta password sampai lolos cek_password.
# boleh_kosong=True dipakai saat admin mengubah data anak (kosong = password tidak diubah).
def input_password(teks="Password baru: ", boleh_kosong=False):
    """Minta password sampai valid.
    Return None jika batal, atau "" jika boleh_kosong dan dikosongkan."""
    pesan = f"Min. {MIN_PASSWORD} karakter, kombinasi huruf besar & angka"
    if boleh_kosong:
        pesan += " (kosongkan = tidak diubah)"
    info(pesan)
    while True:
        password = masukan(teks, strip=False)  # strip=False: spasi pada password tidak dibuang
        if password is None:
            return None
        if password == "" and boleh_kosong:
            return ""
        valid, pesan_error = cek_password(password)  # menerima 2 nilai sekaligus
        if valid:
            return password
        gagal(pesan_error)


# ---------- FILE CSV ----------

# ARTI baca: membaca file CSV menjadi list of dictionary (tiap baris = 1 dictionary).
# Contoh hasil: [{"username": "budi", "password": "Abc123", "role": "user"}, ...]
def baca(file):
    """Membaca file CSV menjadi list of dictionary. File belum ada -> list kosong."""
    if not os.path.exists(file):  # file belum dibuat -> kembalikan list kosong
        return []
    with open(file, newline="") as f:  # "with" otomatis menutup file setelah selesai
        return list(csv.DictReader(f))  # DictReader: baris pertama jadi nama kunci


# ARTI simpan: menulis ulang SELURUH isi file CSV dari list of dictionary.
# Cara kerja semua fitur: baca -> ubah di memori -> simpan lagi.
def simpan(file, kolom, data):
    """Menulis ulang seluruh isi file CSV dari list of dictionary."""
    with open(file, "w", newline="") as f:  # "w" = tulis, isi lama ditimpa
        writer = csv.DictWriter(f, fieldnames=kolom)
        writer.writeheader()  # tulis baris judul kolom
        writer.writerows(data)  # tulis semua baris data


# ARTI pindah_data_pemilik: saat username berganti (lama -> baru), semua data milik username lama
# (dompet, transaksi, kategori, sumber) dipindahkan ke username baru.
def pindah_data_pemilik(lama, baru):
    """Dipakai saat username berubah: dompet, transaksi, kategori, sumber ikut pindah."""
    for item in FILE_DATA_PEMILIK:  # ulangi untuk ke-4 file
        file = item[0]
        kolom = item[1]
        data = baca(file)
        for row in data:
            if row["pemilik"] == lama:
                row["pemilik"] = baru
        simpan(file, kolom, data)


# ---------- FUNGSI PENCARIAN KECIL ----------

# ARTI ada_admin: True jika sudah ada minimal 1 akun orang tua (admin).
def ada_admin(users):
    for u in users:
        if u["role"] == "admin":
            return True
    return False


# ARTI username_ada: True jika username sudah dipakai akun lain.
def username_ada(users, username):
    for u in users:
        if u["username"] == username:
            return True
    return False


# ARTI cari_nama: mencari nama di list tanpa peduli huruf besar/kecil.
# Mengembalikan nama aslinya jika ketemu, None jika tidak ada.
def cari_nama(daftar, nama):
    """Cari nama di list tanpa membedakan huruf besar/kecil. None jika tidak ada."""
    for d in daftar:
        if d.lower() == nama.lower():
            return d
    return None


##############################################################################
##  >>> AKHIR BAGIAN 1 <<<
##############################################################################


##############################################################################
##############################################################################
##  BAGIAN 2 dari 4  -  AKUN, DOMPET, KATEGORI
##  Isi: setup, tambah anggota, login, ubah akun; dompet; kategori & sumber
##############################################################################
##############################################################################

# ---------- AKUN ----------

# ARTI setup_awal: dijalankan sekali di awal program. Jika belum ada akun orang tua,
# paksa membuat akun admin pertama (ayah/ibu). Jika sudah ada, langsung selesai.
def setup_awal():
    """Jika belum ada akun orang tua (admin), buat akun pertama (ayah/ibu)."""
    users = baca(FILE_USER)
    if ada_admin(users):  # sudah ada admin -> tidak perlu setup
        return

    bersihkan()
    banner("SETUP AWAL KEUANGAN KELUARGA")
    print("\nBelum ada akun orang tua. Buat akun pertama (ayah/ibu) sebagai admin.")
    print("Akun anak dan akun orang tua lainnya dibuat dari menu admin.\n")

    while True:  # ulang sampai username valid
        username = input("Username: ").strip()
        if username == "":
            gagal("Username tidak boleh kosong!")
        elif username_ada(users, username):
            gagal("Username sudah dipakai!")
        else:
            break  # username valid, keluar dari loop

    while True:  # ulang sampai password valid (setup tidak boleh dibatalkan)
        password = input_password("Password: ")
        if password is None:
            gagal("Setup awal wajib diselesaikan.")
        else:
            break

    users.append({"username": username, "password": password, "role": "admin"})
    simpan(FILE_USER, KOLOM_USER, users)
    sukses(f"Akun orang tua {username} berhasil dibuat!")
    jeda()


# ARTI tambah_anggota: orang tua membuat akun baru, jenisnya anak (role "user") atau orang tua lain (role "admin").
def tambah_anggota(admin):
    """Orang tua membuat akun anggota keluarga (anak atau orang tua lain)."""
    judul("TAMBAH ANGGOTA KELUARGA")
    users = baca(FILE_USER)
    jenis = pilih("Jenis akun:", ["Anak", "Orang tua (admin)"])
    if jenis is None:
        return "batal"  # "batal" = sinyal agar menu tidak meminta Enter

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

    users.append({"username": username, "password": password, "role": role})  # tambah ke list
    simpan(FILE_USER, KOLOM_USER, users)  # simpan ke file
    sukses(f"Akun {username} ({ROLE_LABEL[role]}) berhasil dibuat!")


# ARTI login: meminta username & password, dicocokkan dengan data akun. Maksimal 3 kali coba.
# Mengembalikan data akun (dictionary) jika berhasil, None jika gagal 3x, "batal" jika dibatalkan.
def login():
    """Return dictionary user jika berhasil, None jika 3x gagal, "batal" jika dibatalkan."""
    judul("LOGIN")
    users = baca(FILE_USER)

    for percobaan in range(3):  # kesempatan 3 kali
        username = masukan("Username: ")
        if username is None:
            return "batal"
        password = masukan("Password: ", strip=False)
        if password is None:
            return "batal"

        for u in users:  # cari akun yang username & password-nya cocok
            if u["username"] == username and u["password"] == password:
                sukses(f"Login berhasil! Selamat datang, {username} ({ROLE_LABEL.get(u['role'], u['role'])}).")
                return u
        gagal("Username atau password salah!")

    gagal("Terlalu banyak percobaan.")
    return None


# ARTI ubah_username: user/admin mengganti username miliknya sendiri.
# Data dompet/transaksi/dst ikut dipindah ke username baru lewat pindah_data_pemilik.
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
    pindah_data_pemilik(lama, baru)  # dompet, transaksi, dll ikut pindah
    user["username"] = baru  # perbarui sesi yang sedang berjalan
    sukses(f"Username berhasil diubah menjadi {baru}!")


# ARTI ubah_password: mengganti password sendiri. Wajib mengetik password lama dulu (keamanan).
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
    user["password"] = baru  # perbarui sesi yang sedang berjalan
    sukses("Password berhasil diubah!")


# ---------- DOMPET (USER) ----------

# ARTI dompet_saya: mengambil semua data dompet milik user yang sedang login (list of dictionary).
def dompet_saya(user):
    hasil = []
    for d in baca(FILE_DOMPET):
        if d["pemilik"] == user["username"]:
            hasil.append(d)
    return hasil


# ARTI dompet_milik: sama seperti dompet_saya, tetapi hanya NAMA dompetnya saja (list teks).
def dompet_milik(user):
    nama = []
    for d in dompet_saya(user):
        nama.append(d["dompet"])
    return nama


# ARTI hitung_saldo: saldo sekarang sebuah dompet = saldo awal + semua pemasukan - semua pengeluaran.
def hitung_saldo(dompet, transaksi):
    """Saldo sekarang = saldo awal + pemasukan - pengeluaran."""
    saldo = float(dompet["saldo_awal"])
    for t in transaksi:
        if t["pemilik"] == dompet["pemilik"] and t["dompet"] == dompet["dompet"]:  # hanya transaksi dompet ini
            jumlah = float(t["jumlah"])
            if t["jenis"] == "Pemasukan":
                saldo += jumlah
            else:
                saldo -= jumlah
    return saldo


# ARTI ada_minus: True jika ada dompet yang saldonya negatif. Dipakai untuk mencegah saldo minus.
def ada_minus(transaksi, dompets):
    """True jika ada dompet yang saldonya jadi minus."""
    for d in dompets:
        if round(hitung_saldo(d, transaksi), 2) < 0:  # round agar tidak salah karena selisih desimal kecil
            return True
    return False


# ARTI saldo_dompet: saldo sekarang untuk satu dompet tertentu milik user.
def saldo_dompet(user, nama):
    """Saldo sekarang untuk satu dompet milik user (None jika dompet tidak ditemukan)."""
    transaksi = baca(FILE_TRANSAKSI)
    for d in dompet_saya(user):
        if d["dompet"] == nama:
            return hitung_saldo(d, transaksi)
    return None


# ARTI tampil_dompet: menampilkan tabel semua dompet user beserta saldo awal, saldo sekarang, dan TOTAL.
def tampil_dompet(user):
    judul(f"DOMPET & SALDO ({user['username']})")
    dompets = dompet_saya(user)
    if len(dompets) == 0:
        info("Belum ada data dompet.")
        return

    transaksi = baca(FILE_TRANSAKSI)
    total = 0.0  # penampung jumlah seluruh saldo
    baris = []
    for d in dompets:
        sekarang = hitung_saldo(d, transaksi)
        total += sekarang
        baris.append([d["dompet"], rupiah(d["saldo_awal"]), rupiah(sekarang)])
    baris.append([warna("TOTAL", BOLD), "", warna(rupiah(total), BOLD)])  # baris terakhir = total
    tabel(baris, ["Dompet", "Saldo Awal", "Saldo Sekarang"], ("left", "right", "right"))


# ARTI tambah_dompet: user menambah dompet baru (pilih dari saran atau ketik sendiri) lalu mengisi saldo awal.
def tambah_dompet(user):
    judul("TAMBAH DOMPET")
    dompets = baca(FILE_DOMPET)
    milik = dompet_milik(user)

    nama = None
    saran = []
    for d in DAFTAR_DOMPET:  # saran hanya dompet yang belum dimiliki
        if d not in milik:
            saran.append(d)

    if len(saran) > 0:
        lain = "Dompet lain (ketik nama sendiri)"
        pilihan = pilih("Pilih dompet:", saran + [lain])  # menggabungkan 2 list dengan +
        if pilihan is None:
            return "batal"
        if pilihan != lain:
            nama = pilihan

    if nama is None:  # user memilih ketik sendiri atau semua saran sudah dimiliki
        nama = masukan("Nama dompet: ")
        if nama is None:
            return "batal"

    if nama == "":
        gagal("Nama dompet tidak boleh kosong!")
        return
    if cari_nama(milik, nama) is not None:  # cegah nama dompet kembar
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


# ARTI ubah_saldo_dompet: mengganti saldo awal sebuah dompet. Ditolak jika membuat saldo jadi minus.
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
    target = None  # dompet yang akan diubah
    for d in dompets:
        if d["pemilik"] == user["username"] and d["dompet"] == nama:
            target = d
    print(f"Saldo awal {nama} saat ini: {rupiah(target['saldo_awal'])}")

    saldo_baru = input_jumlah("Saldo awal baru: ", boleh_nol=True)
    if saldo_baru is None:
        return "batal"
    target["saldo_awal"] = saldo_baru

    if ada_minus(baca(FILE_TRANSAKSI), dompets):  # cek dulu sebelum disimpan
        gagal("Gagal: saldo awal terlalu kecil, saldo dompet jadi minus!")
        return

    simpan(FILE_DOMPET, KOLOM_DOMPET, dompets)
    sukses("Saldo awal berhasil diubah!")


# ARTI hapus_dompet: menghapus satu dompet BESERTA semua transaksinya (setelah konfirmasi y/n).
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
    jumlah = 0  # hitung berapa transaksi yang ikut terhapus
    for t in transaksi:
        if t["pemilik"] == user["username"] and t["dompet"] == nama:
            jumlah += 1

    if not konfirmasi(f"Hapus dompet {nama} beserta {jumlah} transaksinya?"):
        info("Penghapusan dibatalkan.")
        return

    dompet_sisa = []  # cara menghapus: kumpulkan yang TIDAK dihapus, lalu simpan
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


# ---------- KATEGORI & SUMBER ----------

# ARTI ambil_daftar: mengambil daftar pilihan milik user (kategori atau sumber).
# User baru yang belum punya otomatis diberi daftar default lalu disimpan.
def ambil_daftar(user, file, kolom, field, default):
    """Daftar pilihan milik user. User baru otomatis dapat daftar default."""
    data = baca(file)
    milik = []
    for r in data:
        if r["pemilik"] == user["username"]:
            milik.append(r[field])

    if len(milik) == 0:  # user belum punya -> isi dengan default
        for d in default:
            data.append({"pemilik": user["username"], field: d})
            milik.append(d)
        simpan(file, kolom, data)
    return milik


# ARTI kategori_milik: daftar kategori pengeluaran milik user (memanggil ambil_daftar).
def kategori_milik(user):
    return ambil_daftar(user, FILE_KATEGORI, KOLOM_KATEGORI, "kategori", KATEGORI_DEFAULT)


# ARTI sumber_milik: daftar sumber pemasukan milik user (memanggil ambil_daftar).
def sumber_milik(user):
    return ambil_daftar(user, FILE_SUMBER, KOLOM_SUMBER, "sumber", SUMBER_PEMASUKAN)


# ARTI pilih_kategori: user memilih kategori pengeluaran / sumber pemasukan (tergantung jenis),
# atau menambah yang baru langsung dari sini. Jika dompet diberikan, sisa saldonya ditampilkan dulu.
def pilih_kategori(user, jenis, dompet=None):
    """Pilih kategori pengeluaran / sumber pemasukan, atau tambah yang baru dari sini.
    Jika dompet diberikan, sisa saldo dompet itu ditampilkan dulu.
    Mengembalikan nama pilihan, atau None jika batal."""
    if jenis == "Pemasukan":  # siapkan variabel sesuai jenis transaksi
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

    if dompet:  # tampilkan sisa saldo supaya user tahu uangnya cukup atau tidak
        saldo = saldo_dompet(user, dompet)
        if saldo is not None:
            print(f"\nSisa saldo {dompet}: {warna(rupiah(saldo), BOLD)}")

    tambah = warna("+ Tambah baru (ketik sendiri)", GREEN)  # pilihan terakhir di daftar
    pilihan = pilih(teks, daftar + [tambah])
    if pilihan is None:
        return None
    if pilihan != tambah:
        return pilihan  # user memilih yang sudah ada

    while True:  # user memilih tambah baru
        nama = masukan("Nama baru: ")
        if nama is None:
            return None
        if nama == "":
            gagal("Nama tidak boleh kosong!")
            continue

        ada = cari_nama(daftar, nama)
        if ada is not None:  # sudah ada -> pakai yang lama, jangan dobel
            info(f"'{ada}' sudah ada, memakai yang sudah ada.")
            return ada

        data = baca(file)
        data.append({"pemilik": user["username"], field: nama})
        simpan(file, kolom, data)
        sukses(f"'{nama}' berhasil ditambahkan dan dipilih!")
        return nama


##############################################################################
##  >>> AKHIR BAGIAN 2 <<<
##############################################################################


##############################################################################
##############################################################################
##  BAGIAN 3 dari 4  -  TRANSAKSI & LAPORAN
##  Isi: tambah/tampil/cari/ubah/hapus transaksi; laporan; status hemat-boros
##############################################################################
##############################################################################

# ---------- TRANSAKSI (USER) ----------

# ARTI transaksi_saya: mengambil transaksi milik user dalam bentuk [index asli di file, transaksi].
# Index asli disimpan karena nomor di layar (1,2,3..) berbeda dengan posisi di file saat ubah/hapus.
def transaksi_saya(user):
    """Daftar [index asli, transaksi] milik user."""
    semua = baca(FILE_TRANSAKSI)
    hasil = []
    for i in range(len(semua)):
        if semua[i]["pemilik"] == user["username"]:
            hasil.append([i, semua[i]])
    return hasil


# ARTI cetak: menampilkan daftar transaksi dalam tabel (tanpa kolom saldo).
# Dipakai di cari tanggal, ubah, dan hapus.
def cetak(daftar):
    if len(daftar) == 0:
        info("Data tidak ditemukan.")
        return

    baris = []
    nomor = 1  # nomor urut di layar
    for item in daftar:
        t = item[1]  # item[0] = index asli, item[1] = datanya
        baris.append([nomor, t["tanggal"], warna_jenis(t["jenis"]), t["dompet"],
                      t["kategori"], rupiah(t["jumlah"])])
        nomor += 1
    tabel(baris, ["No", "Tanggal", "Jenis", "Dompet", "Kategori / Sumber", "Jumlah"],
          ("right", "left", "left", "left", "left", "right"))


# ARTI cetak_dengan_saldo: seperti cetak, tetapi ada kolom "Sisa Saldo" = saldo dompet setelah tiap transaksi
# (dihitung berurutan dari saldo awal), dan total sisa saldo semua dompet di bawah tabel.
def cetak_dengan_saldo(user, daftar):
    """Seperti cetak(), tetapi ada kolom sisa saldo dompet setelah tiap transaksi
    (dihitung berurutan sesuai urutan data) dan total sisa saldo di bawah tabel."""
    if len(daftar) == 0:
        info("Data tidak ditemukan.")
        return

    saldo = {}  # dictionary {nama dompet: saldo berjalan}
    for d in dompet_saya(user):
        saldo[d["dompet"]] = float(d["saldo_awal"])  # mulai dari saldo awal

    baris = []
    nomor = 1
    for item in daftar:
        t = item[1]
        nama = t["dompet"]
        if nama not in saldo:
            saldo[nama] = 0.0
        if t["jenis"] == "Pemasukan":  # pemasukan menambah, pengeluaran mengurangi
            saldo[nama] += float(t["jumlah"])
        else:
            saldo[nama] -= float(t["jumlah"])
        baris.append([nomor, t["tanggal"], warna_jenis(t["jenis"]), nama,
                      t["kategori"], rupiah(t["jumlah"]), rupiah(saldo[nama])])
        nomor += 1
    tabel(baris, ["No", "Tanggal", "Jenis", "Dompet", "Kategori / Sumber", "Jumlah", "Sisa Saldo"],
          ("right", "left", "left", "left", "left", "right", "right"))

    total = 0.0
    for nama in saldo:  # menjumlahkan saldo semua dompet
        total += saldo[nama]
    print(f"\nTotal sisa saldo semua dompet: {warna(rupiah(total), BOLD)}")


# ARTI pilih_nomor: user memilih nomor baris dari tabel (untuk diubah/dihapus).
# Mengembalikan index ASLI di file, atau None jika batal / mengetik 0.
def pilih_nomor(daftar, aksi):
    """Pilih nomor data dari tabel. 0 = kembali (None).
    Mengembalikan index ASLI di file."""
    while True:
        nomor = masukan(f"Nomor data yang ingin {aksi} (0 = kembali): ")
        if nomor is None or nomor == "0":
            return None
        if nomor.isdigit() and 1 <= int(nomor) <= len(daftar):
            return daftar[int(nomor) - 1][0]  # ambil index asli dari item
        gagal("Nomor tidak valid!")


# ARTI pilih_jenis: memilih jenis transaksi (Pemasukan/Pengeluaran). Jika jenis berubah,
# kategori/sumber harus dipilih ulang karena daftarnya berbeda. True = selesai, False = batal.
def pilih_jenis(user, transaksi):
    """Pilih jenis; kategori/sumber ikut menyesuaikan. Dipakai tambah & ubah transaksi.
    Return True jika selesai, False jika dibatalkan."""
    jenis_lama = transaksi.get("jenis")  # .get -> None jika belum ada (transaksi baru)
    jenis = pilih("\nJenis transaksi:", ["Pemasukan", "Pengeluaran"])
    if jenis is None:
        return False

    transaksi["jenis"] = jenis
    if jenis == jenis_lama:  # jenis tidak berubah -> kategori lama masih cocok
        return True

    kategori = pilih_kategori(user, jenis, transaksi.get("dompet"))
    if kategori is None:
        return False
    transaksi["kategori"] = kategori
    return True


# ARTI tambah_data: menambah transaksi baru. Urutan: pilih dompet -> jenis -> kategori -> tanggal -> jumlah.
# Ditolak jika saldo dompet jadi minus.
def tambah_data(user):
    judul("TAMBAH TRANSAKSI")
    milik = dompet_milik(user)
    if len(milik) == 0:
        info("Anda belum punya dompet. Tambah dulu lewat menu Dompet > Tambah Dompet.")
        return

    transaksi = {"pemilik": user["username"]}  # dictionary yang diisi bertahap

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
    if ada_minus(semua, baca(FILE_DOMPET)):  # cek saldo SEBELUM disimpan
        gagal("Gagal: saldo dompet tidak cukup!")
        return

    simpan(FILE_TRANSAKSI, KOLOM_TRANSAKSI, semua)
    sukses("Transaksi berhasil ditambahkan!")


# ARTI tampilkan_data: menampilkan semua transaksi user lengkap dengan kolom sisa saldo.
def tampilkan_data(user):
    judul("DAFTAR TRANSAKSI")
    cetak_dengan_saldo(user, transaksi_saya(user))


# ARTI cari_data: mencari transaksi berdasarkan tanggal (kosong = hari ini), hasilnya dicetak.
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


# ARTI ubah_data: mengubah transaksi. User memilih nomor, lalu memilih BAGIAN yang diubah
# (bisa berkali-kali) sampai memilih "Simpan perubahan". Perubahan dikerjakan di salinan (baru)
# dan baru disimpan jika saldo tidak minus.
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
    asli = semua[index]  # data sebelum diubah
    baru = dict(asli)  # salinan yang akan diedit (dict() membuat salinan)

    while True:  # menu pilih bagian yang diubah
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

        match bagian:  # match-case: seperti if-elif, mencocokkan nilai "bagian"
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
            case _:  # pilihan lain = "Simpan perubahan"
                break  # keluar dari while

    bersihkan()
    judul("UBAH TRANSAKSI")
    if baru == asli:  # tidak ada yang berubah
        info("Tidak ada perubahan.")
        return

    semua[index] = baru  # timpa data lama dengan data baru
    if ada_minus(semua, baca(FILE_DOMPET)):
        gagal("Gagal: saldo dompet jadi minus!")
        return

    simpan(FILE_TRANSAKSI, KOLOM_TRANSAKSI, semua)
    sukses("Data berhasil diperbarui!")


# ARTI hapus_data: menghapus satu transaksi setelah konfirmasi. Ditolak jika penghapusan membuat saldo minus
# (misal menghapus pemasukan yang uangnya sudah terpakai).
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

    semua.pop(index)  # pop(index) = buang item pada posisi index dari list

    if ada_minus(semua, baca(FILE_DOMPET)):
        gagal("Gagal: saldo dompet jadi minus jika data ini dihapus!")
        return

    simpan(FILE_TRANSAKSI, KOLOM_TRANSAKSI, semua)
    sukses("Data berhasil dihapus!")


# ---------- LAPORAN & STATUS PENGELUARAN ----------

# ARTI hitung_ringkasan: menghitung total saldo awal, pemasukan, pengeluaran, dan saldo sekarang.
# Mengembalikan 4 nilai sekaligus (tuple).
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


# ARTI urutkan_dari_terbesar: mengubah dictionary {nama: jumlah} menjadi list [nama, jumlah]
# yang terurut dari jumlah terbesar, memakai algoritma bubble sort (bandingkan tetangga, tukar jika salah urut).
def urutkan_dari_terbesar(kamus):
    """Ubah dictionary {nama: jumlah} menjadi list [nama, jumlah]
    yang diurutkan dari jumlah terbesar (bubble sort)."""
    hasil = []
    for nama in kamus:  # mengulang dictionary = mengulang kunci (nama)
        hasil.append([nama, kamus[nama]])

    for i in range(len(hasil)):  # bubble sort
        for j in range(len(hasil) - 1 - i):
            if hasil[j][1] < hasil[j + 1][1]:  # kalau kiri lebih kecil dari kanan -> tukar
                sementara = hasil[j]
                hasil[j] = hasil[j + 1]
                hasil[j + 1] = sementara
    return hasil


# ARTI cetak_status_pengeluaran: menampilkan status HEMAT / NORMAL / BOROS tiap anak.
# Rumus: persen = pengeluaran / (saldo awal + pemasukan). <50% hemat, 50-79% normal, >=80% boros.
def cetak_status_pengeluaran(users, dompets, data):
    """Indikator hemat / normal / boros berdasarkan persen uang yang sudah terpakai."""
    print("\nStatus pengeluaran anak:")
    baris = []
    for u in users:
        nama = u["username"]

        d_user = []  # dompet milik anak ini saja
        for d in dompets:
            if d["pemilik"] == nama:
                d_user.append(d)
        t_user = []  # transaksi milik anak ini saja
        for t in data:
            if t["pemilik"] == nama:
                t_user.append(t)

        awal, pemasukan, pengeluaran, saldo = hitung_ringkasan(d_user, t_user)
        dana = awal + pemasukan  # total dana yang pernah dimiliki

        if dana <= 0:  # hindari pembagian dengan nol
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
                      f"{rasio * 100:.1f}%", status])  # rasio dikali 100 jadi persen

    tabel(baris, ["Anak", "Total Dana", "Terpakai", "Persen", "Status"],
          ("left", "right", "right", "right", "left"))
    print(warna("Total dana = saldo awal + pemasukan. "
                "Hemat < 50% | Normal 50-79% | Boros >= 80%", DIM))


# ARTI cetak_laporan: menampilkan tabel ringkasan, pemasukan per sumber, dan pengeluaran per kategori.
# Dipakai bersama oleh laporan anak dan laporan admin.
def cetak_laporan(dompets, data):
    """Tabel ringkasan + pemasukan per sumber + pengeluaran per kategori.
    Dipakai laporan user & admin."""
    awal, pemasukan, pengeluaran, saldo = hitung_ringkasan(dompets, data)

    tabel([["Total Saldo Awal", rupiah(awal)],
           ["Total Pemasukan", warna(rupiah(pemasukan), GREEN)],
           ["Total Pengeluaran", warna(rupiah(pengeluaran), RED)],
           [warna("Saldo Sekarang", BOLD), warna(rupiah(saldo), BOLD)]],
          ["Keterangan", "Jumlah"], ("left", "right"))

    per_kategori = {}  # dictionary {kategori: total pengeluaran}
    per_sumber = {}  # dictionary {sumber: total pemasukan}
    for t in data:
        if t["jenis"] == "Pengeluaran":
            # .get(kunci, 0) = ambil nilai lama, kalau belum ada pakai 0, lalu ditambah jumlah baru
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
        for item in urutkan_dari_terbesar(per_sumber):  # terbesar di atas
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


# ARTI laporan: laporan keuangan pribadi anak = cetak_laporan + status hemat/boros miliknya sendiri.
def laporan(user):
    judul(f"LAPORAN KEUANGAN ({user['username']})")
    dompets = dompet_saya(user)
    data = []
    for item in transaksi_saya(user):
        data.append(item[1])  # ambil datanya saja (buang index)
    cetak_laporan(dompets, data)
    cetak_status_pengeluaran([user], dompets, data)


##############################################################################
##  >>> AKHIR BAGIAN 3 <<<
##############################################################################


##############################################################################
##############################################################################
##  BAGIAN 4 dari 4  -  ADMIN, MENU, MAIN
##  Isi: fitur khusus admin; menu match-case; program utama
##############################################################################
##############################################################################

# ---------- KHUSUS ADMIN ----------

# ARTI daftar_user: menyaring akun, hanya yang role-nya "user" (anak). Akun orang tua dibuang.
def daftar_user(users):
    """Hanya akun anak (role 'user')."""
    anak = []
    for u in users:
        if u["role"] == "user":
            anak.append(u)
    return anak


# ARTI pilih_user: admin memilih satu anak dari daftar. Mengembalikan data akun anak, atau None jika batal.
def pilih_user(daftar, aksi):
    """Pilih anak dari tabel. None jika batal."""
    nama_anak = []
    for u in daftar:
        nama_anak.append(u["username"])

    nama = pilih(f"Pilih anak yang ingin {aksi}:", nama_anak)
    if nama is None:
        return None

    for u in daftar:  # cari data lengkap berdasarkan nama yang dipilih
        if u["username"] == nama:
            return u


# ARTI statistik_user: ringkasan jumlah anak, jumlah transaksi, dan jumlah dompet + transaksi tiap anak.
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
        n_dompet = 0  # penghitung dompet anak ini
        for d in dompets:
            if d["pemilik"] == u["username"]:
                n_dompet += 1
        n_transaksi = 0  # penghitung transaksi anak ini
        for t in transaksi:
            if t["pemilik"] == u["username"]:
                n_transaksi += 1
        baris.append([u["username"], n_dompet, n_transaksi])
    tabel(baris, ["Username", "Dompet", "Transaksi"], ("left", "right", "right"))


# ARTI lihat_semua_akun: admin melihat tabel username, password, dan peran semua akun.
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
                      ROLE_LABEL.get(u["role"], u["role"])])  # ubah "user" jadi "anak", dst
    tabel(baris, ["No", "Username", "Password", "Peran"],
          ("right", "left", "left", "left"))
    print(warna("Data ini bersifat rahasia, jangan dilihat orang lain.", DIM))


# ARTI ubah_user: admin mengubah username dan/atau password anak. Dikosongkan = tidak diubah.
# Jika username berubah, data anak ikut dipindah.
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
        baru = lama  # kosong berarti username tidak diganti

    if baru != lama and username_ada(users, baru):
        gagal("Username sudah dipakai!")
        return

    password = input_password("Password baru: ", boleh_kosong=True)
    if password is None:
        return "batal"

    if baru == lama and password == "":
        info("Tidak ada perubahan.")
        return

    target["username"] = baru  # target adalah bagian dari users, jadi ikut berubah
    if password != "":
        target["password"] = password
    simpan(FILE_USER, KOLOM_USER, users)

    if baru != lama:
        pindah_data_pemilik(lama, baru)
    sukses("Data anak berhasil diubah!")


# ARTI hapus_user: admin menghapus akun anak beserta dompet, kategori, sumber, dan transaksinya (setelah konfirmasi).
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
        users.remove(target)  # remove = buang item tersebut dari list
        simpan(FILE_USER, KOLOM_USER, users)

        for item in FILE_DATA_PEMILIK:  # hapus data anak di ke-4 file
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


# ARTI laporan_keseluruhan: laporan gabungan semua anak + ringkasan tiap anak + status hemat/boros tiap anak.
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

    dompets = []  # hanya dompet milik anak (bukan orang tua)
    for d in baca(FILE_DOMPET):
        if d["pemilik"] in nama_anak:
            dompets.append(d)
    data = []  # hanya transaksi milik anak
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


# ---------- MENU (memakai match-case) ----------

# ARTI tampil_menu: menampilkan banner + tabel menu bernomor, lalu mengembalikan nomor yang diketik user.
# Dipakai oleh semua menu supaya tampilannya seragam. jejak = tulisan posisi menu (Menu Utama > Dompet).
def tampil_menu(jejak, user, daftar_menu, tombol_keluar="Kembali"):
    """Cetak banner + tabel menu, lalu kembalikan pilihan user (teks)."""
    bersihkan()
    banner(jejak.upper(), f"Masuk sebagai: {user['username']} ({ROLE_LABEL.get(user['role'], user['role'])})")
    print()
    baris = []
    for no in range(len(daftar_menu)):
        baris.append([no + 1, daftar_menu[no]])
    baris.append([0, warna(tombol_keluar, DIM)])  # nomor 0 = kembali / logout
    tabel(baris, ["No", "Menu"])
    return input("Pilih menu: ").strip()


# ARTI selesai_fitur: setelah sebuah fitur selesai, tunggu Enter, KECUALI fitur dibatalkan
# (fitur yang dibatalkan mengembalikan teks "batal" sehingga menu langsung muncul lagi).
def selesai_fitur(hasil):
    """Tunggu Enter setelah fitur selesai, kecuali fitur dibatalkan."""
    if hasil != "batal":
        jeda()


# ARTI menu_dompet: submenu dompet. Loop terus sampai user memilih 0 (break = keluar loop).
def menu_dompet(user, jejak):
    while True:
        pilihan = tampil_menu(jejak, user,
                              ["Dompet & Saldo", "Tambah Dompet",
                               "Ubah Saldo Awal Dompet", "Hapus Dompet"])
        match pilihan:  # mencocokkan pilihan dengan tiap case
            case "0":
                break  # kembali ke menu sebelumnya
            case "1":
                bersihkan()
                selesai_fitur(tampil_dompet(user))  # jalankan fitur, hasilnya dicek apakah "batal"
            case "2":
                bersihkan()
                selesai_fitur(tambah_dompet(user))
            case "3":
                bersihkan()
                selesai_fitur(ubah_saldo_dompet(user))
            case "4":
                bersihkan()
                selesai_fitur(hapus_dompet(user))
            case _:  # _ = semua pilihan lain (tidak valid)
                gagal("Pilihan tidak valid!")
                jeda()


# ARTI menu_transaksi: submenu transaksi (tambah, tampil, cari, ubah, hapus).
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


# ARTI menu_akun: submenu akun saya (ubah username / ubah password), dipakai anak dan orang tua.
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


# ARTI menu_anggota: submenu admin untuk mengelola anggota keluarga (ringkasan, tambah, ubah, hapus, lihat akun).
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


# ARTI menu_anak: menu utama untuk anak (role "user"): Dompet, Transaksi, Laporan, Akun Saya. 0 = Logout.
def menu_anak(user):
    """Menu utama untuk anak (role 'user')."""
    jejak = "Menu Utama"
    while True:
        pilihan = tampil_menu(jejak, user,
                              ["Dompet", "Transaksi", "Laporan", "Akun Saya"],
                              "Logout")
        match pilihan:
            case "0":
                break  # logout -> kembali ke layar login
            case "1":
                menu_dompet(user, jejak + " > Dompet")  # jejak ditambah agar terlihat posisi menu
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


# ARTI menu_admin: menu utama untuk orang tua (role "admin"): Anggota Keluarga, Laporan, Akun Saya.
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


# ARTI menu_user: pemilah setelah login. Jika role admin -> menu_admin, selain itu -> menu_anak.
def menu_user(user):
    if user["role"] == "admin":
        menu_admin(user)
    else:
        menu_anak(user)


# ---------- PROGRAM UTAMA ----------

# ARTI main: pintu masuk program. Menjalankan setup awal, lalu menampilkan layar utama
# (Login / Keluar) berulang-ulang sampai user memilih keluar.
def main():
    os.system("")  # trik agar warna ANSI tampil di terminal Windows
    setup_awal()  # buat akun orang tua pertama jika belum ada

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
                if user == "batal":  # login dibatalkan -> kembali ke layar utama
                    continue
                jeda()
                if user is not None:  # None = gagal 3x, tidak masuk menu
                    menu_user(user)
            case "0":
                print("Terima kasih!")
                break  # keluar dari program
            case _:
                gagal("Pilihan tidak valid!")
                jeda()


# if __name__ == "__main__": main() hanya dijalankan jika file ini dijalankan langsung (bukan di-import)
if __name__ == "__main__":
    main()


##############################################################################
##  SELESAI - akhir BAGIAN 4 (akhir program)
##############################################################################