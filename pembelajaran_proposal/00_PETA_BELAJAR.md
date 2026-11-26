# 00. Peta Belajar

Peta ini menunjukkan **cara belajar proposal secara bertahap**. Gunakan sebagai panduan; tidak wajib linear 100%, tetapi disarankan mengikuti urutan karena tiap konsep dibangun di atas konsep sebelumnya.

---

## Alur belajar yang disarankan

```
┌─────────────────────────────────────────────────────────────────────┐
│  TAHAP 1: FONDASI (mengapa penelitian ini ada)                      │
│  ├─ 01_SINGKATAN.md          → kenali istilah                       │
│  └─ 02_KONSEP_DASAR.md       → pahami masalah & objek               │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TAHAP 2: TEORI (alat yang dipakai)                                 │
│  ├─ 03_DETEKSI_PERUBAHAN.md → CUSUM, LLR, ARL                      │
│  └─ 04_HISTERESIS.md        → ambang ganda, zona penyangga          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TAHAP 3: INTI PENELITIAN (algoritma yang dikembangkan)             │
│  └─ 05_ALGORITMA_DIKEMBANGKAN.md → langkah demi langkah             │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TAHAP 4: MEMBUKTIKAN (bagaimana menguji)                           │
│  ├─ 06_METRIK_EVALUASI.md   → E, U, F, QoS                         │
│  ├─ 07_SKENARIO_DAN_HIPOTESIS.md → A–E, H1, H2                     │
│  └─ 08_ARSITEKTUR_SISTEM.md  → bagaimana sistem diwujudkan          │
└─────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────────┐
│  TAHAP 5: PERSIAPAN UJIAN                                          │
│  └─ 09_PERTANYAAN_UJIAN.md  → simulasi tanya-jawab                 │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Metode belajar yang disarankan

1. **Baca + garis bawahi** — untuk setiap file, tandai istilah yang belum dipahami, lalu cari di `01_SINGKATAN.md` dan `02_KONSEP_DASAR.md`.
2. **Ceritakan kembali (Feynman)** — setelah membaca, jelaskan dengan kata-kata sendiri tanpa melihat file. Jika buntu, kembali ke bagian itu.
3. **Jawab "Cek pemahaman"** — di akhir tiap file ada pertanyaan; jawab tertulis.
4. **Hubungkan ke diagram** — gunakan `05_ALGORITMA_DIKEMBANGKAN.md` (alur) dan `08_ARSITEKTUR_SISTEM.md` (komponen) sebagai peta mental.
5. **Uji dengan `09_PERTANYAAN_UJIAN.md`** — setelah semua tahap, jawab pertanyaan ujian dengan batas waktu.

---

## Tabel kesehatan pemahaman

Tandai kolom setelah menguasai tiap file:

| File | Belum | Sebagian | Paham |
|---|---|---|---|
| 01_SINGKATAN.md | | | |
| 02_KONSEP_DASAR.md | | | |
| 03_DETEKSI_PERUBAHAN.md | | | |
| 04_HISTERESIS.md | | | |
| 05_ALGORITMA_DIKEMBANGKAN.md | | | |
| 06_METRIK_EVALUASI.md | | | |
| 07_SKENARIO_DAN_HIPOTESIS.md | | | |
| 08_ARSITEKTUR_SISTEM.md | | | |
| 09_PERTANYAAN_UJIAN.md | | | |

---

## Target kompetensi per tahap

| Tahap | Setelah selesai, Anda mampu… |
|---|---|
| 1. Fondasi | Menjelaskan mengapa PCC statis bermasalah dan apa itu FO/LEO/MikroTik |
| 2. Teori | Menjelaskan CUSUM, LLR, ARL, histeresis tanpa rumus rumit |
| 3. Algoritma | Menjelaskan 6 langkah algoritma usulan secara runtut |
| 4. Evaluasi | Menjelaskan E, U, F dan skenario A–E, H1/H2 |
| 5. Ujian | Menjawab pertanyaan penguji dengan bahasa sendiri |
