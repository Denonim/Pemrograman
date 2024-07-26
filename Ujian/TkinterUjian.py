from datetime import datetime, timedelta

Pekerja = {
    "011": {"nama": "firja", "tanggal_lahir": "1990-12-30", "sebagai": "Manager"},
    "012": {"nama": "andika", "tanggal_lahir": "1990-08-15", "sebagai": "Staff"},
    "013": {"nama": "fariz", "tanggal_lahir": "1991-10-04", "sebagai": "Staff"},
    "014": {"nama": "farhan", "tanggal_lahir": "1990-04-16", "sebagai": "Staff"},
    "015": {"nama": "keytaro", "tanggal_lahir": "1992-03-19", "sebagai": "HRD"},
    "001": {"nama": "abi", "tanggal_lahir": "1991-08-22", "sebagai": "CEO)"}
}


def calculate_age(birthdate):
    today = datetime.today()
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    return today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))

def estimate_retirement(birthdate):
    birthdate = datetime.strptime(birthdate, "%Y-%m-%d")
    perkiraan_pensiun = birthdate.replace(year=birthdate.year + 60)
    return perkiraan_pensiun.strftime("%Y-%m-%d")

def time_difference(actual_time, expected_time):
    delta = actual_time - expected_time
    return delta.total_seconds() // 60

expected_checkin_time = datetime.strptime("07:00", "%H:%M")

pekerja_id = input("Masukkan nomor ID pekerja: ")
user_input = input("Jam Berapa anda Check-in? (HH:MM): ")
actual_checkin_time = datetime.strptime(user_input, "%H:%M")

pekerja = Pekerja.get(pekerja_id, None)

if pekerja:
    umur = calculate_age(pekerja["tanggal_lahir"])
    perkiraan_pensiun = estimate_retirement(pekerja["tanggal_lahir"])

    print(f"\nInformasi Pekerja:\nNomor ID: {pekerja_id}\nNama Lengkap: {pekerja['nama']}\nTanggal Lahir: {pekerja['tanggal_lahir']}\nUmur: {umur} tahun\nSebagai: {pekerja['sebagai']}\nPerkiraan Pensiun: {perkiraan_pensiun}")

    difference_in_minutes = time_difference(actual_checkin_time, expected_checkin_time)

    if difference_in_minutes < 0:
        print(f"\nTerima kasih, Anda datang lebih awal {abs(int(difference_in_minutes))} menit")
    elif difference_in_minutes == 0:
        print("\nTerima kasih, Anda datang tepat waktu")
    else:
        late_minutes = int(difference_in_minutes)
        checkout_time = (actual_checkin_time + timedelta(hours=9)).strftime("%H:%M")
        print(f"\nAnda datang terlambat {late_minutes} menit, harap check-out pukul {checkout_time}")
else:
    print("Nomor ID pekerja tidak ditemukan.")




import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

Pekerja = {
    "011": {"nama": "firja", "tanggal_lahir": "1990-12-30", "sebagai": "Manager"},
    "012": {"nama": "andika", "tanggal_lahir": "1990-08-15", "sebagai": "Staff"},
    "013": {"nama": "fariz", "tanggal_lahir": "1991-10-04", "sebagai": "Staff"},
    "014": {"nama": "farhan", "tanggal_lahir": "1990-04-16", "sebagai": "Staff"},
    "015": {"nama": "keytaro", "tanggal_lahir": "1992-03-19", "sebagai": "HRD"},
    "001": {"nama": "abi", "tanggal_lahir": "1991-08-22", "sebagai": "CEO"}  # Perbaiki typo di "CEO"
}

# ... (fungsi calculate_age, estimate_retirement, time_difference tetap sama) ...

def tampilkan_data_dan_cek_kedatangan_gui():
    """Fungsi GUI untuk menampilkan data pekerja dan melakukan cek kedatangan."""

    def cek_kedatangan_action():
        """Fungsi untuk menangani aksi tombol "Cek Kedatangan"."""
        pekerja_id = id_entry.get()
        user_input = check_in_entry.get()

        try:
            actual_checkin_time = datetime.strptime(user_input, "%H:%M")
        except ValueError:
            hasil_label.config(text="Format waktu tidak valid. Gunakan HH:MM.")
            return

        pekerja = Pekerja.get(pekerja_id, None)

        if pekerja:
            umur = calculate_age(pekerja["tanggal_lahir"])
            perkiraan_pensiun = estimate_retirement(pekerja["tanggal_lahir"])

            data_label.config(
                text=f"Nomor ID: {pekerja_id}\nNama Lengkap: {pekerja['nama']}\nTanggal Lahir: {pekerja['tanggal_lahir']}\nUmur: {umur} tahun\nSebagai: {pekerja['sebagai']}\nPerkiraan Pensiun: {perkiraan_pensiun}"
            )

            difference_in_minutes = time_difference(actual_checkin_time, expected_checkin_time)

            if difference_in_minutes < 0:
                hasil_label.config(text=f"Terima kasih, {pekerja['nama']}, Anda datang lebih awal {abs(int(difference_in_minutes))} menit")
            elif difference_in_minutes == 0:
                hasil_label.config(text=f"Terima kasih, {pekerja['nama']}, Anda datang tepat waktu")
            else:
                late_minutes = int(difference_in_minutes)
                checkout_time = (actual_checkin_time + timedelta(hours=9)).strftime("%H:%M")
                hasil_label.config(text=f"{pekerja['nama']}, Anda datang terlambat {late_minutes} menit, harap check-out pukul {checkout_time}")
        else:
            data_label.config(text="Nomor ID pekerja tidak ditemukan.")

    # Membuat jendela utama
    window = tk.Tk()
    window.title("Cek Kedatangan Karyawan")

    # Label dan Entry untuk ID Pekerja
    id_label = ttk.Label(window, text="ID Pekerja:")
    id_label.grid(row=0, column=0, padx=5, pady=5)
    id_entry = ttk.Entry(window)
    id_entry.grid(row=0, column=1, padx=5, pady=5)

    # Label dan Entry untuk Waktu Check-in
    check_in_label = ttk.Label(window, text="Jam Check-in (HH:MM):")
    check_in_label.grid(row=1, column=0, padx=5, pady=5)
    check_in_entry = ttk.Entry(window)
    check_in_entry.grid(row=1, column=1, padx=5, pady=5)

    # Tombol "Cek Kedatangan"
    cek_button = ttk.Button(window, text="Cek Kedatangan", command=cek_kedatangan_action)
    cek_button.grid(row=2, column=0, columnspan=2, pady=10)

    # Label untuk menampilkan data pekerja
    data_label = ttk.Label(window, text="")
    data_label.grid(row=3, column=0, columnspan=2, pady=5)

    # Label untuk menampilkan hasil cek kedatangan
    hasil_label = ttk.Label(window, text="")
    hasil_label.grid(row=4, column=0, columnspan=2, pady=5)

    window.mainloop()

if __name__ == "__main__":
    tampilkan_data_dan_cek_kedatangan_gui()
