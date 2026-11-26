# 04. Histeresis Asimetris

> **Subbab sumber di proposal:** 1.2.8 (histeresis & handover), 2.5.4 (perancangan ambang histeresis asimetris).

File ini menjelaskan **konsep histeresis** yang menjadi "saringan keputusan" sistem, dan bagaimana ia berhubungan dengan masalah di proposal.

---

## 1. Apa itu histeresis?

**Histeresis** adalah mekanisme yang menetapkan **dua syarat berbeda** untuk mengaktifkan dan menonaktifkan suatu kondisi.

Contoh termostat:
- Nyalakan pemanas saat suhu < 18°C.
- Matikan saat suhu > 22°C.

Ada **celah** antara 18 dan 22°C — ini **zona penyangga**. Tanpa celah ini (misal nyala/mati di titik yang sama), fluktuasi kecil akan membuat perangkat **menghidup-matiikan terus-menerus** (osilasi).

---

## 2. Mengapa histeresis relevan di sini?

Dalam jaringan, kita mengambil keputusan `SEHAT ⇄ DIEVAKUASI` untuk tiap jalur. Tanpa histeresis, jika kita memakai satu ambang saja, fluktuasi kecil pada kualitas jalur akan membuat status **bolak-balik** (flapping) — parah untuk jaringan.

Dengan histeresis, kita memakai **dua ambang berbeda**:
- **Ambang evakuasi (h↓)**: untuk memutuskan "jalur ini buruk, evakuasi".
- **Ambang pemulihan (h↑)**: untuk memutuskan "jalur ini sudah pulih, gunakan lagi".

Karena h↑ > h↓ (pemulihan lebih ketat), ada zona penyangga yang mencegah keputusan berbalik akibat fluktuasi kecil.

---

## 3. Histeresis asimetris: rekoverihan lebih hati-hati

Proposal memakai histeresis **asimetris**: syarat pemulihan **lebih ketat** daripada syarat degradasi.

| Arah | Ambang | Sifat |
|---|---|---|
| Degradasi (SEHAT → DIEVAKUASI) | h↓ | Lebih rendah → cepat bereaksi |
| Pemulihan (DIEVAKUASI → SEHAT) | h↑ | Lebih tinggi → hati-hati, menahan diri |

**Alasan logis:** dalam jaringan, pemulihan yang terlalu cepat berbahaya — jika kita menganggap jalur sudah pulih padahal belum, kita akan mengirim koneksi baru ke jalur yang masih buruk, dan koneksi itu "tertambat" di sana untuk seluruh umurnya. Maka lebih aman **menahan pemulihan** sampai benar-benar yakin.

---

## 4. Kaitan dengan handover seluler

Konsep ini analog dengan **handover** pada jaringan seluler/satelit:
- **Margin histeresis** — selisih sinyal minimum sebelum pindah sel.
- **Time-To-Trigger (TTT)** — waktu tahan sebelum handover dipicu.

Di literatur, margin dan TTT ini umumnya **ditetapkan heuristik** (tebakan berdasarkan pengalaman) dan **simetris**. Proposal menekankan: **besarnya asimetri seharusnya diturunkan dari biaya keputusan**, bukan ditebak.

---

## 5. Penelitian ini: asimetri dari biaya (bukan tebakan)

Poin kunci proposal:

> Asimetri ambang (h↑ vs h↓) **bukan parameter tebakan**, melainkan hasil turunan dari **biaya keputusan** dan **headroom kapasitas**.

Dengan kata lain: seberapa "hati-hati" kita pulih bergantung pada:
- Berapa mahal salah keputusan (evakuasi palsu vs pemulihan terlalu cepat).
- Berapa banyak kapasitas cadangan (headroom) yang tersedia.

Rincian derivasi ada di `05_ALGORITMA_DIKEMBANGKAN.md` (langkah 3).

---

## 6. Bukti empiris awal

Data studi pendahuluan (rekaman 10 jam) menunjukkan bahwa **asimetri bekerja**:
- Aturan k-sampel-berturut: 60 kali ganti status per periode.
- CUSUM simetris: 26 kali.
- **CUSUM asimetris: hanya 4 kali.**

Jadi asimetri jelas mengurangi flapping. Tapi — dan ini penting — **besarnya tidak boleh ditebak**; ia harus diturunkan dari biaya dan headroom. Ini celah yang diisi penelitian.

---

## Cek pemahaman

1. Jelaskan histeresis dengan contoh termostat.
2. Apa fungsi zona penyangga?
3. Mengapa pemulihan dibuat lebih hati-hati daripada evakuasi?
4. Apa perbedaan "asimetri informasi" dan "asimetri biaya"?
5. Mengapa besarnya asimetri tidak boleh hanya ditebak?
