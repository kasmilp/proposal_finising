# Folder Pembelajaran Proposal Tesis

> **Judul penelitian:** Pengembangan Histeresis Asimetris Sekuensial untuk Penyesuaian Rasio Dinamis Pembagian Beban Multi-WAN Fiber Optic dan Satelit LEO (Studi Kasus: PCC pada Router MikroTik)

Folder ini dibuat untuk membantu **memahami proposal secara bertahap** — dari nol (singkatan dan konsep dasar) hingga benar-benar mengerti algoritma yang dikembangkan. Setiap file disusun berurutan: baca sesuai nomor.

---

## Cara menggunakan folder ini

1. Mulai dari `00_PETA_BELAJAR.md` — lihat peta dan alur belajar yang disarankan.
2. Ikuti urutan file `01`, `02`, `03`, … — tiap file membahas satu konsep dengan bahasa bertingkat.
3. Untuk setiap file, ada bagian **"Cek pemahaman"** di akhir — jawab sendiri sebelum lanjut.
4. Istilah asing yang belum dipahami → buka `01_SINGKATAN.md`.

---

## Daftar isi folder

| No | File | Isi | Prasyarat |
|---|---|---|---|
| 00 | `00_PETA_BELAJAR.md` | Peta belajar, jalur rekomendasi, dan cara menilai pemahaman | — |
| 01 | `01_SINGKATAN.md` | Daftar lengkap singkatan/akronim + definisi singkat | — |
| 02 | `02_KONSEP_DASAR.md` | Konsep fondasi: QoS, multi-WAN, FO & LEO, MikroTik/PCC, hash | 01 |
| 03 | `03_DETEKSI_PERUBAHAN.md` | Quickest Change Detection: CUSUM, LLR, ARL, tunda deteksi | 02 |
| 04 | `04_HISTERESIS.md` | Histeresis asimetris, zona penyangga, kaitan dgn handover | 03 |
| 05 | `05_ALGORITMA_DIKEMBANGKAN.md` | **Inti**: algoritma diusulkan, langkah demi langkah | 03, 04 |
| 06 | `06_METRIK_EVALUASI.md` | Metrik E, U, F, QoS dan bagaimana mengukurnya | 05 |
| 07 | `07_SKENARIO_DAN_HIPOTESIS.md` | Skenario A–E, H1/H2, dan uji statistik | 06 |
| 08 | `08_ARSITEKTUR_SISTEM.md` | Arsitektur dua-loop, komponen, perangkat keras/lunak | 05, 07 |
| 09 | `09_PERTANYAAN_UJIAN.md` | Pertanyaan yang mungkin diajukan penguji + cara menjawab | semua |
| 10 | `10_KUIS.md` | Kuis pilihan ganda + esai + kunci jawaban | semua |

---

## Ringkasan satu kalimat per tahap belajar

- **Tahap 1 (Konsep dasar)** — Apa masalahnya? Mengapa PCC statis tidak cukup?
- **Tahap 2 (Teori deteksi)** — Bagaimana mendeteksi perubahan kualitas jalur secara otomatis?
- **Tahap 3 (Algoritma usulan)** — Bagaimana mengubah deteksi menjadi keputusan rasio yang stabil dan murah?
- **Tahap 4 (Evaluasi)** — Bagaimana membuktikan bahwa usulan lebih baik?

---

## Diagram pendukung

Folder `diagram/` berisi gambar vektor (SVG) yang bisa dibuka di browser:

| Diagram | File | Terkait dengan |
|---|---|---|
| Alur algoritma usulan (8 langkah) | `diagram/alur_algoritma.svg` | `05_ALGORITMA_DIKEMBANGKAN.md` |
| Arsitektur dua skala waktu | `diagram/arsitektur_sistem.svg` | `08_ARSITEKTUR_SISTEM.md` |
| Frontier E–U (posisi kebijakan) | `diagram/frontier_eu.svg` | `06_METRIK_EVALUASI.md` |

---

## Peta subbab proposal ↔ file pembelajaran

| Subbab proposal | Topik | File pembelajaran |
|---|---|---|
| 1.1 | Latar belakang & masalah | 02 |
| 1.2.1 | QoS/QoE | 02 |
| 1.2.2 | FO & LEO | 02 |
| 1.2.3 | MikroTik/RouterOS | 02 |
| 1.2.4 | PCC | 02, 05 |
| 1.2.5 | Load balancing/SD-WAN | 02 |
| 1.2.6–1.2.7 | QCD & CUSUM | 03 |
| 1.2.8 | Histeresis | 04 |
| 1.2.9–1.2.10 | Komitmen & integrasi | 05 |
| 1.3–1.4 | Rumusan masalah & hipotesis | 07, 09 |
| 1.5–1.6 | Tujuan & manfaat | 06, 09 |
| 2.1 | Jenis penelitian | 07 |
| 2.3 | Tahapan/NDLC | 08 |
| 2.4 | Perangkat | 08 |
| 2.5 | Perancangan sistem | 05, 08 |
| 2.6 | Skenario & variabel | 07 |
| 2.7 | Analisis data | 06, 07 |

---

## Catatan

- Materi ini **dirangkum dari proposal** (`Proposal_krm_shr_mekanisme_baru.docx`). Untuk detail lengkap, selalu kembalikan ke proposal asli.
- Beberapa rumus ditampilkan dalam bentuk konseptual; formula eksak ada di subbab 2.5 proposal.
- Jika menemukan istilah yang tidak ada di `01_SINGKATAN.md`, catat dan tambahkan agar folder tetap lengkap.
- Tiap file 01–09 kini mencantumkan **subbab sumber** di bagian atas agar mudah dicek silang dengan proposal.
