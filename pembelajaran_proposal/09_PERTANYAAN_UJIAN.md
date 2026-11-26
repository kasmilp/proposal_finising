# 09. Pertanyaan Ujian dan Cara Menjawab

> **Subbab sumber di proposal:** seluruh isi proposal (Bab I & II); intinya pada 1.4 (hipotesis), 2.5 (perancangan), dan 2.7 (analisis data).

File ini berisi **pertanyaan yang mungkin diajukan penguji** saat sidang proposal, beserta kunci jawaban singkat. Gunakan sebagai latihan menjawab lisan.

---

## Kelompok 1: Konsep dasar & motivasi

**Q1. Mengapa Anda tidak cukup memakai PCC statis?**
*Kunci:* PCC statis menetapkan rasio tetap (mis. 1:1:1) sekali saja, tidak mengevaluasi ulang kondisi jalur. Karena jalur LEO dinamis (degradasi transien, obstruksi, rekonfigurasi), rasio tetap mengirim koneksi baru ke jalur yang sedang buruk → QoS turun.

**Q2. Mengapa memakai dua Starlink (LEO) dan satu FO?**
*Kunci:* Lokasi penelitian (RT/RW Net) memang punya konfigurasi itu. Dua Starlink di sini sekaligus menjadi ilustrasi **SRLG** — keduanya berbagi risiko (terbukti korelasi degradasi 0,70–0,78), sehingga tidak bisa diperlakukan sebagai cadangan independen.

**Q3. Apa beda QoE dan QoS?**
*Kunci:* QoS = kualitas dari sisi jaringan (delay, jitter, loss, throughput). QoE = yang dirasakan pengguna. Eksperimen utama berbasis QoS sisi klien; QoE dibahas sebagai konteks di tinjauan pustaka.

---

## Kelompok 2: Teori deteksi

**Q4. Jelaskan CUSUM dengan sederhana.**
*Kunci:* CUSUM mengakumulasi LLR setiap pengamatan untuk "mengingat" bukti. Statistik dibatasi di bawah nol; alarm saat melampaui ambang. Keunggulan: menimbang kekuatan tiap sampel, bukan sekadar menghitung.

**Q5. Apa itu ARL dan tunda deteksi? Mengapa bertentangan?**
*Kunci:* ARL = rata-rata jumlah pengamatan sampai alarm (palsu); tunda deteksi = waktu dari perubahan nyata sampai alarm. Ambang besar → alarm palsu jarang tapi tunda lama; ambang kecil → sebaliknya.

**Q6. Mengapa tidak memakai machine learning / SAW / AHP?**
*Kunci:* Skoring multi-kriteria menilai sesaat tanpa memori; ML butuh banyak data berlabel dan prediksi Starlink terbatas; aturan k-sampel tidak menimbang kekuatan sampel. CUSUM menggabungkan akumulasi bukti + kendali eksplisit atas tradeoff tunda–alarm.

---

## Kelompok 3: Algoritma usulan

**Q7. Apa kebaruan utama penelitian Anda?**
*Kunci:* Menurunkan **asimetri ambang evakuasi vs pemulihan dari biaya komitmen per-koneksi dan headroom**, lalu menerjemahkannya menjadi rasio hash yang sadar SRLG dengan perubahan pemetaan minimal. Bukan sekadar "PCC dinamis", "CUSUM", atau "histeresis" — ketiganya sudah ada; yang baru adalah penurunan asimetri dari biaya + penerjemahan ke bobot hash.

**Q8. Bagaimana Anda menentukan h↓ dan h↑?**
*Kunci:* Meminimalkan biaya harapan per siklus = (biaya keputusan salah × laju alarm palsu) + (biaya penundaan × tunda deteksi). Karena struktur biaya evakuasi dan pemulihan berlawanan, hasilnya dua ambang berbeda; diperbarui di loop lambat sesuai headroom.

**Q9. Apa peran headroom?**
*Kunci:* Saat kapasitas melimpah, pemulihan dibuat lebih hati-hati (asimetri besar). Saat kapasitas langka, bobot kapasitas tertahan β(H) membesar → asimetri mengecil otomatis.

**Q10. Mengapa porsi Starlink yang dievakuasi dialihkan ke FO, bukan ke Starlink lain?**
*Kunci:* Karena dua Starlink berbagi risiko (SRLG). Memindahkan ke Starlink lain tidak memberi keamanan; FO adalah jalur yang tidak berbagi risiko.

**Q11. Apa itu kuantisasi minimal-remap dan mengapa penting?**
*Kunci:* Rasio PCC hanya bisa kelipatan 1/N. Bobot target dikuantisasi ke kelompok hash dengan memilih pemetaan yang paling sedikit mengubah kelompok → menekan frekuensi rekonfigurasi F dan dampak pada koneksi baru.

---

## Kelompok 4: Metrik & evaluasi

**Q12. Apa itu E, U, dan F?**
*Kunci:* E = porsi koneksi baru ke jalur terdegradasi; U = kapasitas jalur sehat yang tak terpakai; F = frekuensi perubahan status/pemetaan per jam. Semua "lebih kecil lebih baik".

**Q13. Mengapa tidak cukup meminimalkan E saja?**
*Kunci:* Ada tradeoff E–U. Menurunkan E dengan agresif membuang kapasitas sehat (U naik). Karena itu dibandingkan E pada U setara / kurva E–U.

**Q14. Bagaimana Anda memastikan perbandingan yang adil antar kebijakan?**
*Kunci:* Replay offline (masukan identik), gateway uji paralel (kondisi jalur sama, serentak), variabel kontrol dikendalikan (klien & pola trafik identik), dan pengujian berjenjang.

---

## Kelompok 5: Metodologi & keterbatasan

**Q15. Apa kelemahan desain kuasi-eksperimental Anda?**
*Kunci:* Kondisi cuaca, perilaku pelanggan, beban aktual di luar kendali. Diakomodasi lewat **stratifikasi** (cuaca, jam sibuk, headroom) dan klaim generalisasi yang dibatasi pada satu situs.

**Q16. Bagaimana menangani autokorelasi / asumsi i.i.d. CUSUM?**
*Kunci:* CUSUM klasik mengasumsikan observasi i.i.d. Penelitian (i) menguji autokorelasi residu, (ii) memakai window-limited CUSUM, (iii) menyiapkan pembanding robustness (AR-CuSum). (Rujukan: Sun & Zou 2024; Xie et al. 2023.)

**Q17. Mengapa model observasi hanya dua nilai LLR?**
*Kunci:* Penyederhanaan model pola multi-target menjadi dua nilai (11 = keduanya buruk vs lainnya) membuat perhitungan ringan — hanya penjumlahan — sesuai loop cepat. Nilai dikalibrasi dari data lokasi.

**Q18. Apakah hasil bisa digeneralisasi?**
*Kunci:* Model netral-vendor (berlaku untuk PCC, ECMP, nftables, SD-WAN), tetapi **validasi empiris hanya satu situs**. Generalisasi lebih luas memerlukan pengujian tambahan.

---

## Kelompok 6: Pertanyaan "jebakan"

**Q19. Bukankah "sadar biaya" sudah ada di quality control / SD-WAN?**
*Kunci:* Ya, desain ekonomi control chart dan cost-aware SD-WAN sudah ada. Namun model yang ada belum memuat **komitmen per-koneksi** (λ, w, L, G) dan belum diterjemahkan menjadi **rasio hash per-koneksi** dengan SRLG pada multi-WAN. Itu yang menjadikan kontribusi ini spesifik.

**Q20. Mengapa tidak langsung memakai MDP (solusi optimal eksak)?**
*Kunci:* MDP memerlukan model transisi lengkap dan komputasi besar. Penelitian memakai pendekatan orde-pertama (Lorden) yang lebih praktis untuk loop cepat; MDP dinyatakan sebagai batasan/arah lanjutan.

---

## Tips menjawab sidang

1. **Mulai dari masalah**, bukan dari rumus: "Masalahnya adalah…"
2. Jangan menghafal; **ceritakan kembali** dengan kata-kata sendiri.
3. Untuk rumus, pahami **makna tiap simbol**, bukan sekadar menghafal bentuk.
4. Jika tidak tahu, akui batasan dan hubungkan ke langkah lanjutan.
5. Selalu tutup dengan **"karena itu, kontribusi saya adalah…"**.

---

## Latihan: jawab tanpa melihat file

1. Gambarkan alur 6 langkah algoritma.
2. Jelaskan pertukaran E–U–F dengan contoh angka dari studi pendahuluan.
3. Tuliskan H1 dan H2.
4. Jelaskan mengapa asimetri diturunkan dari biaya, bukan ditebak.
5. Sebutkan tiga kelemahan desain dan bagaimana Anda menanganinya.
