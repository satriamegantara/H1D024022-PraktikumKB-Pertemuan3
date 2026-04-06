import numpy as np
import skfuzzy as fuzz 
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt

jumlah_terjual = ctrl.Antecedent(np.arange(0, 101), 'barang_terjual')
jumlah_permintaan = ctrl.Antecedent(np.arange(0, 301), 'permintaan')
harga_satuan = ctrl.Antecedent(np.arange(0, 100001), 'harga_per_item')
laba = ctrl.Antecedent(np.arange(0, 4000001), 'profit')
stok_persediaan = ctrl.Consequent(np.arange(0, 1001), 'stok_makanan')

# barang terjual [0-100]
jumlah_terjual['rendah'] = fuzz.trapmf(jumlah_terjual.universe, [0, 0, 20, 50])
jumlah_terjual['sedang'] = fuzz.trimf(jumlah_terjual.universe, [20, 50, 80])
jumlah_terjual['tinggi'] = fuzz.trapmf(jumlah_terjual.universe, [50, 80, 100, 100])

# permintaan [0-300]
jumlah_permintaan['rendah'] = fuzz.trapmf(jumlah_permintaan.universe, [0, 0, 75, 150])
jumlah_permintaan['sedang'] = fuzz.trimf(jumlah_permintaan.universe, [75, 150, 225])
jumlah_permintaan['tinggi'] = fuzz.trapmf(jumlah_permintaan.universe, [150, 225, 300, 300])

# harga per item [0-100000]
harga_satuan['murah'] = fuzz.trapmf(harga_satuan.universe, [0, 0, 25000, 50000])
harga_satuan['sedang'] = fuzz.trimf(harga_satuan.universe, [25000, 50000, 75000])
harga_satuan['mahal'] = fuzz.trapmf(harga_satuan.universe, [50000, 75000, 100000, 100000])

# profit [0-4000000]
laba['rendah'] = fuzz.trapmf(laba.universe, [0, 0, 1000000, 2000000])
laba['sedang'] = fuzz.trimf(laba.universe, [1000000, 2000000, 3000000])
laba['tinggi'] = fuzz.trapmf(laba.universe, [2000000, 3000000, 4000000, 4000000])
stok_persediaan['sedang'] = fuzz.trimf(stok_persediaan.universe, [200, 500, 800])
stok_persediaan['banyak'] = fuzz.trapmf(stok_persediaan.universe, [400, 600, 1000, 1000])

# rules
aturan_1 = ctrl.Rule(jumlah_terjual['tinggi'] & jumlah_permintaan['tinggi'] & harga_satuan['murah'] & laba['tinggi'], stok_persediaan['banyak'])
aturan_2 = ctrl.Rule(jumlah_terjual['tinggi'] & jumlah_permintaan['tinggi'] & harga_satuan['murah'] & laba['sedang'], stok_persediaan['sedang'])
aturan_3 = ctrl.Rule(jumlah_terjual['tinggi'] & jumlah_permintaan['sedang'] & harga_satuan['murah'] & laba['sedang'], stok_persediaan['sedang'])
aturan_4 = ctrl.Rule(jumlah_terjual['sedang'] & jumlah_permintaan['tinggi'] & harga_satuan['murah'] & laba['sedang'], stok_persediaan['sedang'])
aturan_5 = ctrl.Rule(jumlah_terjual['sedang'] & jumlah_permintaan['tinggi'] & harga_satuan['murah'] & laba['tinggi'], stok_persediaan['banyak'])
aturan_6 = ctrl.Rule(jumlah_terjual['rendah'] & jumlah_permintaan['rendah'] & harga_satuan['sedang'] & laba['sedang'], stok_persediaan['sedang'])

sistem_stok = ctrl.ControlSystem([aturan_1, aturan_2, aturan_3, aturan_4, aturan_5, aturan_6])
simulasi_stok = ctrl.ControlSystemSimulation(sistem_stok)

# input soal
simulasi_stok.input['barang_terjual'] = 80
simulasi_stok.input['permintaan'] = 255
simulasi_stok.input['harga_per_item'] = 25000
simulasi_stok.input['profit'] = 3500000

simulasi_stok.compute()
print("Jumlah Persediaan Stok Makanan =", round(simulasi_stok.output['stok_makanan'], 2), "unit")

stok_persediaan.view(sim=simulasi_stok)
plt.show()