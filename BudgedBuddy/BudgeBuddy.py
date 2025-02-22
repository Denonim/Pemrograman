import tkinter as tk
from tkinter import ttk
import locale
import tkinter.messagebox as messagebox
from datetime import datetime

class TransaksiBaru:
    def __init__(self, root, aplikasi_keuangan):
        self.root = root
        self.aplikasi_keuangan = aplikasi_keuangan
        self.root.title("Transaksi Baru")
        self.root.configure(bg='#D3D3D3')

        # Mengatur bahasa dan negara untuk format rupiah
        locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

        # Variabel untuk menyimpan data keuangan dan tanggal
        self.transaksi_var = tk.StringVar()
        self.nilai_var = tk.DoubleVar()
        self.hari_var = tk.StringVar()
        self.bulan_var = tk.StringVar()
        self.tahun_var = tk.StringVar()
        self.keterangan_var = tk.StringVar()

        # Label dan Combobox untuk memilih tanggal
        ttk.Label(root, text="Tanggal:", background='#D3D3D3', foreground='black').grid(column=0, row=0, padx=10, pady=10)
        self.hari_combobox = ttk.Combobox(root, values=[str(i) for i in range(1, 32)], state="readonly", background='#C0C0C0', foreground='black')
        self.hari_combobox.grid(column=1, row=0, padx=10, pady=10)
        self.hari_combobox.set("1")  # Set opsi default
        self.bulan_combobox = ttk.Combobox(root, values=[
            "Januari", "Februari", "Maret", "April", "Mei", "Juni",
            "Juli", "Agustus", "September", "Oktober", "November", "Desember"
        ], state="readonly", background='#C0C0C0', foreground='black')
        self.bulan_combobox.grid(column=2, row=0, padx=10, pady=10)
        self.bulan_combobox.set("Januari")  # Set opsi default
        self.tahun_combobox = ttk.Combobox(root, values=[str(i) for i in range(2000, 2024)], state="readonly", background='#C0C0C0', foreground='black')
        self.tahun_combobox.grid(column=3, row=0, padx=10, pady=10)
        self.tahun_combobox.set("2000")  # Set opsi default

        # Combobox untuk memilih jenis transaksi
        ttk.Label(root, text="Jenis Transaksi:", background='#D3D3D3', foreground='black').grid(column=0, row=1, padx=10, pady=10)
        jenis_transaksi_combobox = ttk.Combobox(root, textvariable=self.transaksi_var, values=["Pemasukan", "Pengeluaran"], state="readonly", background='#C0C0C0', foreground='black')
        jenis_transaksi_combobox.grid(column=1, row=1, padx=10, pady=10)
        jenis_transaksi_combobox.set("Pemasukan")  # Set opsi default

        # Entry untuk memasukkan nilai transaksi dengan format rupiah
        ttk.Label(root, text="Nilai:", background='#D3D3D3', foreground='black').grid(column=0, row=2, padx=10, pady=10)
        self.nilai_entry = ttk.Entry(root, textvariable=self.nilai_var)
        self.nilai_entry.grid(column=1, row=2, padx=10, pady=10)

        # Entry untuk memasukkan keterangan transaksi
        ttk.Label(root, text="Keterangan:", background='#D3D3D3', foreground='black').grid(column=0, row=3, padx=10, pady=10)
        ttk.Entry(root, textvariable=self.keterangan_var).grid(column=1, row=3, padx=10, pady=10)

        # Tombol untuk menyimpan transaksi
        ttk.Button(root, text="Simpan", command=self.simpan_transaksi, style='TButton').grid(column=0, row=4, columnspan=2, pady=10)

        # Tombol untuk kembali ke halaman utama
        ttk.Button(root, text="Kembali", command=self.kembali_ke_halaman_utama, style='TButton').grid(column=1, row=5, columnspan=2, pady=10)

    def simpan_transaksi(self):
        try:
            nilai = float(self.nilai_var.get())
            jenis_transaksi = self.transaksi_var.get()
            hari = self.hari_combobox.get()
            bulan = self.bulan_combobox.get()
            tahun = self.tahun_combobox.get()
            keterangan = self.keterangan_var.get()

            # Validasi nilai transaksi
            if nilai <= 0:
                messagebox.showerror("Error", "Nilai transaksi harus lebih dari 0")
                return

            # Validasi tanggal
            try:
                # Coba parsing tanggal
                tanggal = datetime.strptime(f"{tahun}-{bulan}-{hari}", "%Y-%B-%d").strftime("%d %B %Y")
            except ValueError:
                messagebox.showerror("Error", "Tanggal tidak valid")
                return

            # Format nilai sebagai rupiah
            nilai_rupiah = locale.currency(nilai, grouping=True)

            # Ambil saldo terakhir dari histori jika ada
            if self.aplikasi_keuangan.histori_transaksi.size() > 0:
                saldo_terakhir = float(self.aplikasi_keuangan.histori_transaksi.get(tk.END).split("Saldo Akhir ")[1])
            else:
                saldo_terakhir = 0

            # Hitung saldo akhir berdasarkan jenis transaksi
            if jenis_transaksi == "Pemasukan":
                saldo_akhir = nilai + saldo_terakhir
            else:
                saldo_akhir = saldo_terakhir - nilai

            # Tambahkan entri ke kotak history di halaman utama
            histori_text = f"{tanggal}: {jenis_transaksi} {nilai_rupiah}, Keterangan: {keterangan}, Saldo Akhir {saldo_akhir}"
            self.aplikasi_keuangan.histori_transaksi.insert(tk.END, histori_text)

            # Update total saldo di halaman utama
            self.aplikasi_keuangan.total_saldo = saldo_akhir
            self.aplikasi_keuangan.update_total_saldo()

            # Tutup jendela transaksi baru
            self.root.destroy()

        except ValueError:
            # Tangani jika input tidak valid
            messagebox.showerror("Error", "Input tidak valid")

    def kembali_ke_halaman_utama(self):
        # Tutup jendela transaksi baru
        self.root.destroy()

class HapusTransaksi:
    def __init__(self, root, aplikasi_keuangan):
        self.root = root
        self.aplikasi_keuangan = aplikasi_keuangan
        self.root.title("Hapus Transaksi")
        self.root.configure(bg='#D3D3D3')

        # Mengatur bahasa dan negara untuk format rupiah
        locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

        # Label dan Listbox untuk menampilkan histori transaksi
        ttk.Label(root, text="Histori Transaksi:", background='#D3D3D3', foreground='black').grid(column=0, row=0, padx=10, pady=10)
        self.histori_transaksi_listbox = tk.Listbox(root, width=60, height=15, bg='#C0C0C0', fg='black')
        self.histori_transaksi_listbox.grid(column=0, row=1, rowspan=5, padx=10, pady=10)

        # Mengisi Listbox dengan data histori transaksi
        for entry in self.aplikasi_keuangan.histori_transaksi.get(0, tk.END):
            self.histori_transaksi_listbox.insert(tk.END, entry)

        # Tombol untuk menghapus transaksi terpilih
        ttk.Button(root, text="Hapus Transaksi", command=self.hapus_transaksi, style='TButton').grid(column=1, row=6, pady=10)

        # Tombol untuk kembali ke halaman utama
        ttk.Button(root, text="Kembali", command=self.kembali_ke_halaman_utama, style='TButton').grid(column=1, row=7, columnspan=2, pady=10)

    def hapus_transaksi(self):
        try:
            # Ambil indeks transaksi yang dipilih
            selected_index = self.histori_transaksi_listbox.curselection()

            if not selected_index:
                messagebox.showinfo("Informasi", "Pilih transaksi yang akan dihapus.")
                return

            selected_index = int(selected_index[0])

            # Ambil data transaksi yang dipilih
            selected_entry = self.histori_transaksi_listbox.get(selected_index)

            # Parsing nilai transaksi dari data transaksi yang dipilih
            nilai_transaksi = float(selected_entry.split(" ")[2].replace(",", ""))

            # Parsing jenis transaksi dari data transaksi yang dipilih
            jenis_transaksi = selected_entry.split(" ")[1]

            # Ambil saldo terakhir dari histori jika ada
            if selected_index > 0:
                saldo_terakhir = float(self.histori_transaksi_listbox.get(selected_index - 1).split("Saldo Akhir ")[1])
            else:
                saldo_terakhir = 0

            # Hitung saldo akhir setelah penghapusan transaksi
            if jenis_transaksi == "Pemasukan":
                saldo_akhir = saldo_terakhir - nilai_transaksi
            else:
                saldo_akhir = saldo_terakhir + nilai_transaksi

            # Hapus transaksi dari histori
            self.histori_transaksi_listbox.delete(selected_index)

            # Update total saldo di halaman utama
            self.aplikasi_keuangan.total_saldo = saldo_akhir
            self.aplikasi_keuangan.update_total_saldo()

        except ValueError:
            # Tangani jika terjadi kesalahan dalam penghapusan
            messagebox.showerror("Error", "Gagal menghapus transaksi")

    def kembali_ke_halaman_utama(self):
        # Tutup jendela hapus transaksi
        self.root.destroy()

class AplikasiKeuangan:
    def __init__(self, root):
        self.root = root
        self.root.title("BudgeBuddy - Manajemen Keuangan Pribadi")
        self.root.configure(bg='#D3D3D3')

        # Mengatur bahasa dan negara untuk format rupiah
        locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

        # Label untuk menampilkan total saldo
        self.total_saldo_label = ttk.Label(root, text="Total Saldo: 0", background='#D3D3D3', foreground='black')
        self.total_saldo_label.grid(column=2, row=8, columnspan=2, pady=10)

        # Tombol untuk transaksi baru
        ttk.Button(root, text="Transaksi Baru", command=self.buat_transaksi_baru, style='TButton').grid(column=0, row=4, columnspan=2, pady=10)

        # Tombol untuk hapus semua histori
        ttk.Button(root, text="Hapus Semua Histori", command=self.hapus_semua_histori, style='TButton').grid(column=2, row=6, pady=10)

        # Tombol untuk urutkan berdasarkan
        ttk.Label(root, text="Urutkan berdasarkan:", background='#D3D3D3', foreground='black').grid(column=2, row=7, pady=10)
        urutkan_combobox = ttk.Combobox(root, values=["Waktu Terlama", "Waktu Terbaru", "Jumlah Terbesar", "Jumlah Terkecil"], state="readonly", background='#C0C0C0', foreground='black')
        urutkan_combobox.grid(column=3, row=7, pady=10)
        urutkan_combobox.set("Waktu Terlama")  # Set opsi default
        ttk.Button(root, text="Urutkan", command=lambda: self.urutkan_history(urutkan_combobox.get()), style='TButton').grid(column=4, row=7, pady=10)

        # Tombol untuk buka halaman hapus transaksi
        ttk.Button(root, text="Hapus Transaksi", command=self.buka_hapus_transaksi, style='TButton').grid(column=1, row=8, columnspan=2, pady=10)

        # Tombol untuk buka halaman cari transaksi
        ttk.Button(root, text="Cari Transaksi", command=self.buka_cari_transaksi, style='TButton').grid(column=1, row=9, columnspan=2, pady=10)

        # Histori transaksi (Listbox)
        self.histori_transaksi = tk.Listbox(root, width=60, height=15, bg='#C0C0C0', fg='black')
        self.histori_transaksi.grid(column=2, row=1, rowspan=5, padx=10, pady=10, columnspan=2)

        # Inisialisasi total saldo
        self.total_saldo = 0
        self.histori_asli = []  # Menyimpan salinan histori transaksi asli
    
    def urutkan_history(self, kriteria):
        # Dapatkan semua entri dari Listbox
        entries = self.histori_asli if self.histori_asli else self.histori_transaksi.get(0, tk.END)

        if kriteria == "Waktu Terlama":
            # Urutkan entri berdasarkan tanggal terlama
            sorted_entries = sorted(entries, key=lambda x: x.split(":")[0])
        elif kriteria == "Waktu Terbaru":
            # Urutkan entri berdasarkan tanggal terbaru
            sorted_entries = sorted(entries, key=lambda x: x.split(":")[0], reverse=True)
        elif kriteria == "Jumlah Terbesar":
            # Urutkan entri berdasarkan jumlah terbesar
            sorted_entries = sorted(entries, key=lambda x: float(x.split("Saldo Akhir ")[1]), reverse=True)
        elif kriteria == "Jumlah Terkecil":
            # Urutkan entri berdasarkan jumlah terkecil
            sorted_entries = sorted(entries, key=lambda x: float(x.split("Saldo Akhir ")[1]))

        # Hapus semua entri dari Listbox
        self.histori_transaksi.delete(0, tk.END)

        # Masukkan entri yang sudah diurutkan ke Listbox
        for entry in sorted_entries:
            self.histori_transaksi.insert(tk.END, entry)


    def hapus_semua_histori(self):
        # Konfirmasi sebelum menghapus semua histori
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus semua histori transaksi?")
        if confirm:
            # Hapus semua entri dari Listbox
            self.histori_transaksi.delete(0, tk.END)

            # Reset total saldo
            self.total_saldo = 0
            self.update_total_saldo()

    def buat_transaksi_baru(self):
        # Membuat jendela baru untuk transaksi baru
        top = tk.Toplevel(self.root)
        transaksi_baru = TransaksiBaru(top, self)

    def hapus_transaksi(self):
        # Membuat jendela baru untuk hapus transaksi
        top = tk.Toplevel(self.root)
        hapus_transaksi = HapusTransaksi(top, self)

    def buka_hapus_transaksi(self):
        # Buka halaman hapus transaksi
        self.hapus_transaksi()

    def buka_cari_transaksi(self):
        # Buka halaman cari transaksi
        top = tk.Toplevel(self.root)
        cari_transaksi = CariTransaksi(top, self)

    def update_total_saldo(self):
        # Update label total saldo
        self.total_saldo_label.config(text=f"Total Saldo: {locale.currency(self.total_saldo, grouping=True)}")

class CariTransaksi:
    def __init__(self, root, aplikasi_keuangan):
        self.root = root
        self.aplikasi_keuangan = aplikasi_keuangan
        self.root.title("Cari Transaksi")
        self.root.configure(bg='#D3D3D3')

        # Mengatur bahasa dan negara untuk format rupiah
        locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')

        # Label dan Entry untuk mencari transaksi
        ttk.Label(root, text="Cari Transaksi:", background='#D3D3D3', foreground='black').grid(column=0, row=0, padx=10, pady=10)
        self.cari_entry = ttk.Entry(root)
        self.cari_entry.grid(column=1, row=0, padx=10, pady=10)

        # Tombol untuk mencari transaksi
        ttk.Button(root, text="Cari", command=self.cari_transaksi, style='TButton').grid(column=2, row=0, pady=10)

        # Listbox untuk menampilkan hasil pencarian
        self.hasil_listbox = tk.Listbox(root, width=60, height=15, bg='#C0C0C0', fg='black')
        self.hasil_listbox.grid(column=0, row=1, rowspan=5, padx=10, pady=10, columnspan=3)

        # Tombol untuk kembali ke halaman utama
        ttk.Button(root, text="Kembali", command=self.kembali_ke_halaman_utama, style='TButton').grid(column=1, row=7, pady=10)

    def cari_transaksi(self):
        # Ambil kata kunci pencarian
        kata_kunci = self.cari_entry.get().lower()

        # Hapus semua entri dari Listbox
        self.hasil_listbox.delete(0, tk.END)

        # Cari transaksi berdasarkan kata kunci
        for entry in self.aplikasi_keuangan.histori_transaksi.get(0, tk.END):
            if kata_kunci in entry.lower():
                self.hasil_listbox.insert(tk.END, entry)

    def kembali_ke_halaman_utama(self):
        # Tutup jendela cari transaksi
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    aplikasi = AplikasiKeuangan(root)
    root.mainloop()
