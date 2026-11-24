# Kandidat yang Tidak Masuk Folder Utama

Folder utama hanya memuat paper yang memenuhi tiga kriteria:

1. terbit 2023-2026;
2. dapat diverifikasi melalui DOI;
3. berasal dari IEEE Xplore, Elsevier ScienceDirect, atau penerbit yang umumnya terindeks Scopus.

## 1. Ditolak karena status indeks belum terverifikasi

| Paper | Alasan |
|---|---|
| Nugroho et al. (2026), *Quality Analysis of Service Load Balancing Using PCC, ECMP, and NTH Methods*, JANAPATI | Sangat relevan secara topik, tetapi status Scopus belum diverifikasi; jurnal nasional (SINTA) |
| Ahmadi et al. (2025), *Optimizing MikroTik Networks Using PCC Load Balancing with the PPDIOO Approach*, Jurnal Algoritma | Relevan sebagai praktik PCC, tetapi status Scopus belum diverifikasi |

Jika Anda ingin memasukkan dua paper Indonesia tersebut, letakkan di subbab 1.2.3 sebagai “praktik lokal” dan beri catatan “jurnal nasional, bukan Scopus”.

> Catatan: Putra et al. (2026), *Comparison of Load Balancing Performance Between Mikrotik ECMP and Ruijie Reyee Smart Balancing* (IEEE ICCSC) **tetap dimasukkan** sebagai P11 karena terbit di IEEE Xplore, meskipun fokusnya ECMP, bukan PCC.

## 2. Ditolak karena fokus/abstrak

| Paper | Alasan |
|---|---|
| Wan et al. (2024), *DeFlow: Differential flowlet switching for load balancing in datacenter networks*, Computer Networks | Fokus data center/flowlet, bukan multi-WAN; abstrak tidak tersedia saat verifikasi |
| Beberapa paper MikroTik 2023-2025 | Umumnya konfigurasi teknis tanpa evaluasi ilmiah yang kuat; tidak memenuhi kriteria kualitas |

## 3. Duplikasi

| Paper | Keputusan |
|---|---|
| Matsuura et al. (2023), GLOBECOM | Tidak dimasukkan karena merupakan versi konferensi dari P49 (JOCN 2024) |
| Mohan et al. (2024), WWW | Dimasukkan sebagai P08; versi arXiv tidak dihitung terpisah |
| Mbulwa et al. (2024), IEEE Access (P33) dan I2CACIS (P35) | Dua paper berbeda (optimasi parameter vs analisis kinerja), bukan duplikat; keduanya dipakai di 1.2.8 |

## 4. Paper dengan abstrak terbatas

| ID | Paper | Tindakan |
|---|---|---|
| P02 | Beshley et al. (2023), *Simulation Modelling Practice and Theory* | Baca teks penuh sebelum mengutip detail |
| P36 | Xie et al. (2026), *Ad Hoc Networks* | Baca teks penuh; ringkasan hanya berdasarkan judul |
| P39 | García-Bustos & Ramírez-Figueroa (2023), *Computers & Industrial Engineering* | Baca teks penuh; fokus pada metode economic design |

## 5. Mengapa tidak ada PDF

- Banyak paper IEEE/Elsevier berbayar; mengunduh dan mendistribusikan ulang PDF melanggar lisensi.
- Folder ini menyediakan DOI, metadata, dan catatan review; PDF dapat diunduh melalui akses institusi.
- Untuk paper open access, gunakan tombol “Download” pada halaman DOI.

## 6. Cara menambah paper baru

1. Cek DOI di `https://doi.org/...`.
2. Pastikan tahun 2023-2026.
3. Tambahkan entri ke `build_review.py` (atau buat file Markdown baru).
4. Perbarui `01_DAFTAR_JURNAL.md`, CSV, dan BibTeX.
5. Tandai subbab dan peran (Inti/Pendukung/Latar).
