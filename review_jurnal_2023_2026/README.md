# Review Jurnal 2023-2026 — Proposal Tesis Kasmil Papalia

Folder ini berisi **review literatur terstruktur** untuk proposal:

> *Pengembangan Histeresis Asimetris Sekuensial untuk Penyesuaian Rasio Dinamis Pembagian Beban Multi-WAN Fiber Optic dan Satelit LEO (Studi Kasus: PCC pada Router MikroTik).*

## 1. Isi folder

- **50 paper** terbit 2023-2026.
- **33 artikel jurnal** dan **17 prosiding**.
- **34 paper IEEE Xplore**, **10 paper Elsevier ScienceDirect**, dan **6 paper dari penerbit lain yang umumnya terindeks Scopus** (ACM, Springer, Wiley, Optica, KSII).
- Setiap paper diberi **tag subbab** 1.2.1-1.2.10, **peran** (Inti/Pendukung/Latar), ringkasan, alasan relevansi, cara pakai, dan keterbatasan.
- Metadata DOI diverifikasi pada **25 November 2026** melalui DOI content negotiation dan OpenAlex.
- Data mentah pencarian disimpan di `data_mentah/` agar dapat diaudit ulang tanpa mengganggu file review.

> Catatan: folder ini **tidak memuat PDF berbayar**. Setiap entri menyertakan DOI; unduh PDF melalui akses institusi atau akses terbuka yang disediakan penerbit.

## 2. Cara cepat memakai folder

1. Buka `00_RINGKASAN_REVIEW.md` untuk melihat temuan utama dan peta celah.
2. Buka `per_pembahasan/` sesuai subbab yang sedang ditulis.
3. Untuk menyalin sitasi, gunakan `03_DAFTAR_JURNAL.bib` (BibTeX) atau `01_DAFTAR_JURNAL.md`.
4. Untuk melihat paper mana yang mendukung klaim tertentu, buka `catatan/02_PETA_KUTIPAN.md`.
5. Untuk revisi proposal, buka `catatan/03_REVISI_YANG_DISARANKAN.md`.

## 3. Peta subbab

| Subbab | Topik | Paper inti | Jumlah |
|---|---|---|---|
| 1.2.1 | QoS dan QoE | P04 | 4 |
| 1.2.2 | FO dan LEO Starlink | P05, P06, P08 | 6 |
| 1.2.3 | MikroTik dan PCC praktik | P12 | 2 |
| 1.2.4 | PCC dan hash per-koneksi | P13, P14 | 5 |
| 1.2.5 | Load balancing dan SD-WAN | P18, P19, P20, P21 | 5 |
| 1.2.6 | Quickest change detection | P23, P24 | 6 |
| 1.2.7 | CUSUM dua arah | P29 | 3 |
| 1.2.8 | Histeresis dan handover | P32, P33, P34 | 6 |
| 1.2.9 | Komitmen koneksi dan biaya | P38, P40 | 4 |
| 1.2.10 | Integrasi, SRLG, dan TE | P45, P46, P48, P49 | 9 |

## 4. Sepuluh paper yang paling wajib dibaca

1. **P23** Sun & Zou (2024), *Quickest Change Detection in Autoregressive Models* — menjawab kritik asumsi i.i.d.
2. **P24** Xie, Moustakides & Xie (2023), *Window-Limited CUSUM* — CUSUM dengan parameter pasca-perubahan tidak diketahui.
3. **P13** Levi & Keslassy (2023), *Beyond the Ring: Quantized Heterogeneous Consistent Hashing* — dasar kuantisasi hash.
4. **P21** Botta et al. (2026), *Seeing Through the Overlay* — deteksi bottleneck bersama via korelasi latensi.
5. **P38** Amend & Rakocevic (2024), *Cost-efficient multipath scheduling* — biaya jalur mahal vs QoE.
6. **P40** Shojaee et al. (2024), *Economic-statistical design* — ambang dari biaya, bukan ARL saja.
7. **P32** Eydian et al. (2025), *Handover Strategy ... Hysteresis Margin* — histeresis di LEO.
8. **P45** Ju et al. (2025), *Dynamic Load-Balancing Routing Strategy for LEO* — state of the art LB LEO.
9. **P46** Kim et al. (2026), *Utilization-aware multipath traffic splitting* — splitting rasio di LEO.
10. **P12** Amalia et al. (2023), *PCC + failover pada MikroTik* — baseline PCC praktis.

## 5. Tiga klaim yang paling kuat didukung literatur

1. **Rasio statis tidak lagi memadai** ketika jalur LEO mengalami degradasi cepat dan kapasitas berubah (P05, P06, P08, P12, P18).
2. **Ambang deteksi dapat diturunkan dari biaya**, bukan hanya dari ARL, dan desain ekonomi chart sudah menunjukkan manfaatnya (P23, P24, P38, P40).
3. **Kuantisasi hash dan SRLG dapat dipertemukan**, tetapi belum ada yang melakukannya untuk rasio per-koneksi multi-WAN (P13, P14, P21, P48, P49).

## 6. Batasan folder ini

- Fokus pada paper 2023-2026; paper klasik (Page, Lorden, Moustakides, Duncan) tetap perlu dikutip dari sumber aslinya.
- Status Scopus untuk penerbit non-IEEE/Elsevier perlu dicek ulang di *Scopus Source List* institusi.
- Beberapa paper 2026 masih *early access* atau belum memiliki volume/halaman final.
- Paper tanpa abstrak daring ditandai eksplisit; ringkasannya harus diverifikasi pada teks penuh.
- Folder ini adalah alat bantu review, bukan pengganti membaca paper.

## 7. Struktur folder

```
review_jurnal_2023_2026/
├── README.md
├── 00_RINGKASAN_REVIEW.md
├── 01_DAFTAR_JURNAL.md
├── 02_DAFTAR_JURNAL.csv
├── 03_DAFTAR_JURNAL.bib
├── per_pembahasan/
│   ├── 1.2.1_QoS_dan_QoE.md
│   ├── 1.2.2_FO_dan_LEO_Starlink.md
│   ├── 1.2.3_MikroTik_dan_PCC_praktik.md
│   ├── 1.2.4_PCC_dan_hash_per_koneksi.md
│   ├── 1.2.5_Load_balancing_dan_SD-WAN.md
│   ├── 1.2.6_Quickest_change_detection.md
│   ├── 1.2.7_CUSUM_dua_arah.md
│   ├── 1.2.8_Histeresis_dan_handover.md
│   ├── 1.2.9_Komitmen_koneksi_dan_biaya.md
│   └── 1.2.10_Integrasi_SRLG_dan_TE.md
├── catatan/
│   ├── 01_MATRIKS_GAP.md
│   ├── 02_PETA_KUTIPAN.md
│   ├── 03_REVISI_YANG_DISARANKAN.md
│   ├── 04_KANDIDAT_DITOLAK_DAN_CATATAN.md
│   ├── 05_VERIFIKASI_METADATA.md
│   ├── 06_KALIMAT_SIAP_PAKAI.md
│   └── 07_DRAFT_KONTRIBUSI.md
└── data_mentah/
    ├── _selected_raw.json
    ├── _csl.json
    ├── _digest.txt
    ├── _targeted.json
    └── _raw_openalex.json
```
