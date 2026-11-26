# 05. Algoritma yang Dikembangkan: Histeresis Asimetris Sekuensial Sadar Biaya Keputusan

> **Subbab sumber di proposal:** 2.5.3–2.5.6 (model observasi, ambang asimetris, peta aksi, diagram alur).
> **Diagram pendukung:** `diagram/alur_algoritma.svg`.

> Ini **file inti** folder pembelajaran. Setelah memahami konsep dasar (`02`), deteksi (`03`), dan histeresis (`04`), di sini Anda memahami bagaimana semuanya menyatu menjadi algoritma usulan.

---

## Gambaran besar (ringkasan 6 langkah)

Sistem berjalan sebagai **loop** per siklus probe. Setiap siklus, sistem melakukan:

```
1. Probe aktif ke M target per jalur  → menghasilkan pola pengamatan
2. Ubah pola menjadi LLR
3. Akumulasi CUSUM dua arah (S↓/S↑)
4. Bandingkan dgn ambang (h↓ / h↑) → jika transisi status, lanjut
5. Hitung bobot target via peta aksi (SRLG-aware)
6. Kuantisasi bobot ke N kelompok hash dgn perubahan minimal → tulis ke aktuator (PCC)
```

Selain loop cepat ini, ada **loop lambat** (hitungan menit) yang memperbarui parameter biaya dan ambang berdasarkan kondisi terkini.

---

## Langkah 1 — Probe aktif dan pola pengamatan

Untuk tiap jalur, kita mengirim **probe** ke **M target** (misal 2 target). Dari tiap target kita dapat `RTT` dan status `loss`.

Dari M target, kita bangun **pola pengamatan** (misal untuk M=2):
- `00` — kedua target normal
- `10` — target 1 buruk, target 2 normal
- `01` — target 1 normal, target 2 buruk
- `11` — kedua target buruk

**Model observasi** ini penting karena dua terminal Starlink **berbagi risiko** (SRLG): jika satu buruk, yang lain cenderung ikut buruk. Model memakai probabilitas pola untuk menghitung LLR.

---

## Langkah 2 — Hitung LLR

Setiap pola dipetakan ke nilai LLR. Dalam model yang disederhanakan, hanya ada **dua nilai**:

| Pola | LLR | Makna |
|---|---|---|
| `11` (kedua target buruk) | `ℓ(11)` positif besar | Bukti kuat degradasi |
| `00`, `10`, `01` | `ℓ(lainnya)` negatif | Bukti normal |

Contoh nilai dari proposal (dalam nat per siklus):
| Jalur | ℓ(11) | ℓ(lainnya) |
|---|---|---|
| LEO (Starlink) | 4,40 | −0,288 |
| FO | 5,34 | −0,288 |

Perhatikan: `ℓ(11)` jauh lebih besar dari `ℓ(lainnya)` secara mutlak → **satu sampel buruk memberi bukti jauh lebih kuat daripada satu sampel baik**. Inilah asimetri informasi.

---

## Langkah 3 — Akumulasi CUSUM dua arah

Dua statistik per jalur:

```
S↓(baru) = max(0, S↓(lama) + LLR)   // degradasi, dipakai saat SEHAT
S↑(baru) = max(0, S↑(lama) + LLR)   // pemulihan, dipakai saat DIEVAKUASI
```

Keduanya dibatasi di bawah oleh nol. Ketika statistik melampaui ambangnya, terjadi **transisi status**.

---

## Langkah 4 — Ambang asimetris sadar biaya keputusan

Ini **novelty utama**. Ambang bukan ditebak, melainkan diturunkan dari **biaya keputusan**.

**Konsep biaya keputusan:**

| Jenis kesalahan | Akibat | Biaya |
|---|---|---|
| Evakuasi palsu (jalur sehat dianggap buruk) | Kapasitas jalur sehat menganggur sementara | Besar saat headroom kecil |
| Keterlambatan evakuasi | Koneksi baru tetap dikirim ke jalur buruk | λ·w·Δt koneksi per siklus |
| Pemulihan terlalu cepat | Koneksi baru tertambat di jalur yang belum pulih | ~ umur koneksi L & sisa degradasi G |
| Pemulihan terlambat | Kapasitas jalur sehat tertahan | sebanding kapasitas tertahan |

**Ide derivasi:** pilih ambang tiap arah untuk **meminimalkan biaya harapan per siklus**:

```
Biaya harapan = (biaya keputusan salah × laju alarm palsu) + (biaya penundaan × tunda deteksi)
```

Dengan pendekatan orde-pertama, ambang optimum berbentuk fungsi dari:
- laju kejadian perubahan nyata `ν`,
- biaya satu keputusan salah `C_salah`,
- biaya tiap siklus penundaan `C_tunda`.

Karena struktur biaya evakuasi dan pemulihan **berlawanan**, hasilnya dua ambang berbeda:
- `h↓` (evakuasi) — ditentukan oleh biaya menahan kapasitas sehat vs biaya mengirim ke jalur buruk.
- `h↑` (pemulihan) — ditentukan oleh biaya menambatkan koneksi di jalur yang belum pulih vs biaya menahan kapasitas.

**Peran headroom (H):** ambang diperbarui pada loop lambat sesuai H terukur:
- Saat kapasitas **melimpah** → pemulihan dibuat jauh lebih hati-hati daripada evakuasi (asimetri besar).
- Saat kapasitas **langka** → bobot kapasitas tertahan `β(H)` membesar → **asimetri mengecil otomatis**.

> Inilah "sadar biaya keputusan": besarnya asimetri menyesuaikan diri dengan biaya aktual dan ketersediaan kapasitas.

---

## Langkah 5 — Peta aksi (SRLG-aware)

Ketika terjadi transisi status, kita menghitung **bobot target** untuk tiap jalur dari bobot nominal (misal sebanding kapasitas kontrak). Aturan peta aksi:

1. **Porsi jalur Starlink yang dievakuasi → dialihkan ke FO** (bukan ke Starlink lain yang berbagi risiko).
2. **Porsi FO yang dievakuasi → dibagi ke Starlink yang sehat** secara proporsional.
3. Jika **semua jalur dievakuasi** → pertahankan bobot nominal (tidak ada alternatif lebih baik).

Aturan #1 mencerminkan **SRLG**: karena dua Starlink berbagi risiko, memindahkan beban dari satu Starlink ke Starlink lain tidak memberi keamanan, maka tujuan evakuasi adalah FO.

---

## Langkah 6 — Kuantisasi bobot ke kelompok hash (minimal-remap)

Bobot target bersifat kontinu, tetapi PCC hanya bisa merealisasikan rasio dalam kelipatan `1/N` (N = jumlah kelompok hash). Maka:

1. Ubah bobot target menjadi jumlah kelompok (bucket) bulat.
2. Pilih pemetaan yang **paling sedikit mengubah kelompok** dari pemetaan sebelumnya (meminimalkan remap).
3. Tulis pemetaan baru ke aktuator (PCC RouterOS via API, atau nftables).

Alasan meminimalkan remap: perubahan pemetaan memengaruhi koneksi baru yang jatuh pada kelompok yang dipindahkan. Semakin sedikit kelompok yang dipindah → semakin rendah **frekuensi rekonfigurasi (F)**.

---

## Dua skala waktu (loop cepat & lambat)

| Loop | Skala waktu | Isi |
|---|---|---|
| **Cepat** | Detik (per siklus probe) | Probe, LLR, CUSUM, perbandingan ambang, transisi status |
| **Lambat** | Menit | Estimasi biaya (λ, L, G, H), perbarui ambang, kalibrasi |

Pemisahan ini disengaja: loop cepat hanya melakukan penjumlahan/perbandingan (ringan), sedangkan estimasi biaya yang lebih mahal berjalan jarang.

---

## Alur keputusan lengkap (narasi)

1. Setiap siklus, probe mengamati kondisi tiap jalur.
2. Pola pengamatan → LLR.
3. CUSUM mengakumulasi bukti.
4. Jika bukti melampaui ambang evakuasi `h↓` (saat sehat) → status menjadi DIEVAKUASI. Jika melampaui ambang pemulihan `h↑` (saat dievakuasi) → status kembali SEHAT.
5. Jika ada transisi status → hitung bobot target via peta aksi.
6. Kuantisasi bobot ke kelompok hash dengan perubahan minimal.
7. Tulis ke aktuator PCC → koneksi baru mulai mengikuti rasio baru.

---

## Ringkasan kontribusi (mengapa ini "baru")

| Komponen | Sudah ada di literatur | Yang ditambahkan |
|---|---|---|
| CUSUM | Ya, dan terbukti optimal | Dipakai untuk **pembagian beban multi-WAN per-koneksi** |
| Histeresis asimetris | Ya (handover) | Asimetri **diturunkan dari biaya**, bukan parameter tebakan |
| Model biaya | Ada di quality control/SD-WAN | Memuat **komitmen per-koneksi** (λ, w, L, G) |
| SRLG | Ada (routing backbone) | Diterapkan pada **peta aksi bobot hash** |
| Kuantisasi hash | Ada (consistent hashing) | Digabung dengan **status jalur & perubahan minimal** |

---

## Cek pemahaman

1. Sebutkan 6 langkah algoritma secara berurutan.
2. Mengapa LLR hanya punya dua nilai dalam model ini?
3. Apa beda h↓ dan h↑, dan mengapa keduanya berbeda?
4. Bagaimana headroom memengaruhi besarnya asimetri?
5. Mengapa porsi Starlink yang dievakuasi dialihkan ke FO, bukan ke Starlink lain?
6. Mengapa kita meminimalkan remap saat kuantisasi?
7. Apa beda loop cepat dan loop lambat?
