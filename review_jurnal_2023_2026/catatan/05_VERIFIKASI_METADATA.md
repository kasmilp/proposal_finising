# Verifikasi Metadata

**Tanggal:** 25 November 2026  
**Jumlah paper:** 50  
**Rentang:** 2023-2026

## 1. Metode

- DOI setiap paper diselesaikan melalui `https://doi.org/DOI` dengan content negotiation `application/vnd.citationstyles.csl+json`.
- Metadata pelengkap (abstrak, status OA, sitasi) diambil dari OpenAlex.
- Tahun yang dipakai adalah tahun terbit resmi pada record CSL/issue, bukan tahun unggah pertama.
- Tidak ada paper yang dimasukkan hanya berdasarkan judul tanpa DOI yang valid.

## 2. Komposisi

| Kategori | Jumlah |
|---|---|
| Total paper | 50 |
| Artikel jurnal | 33 |
| Prosiding | 17 |
| IEEE Xplore | 34 |
| Elsevier ScienceDirect | 10 |
| Penerbit lain (Scopus) | 6 |

## 3. Anomali metadata yang perlu diketahui

| ID | Isu | Tindakan |
|---|---|---|
| P03 | DOI 2025, tetapi issue resmi 2026 (vol. 34) | Gunakan 2026; cek halaman jurnal |
| P12 | DOI berakhiran 2022 dan daring Desember 2022, tetapi volume resmi 216 terbit 2023 | Gunakan 2023; sebut “daring 2022” bila perlu |
| P16 | Daring 30 November 2025, tetapi issue resmi Januari 2026 (vol. 36 no. 1) | Gunakan 2026 |
| P18 | DOI 2025, tetapi issue resmi 2026 (vol. 28) | Gunakan 2026; cek halaman jurnal |
| P33 | DOI 2023, tetapi issue resmi 2024 (vol. 12) | Gunakan 2024 |
| P41 | Halaman belum tersedia | Cantumkan volume/issue saja |
| P46 | Artikel in press, volume/halaman belum ada | Cantumkan “in press” |
| P49 | Halaman hanya tersedia sebagai nomor artikel E23 | Cantumkan E23, bukan rentang halaman |
| P02 | Abstrak tidak tersedia; judul mengandung karakter Cyrillic | Karakter dinormalisasi; verifikasi teks penuh |
| P36 | Abstrak tidak tersedia | Verifikasi teks penuh |
| P39 | Abstrak tidak tersedia | Verifikasi teks penuh |

## 4. Status indeks

- **IEEE Xplore** dan **Elsevier ScienceDirect** adalah sumber utama.
- **ACM, Springer, Wiley, Optica, KSII** umumnya terindeks Scopus, tetapi status final harus dicek di *Scopus Source List* institusi.
- Folder ini **tidak** mengklaim kuartil (Q1/Q2/Q3/Q4) karena kuartil berubah setiap tahun dan memerlukan akses Scimago/Scopus.

## 5. Cara mengecek ulang

1. Buka DOI.
2. Cocokkan judul, penulis, venue, tahun, volume, halaman.
3. Cek status indeks di Scopus Source List.
4. Cek apakah paper masih “early access” atau sudah final.
5. Untuk paper berbayar, gunakan akses perpustakaan kampus.

## 6. Yang belum diverifikasi

- Isi lengkap semua paper (baru abstrak/metadata).
- Kualitas metodologis secara rinci (sample size, validitas statistik).
- Status Scopus per paper (hanya level venue).
- Kesesuaian format sitasi dengan pedoman Universitas Hasanuddin.

> Gunakan file ini sebagai peta, bukan sebagai pengganti membaca paper.
