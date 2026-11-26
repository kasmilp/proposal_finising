# 10. Kuis Pemahaman (dengan Kunci Jawaban)

Gunakan kuis ini untuk menguji diri setelah membaca `01`–`08`. Jawab **sebelum** melihat kunci jawaban di bagian bawah.

---

## Bagian A — Pilihan ganda (pilih satu jawaban paling tepat)

**A1.** Apa masalah utama PCC statis?
- a) Ia tidak bisa membagi beban sama rata
- b) Ia tidak mengevaluasi ulang kondisi jalur, sehingga tetap mengirim koneksi ke jalur yang buruk
- c) Ia hanya bekerja pada satu jalur saja
- d) Ia terlalu mahal untuk diterapkan

**A2.** Mengapa dua terminal Starlink tidak dapat diperlakukan sebagai cadangan independen?
- a) Karena keduanya dari vendor yang sama
- b) Karena keduanya berbagi risiko (SRLG) dan degradasinya berkorelasi tinggi
- c) Karena kapasitasnya terlalu kecil
- d) Karena hanya satu yang bisa aktif

**A3.** LLR (Log-Likelihood Ratio) bernilai besar dan positif menunjukkan…
- a) Bukti kuat bahwa jalur normal
- b) Bukti kuat bahwa jalur terdegradasi
- c) Tidak ada informasi
- d) Alarm palsu

**A4.** Statistik CUSUM dibatasi di bawah oleh nol. Tujuannya adalah…
- a) Agar cepat membunyikan alarm
- b) Agar bukti lama tidak menumpuk tanpa batas
- c) Agar ambang selalu sama
- d) Agar tidak perlu probe

**A5.** Jika ambang h diperbesar, maka…
- a) Alarm palsu lebih jarang, tapi tunda deteksi lebih lama
- b) Alarm palsu lebih sering, tunda lebih singkat
- c) Keduanya (alarm & tunda) mengecil
- d) Tidak ada pengaruh

**A6.** Apa fungsi zona penyangga pada histeresis?
- a) Mempercepat keputusan
- b) Mencegah keputusan berbalik akibat fluktuasi kecil
- c) Menambah beban komputasi
- d) Mengganti probe

**A7.** Mengapa pemulihan dibuat lebih hati-hati (asimetris) daripada evakuasi?
- a) Karena evakuasi selalu salah
- b) Karena pemulihan terlalu cepat berisiko menambatkan koneksi baru di jalur yang belum pulih
- c) Karena pemulihan lebih murah
- d) Karena jaringan lebih suka status DIEVAKUASI

**A8.** Metrik yang menunjukkan porsi koneksi baru yang masuk ke jalur terdegradasi adalah…
- a) U
- b) F
- c) E
- d) QoS

**A9.** Menurunkan E secara agresif umumnya mengakibatkan…
- a) U menurun juga
- b) U naik (kapasitas sehat terbuang)
- c) F selalu nol
- d) Tidak ada dampak

**A10.** Dalam peta aksi, porsi Starlink yang dievakuasi dialihkan ke…
- a) Starlink lain
- b) FO (yang tidak berbagi risiko)
- c) Dibagi ke semua jalur termasuk Starlink yang berbagi risiko
- d) Disimpan saja

**A11.** Mengapa bobot target dikuantisasi ke kelompok hash?
- a) Karena PCC hanya bisa merealisasikan rasio kelipatan 1/N
- b) Karena hash lebih cepat
- c) Karena probe tidak bisa diukur
- d) Karena agar tersimpan di basis data

**A12.** Uji statistik yang dipakai bila data tidak normal adalah…
- a) Uji-t berpasangan
- b) Wilcoxon signed-rank
- c) ANOVA
- d) Regresi linear

**A13.** "Shadow mode" dalam pengujian berarti…
- a) Menjalankan sistem penuh langsung
- b) Menghitung & mencatat keputusan tanpa menuliskannya ke aktuator
- c) Mematikan jaringan
- d) Menggunakan data buatan

**A14.** Skenario "E" dalam rancangan percobaan berfungsi sebagai…
- a) Kandidat pembanding utama
- b) Acuan batas untuk menempatkan kurva E–U
- c) Baseline utama
- d) Mode hujan

**A15.** Konsep "netral-vendor" berarti…
- a) Model hanya berlaku untuk MikroTik
- b) Model tidak terikat pada merek perangkat tertentu
- c) Tidak memakai vendor sama sekali
- d) Hanya untuk Linux

---

## Bagian B — Esai singkat

**B1.** Jelaskan alur 6 langkah algoritma usulan secara berurutan.

**B2.** Jelaskan mengapa asimetri ambang (h↓ vs h↑) diturunkan dari biaya keputusan dan headroom, bukan ditebak.

**B3.** Tuliskan H1 dan H2 dengan kata-kata sendiri.

**B4.** Jelaskan tradeoff E–U–F dan mengapa perbandingan dilakukan pada U yang setara.

**B5.** Mengapa penelitian tidak langsung memakai MDP untuk solusi optimal eksak?

---

## Kunci jawaban

### Bagian A

| No | Jawaban | No | Jawaban | No | Jawaban |
|---|---|---|---|---|---|---|
| A1 | b | A6 | b | A11 | a |
| A2 | b | A7 | b | A12 | b |
| A3 | b | A8 | c | A13 | b |
| A4 | b | A9 | b | A14 | b |
| A5 | a | A10 | b | A15 | b |

### Bagian B (kunci ringkas)

**B1.** 1) Probe aktif → pola pengamatan; 2) pola → LLR; 3) akumulasi CUSUM dua arah (S↓/S↑); 4) bandingkan dgn ambang h↓/h↑ → transisi status; 5) hitung bobot target via peta aksi SRLG-aware; 6) kuantisasi ke N kelompok hash dgn minimal-remap → tulis ke aktuator PCC.

**B2.** Ambang dipilih untuk meminimalkan biaya harapan per siklus = (biaya keputusan salah × laju alarm palsu) + (biaya penundaan × tunda deteksi). Karena struktur biaya evakuasi (menahan kapasitas sehat vs mengirim ke jalur buruk) dan pemulihan (menambatkan koneksi di jalur belum pulih vs menahan kapasitas) berlawanan, hasilnya dua ambang berbeda. Saat headroom melimpah, asimetri besar; saat headroom langka, β(H) membesar sehingga asimetri mengecil otomatis. Jadi bukan parameter tebakan.

**B3.** H1: ambang asimetris dari biaya menurunkan E (pada U setara) dan menurunkan F dibanding k-sampel-berturut dan CUSUM simetris. H2: sistem usulan menurunkan E dan memperbaiki QoS klien dibanding baseline (PCC statis).

**B4.** Menurunkan E (menghindari jalur buruk) cenderung menaikkan U (kapasitas sehat terbuang); menurunkan F (jarang ganti) bisa menaikkan E jika terlalu malas bereaksi. Karena itu membandingkan E pada U setara / kurva E–U lebih jujur daripada sekadar meminimalkan E.

**B5.** MDP memerlukan model transisi lengkap dan komputasi besar; penelitian memakai pendekatan orde-pertama (Lorden) yang ringan untuk loop cepat. MDP dinyatakan sebagai batasan dan arah lanjutan.

---

## Skor

- Bagian A: 15 soal. Hitung benar.
- Bagian B: bisa "meluluskan" bila Anda mampu menjawab B1–B5 tanpa melihat catatan dengan lancar.
- Target: **A ≥ 13 benar** dan **B1–B5 lancar** sebelum dianggap siap ujian.
