# Ringkasan Review Literatur

**Tanggal review:** 25 November 2026  
**Cakupan:** 50 paper, 2023-2026, terbagi dalam 10 subbab proposal.

## 1. Tujuh temuan utama

1. **PCC praktis masih statis.** Implementasi MikroTik yang ada menetapkan rasio dan failover di awal; belum ada mekanisme yang mengubah rasio berdasarkan biaya keputusan (P12, P11).
2. **SD-WAN sudah adaptif, tetapi granularitasnya berbeda.** Solusi SD-WAN/DRL memilih overlay atau situs, bukan rasio hash per-koneksi (P18, P19, P20).
3. **QCD sudah optimal secara statistik, tetapi tidak sadar biaya.** Ambang CUSUM diturunkan dari batasan ARL, bukan dari biaya evakuasi versus pemulihan (P23, P24, P26).
4. **Asumsi i.i.d. adalah titik lemah.** Data jaringan berkorelasi; sudah ada QCD untuk model AR/Markov dan CUSUM dengan estimasi pasca-perubahan (P23, P24, P28, P29).
5. **Histeresis terbukti mengurangi handover, tetapi marginnya heuristik.** Belum ada margin asimetris yang merupakan fungsi biaya dan headroom (P32, P33, P34).
6. **Kuantisasi hash sudah matang, tetapi belum sadar SRLG.** Consistent hashing/quantized hashing sudah menjaga stabilitas, tetapi belum menerima status jalur (P13, P14, P16).
7. **SRLG dan TE LEO sudah maju secara terpisah.** Belum ada peta aksi SRLG-aware yang diterjemahkan menjadi bobot hash per-koneksi (P21, P45, P46, P48, P49).

## 2. Peta celah → kontribusi → paper kunci

| Celah | Kontribusi yang menjawab | Paper kunci |
|---|---|---|
| Rasio statis, tidak responsif terhadap degradasi parsial | K1: model keputusan per-koneksi; K2: ambang adaptif | P12, P18, P19, P20 |
| Ambang QCD dari ARL, bukan biaya | K2: derivasi ambang asimetris dari biaya | P23, P24, P38, P40 |
| Histeresis simetris/heuristik | K2: asimetri sebagai fungsi headroom | P32, P33, P34 |
| Kuantisasi hash belum sadar status jalur | K3: kuantisasi minimal-remap + SRLG | P13, P14, P16 |
| SRLG hanya untuk jalur primer/backup | K3: peta aksi SRLG-aware ke bobot hash | P21, P48, P49 |
| TE LEO di dalam konstelasi, bukan multi-WAN klien | K1/K4: model netral-vendor + validasi FO+LEO | P45, P46, P47 |
| Validasi FO+LEO terbatas | K4: validasi bertahap replay → testbed → shadow → produksi | P05, P06, P08, P12 |

## 3. Paper yang paling dekat dengan novelty (dan mengapa belum sama)

| Paper | Kedekatan | Beda kunci |
|---|---|---|
| P04 Pieskä et al. (2024) | Cost-aware multipath scheduling | Per-paket, bukan komitmen per-koneksi; tanpa hash/SRLG |
| P13 Levi & Keslassy (2023) | Quantized heterogeneous consistent hashing | Heterogenitas server, bukan status jalur |
| P19 Botta et al. (2024) | SD-WAN adaptif dengan batasan biaya | Keputusan overlay/site, bukan rasio hash |
| P21 Botta et al. (2026) | Deteksi bottleneck bersama via korelasi | Memilih overlay disjoint, bukan mengkuantisasi rasio |
| P23 Sun & Zou (2024) | QCD pada model AR | Tanpa biaya asimetris dan aksi hash |
| P24 Xie et al. (2023) | CUSUM dengan parameter pasca-perubahan tidak diketahui | Tanpa biaya dan komitmen koneksi |
| P32 Eydian et al. (2025) | Hysteresis margin di LEO | Margin tetap, bukan fungsi biaya/headroom |
| P38 Amend & Rakocevic (2024) | Cost-aware multipath untuk VoD | Scheduling aliran, bukan hash per-koneksi |
| P40 Shojaee et al. (2024) | Desain ekonomi-statistik chart | Quality control, bukan jaringan |
| P45 Ju et al. (2025) | Load balancing LEO | Routing di konstelasi, bukan multi-WAN klien |
| P46 Kim et al. (2026) | Multipath splitting berbasis utilisasi | Simulasi jaringan, bukan hash per-koneksi |
| P48/P49 SRLG | Jalur disjoint / primer-backup | Tidak ada kuantisasi rasio |

## 4. Tiga kalimat kontribusi yang bisa langsung dipakai

1. “Literatur PCC/SD-WAN telah menunjukkan manfaat pembagian beban adaptif, tetapi keputusannya belum diturunkan dari biaya komitmen per-koneksi dan belum diterjemahkan menjadi rasio hash yang stabil.”
2. “Literatur QCD telah memberikan optimalitas deteksi, tetapi ambangnya diturunkan dari batasan alarm palsu, bukan dari biaya evakuasi versus pemulihan.”
3. “Literatur SRLG telah memberikan jalur disjoint, tetapi belum menghubungkannya dengan kuantisasi bobot hash per-koneksi.”

## 5. Catatan tentang klaim “novel”

Klaim yang paling defensible bukan “PCC dinamis” atau “CUSUM” atau “histeresis”, melainkan:

> **Ambang asimetris yang diturunkan dari biaya komitmen per-koneksi dan headroom, lalu diterjemahkan menjadi rasio hash yang sadar SRLG dan meminimalkan perubahan pemetaan, serta divalidasi bertahap pada jaringan FO+LEO nyata.**

Lihat `catatan/03_REVISI_YANG_DISARANKAN.md` untuk cara menulis klaim ini tanpa overclaim.
