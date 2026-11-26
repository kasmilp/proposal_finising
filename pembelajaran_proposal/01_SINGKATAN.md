# 01. Daftar Singkatan dan Istilah

> **Subbab sumber di proposal:** menyebar di seluruh dokumen (Bab I & II). Akronim spesifik sering muncul pada 1.2.1–1.2.10.

Daftar ini mencakup semua akronim dan istilah kunci yang dipakai dalam proposal. Disusun berdasarkan abjad. Untuk pemahaman konsep yang lebih dalam, lanjut ke `02_KONSEP_DASAR.md`.

---

## A. Akronim

| Akronim | Kepanjangan | Penjelasan singkat |
|---|---|---|
| **AHP** | Analytic Hierarchy Process | Metode skoring multi-kriteria untuk memilih/meranking alternatif; disebut sebagai pembanding yang menilai kondisi sesaat |
| **API** | Application Programming Interface | Antarmuka perangkat lunak; dipakai kontroler untuk membaca statistik & menulis pemetaan ke router |
| **ARL** | Average Run Length | Rata-rata jumlah pengamatan sampai terjadi alarm (biasanya alarm palsu) pada prosedur deteksi |
| **ATSSS** | Access Traffic Steering, Switching and Splitting | Kerangka 3GPP (5G) untuk mengarahkan trafik multipath; menjadi salah satu rujukan pembanding |
| **CHO** | Conditional HandOver | Prosedur handover 5G dengan kondisi yang disiapkan lebih awal |
| **CPE** | Customer Premises Equipment | Perangkat di sisi pelanggan (mis. router/ONT) |
| **CUSUM** | Cumulative Sum | Prosedur deteksi perubahan yang mengakumulasi jumlah kumulatif (LLR) |
| **ECMP** | Equal-Cost Multi-Path | Skema pembagian beban RouterOS yang mendistribusikan sesi merata ke jalur berbiaya setara |
| **FO** | Fiber Optic | Jalur WAN berbasis kabel serat optik (mis. IndiHome) |
| **GEO** | Geostationary Earth Orbit | Satelit orbit geostasioner (tinggi, "diam" relatif terhadap bumi) |
| **GNS3** | Graphical Network Simulator 3 | Alat simulasi jaringan; dipakai pada beberapa rujukan PCC |
| **H1 / H2** | Hipotesis 1 / Hipotesis 2 | Dua hipotesis kerja penelitian (lihat `07_SKENARIO_DAN_HIPOTESIS.md`) |
| **HEO** | Highly Elliptical Orbit | Orbit satelit sangat eliptik |
| **ISP** | Internet Service Provider | Penyedia layanan internet (IndiHome, Starlink, dll.) |
| **LLR** | Log-Likelihood Ratio | Logaritma perbandingan peluang pengamatan di bawah kondisi terdegradasi vs normal |
| **LEO** | Low Earth Orbit | Satelit orbit rendah Bumi (mis. Starlink) |
| **MDP** | Markov Decision Process | Kerangka pengambilan keputusan sekuensial; disebut sebagai pendekatan eksak tapi di luar cakupan |
| **NDLC** | Network Development Life Cycle | Kerangka pengembangan jaringan: Analysis → Design → Simulation Prototyping → Implementation → Monitoring → Management |
| **ONT** | Optical Network Terminal | Perangkat terminasi jalur fiber optik di sisi pelanggan |
| **PCC** | Per-Connection Classifier | Metode load balancing RouterOS yang mengelompokkan koneksi via hash lalu mengarahkan tiap kelompok ke gateway |
| **QCD** | Quickest Change Detection | Bidang deteksi perubahan sekuensial (mendeteksi perubahan distribusi secepat mungkin) |
| **QoS** | Quality of Service | Ukuran kualitas layanan jaringan (delay, jitter, packet loss, throughput) |
| **QoE** | Quality of Experience | Kualitas yang dirasakan pengguna akhir |
| **R&D** | Research and Development | Pendekatan penelitian-pengembangan |
| **RTT** | Round-Trip Time | Waktu tempuh pulang-pergi paket probe |
| **RouterOS** | Router Operating System | Sistem operasi router MikroTik |
| **RT/RW Net** | Rukun Tetangga/Rukun Warga Network | Jaringan internet komunal skala kecil-menengah di Indonesia (lokasi penelitian) |
| **SAW** | Simple Additive Weighting | Metode skoring multi-kriteria sederhana |
| **SD-WAN** | Software-Defined Wide Area Network | Arsitektur WAN yang memisahkan kontrol dan data, memilih jalur berdasar SLA |
| **SLA** | Service Level Agreement | Perjanjian tingkat layanan; ambang kualitas yang menjadi acuan |
| **SRLG** | Shared Risk Link Group | Kelompok jalur yang berbagi risiko kegagalan bersama (mis. dua Starlink serupa) |
| **THIPON** | (TIPHON) Telecommunications and Internet Protocol Harmonization Over Networks | Standar penilaian QoS (skor 1–4) yang dipakai rujukan PCC |
| **TOPSIS** | Technique for Order Preference by Similarity to Ideal Solution | Metode skoring multi-kriteria |
| **TTT** | Time-To-Trigger | Waktu tahan sebelum handover dipicu |
| **WAN** | Wide Area Network | Jaringan area luas; "multi-WAN" = memakai beberapa jalur ISP sekaligus |

---

## B. Simbol / variabel penting

| Simbol | Arti | Catatan |
|---|---|---|
| λ | Laju koneksi baru | Per detik; diukur dari tabel koneksi |
| w | Porsi beban suatu jalur | Bobot target/nominal |
| L | Umur koneksi (median) | Diukur dari tabel koneksi |
| G | Sisa durasi degradasi | Saat keputusan diambil |
| Δt | Interval siklus probe | Skala detik |
| M | Jumlah target probe per jalur | Model observasi multi-target |
| N | Jumlah kelompok hash | PCC mengkuantisasi rasio ke kelipatan 1/N |
| h↓ / h↑ | Ambang evakuasi / pemulihan | Asimetris |
| S↓ / S↑ | Statistik CUSUM degradasi / pemulihan | Diperbarui tiap siklus |
| ν | Laju kejadian perubahan nyata | Per detik |
| C_salah | Biaya satu keputusan salah | |
| C_tunda | Biaya tiap siklus penundaan | |
| H | Headroom kapasitas | Kapasitas cadangan |
| β(H) | Bobot kapasitas tertahan | Fungsi headroom; membesar saat kapasitas langka |
| E | Paparan (exposure) | Porsi beban pada jalur terdegradasi |
| U | Kapasitas tertahan (unused) | Kapasitas jalur sehat yang tak terpakai |
| F | Frekuensi rekonfigurasi | Jumlah perubahan status/pemetaan per jam |
| ℓ(11), ℓ(lainnya) | Nilai LLR untuk pola pengamatan tertentu | Lihat tabel 6 proposal |

---

## C. Konsep singkat (glosarium minimal)

| Istilah | Definisi |
|---|---|
| **Load balancing** | Membagi beban trafik ke beberapa jalur agar tidak ada jalur kelebihan muatan |
| **Failover** | Memindahkan trafik ke jalur cadangan ketika jalur utama gagal |
| **Rasio statis** | Perbandingan pembagian yang ditetapkan tetap (mis. 1:1:1) |
| **Degradasi** | Penurunan kualitas jalur (delay/loss naik, throughput turun) |
| **Pemulihan** | Kembalinya kualitas jalur ke kondisi normal |
| **Histeresis** | Dua ambang berbeda untuk mengaktifkan vs menonaktifkan suatu kondisi |
| **Headroom** | Kapasitas cadangan yang tersisa |
| **Remap / remapping** | Pemindahan pemetaan kelompok hash dari satu jalur ke jalur lain |
| **Netral-vendor** | Model yang tidak terikat pada merek perangkat tertentu |
| **Shadow mode** | Mode bayangan: menghitung & mencatat keputusan tanpa menuliskannya |
| **Replay data** | Menjalankan ulang rekaman data lama pada semua kebijakan |
| **Gateway uji paralel** | Gateway pembanding yang berjalan serentak tanpa mengganggu trafik pelanggan |

---

## Cek pemahaman

1. Apa beda PCC dan ECMP pada RouterOS?
2. Jelaskan arti LLR dan CUSUM dalam satu kalimat.
3. Mengapa E, U, dan F penting untuk penelitian ini?
4. Apa yang dimaksud "netral-vendor" dan mengapa disebutkan dalam proposal?
5. Apa fungsi headroom (H) dan β(H)?
