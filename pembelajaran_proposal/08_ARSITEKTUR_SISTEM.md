# 08. Arsitektur Sistem

> **Subbab sumber di proposal:** 2.3 (tahapan/NDLC), 2.4 (perangkat), 2.5.1 (arsitektur), 2.6.3 (prosedur pengambilan data).
> **Diagram pendukung:** `diagram/arsitektur_sistem.svg`.

File ini menjelaskan **bagaimana algoritma diwujudkan** menjadi sistem nyata: komponen, perangkat, dan alur data.

---

## 1. Arsitektur dua skala waktu

Sistem terdiri dari **dua loop** yang berjalan pada kecepatan berbeda:

```
┌─────────────────────────── LOOP CEPAT (detik) ───────────────────────────┐
│  Probe aktif → model observasi → LLR → CUSUM (S↓/S↑) → bandingkan ambang │
│                     → transisi status → peta aksi → kuantisasi → aktuator │
└──────────────────────────────────────────────────────────────────────────┘
                              │ (parameter biaya, ambang, H)
                              ▼
┌─────────────────────────── LOOP LAMBAT (menit) ─────────────────────────┐
│  Estimasi λ, L, G, H dari tabel koneksi → perbarui ambang h↓/h↑ →      │
│  kalibrasi model observasi                                              │
└──────────────────────────────────────────────────────────────────────────┘
```

- **Loop cepat** hanya menjalankan penjumlahan & perbandingan (ringan), berjalan setiap siklus probe.
- **Loop lambat** melakukan estimasi biaya yang lebih mahal, berjalan dalam hitungan menit.

---

## 2. Kontroler eksternal (di luar router)

Keputusan dihitung oleh sebuah **kontroler eksternal** (server) — bukan di dalam router. Ini penting:
- Model **netral-vendor**: kontroler tidak tergantung pada merek router.
- Router (MikroTik) hanya bertindak sebagai **aktuator** — mengeksekusi pemetaan yang diberikan.

Kontroler berkomunikasi dengan router via **REST API**.

---

## 3. Komponen utama sistem

| Komponen | Fungsi |
|---|---|
| **Probe** | Mengukur RTT/loss ke target per jalur |
| **Model observasi / LLR** | Mengubah pola pengamatan menjadi LLR |
| **CUSUM dua arah** | Mengakumulasi bukti degradasi & pemulihan |
| **Ambang asimetris** | Menentukan kapan transisi status (dari biaya) |
| **Peta aksi SRLG** | Menerjemahkan status → bobot target |
| **Kuantisasi hash** | Ubah bobot → kelompok hash, minimal-remap |
| **Aktuator** | PCC RouterOS / nftables: menulis pemetaan |
| **Basis data** | Menyimpan sampel probe, statistik CUSUM, log keputusan |

---

## 4. Perangkat keras (ringkasan)

| Perangkat | Fungsi |
|---|---|
| Router MikroTik (RB1100AHx4) | Router produksi; eksekutor PCC via API |
| Modem/ONT Fiber Optic | Terminasi WAN1 (FO) |
| Terminal Starlink A | Terminasi WAN2 (LEO) |
| Terminal Starlink B | Terminasi WAN3 (LEO) |
| Gateway uji paralel (mikroTik kedua / mini-PC Linux) | Menjalankan kebijakan pembanding serentak; titik injeksi gangguan |
| Server Controller (mini PC / Raspberry Pi) | Menjalankan probe, CUSUM, ambang, peta aksi, kuantisasi, API |
| Switch client / switch uji | Distribusi LAN |
| Laptop/PC pengujian | Klien uji & alat ukur QoS |

---

## 5. Perangkat lunak (ringkasan)

| Perangkat lunak | Fungsi |
|---|---|
| RouterOS 7.22.2 | OS router; REST API, PCC, statistik |
| Ubuntu Server 22.04 | OS kontroler |
| Python 3.11.9 | Implementasi algoritma |
| RouterOS REST API / librouteros | Komunikasi dengan router |
| NumPy / SciPy / pandas | Perhitungan & analisis |
| SQLite / InfluxDB | Penyimpanan deret waktu |
| Linux nftables (jhash) | Aktuator pembanding netral-vendor |
| tc / netem | Emulasi loss/delay (injeksi gangguan) |
| Wireshark, ping, iperf3, speedtest-cli | Pengukuran QoS |

---

## 6. Model data (basis data)

Kontroler menyimpan deret waktu, karena CUSUM bergantung pada **urutan** pengamatan. Kolom inti (Tabel 4 proposal):

| Kolom | Arti |
|---|---|
| timestamp, siklus_k | Waktu & nomor siklus |
| link_id | Identitas jalur (FO/SL-A/SL-B) + grup risiko |
| rtt_ms, loss, bad | Hasil probe; bad = hilang atau RTT > median bergulir + 30ms |
| pola_y, llr | Pola pengamatan & LLR |
| S_down, S_up, h_down, h_up | Statistik CUSUM & ambang aktif |
| status | SEHAT / DIEVAKUASI |
| bucket_map | Pemetaan kelompok hash → jalur |
| laju_baru, umur_median, headroom | Ringkasan tabel koneksi (loop lambat) |

---

## 7. Prosedur pengambilan data

1. Sebelum sesi: catat kondisi awal, reset statistik CUSUM.
2. Selama sesi: catat sampel probe tiap siklus, status, statistik pemicu.
3. Catat setiap transisi status & perubahan pemetaan (untuk F dan tunda deteksi).
4. Ukur QoS klien pada waktu yang sama untuk semua kebijakan.
5. Rekam kejadian degradasi nyata (hujan, gangguan FO) untuk analisis.

---

## 8. Alur pengembangan (NDLC)

```
Analysis        → studi literatur, analisis kebutuhan, rekaman baseline
Design          → perumusan model, CUSUM, ambang, arsitektur sistem
Simulation Prototyping → replay offline, gateway uji paralel
Implementation  → shadow mode, lalu aktif di jaringan produksi
Monitoring      → pengumpulan data E, U, F, QoS
Management      → analisis, evaluasi hipotesis, laporan
```

---

## Cek pemahaman

1. Apa beda loop cepat dan loop lambat?
2. Mengapa kontroler berada di luar router (eksternal)?
3. Sebutkan 5 komponen inti sistem.
4. Mengapa basis data menyimpan deret waktu, bukan hanya nilai sesaat?
5. Apa fungsi gateway uji paralel?
6. Mengapa shadow mode dilakukan sebelum aktif penuh?
