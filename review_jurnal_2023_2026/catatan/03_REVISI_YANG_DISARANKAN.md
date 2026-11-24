# Revisi yang Disarankan Berdasarkan Literatur

Diurutkan dari yang paling mendesak. Setiap butir menyebut paper pendukung.

## R1. Definisikan E, U, dan F secara formal (prioritas tertinggi)

Tambahkan definisi operasional sebelum masuk ke hipotesis:

- **E (exposure):** proporsi koneksi baru yang ditempatkan pada jalur berstatus terdegradasi, diukur pada jendela waktu yang sama dengan status jalur.
- **U (unused capacity):** kapasitas jalur sehat yang tidak terpakai karena rasio terlalu konservatif.
- **F (reconfiguration frequency):** jumlah perubahan bobot/status per jam, atau jumlah remap bucket per jam.

Paper: P04 (excess delay), P38 (biaya jalur mahal), P41 (migration overhead), P12 (QoS agregat).

Mengapa: tanpa definisi ini, klaim “E lebih rendah pada U setara” tidak dapat diuji dan mudah dibantah penguji.

## R2. Ganti “U setara” dengan uji frontier E–U

Jangan hanya membandingkan pada satu titik U. Buat kurva E–U dengan beberapa nilai ambang, lalu bandingkan:

- E pada U yang sama (matched-U), atau
- luas area di bawah frontier (semakin kecil semakin baik).

Paper: P40 (tradeoff ekonomi-statistik), P35 (tradeoff handover success vs spectral efficiency), P04 (delay vs utilization).

Mengapa: “U setara” adalah klaim kuat yang sulit dibuktikan dengan satu konfigurasi. Frontier lebih jujur dan lebih informatif.

## R3. Akui asumsi i.i.d. dan siapkan alternatif

Tambahkan satu paragraf:

> “CUSUM klasik mengasumsikan observasi i.i.d. sebelum perubahan. Data probe jaringan dapat berkorelasi karena rekonfigurasi periodik, cuaca, dan beban. Karena itu, penelitian ini (i) menguji autokorelasi residu, (ii) memakai window-limited CUSUM, dan (iii) menyiapkan AR-CuSum sebagai pembanding robustness.”

Paper: P23 (QCD AR), P24 (window-limited CUSUM), P27 (robust score-based), P28 (Markov), P29 (post-change estimation).

Mengapa: ini adalah kritik metodologis paling mungkin dari penguji QCD.

## R4. Perkuat model observasi M=2

Jelaskan:

- mengapa dua target cukup (biaya probe, independensi, cakupan),
- bagaimana menangani target yang mati,
- bagaimana menggabungkan dua target (AND/OR/median),
- uji sensitivitas terhadap jumlah target.

Paper: P05 (dynamics), P06 (obstruction/burst loss), P08 (15-s reconfiguration), P31 (multivariate CUSUM).

Mengapa: model observasi dua target dengan rolling median dan p1=0.25 terlihat rapuh; penguji akan bertanya apa yang terjadi jika satu target bias.

## R5. Tambahkan tabel aksi 8 status dan batasan SRLG

Buat tabel lengkap:

| Status FO | Status LEO A | Status LEO B | Bobot target | Catatan SRLG |
|---|---|---|---|---|
| baik | baik | baik | ... | ... |
| baik | buruk | baik | ... | ... |
| ... | ... | ... | ... | ... |

Paper: P21 (joint/disjoint overlay), P48 (regional SRLG), P49 (SRLG-disjoint path), P50 (SBPP).

Mengapa: proposal saat ini belum menunjukkan peta aksi lengkap; ini celah yang mudah dilihat penguji.

## R6. Jelaskan algoritma kuantisasi dan sapuan N

Tambahkan pseudocode:

1. Hitung bobot kontinu dari status jalur.
2. Kuantisasi ke N bucket.
3. Terapkan `keep-min(c_i, n_i)` untuk meminimalkan remap.
4. Ukur quantization error dan F.

Paper: P13 (quantized CH), P14 (weighted DxHash), P16 (CHCA), P17 (survey).

Mengapa: klaim “minimal remap” harus dibuktikan, bukan diasumsikan.

## R7. Tambahkan baseline A0–A7 dan protokol tuning yang adil

Minimal:

- A0: PCC statis 1:1:1.
- A1: PCC statis dengan rasio kapasitas.
- A2: failover reaktif.
- A3: histeresis k-sampel.
- A4: CUSUM simetris.
- A5: CUSUM asimetris tanpa SRLG.
- A6: CUSUM asimetris + SRLG, kuantisasi naif.
- A7: usulan lengkap (minimal-remap).

Paper: P12, P19, P20, P38, P40.

Mengapa: tanpa ablation, kontribusi K2 dan K3 tidak terpisahkan.

## R8. Tambahkan tabel parameter biaya dan analisis sensitivitas

Tabel: `C_salah`, `C_tunda`, `ν`, `Δt`, `λ`, `w`, `L`, `G`, `H`.

Lakukan sensitivitas ±25% dan tunjukkan perubahan `h*`.

Paper: P40 (sensitivity to shift misestimation), P39 (economic design), P38 (cost vs QoE).

Mengapa: rumus `h*` hanya kredibel jika parameter dan asumsinya jelas.

## R9. Perjelas evaluasi shadow-mode

Jelaskan:

- bagaimana trafik produksi dicatat,
- bagaimana keputusan shadow dibandingkan dengan keputusan aktual,
- bagaimana counterfactual dihitung,
- bagaimana menghindari selection bias.

Paper: P19 (SD-WAN testbed), P21 (Mininet + real topology), P12 (production deployment).

Mengapa: shadow-mode adalah bagian yang paling mudah dipertanyakan secara metodologis.

## R10. Perbaiki timeline 3 bulan

Timeline saat ini terlalu padat untuk:

- kalibrasi q0,
- replay,
- testbed,
- shadow,
- produksi,
- analisis.

Saran: tambahkan pilot 1-2 minggu dan buffer analisis; kurangi jumlah skenario jika perlu.

Paper: P12 (NDLC), P18 (SD-WAN deployment), P05 (measurement campaign).

## R11. Perbaiki inkonsistensi dokumen

- “VSAT/LEO”: VSAT umumnya GEO; pisahkan atau jelaskan.
- Heading 1.2.5 berbahasa Inggris: seragamkan ke Indonesia.
- Tabel State of the Art bernomor 12 tetapi tidak ada di Daftar Tabel.
- “keempat level” vs lima skenario A–E: samakan.
- Typo “kebururukan”, “single point  of failure”.
- Placeholder referensi `**` untuk Putra (2024) dan Ullah et al. (2025).
- Format nama “Duliades Mirsal & Herman Bedi Agtriadi”.
- “G. S. G.S. Kuo” duplikasi.

## R12. Tambahkan subbab 1.5 Kontribusi Penelitian

Lihat `catatan/07_DRAFT_KONTRIBUSI.md` untuk draft tiga paragraf dan tabel kontribusi → RQ → hipotesis → metrik.
