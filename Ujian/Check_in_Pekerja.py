import datetime

data_pekerja = {
    "1": ("Abi Satria", "2006-08-22", "Manajer"),  # Perbaiki format tanggal lahir
    # ... data pekerja lainnya ...
}

def tampilkan_data_dan_cek_kedatangan():
    """Fungsi untuk menampilkan data pekerja berdasarkan ID dan melakukan cek kedatangan."""

    while True:
        id_pekerja = input("Masukkan ID pekerja: ")
        if id_pekerja in data_pekerja:
            nama, tanggal_lahir_str, jabatan = data_pekerja[id_pekerja]
            tanggal_lahir = datetime.datetime.strptime(tanggal_lahir_str, "%Y-%m-%d").date()

            umur = datetime.date.today().year - tanggal_lahir.year
            tahun_pensiun = tanggal_lahir.year + 58  # Usia pensiun 58 tahun

            print("\nData Pekerja:")
            print(f"ID: {id_pekerja}, Nama: {nama}, Tanggal Lahir: {tanggal_lahir_str}, Umur: {umur}, Jabatan: {jabatan}, Perkiraan Pensiun: {tahun_pensiun}")

            # Cek Kedatangan
            jam_masuk = datetime.time(7, 0)  # Pukul 07.00 WIB

            while True:
                try:
                    check_in_str = input("Jam berapa Anda check-in (format HH:MM)? ")
                    check_in_time = datetime.datetime.strptime(check_in_str, "%H:%M").time()
                    break
                except ValueError:
                    print("Format waktu tidak valid. Gunakan HH:MM.")

            selisih = datetime.datetime.combine(datetime.date.today(), check_in_time) - datetime.datetime.combine(datetime.date.today(), jam_masuk)

            if selisih < datetime.timedelta(0):
                menit_awal = abs(selisih.total_seconds()) // 60
                print(f"Terima kasih, {nama}, Anda datang lebih awal {menit_awal} menit.")  # Tambahkan nama
            elif selisih == datetime.timedelta(0):
                print(f"Terima kasih, {nama}, Anda datang tepat waktu.")  # Tambahkan nama
            else:
                menit_terlambat = selisih.total_seconds() // 60
                jam_checkout = (datetime.datetime.combine(datetime.date.today(), jam_masuk) + datetime.timedelta(hours=9, minutes=menit_terlambat)).time()
                print(f"{nama}, Anda datang terlambat {menit_terlambat} menit, harap check-out pukul {jam_checkout.strftime('%H:%M')}")  # Tambahkan nama
            break  # Keluar dari loop jika ID valid dan cek kedatangan selesai

        else:
            print("ID pekerja tidak ditemukan.")

if __name__ == "__main__":
    tampilkan_data_dan_cek_kedatangan()
