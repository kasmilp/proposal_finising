# 02. Konsep Dasar

> **Subbab sumber di proposal:** 1.1 (latar belakang), 1.2.1–1.2.5 (QoS, FO/LEO, MikroTik, PCC, load balancing).

File ini membangun pemahaman fondasi. Semua istilah penting ada di `01_SINGKATAN.md`. Baca perlahan; tiap bagian menjelaskan **mengapa** konsep itu ada.

---

## 1. Masalah utama: PCC statis tidak cukup

Bayangkan jaringan RT/RW Net dengan **tiga jalur internet**:
- 1 jalur **Fiber Optic (FO)** — kabel, relatif stabil.
- 2 jalur **Satelit LEO (Starlink)** — nirkabel, sangat dinamis.

Pada konfigurasi lama, beban dibagi dengan **rasio tetap**, misalnya `1:1:1` (sepertiga ke tiap jalur). Ini disebut **PCC statis**.

**Masalahnya:** kualitas jalur tidak konstan. Ketika salah satu Starlink terganggu (hujan, obstruksi, rekonfigurasi satelit), router **tetap** mengirim sepertiga koneksi baru ke jalur itu. Akibatnya, banyak koneksi mampir ke jalur yang buruk → kualitas pelanggan turun.

> **Inti masalah:** keputusan tidak "menyadari" kondisi jalur terkini.

---

## 2. Apa itu Multi-WAN?

**Multi-WAN** = memakai beberapa jalur ISP sekaligus (multi = banyak, WAN = Wide Area Network). Tujuannya:
- **High availability** — jika satu jalur gagal, yang lain tetap berjalan.
- **Agregasi** — menggabungkan kapasitas beberapa jalur.

Tantangan multi-WAN: **bagaimana membagi beban secara adil dan adaptif** di antara jalur yang kemampuannya berbeda dan berubah-ubah.

---

## 3. QoS dan QoE

| Istilah | Arti | Contoh metrik |
|---|---|---|
| **QoS** | Kualitas layanan dari sisi jaringan | delay, jitter, packet loss, throughput |
| **QoE** | Kualitas yang dirasakan pengguna | skor kepuasan, kelancaran video |

Proposal memakai **QoS sisi klien** (ping, iperf3, speedtest) sebagai salah satu tolok ukur. QoE disebut di tinjauan pustaka, tetapi eksperimen utama berbasis QoS.

---

## 4. Jalur FO vs LEO (Starlink)

| Sifat | Fiber Optic (FO) | Satelit LEO (Starlink) |
|---|---|---|
| Media | Kabel serat | Gelombang radio dari satelit |
| Stabilitas | Relatif stabil | **Sangat dinamis** |
| Skala waktu degradasi | Menit–jam (gangguan fisik, cuaca) | **Detik–menit** (obstruksi, hujan, rekonfigurasi 15 detik) |
| Kegagalan | Terkadang ireversibel | Sering transien/singkat |

**Kunci:** data pengukuran menunjukkan LEO memiliki variasi jauh lebih besar daripada terestrial, termasuk **outage**, **burst packet loss** akibat obstruksi, dan **rekonfigurasi periodik 15 detik**. Ini yang membuat deteksi otomatis dibutuhkan.

---

## 5. MikroTik dan RouterOS

**MikroTik** adalah vendor router murah yang banyak dipakai di jaringan kecil-menengah Indonesia. **RouterOS** adalah sistem operasinya.

Fitur relevan:
- **PCC** — load balancing berbasis hash per-koneksi.
- **ECMP** — pembagian merata ke jalur berbiaya setara.
- **REST API** — memungkinkan kontroler eksternal membaca statistik & menulis pemetaan.

Karena model penelitian **netral-vendor**, PCC hanyalah satu "aktuator" (alat untuk merealisasikan keputusan). Model yang sama bisa dipakai di ECMP, nftables Linux, atau SD-WAN.

---

## 6. Per-Connection Classifier (PCC)

**PCC** bekerja dengan cara:
1. Setiap koneksi baru di-hash berdasarkan atributnya (source address, destination address, port…).
2. Hash dipetakan ke salah satu dari **N kelompok**.
3. Tiap kelompok diarahkan ke satu **gateway** (jalur) lewat routing mark.

**Dua sifat penting PCC:**
- **Kuantisasi rasio:** rasio hanya bisa diubah dalam kelipatan `1/N`. Contoh: jika N=12, rasio memungkinkan adalah 0/12, 1/12, …, 12/12.
- **Koneksi tetap di jalur awal:** karena tabel koneksi/NAT "mengikat" koneksi ke jalur awalnya. Jadi **mengubah pemetaan kelompok hanya memengaruhi koneksi baru** yang jatuh pada kelompok yang dipindahkan — koneksi lama tidak terganggu.

> Ini sangat penting: berarti keputusan rasio **tidak perlu khawatir memutus koneksi yang sedang berjalan**. Ini yang disebut **komitmen per-koneksi**.

---

## 7. Hash, consistent hashing, dan remap

- **Hash** = fungsi yang memetakan data ke angka; dipakai untuk mengelompokkan koneksi.
- **Consistent hashing** = teknik agar saat ada perubahan jumlah node/kelompok, hanya sedikit kunci yang perlu dipindahkan.
- **Remap** = memindahkan pemetaan kelompok dari satu jalur ke jalur lain.

Penelitian ini memakai prinsip **kuantisasi dengan perubahan pemetaan minimal**: ketika rasio berubah, kita ingin se-minimal mungkin memindahkan kelompok (agar frekuensi rekonfigurasi F rendah).

---

## 8. Kerangka pengembangan NDLC

Proposal memakai **NDLC** (Network Development Life Cycle):

```
Analysis → Design → Simulation Prototyping → Implementation → Monitoring → Management
```

Ini alur pengembangan sistem di penelitian ini (lihat `08_ARSITEKTUR_SISTEM.md`).

---

## 9. Peta konsep keseluruhan

```
Masalah: PCC statis tidak adaptif
        │
        ▼
Solusi: lapisan keputusan di atas mekanisme PCC
        │
        ├── DETEKSI  : CUSUM dua arah (mendeteksi degradasi/pemulihan)
        ├── KEPUTUSAN: ambang asimetris sadar biaya keputusan (histeresis)
        ├── PEMETAAN  : peta aksi SRLG-aware + kuantisasi hash minimal-remap
        └── AKTUATOR  : PCC RouterOS (atau nftables)
```

---

## Cek pemahaman

1. Apa masalah utama PCC statis?
2. Mengapa LEO lebih sulit dikelola daripada FO?
3. Jelaskan sifat "kuantisasi" PCC: mengapa rasio tidak bisa sembarang?
4. Apa arti "komitmen per-koneksi" dan mengapa ia membuat perubahan rasio lebih aman?
5. Apa perbedaan QoS dan QoE?
