# 03. Deteksi Perubahan Sekuensial (Quickest Change Detection)

> **Subbab sumber di proposal:** 1.2.6–1.2.7 (QCD & CUSUM), 2.5.3 (model observasi & uji CUSUM).

File ini menjelaskan **teori deteksi** yang menjadi "mata" sistem. Ini adalah fondasi untuk memahami algoritma usulan (file `05`).

---

## 1. Masalah yang dipecahkan

Kita mengamati sebuah jalur setiap siklus (misal tiap 1–2 detik). Kualitasnya kadang normal, kadang menurun (**terdegradasi**). Kita ingin **mendeteksi perubahan** ini secepat mungkin, tetapi tanpa terlalu sering **alarm palsu** (mengira buruk padahal sebenarnya normal).

Ini adalah masalah **Quickest Change Detection (QCD)**: mendeteksi perubahan distribusi pengamatan secepat mungkin dengan batasan frekuensi alarm palsu.

---

## 2. Dua besaran yang bertentangan

| Besaran | Arti | Kita ingin… |
|---|---|---|
| **Tunda deteksi** | Waktu antara perubahan nyata dan alarm | Sekecil mungkin |
| **ARL (Average Run Length)** | Rata-rata jumlah pengamatan sampai alarm (palsu) | Sebesar mungkin |

Keduanya **bertentangan**: jika kita mudah membunyikan alarm, tunda kecil tapi alarm palsu banyak; sebaliknya jika terlalu hati-hati, alarm palsu sedikit tapi tunda besar. QCD mencari titik tengah yang optimal.

---

## 3. LLR: menimbang "seberapa kuat" bukti

Untuk setiap pengamatan, kita hitung **Log-Likelihood Ratio (LLR)**:

```
LLR = log( peluang pengamatan jika terdegradasi / peluang pengamatan jika normal )
```

- Jika LLR **positif besar** → bukti kuat bahwa jalur terdegradasi.
- Jika LLR **negatif** → bukti bahwa jalur normal.
- Jika LLR ≈ 0 → tidak informatif.

Dalam proposal, karena model observasi disederhanakan, LLR tiap siklus hanya memiliki **dua kemungkinan nilai**:
- `ℓ(11)` — saat kedua target probe buruk (bukti degradasi kuat, positif besar).
- `ℓ(lainnya)` — saat bukan itu (negatif kecil).

> Inilah yang membuat perhitungan sangat ringan: cukup penjumlahan, tidak ada operasi mahal.

---

## 4. CUSUM: mengakumulasi bukti

**CUSUM (Cumulative Sum)** mengakumulasi LLR seiring waktu untuk "mengingat" bukti:

```
S(baru) = max( 0, S(lama) + LLR )
```

- Statistik `S` diakumulasi tiap siklus.
- Dibatasi di bawah oleh nol sehingga bukti lama tidak menumpuk tanpa batas (jika jalur normal dalam waktu lama, S kembali ke 0).
- **Alarm** dibunyikan ketika `S` melampaui **ambang h**.

**Hubungan ambang & kinerja (klasik):**
- Tunda deteksi rata-rata ≈ `h / D`, dengan `D` = divergensi KL (informasi) antar distribusi.
- ARL alarm palsu ≈ `e^h` (tumbuh eksponensial dengan h).

Jadi: **makin besar h → makin jarang alarm palsu, tapi makin lama mendeteksi**. Ini pertukaran dasar.

---

## 5. CUSUM dua arah (dua statistik)

Karena kita perlu mendeteksi **dua arah** perubahan:

| Statistik | Dipakai saat | Mendeteksi |
|---|---|---|
| **S↓** | Jalur berstatus **SEHAT** | Degradasi → pindah ke DIEVAKUASI |
| **S↑** | Jalur berstatus **DIEVAKUASI** | Pemulihan → kembali ke SEHAT |

Jadi tiap jalur punya dua counter CUSUM. Kenapa perlu dua? Karena **bukti degradasi dan pemulihan tidak simetris**: satu sampel buruk memberi bukti jauh lebih kuat daripada satu sampel baik. Akibatnya, dengan ambang yang sama pun, tunda evakuasi dan tunda pemulihan berbeda.

> Ini disebut **asimetri informasi** — titik awal sebelum asimetri biaya ditambahkan.

---

## 6. Kenapa CUSUM dipilih (bukan yang lain)?

| Metode | Kelemahan |
|---|---|
| Skoring multi-kriteria (SAW/AHP/TOPSIS) | Menilai kondisi sesaat, tanpa memori lintas waktu; satu sampel transien bisa membalik keputusan |
| Prediksi machine learning | Butuh data berlabel besar; akurasi pada Starlink terbatas |
| Aturan **k-sampel-berturut** | Punya memori tapi hanya menghitung, tidak menimbang *seberapa kuat* tiap sampel |
| **CUSUM** ✓ | Mengakumulasi bukti **dan** menimbang kekuatan tiap sampel; ambang bisa dikaitkan langsung dengan biaya |

---

## 7. Ringkasan alur deteksi

```
Probe → pola pengamatan → LLR → akumulasi CUSUM (S↓/S↑) → bandingkan dgn ambang → transisi status
```

---

## Cek pemahaman

1. Apa itu QCD dan dua besaran yang bertentangan?
2. Jelaskan LLR dengan kata-kata sendiri: apa artinya bernilai positif besar?
3. Mengapa CUSUM dibatasi di bawah oleh nol?
4. Apa fungsi ambang h? Apa yang terjadi jika h diperbesar?
5. Mengapa perlu dua statistik CUSUM (dua arah)?
6. Sebutkan satu kelemahan aturan "k-sampel-berturut" dibanding CUSUM.
