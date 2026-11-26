# 07. Skenario dan Hipotesis

> **Subbab sumber di proposal:** 1.3–1.4 (rumusan masalah & hipotesis), 2.1 (jenis penelitian), 2.6 (skenario & variabel), 2.7.3–2.7.4 (uji hipotesis & flapping).

File ini menjelaskan **bagaimana eksperimen dirancang** dan **apa yang hendak dibuktikan** (hipotesis).

---

## 1. Skenario percobaan (A–E)

Penelitian membandingkan beberapa kebijakan. Skenario utama:

| Skenario | Nama | Konfigurasi |
|---|---|---|
| **A** | Baseline | PCC statis, rasio tetap 1:1:1 (konfigurasi eksisting) |
| **B** | Histeresis k-sampel-berturut | Status berubah setelah k sampel buruk/baik berturut-turut (praktik failover umum) |
| **C** | CUSUM simetris | Uji dua arah dengan ambang & peta aksi sama dengan D, tapi simetris |
| **D** | **Usulan** | CUSUM dua arah + ambang asimetris sadar biaya keputusan + peta aksi SRLG + kuantisasi minimal-remap |
| **E** | Acuan batas | FO jalur utama + failover ke Starlink; dipakai untuk menempatkan kurva E–U, bukan kandidat |

> **Fokus:** membandingkan **D** (usulan) vs **A** (baseline), **B** (k-sampel), dan **C** (CUSUM simetris).

---

## 2. Pengujian berjenjang (tiga tahap)

Karena menguji di jaringan nyata berisiko, pengujian dilakukan bertahap:

1. **Replay offline** — jalankan ulang rekaman probe yang sama pada semua kebijakan, sehingga semua menerima masukan identik. (Pertama, paling aman.)
2. **Gateway uji paralel** — dua gateway berjalan serentak pada kondisi jalur yang sama, tanpa menyentuh trafik pelanggan.
3. **Jaringan produksi** — diawali **shadow mode** (hanya menghitung/mencatat keputusan, belum menulis), lalu aktif.

---

## 3. Variabel penelitian

| Jenis | Isi |
|---|---|
| **Bebas** | Kebijakan penyesuaian rasio (A/B/C/D); rasio asimetri ×2, ×4, ×8 sebagai analisis sensitivitas |
| **Terikat** | E, U, F per jam; tunda evakuasi/pemulihan; alarm palsu; QoS klien |
| **Kontrol** | Lokasi, interval siklus Δt, target probe, jumlah kelompok N, rasio nominal, durasi pengamatan; pada gateway uji: klien & pola trafik identik |
| **Diamati (tidak dimanipulasi)** | Cuaca, jam sibuk/normal, headroom, laju koneksi baru (untuk stratifikasi) |

---

## 4. Hipotesis

**H1 (kinerja deteksi + stabilitas):**
> Ambang asimetris yang diturunkan dari biaya keputusan menghasilkan **E lebih rendah** dibanding histeresis k-sampel-berturut dan CUSUM simetris pada **U setara**, dengan **F lebih rendah**.

Pemecah:
- H1 menguji **D vs B** dan **D vs C**.
- Variabel dibandingkan: E, U, F per jam.

**H2 (perbaikan QoS klien):**
> Sistem usulan menurunkan **E** dan memperbaiki **QoS klien** dibanding baseline.

Pemecah:
- H2 menguji **D vs A**.
- Variabel: E dan QoS klien per jam.

**H0 (hipotesis nol):**
> Tidak ada perbedaan signifikan antara usulan dan pembanding.

---

## 5. Uji statistik

| Langkah | Metode |
|---|---|
| Prasyarat | Uji normalitas (untuk menentukan uji parametrik/nonparametrik) |
| Jika data normal | **Uji-t berpasangan** |
| Jika tidak normal | **Wilcoxon signed-rank** |

- Karena pengukuran dilakukan pada unit yang sama (pasangan per jam), dipakai **paired test**.
- Frekuensi flapping dianalisis juga secara kualitatif lewat garis waktu status & pemetaan (Gambar 4).

---

## 6. Analisis stratifikasi

Karena kondisi eksternal tak terkendali, hasil **dikelompokkan (stratifikasi)** berdasarkan:
- Kondisi cuaca (cerah/hujan).
- Jam sibuk/normal.
- Headroom kapasitas.
- Laju koneksi baru.

Ini menjelaskan mengapa klaim generalisasi harus hati-hati (kuasi-eksperimental).

---

## 7. Peta dari pertanyaan → skenario → hipotesis

```
Rumusan masalah
   │
   ├─ "Apakah asimetri dari biaya menurunkan E & F?" → H1 → D vs B, D vs C
   └─ "Apakah memperbaiki QoS?"                     → H2 → D vs A
```

---

## Cek pemahaman

1. Sebutkan 5 skenario dan peran masing-masing.
2. Apa beda replay offline, gateway uji, dan shadow mode?
3. Tuliskan H1 dan H2 dengan kata-kata sendiri.
4. Mengapa dipakai uji berpasangan?
5. Apa fungsi stratifikasi?
6. Mengapa E hanya "acuan batas", bukan kandidat pembanding?
