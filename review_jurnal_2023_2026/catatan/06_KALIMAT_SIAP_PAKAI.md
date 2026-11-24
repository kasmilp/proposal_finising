# Kalimat Siap Pakai per Subbab

Gunakan sebagai kerangka; sesuaikan dengan gaya APA 7 dan pedoman Universitas Hasanuddin.

## 1.2.1 QoS dan QoE

> QoS agregat (delay, jitter, packet loss, throughput) perlu dilengkapi QoE sisi pengguna, karena alokasi yang tampak baik pada throughput dapat menurunkan pengalaman aplikasi dan memboroskan kapasitas jalur mahal (Sultan & El-Sayed, 2023; Su et al., 2026; Pieskä et al., 2024).

## 1.2.2 FO dan LEO Starlink

> Pengukuran Starlink menunjukkan variasi throughput dan latensi yang jauh lebih besar daripada jaringan terestrial, termasuk outage, burst loss akibat obstruksi, dan variasi periodik 15 detik (Ma et al., 2023; Laniewski et al., 2025; Mohan et al., 2024). Pola ini menuntut probe dan ambang yang mampu membedakan degradasi singkat dari degradasi persisten.

## 1.2.3 MikroTik dan PCC

> Implementasi PCC pada MikroTik umumnya menetapkan rasio dan aturan failover secara statis, sehingga pembagian beban tidak merespons degradasi parsial secara adaptif (Amalia et al., 2023). Perbandingan vendor menunjukkan bahwa smart balancing sudah menjadi fitur komersial, tetapi mekanismenya tidak transparan dan tidak netral-vendor (Putra et al., 2026).

## 1.2.4 Hash per-koneksi

> Consistent hashing dan kuantisasi hash telah terbukti menjaga stabilitas pemetaan serta meminimalkan migrasi saat kapasitas berubah (Levi & Keslassy, 2023; Dong et al., 2024). Namun, mekanisme yang ada menerima bobot kapasitas server, bukan status degradasi jalur multi-WAN.

## 1.2.5 SD-WAN

> SD-WAN adaptif dan pembelajaran penguatan telah menunjukkan perbaikan kinerja, tetapi keputusannya umumnya berada pada tingkat overlay atau situs dan belum memberikan ambang yang dapat dijelaskan untuk rasio hash per-koneksi (Troia et al., 2026; Botta et al., 2024; Cruvellier et al., 2025).

## 1.2.6 QCD

> CUSUM klasik optimal di bawah kriteria Lorden, tetapi jaminan tersebut bertumpu pada asumsi distribusi dan ambang alarm palsu, bukan pada biaya evakuasi versus pemulihan yang berbeda (Xie et al., 2023; Sun & Zou, 2024). Data jaringan yang berkorelasi juga melanggar asumsi i.i.d. yang menjadi dasar banyak analisis ARL.

## 1.2.7 CUSUM dua arah

> Varian CUSUM dengan estimasi distribusi pasca-perubahan menunjukkan bahwa deteksi tetap dapat dilakukan ketika bentuk degradasi tidak diketahui sebelumnya (Liang & Veeravalli, 2024), dan CUSUM multivariat telah dipakai untuk monitoring jaringan kabel optik (Xu et al., 2025). Keduanya belum memasukkan biaya asimetris dan aksi hash.

## 1.2.8 Histeresis

> Histeresis margin dan time-to-trigger efektif menekan handover yang tidak perlu (Eydian et al., 2025; Mbulwa et al., 2024), tetapi nilai margin umumnya ditetapkan tetap atau dioptimalkan secara heuristik, bukan diturunkan dari biaya keputusan dan headroom kapasitas.

## 1.2.9 Komitmen dan biaya

> Desain ekonomi chart menunjukkan bahwa parameter deteksi dapat dipilih dengan meminimalkan biaya total, bukan hanya ARL (Shojaee et al., 2024; García-Bustos & Ramírez-Figueroa, 2023). Namun, model tersebut belum memuat komitmen umur koneksi dan porsi beban pada jaringan multi-WAN.

## 1.2.10 SRLG dan TE

> Literatur SRLG menyediakan jalur primer/backup yang disjoint (Bérczi-Kovács et al., 2024; Matsuura et al., 2024), dan literatur LEO menyediakan traffic engineering berbasis prediksi serta multipath splitting (Ju et al., 2025; Kim et al., 2026). Belum ada yang menerjemahkan risiko bersama tersebut menjadi rasio hash per-koneksi.

## Paragraf penghubung ke kontribusi

> Dengan demikian, celah yang diisi penelitian ini bukan pada PCC, CUSUM, atau histeresis sebagai komponen tunggal, melainkan pada penurunan asimetri ambang dari biaya komitmen per-koneksi dan headroom, serta penerjemahannya menjadi rasio hash yang sadar SRLG dan meminimalkan perubahan pemetaan.
