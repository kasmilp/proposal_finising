# Matriks Gap → Kontribusi

Matriks ini menghubungkan **celah literatur** dengan **empat titik kontribusi** proposal. Kolom “Paper pembeda” menunjukkan paper yang paling dekat, sehingga kalimat pembeda tidak boleh lebih kuat daripada yang dapat dibuktikan.

| No | Celah literatur | Bukti utama | Kontribusi yang menjawab | Paper pembeda | Kalimat pembeda yang aman |
|---|---|---|---|---|---|
| G1 | Rasio PCC/SD-WAN statis; failover reaktif | P12, P11, P18, P19, P20 | K1 + K2 | P12, P19, P20 | “Literatur menetapkan rasio/overlay di awal atau memakai DRL black-box; belum menurunkan rasio hash dari biaya keputusan.” |
| G2 | Ambang QCD dari ARL, bukan biaya | P23, P24, P26, P40 | K2 | P23, P24, P40 | “Ambang CUSUM dioptimalkan untuk alarm palsu, bukan untuk biaya evakuasi versus pemulihan.” |
| G3 | Histeresis simetris/heuristik | P32, P33, P34, P35 | K2 | P32, P33, P34 | “Margin/TTT ditetapkan tetap atau dituning heuristik; belum menjadi fungsi biaya dan headroom.” |
| G4 | Hash quantization belum sadar status jalur | P13, P14, P15, P16 | K3 | P13, P14, P16 | “Kuantisasi hash menjaga stabilitas, tetapi masukannya kapasitas server, bukan status degradasi jalur.” |
| G5 | SRLG hanya untuk jalur primer/backup | P21, P48, P49, P50 | K3 | P21, P48, P49 | “SRLG menghasilkan jalur disjoint, bukan bobot hash yang meminimalkan remap.” |
| G6 | TE LEO di dalam konstelasi, bukan multi-WAN klien | P45, P46, P47 | K1 + K4 | P45, P46 | “Load balancing LEO berfokus pada routing internal; belum menyentuh keputusan klien di gateway multi-WAN.” |
| G7 | Model biaya belum memuat umur koneksi | P38, P39, P40 | K1 + K2 | P38, P40 | “Biaya tunda/kapasitas sudah ada, tetapi belum memuat λ, w, L, dan G sebagai komitmen per-koneksi.” |
| G8 | Evaluasi E/U/F belum menjadi standar | P12, P18, P20 | K4 | P12, P20 | “Evaluasi umumnya QoS agregat; belum ada frontier E–U dengan ablasi dan uji pada U setara.” |

## Celah yang paling defensible

1. **K2 (ambang asimetris sadar biaya)** paling kuat karena menghubungkan QCD dengan economic design chart dan biaya komitmen per-koneksi.
2. **K3 (kuantisasi minimal-remap + SRLG)** juga kuat karena belum ada paper yang secara eksplisit menggabungkan status SRLG dengan bobot hash.
3. **K1 (model komitmen per-koneksi)** berfungsi sebagai jembatan: tanpa K1, K2 hanya “cost-aware threshold” generik yang sudah ada di quality control.
4. **K4 (validasi FO+LEO)** adalah kontribusi empiris; klaim generalisasi harus dibatasi pada satu situs.

## Implikasi untuk rumusan masalah

| Rumusan masalah | Celah yang dijawab | Paper yang harus dikutip |
|---|---|---|
| Bagaimana merancang lapisan keputusan per-koneksi? | G1, G7 | P12, P18, P19, P38 |
| Bagaimana menurunkan ambang asimetris? | G2, G3, G7 | P23, P24, P32, P40 |
| Bagaimana memetakan status ke rasio hash? | G4, G5 | P13, P14, P21, P48, P49 |
| Apakah lapisan menurunkan E/F dan memperbaiki QoS? | G6, G8 | P05, P06, P08, P12, P20, P45, P46 |

## Catatan

- Jangan menulis “belum ada penelitian yang…” tanpa kualifikasi. Tulis “sejauh penelusuran penulis pada literatur 2023-2026…”.
- Untuk G2, paper economic design chart (P39/P40) adalah bukti bahwa ambang dari biaya bukan hal baru di quality control; kebaruan Anda adalah **penerapannya pada komitmen per-koneksi dan aksi hash multi-WAN**.
- Untuk G4/G5, hindari klaim “algoritma baru” jika hanya menggabungkan komponen yang sudah ada; klaim yang tepat adalah “formulasi dan algoritma kuantisasi yang meminimalkan remap dengan batasan SRLG”.
