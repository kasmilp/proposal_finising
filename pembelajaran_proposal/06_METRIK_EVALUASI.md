# 06. Metrik Evaluasi: E, U, F, dan QoS

> **Subbab sumber di proposal:** 1.5 (tujuan), 2.5.2 (basis data metrik), 2.7.1 (analisis deskriptif / kurva E–U).
> **Diagram pendukung:** `diagram/frontier_eu.svg`.

File ini menjelaskan **bagaimana membuktikan** bahwa usulan lebih baik. Ada tiga metrik utama (E, U, F) plus QoS sisi klien.

---

## 1. Mengapa perlu metrik?

Untuk menguji hipotesis, kita perlu **angka yang bisa diukur dan dibandingkan**. Empat metrik di bawah menjadi "bahasa umum" untuk membandingkan kebijakan.

---

## 2. E — Paparan (Exposure)

**Definisi:** porsi koneksi **baru** yang ditempatkan pada jalur berstatus terdegradasi, diukur pada jendela waktu yang sama dengan status jalur.

- Artinya: dari semua koneksi baru, berapa persen yang "terjebak" masuk ke jalur yang sedang buruk.
- **Makin kecil E, semakin baik** — artinya sistem berhasil menghindari mengirim trafik ke jalur buruk.

**Contoh dari studi pendahuluan:**
- PCC statis 1:1:1 → E = 6,52%
- k-sampel-berturut → E = 5,94%
- CUSUM dua arah simetris → E = 2,39%
- CUSUM dengan ambang pemulihan 4× evakuasi → E = 0,26%

---

## 3. U — Kapasitas Tertahan (Unused capacity)

**Definisi:** kapasitas jalur **sehat** yang tidak terpakai karena rasio terlalu konservatif.

- Artinya: ada jalur bagus tapi tidak dipakai penuh karena kita terlalu "takut" memakai jalur yang sedang mencurigakan.
- **Makin kecil U, semakin baik** — artinya kapasitas sehat tidak terbuang.

**Peringatan:** ada **pertukaran (tradeoff) antara E dan U**. Jika kita sangat agresif menurunkan E (menghindari jalur buruk), kita bisa membuang banyak kapasitas sehat (U naik). Sebaliknya, jika kita pengecut memakai semua kapasitas, E bisa naik. Inilah mengapa kita membandingkan **E pada U yang setara** — bukan sekadar E terkecil.

**Contoh:** menaikkan rasio dari 1 ke 4 menurunkan E dari 2,39% → 0,26%, tapi menaikkan U dari 1,2% → 4,6%. Di atas rasio tertentu, E hampir tidak membaik tapi U melonjak (misal 17,8%) — inilah "daerah lutut" kurva E–U.

---

## 4. F — Frekuensi Rekonfigurasi

**Definisi:** jumlah perubahan status/pemetaan per jam (jumlah remap bucket per jam).

- Artinya: seberapa sering sistem mengubah keputusan.
- **Makin kecil F, semakin baik** — sistem tidak "flapping" (bolak-balik ganti status).

**Contoh (per periode):**
- k-sampel-berturut: 60 kali ganti status
- CUSUM simetris: 26 kali
- CUSUM asimetris: hanya 4 kali

F penting karena setiap perubahan pemetaan berpotensi memengaruhi koneksi baru dan menambah beban kontroler.

---

## 5. Hubungan E–U–F

| Metrik | Arah yang baik | Makna |
|---|---|---|
| E | ↓ lebih baik | Sedikit koneksi ke jalur buruk |
| U | ↓ lebih baik | Sedikit kapasitas sehat terbuang |
| F | ↓ lebih baik | Jarang ganti keputusan |

**Tantangan:** ketiganya saling terkait. Menurunkan E sering menaikkan U; menurunkan F bisa menaikkan E (jika terlalu malas bereaksi). Karena itu penelitian memakai **kurva E–U** (frontier) dan membandingkan kebijakan pada U yang setara.

---

## 6. Metrik tambahan

| Metrik | Arti |
|---|---|
| Tunda evakuasi | Waktu dari degradasi nyata hingga status DIEVAKUASI |
| Tunda pemulihan | Waktu dari pemulihan nyata hingga status SEHAT |
| Alarm palsu | Status berubah padahal tidak ada perubahan nyata |
| QoS sisi klien | delay, jitter, packet loss, throughput (ping, iperf3, speedtest) |

---

## 7. Bagaimana mengukur E, U, F di sistem nyata

- **E**: dari tabel koneksi, hitung proporsi koneksi baru yang jatuh pada jalur yang sedang berstatus DIEVAKUASI.
- **U**: dari kapasitas kontrak vs utilisasi aktual jalur sehat.
- **F**: dari log perubahan pemetaan (riwayat bucket_map) — hitung jumlah perubahan per jam.
- **QoS**: aktifkan pengukuran di klien uji pada waktu yang sama untuk semua kebijakan.

---

## 8. Kurva E–U (frontier)

Daripada hanya membandingkan satu titik, penelitian membuat **kurva E–U**: dengan beberapa nilai ambang, plot E vs U. Kebijakan yang lebih baik berada **lebih kiri-bawah** (E dan U sama-sama kecil). Ini lebih jujur daripada mengklaim "U setara" pada satu konfigurasi.

---

## Cek pemahaman

1. Apa arti E, U, dan F? Ke arah mana masing-masing "lebih baik"?
2. Mengapa tidak cukup hanya meminimalkan E?
3. Terangkan pertukaran antara E dan U.
4. Mengapa F penting?
5. Apa gunanya kurva E–U?
6. Sebutkan alat yang dipakai untuk mengukur QoS sisi klien.
