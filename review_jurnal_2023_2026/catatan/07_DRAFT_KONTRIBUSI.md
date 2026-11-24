# Draft Subbab 1.5 Kontribusi Penelitian

Letakkan sebagai subbab baru setelah 1.4 Hipotesis (geser penomoran setelahnya), atau sebagai bagian awal 1.6 Manfaat.

## 1.5 Kontribusi Penelitian

Kontribusi utama penelitian ini terletak pada persimpangan tiga bidang yang selama ini berkembang terpisah: deteksi perubahan sekuensial, pembagian beban per-koneksi berbasis hash, dan penanganan risiko bersama pada jaringan multi-WAN heterogen. Literatur deteksi perubahan sekuensial menyediakan prosedur CUSUM yang optimal untuk mendeteksi perubahan distribusi, tetapi ambangnya diturunkan dari batasan alarm palsu, bukan dari biaya keputusan yang berbeda antara evakuasi dan pemulihan. Literatur PCC dan pembagian beban berbasis hash menyediakan mekanisme per-koneksi yang menjaga keutuhan sesi, tetapi rasionya statis dan tidak merespons degradasi jalur. Literatur SD-WAN, handover, dan SRLG menyediakan gagasan histeresis, probe, dan jalur cadangan, tetapi ambang dan pengatur waktunya ditetapkan secara heuristik serta tidak memperhitungkan komitmen per-koneksi dan kuantisasi rasio.

Penelitian ini mengisi celah tersebut melalui empat kontribusi. Pertama, model keputusan netral-vendor yang secara eksplisit memuat komitmen per-koneksi: keputusan hanya memengaruhi koneksi baru, dan biaya keputusan salah merupakan fungsi dari laju koneksi baru, porsi beban, umur koneksi, dan sisa durasi degradasi. Kedua, derivasi ambang evakuasi dan pemulihan yang asimetris dari biaya keputusan salah, biaya penundaan, divergensi informasi, dan headroom kapasitas, sehingga asimetri tidak lagi berupa parameter tetap melainkan fungsi dari kondisi kapasitas. Ketiga, peta aksi yang memperhitungkan risiko degradasi bersama antara dua terminal Starlink dan algoritma kuantisasi rasio ke N kelompok hash yang meminimalkan perubahan pemetaan. Keempat, validasi empiris bertahap pada jaringan nyata yang menggabungkan satu jalur fiber optic dan dua jalur satelit LEO, mencakup replay, gateway uji paralel, mode bayangan, dan pengujian produksi, dengan metrik paparan E, kapasitas tertahan U, frekuensi rekonfigurasi F, serta QoS sisi klien.

Dengan demikian, kebaruan penelitian ini bukan pada penggunaan PCC, CUSUM, atau histeresis sebagai komponen tunggal—ketiganya sudah dikenal—melainkan pada penurunan asimetri ambang dari biaya komitmen per-koneksi dan headroom, serta penerjemahannya menjadi rasio hash yang sadar risiko bersama dan meminimalkan perubahan pemetaan. Formulasi ini bersifat netral-vendor sehingga dapat direalisasikan pada PCC RouterOS, nftables, ECMP, maupun kebijakan jalur SD-WAN.

## Tabel kontribusi → RQ → hipotesis → eksperimen → metrik

| Titik | RQ | Hipotesis | Eksperimen | Metrik | Indikator |
|---|---|---|---|---|---|
| K1 | Bagaimana memodelkan komitmen per-koneksi dan aktuator hash terkuantisasi secara netral-vendor? | H1/H2 | Replay + testbed; sensitivitas L | E_new, E_traffic | Model biaya memprediksi asimetri |
| K2 | Bagaimana menurunkan ambang evakuasi/pemulihan asimetris dari biaya, tunda, dan headroom? | H1 | E–U frontier; oracle; strata H | E pada U setara; cost regret | h* mendekati oracle; asimetri mengecil saat H menipis |
| K3 | Bagaimana memetakan status jalur ke rasio dengan SRLG dan perubahan minimal? | H1b | Ablasi A6/A7; sapuan N | F_map; quantization error | F lebih rendah pada E/U setara |
| K4 | Apakah lapisan usulan menurunkan E/F dan memperbaiki QoS klien? | H1/H2 | Produksi A/D; replay; testbed | E, U, F, QoS, ARL | E/F lebih rendah; QoS lebih baik |

## Catatan

- Jangan menulis “PCC belum pernah diteliti”; tulis “PCC telah banyak dipakai, tetapi rasio statis”.
- Jangan menulis “CUSUM belum pernah dipakai untuk jaringan”; tulis “CUSUM telah dipakai, tetapi ambangnya belum diturunkan dari biaya komitmen per-koneksi”.
- Klaim “minimal remap” harus disertai bukti algoritmik/eksperimental, bukan hanya nama algoritma.
