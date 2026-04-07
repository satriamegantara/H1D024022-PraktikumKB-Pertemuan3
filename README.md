# Praktikum Kecerdasan Buatan - Pertemuan 3

Repository untuk tugas praktikum Kecerdasan Buatan.

---

## Requirement

Instalasi

```
pip install numpy scikit-fuzzy matplotlib
```

**Penjelasan**

- `numpy` - library untuk operasi array dan matematika
- `scikit-fuzzy (skfuzzy)` - library untuk fuzzy logic
- `matplotlib` - library untuk visualisasi grafik

---

## Penjelasan Kode: pelayananMasyarakat.py

Program ini menggunakan fuzzy logic (Metode Mamdani) untuk menghitung tingkat kepuasan pelayanan masyarakat berdasarkan 4 kriteria input.

### Bagian Import Library (Baris 1-4)

```python
import numpy as np
```

- Mengimpor NumPy untuk operasi array dan perhitungan numerik

```python
import skfuzzy as fuzz
```

- Mengimpor scikit-fuzzy untuk fungsi membership (trapezoid dan triangular)

```python
from skfuzzy import control as ctrl
```

- Mengimpor modul control dari skfuzzy untuk membuat sistem fuzzy

```python
import matplotlib.pyplot as plt
```

- Mengimpor matplotlib untuk menampilkan grafik hasil fuzzy

### Bagian Deklarasi Input & Output (Baris 6-10)

```python
kejelasanInformasi = ctrl.Antecedent(np.arange(0, 101), 'kejelasan_informasi')
kejelasanPersyaratan = ctrl.Antecedent(np.arange(0, 101), 'kejelasan_persyaratan')
kemampuanPetugas = ctrl.Antecedent(np.arange(0, 101), 'kemampuan_petugas')
ketersediaanSarpras = ctrl.Antecedent(np.arange(0, 101), 'ketersediaan_sarpras')
```

- Deklarasi 4 variabel **input** (Antecedent) dengan range 0-100
- `Antecedent` = variabel input dalam fuzzy logic
- `np.arange(0, 101)` = membuat array dari 0 hingga 100
- Parameter kedua = nama variabel dalam sistem

```python
kepuasanPelayanan = ctrl.Consequent(np.arange(0, 401), 'kepuasan_pelayanan')
```

- Deklarasi variabel **output** (Consequent) dengan range 0-400
- `Consequent` = variabel output dalam fuzzy logic
- Range lebih besar karena output adalah hasil kombinasi 4 input

### Bagian Fungsi Membership Input (Baris 12-23)

```python
def define_input_mf(var):
    var['tidak memuaskan'] = fuzz.trapmf(var.universe, [0, 0, 60, 75])
    var['cukup memuaskan'] = fuzz.trimf(var.universe, [60, 75, 90])
    var['memuaskan'] = fuzz.trapmf(var.universe, [75, 90, 100, 100])
```

- Mendefinisikan fungsi untuk membuat membership function dengan 3 kategori:
  - `tidak memuaskan` = trapezoid [0, 0, 60, 75]
  - `cukup memuaskan` = triangular [60, 75, 90]
  - `memuaskan` = trapezoid [75, 90, 100, 100]

**Penjelasan fungsi:**

- `trapmf` = trapezoid membership function dengan 4 parameter (a, b, c, d)
- `trimf` = triangular membership function dengan 3 parameter (a, b, c)

```python
define_input_mf(kejelasanInformasi)
define_input_mf(kejelasanPersyaratan)
define_input_mf(kemampuanPetugas)
define_input_mf(ketersediaanSarpras)
```

- Menjalankan fungsi untuk menetapkan membership function ke semua 4 input

### Bagian Membership Function Output (Baris 25-29)

```python
kepuasanPelayanan['tidak memuaskan'] = fuzz.trapmf(kepuasanPelayanan.universe, [0, 0, 50, 100])
kepuasanPelayanan['kurang memuaskan'] = fuzz.trimf(kepuasanPelayanan.universe, [50, 100, 175])
kepuasanPelayanan['cukup memuaskan'] = fuzz.trimf(kepuasanPelayanan.universe, [150, 225, 275])
kepuasanPelayanan['memuaskan'] = fuzz.trimf(kepuasanPelayanan.universe, [250, 300, 350])
kepuasanPelayanan['sangat memuaskan'] = fuzz.trapmf(kepuasanPelayanan.universe, [325, 375, 400, 400])
```

- Mendefinisikan 5 kategori output kepuasan:
  - Range yang lebih lebar karena output adalah kombinasi 4 input
  - Setiap kategori punya overlap untuk transisi smooth

### Bagian IF-THEN Rules (Baris 32-113)

```python
rule1 = ctrl.Rule(kejelasanInformasi['tidak memuaskan'] & kejelasanPersyaratan['tidak memuaskan'] & kemampuanPetugas['tidak memuaskan'] & ketersediaanSarpras['tidak memuaskan'], kepuasanPelayanan['kurang memuaskan'])
```

- Total 81 rule (rule1 sampai rule81)
- Setiap rule adalah kombinasi IF kondisi input THEN hasil output
- Menggunakan operator `&` (AND) untuk menggabungkan kondisi input
- **Contoh:** Jika semua input "tidak memuaskan" maka output "kurang memuaskan"

### Bagian Control System (Baris 115)

```python
kepuasanControl = ctrl.ControlSystem([rule1, rule2, ... rule81])
```

- Membuat sistem fuzzy yang menggabungkan semua 81 rule
- Sistem akan menggunakan metode Mamdani secara otomatis

### Bagian Simulasi (Baris 116)

```python
kepuasanSimulasi = ctrl.ControlSystemSimulation(kepuasanControl)
```

- Membuat objek simulasi untuk menjalankan fuzzy logic

### Bagian Input Nilai (Baris 118-121)

```python
kepuasanSimulasi.input['kejelasan_informasi'] = 80
kepuasanSimulasi.input['kejelasan_persyaratan'] = 60
kepuasanSimulasi.input['kemampuan_petugas'] = 50
kepuasanSimulasi.input['ketersediaan_sarpras'] = 90
```

- Memasukkan nilai input untuk simulasi fuzzy
- Nilai-nilai ini akan di-proses sesuai membership function

### Bagian Computation & Output (Baris 123-126)

```python
kepuasanSimulasi.compute()
```

- Menjalankan proses fuzzy logic (inferensi)

```python
print("Nilai Kepuasan Pelayanan: ", round(kepuasanSimulasi.output['kepuasan_pelayanan'], 2))
```

- Menampilkan hasil output kepuasan (dibulatkan 2 desimal)

```python
kepuasanPelayanan.view(sim=kepuasanSimulasi)
plt.show()
```

- Menampilkan grafik membership function hasil fuzzy

---

## Penjelasan Kode: tokoHewan.py

Program ini menggunakan fuzzy logic untuk memprediksi jumlah stok makanan hewan berdasarkan 4 kriteria input.

### Bagian Import Library (Baris 1-4)

```python
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
```

- Sama dengan penjelasan di pelayananMasyarakat.py

### Bagian Deklarasi Input & Output (Baris 6-10)

```python
jumlah_terjual = ctrl.Antecedent(np.arange(0, 101), 'barang_terjual')
jumlah_permintaan = ctrl.Antecedent(np.arange(0, 301), 'permintaan')
harga_satuan = ctrl.Antecedent(np.arange(0, 100001), 'harga_per_item')
laba = ctrl.Antecedent(np.arange(0, 4000001), 'profit')
stok_persediaan = ctrl.Consequent(np.arange(0, 1001), 'stok_makanan')
```

- Deklarasi 4 input dengan range berbeda:
  - `jumlah_terjual` = 0-100 (jumlah unit terjual)
  - `jumlah_permintaan` = 0-300 (permintaan dari pelanggan)
  - `harga_satuan` = 0-100.000 (harga per item)
  - `laba` = 0-4.000.000 (profit yang didapat)
- Output `stok_persediaan` = 0-1000 unit

### Bagian Membership Function Input (Baris 12-29)

```python
jumlah_terjual['rendah'] = fuzz.trapmf(jumlah_terjual.universe, [0, 0, 20, 50])
jumlah_terjual['sedang'] = fuzz.trimf(jumlah_terjual.universe, [20, 50, 80])
jumlah_terjual['tinggi'] = fuzz.trapmf(jumlah_terjual.universe, [50, 80, 100, 100])
```

- Barang terjual memiliki 3 kategori: rendah, sedang, tinggi

```python
jumlah_permintaan['rendah'] = fuzz.trapmf(jumlah_permintaan.universe, [0, 0, 75, 150])
jumlah_permintaan['sedang'] = fuzz.trimf(jumlah_permintaan.universe, [75, 150, 225])
jumlah_permintaan['tinggi'] = fuzz.trapmf(jumlah_permintaan.universe, [150, 225, 300, 300])
```

- Permintaan memiliki 3 kategori: rendah, sedang, tinggi

```python
harga_satuan['murah'] = fuzz.trapmf(harga_satuan.universe, [0, 0, 25000, 50000])
harga_satuan['sedang'] = fuzz.trimf(harga_satuan.universe, [25000, 50000, 75000])
harga_satuan['mahal'] = fuzz.trapmf(harga_satuan.universe, [50000, 75000, 100000, 100000])
```

- Harga satuan memiliki 3 kategori: murah, sedang, mahal

```python
laba['rendah'] = fuzz.trapmf(laba.universe, [0, 0, 1000000, 2000000])
laba['sedang'] = fuzz.trimf(laba.universe, [1000000, 2000000, 3000000])
laba['tinggi'] = fuzz.trapmf(laba.universe, [2000000, 3000000, 4000000, 4000000])
```

- Laba memiliki 3 kategori: rendah, sedang, tinggi

### Bagian Membership Function Output (Baris 31-32)

```python
stok_persediaan['sedang'] = fuzz.trimf(stok_persediaan.universe, [200, 500, 800])
stok_persediaan['banyak'] = fuzz.trapmf(stok_persediaan.universe, [400, 600, 1000, 1000])
```

- Output stok memiliki 2 kategori: sedang dan banyak

### Bagian IF-THEN Rules (Baris 35-40)

```python
aturan_1 = ctrl.Rule(jumlah_terjual['tinggi'] & jumlah_permintaan['tinggi'] & harga_satuan['murah'] & laba['tinggi'], stok_persediaan['banyak'])
aturan_2 = ctrl.Rule(jumlah_terjual['tinggi'] & jumlah_permintaan['tinggi'] & harga_satuan['murah'] & laba['sedang'], stok_persediaan['sedang'])
...
aturan_6 = ctrl.Rule(jumlah_terjual['rendah'] & jumlah_permintaan['rendah'] & harga_satuan['sedang'] & laba['sedang'], stok_persediaan['sedang'])
```

- Total 6 rule untuk kombinasi kondisi input
- **Contoh rule 1:** Jika penjualan tinggi AND permintaan tinggi AND harga murah AND profit tinggi, maka stok banyak

### Bagian Control System & Simulasi (Baris 42-43)

```python
sistem_stok = ctrl.ControlSystem([aturan_1, aturan_2, aturan_3, aturan_4, aturan_5, aturan_6])
simulasi_stok = ctrl.ControlSystemSimulation(sistem_stok)
```

- Membuat sistem fuzzy dari 6 rule
- Membuat simulasi untuk menjalankan fuzzy logic

### Bagian Input Nilai (Baris 46-49)

```python
simulasi_stok.input['barang_terjual'] = 80
simulasi_stok.input['permintaan'] = 255
simulasi_stok.input['harga_per_item'] = 25000
simulasi_stok.input['profit'] = 3500000
```

- Memasukkan nilai input:
  - Barang terjual: 80 unit
  - Permintaan: 255 unit
  - Harga per item: Rp 25.000
  - Profit: Rp 3.500.000

### Bagian Computation & Output (Baris 51-56)

```python
simulasi_stok.compute()
```

- Menjalankan proses fuzzy logic

```python
print("Jumlah Persediaan Stok Makanan =", round(simulasi_stok.output['stok_makanan'], 2), "unit")
```

- Menampilkan hasil prediksi stok makanan (dibulatkan 2 desimal)

```python
stok_persediaan.view(sim=simulasi_stok)
plt.show()
```

- Menampilkan grafik membership function hasil fuzzy

---

## Perbedaan Kedua Program

| Aspek                 | Pelayanan Masyarakat | Toko Hewan                 |
| --------------------- | -------------------- | -------------------------- |
| **Input**             | 4 variabel (0-100)   | 4 variabel (berbeda range) |
| **Output**            | Kepuasan (0-400)     | Stok (0-1000)              |
| **Membership Input**  | 3 kategori (sama)    | 3 kategori (sama)          |
| **Membership Output** | 5 kategori           | 2 kategori                 |
| **Total Rule**        | 81 rule              | 6 rule                     |
| **Metode**            | Mamdani              | Mamdani                    |

---

## Kesimpulan

Kedua program mendemonstrasikan bagaimana fuzzy logic dapat menyelesaikan masalah keputusan:

- **Pelayanan Masyarakat**: Mengukur kepuasan pelanggan dari aspek layanan
- **Toko Hewan**: Memprediksi stok optimal berdasarkan data penjualan dan demand
