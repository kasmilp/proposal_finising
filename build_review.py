# -*- coding: utf-8 -*-
"""Build a structured literature review folder for the thesis proposal.

Metadata source: DOI content negotiation (CSL JSON) and OpenAlex, retrieved
2026-11-25. The notes are written for the proposal's literature-review
subsections (1.2.1-1.2.10).
"""
import csv
import html
import json
import os
import re
import unicodedata

BASE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(BASE, "review_jurnal_2023_2026")
os.makedirs(OUT, exist_ok=True)
os.makedirs(os.path.join(OUT, "per_pembahasan"), exist_ok=True)
os.makedirs(os.path.join(OUT, "catatan"), exist_ok=True)
os.makedirs(os.path.join(OUT, "data_mentah"), exist_ok=True)

with open(os.path.join(OUT, "data_mentah", "_selected_raw.json"), encoding="utf-8") as f:
    OA = json.load(f)
with open(os.path.join(OUT, "data_mentah", "_csl.json"), encoding="utf-8") as f:
    CSL = json.load(f)

# ---------------------------------------------------------------------------
# Section metadata
# ---------------------------------------------------------------------------
SECTIONS = {
    "1.2.1": {
        "title": "QoS dan QoE",
        "file": "1.2.1_QoS_dan_QoE.md",
        "function": "Menetapkan definisi QoS/QoE dan metrik evaluasi (delay, jitter, packet loss, throughput, QoE) yang dipakai untuk menguji H2.",
        "message": "QoS jaringan saja tidak cukup; QoE dan biaya tunda perlu masuk ke kerangka evaluasi, tetapi literatur yang ada belum menyatukannya dengan keputusan per-koneksi.",
        "gap": "Belum ada kerangka yang menyatukan QoS/QoE sisi klien dengan biaya keputusan per-koneksi dan aktuator hash.",
        "sentence": "Evaluasi kebijakan pembagian beban perlu melampaui QoS agregat dan memasukkan QoE serta biaya tunda, karena alokasi yang tampak baik pada throughput dapat merugikan pengalaman pengguna dan memboroskan kapasitas jalur mahal (Sultan & El-Sayed, 2023; Su et al., 2026; Pieskä et al., 2024).",
    },
    "1.2.2": {
        "title": "FO dan LEO Starlink",
        "file": "1.2.2_FO_dan_LEO_Starlink.md",
        "function": "Menjelaskan sifat dinamis jalur FO dan LEO Starlink serta skala waktu degradasi yang menjadi dasar pemilihan interval probe dan waktu reaksi histeresis.",
        "message": "LEO Starlink sangat dinamis pada skala detik sampai menit; outage, obstruksi, dan rekonfigurasi periodik harus tercermin dalam desain sampling dan ambang.",
        "gap": "Belum ada model yang menghubungkan pola degradasi LEO yang terukur dengan ambang keputusan pembagian beban secara eksplisit.",
        "sentence": "Pengukuran Starlink menunjukkan variasi throughput dan latensi yang jauh lebih besar daripada jaringan terestrial, termasuk outage dan lonjakan packet loss akibat obstruksi serta rekonfigurasi periodik (Ma et al., 2023; Laniewski et al., 2025; Mohan et al., 2024).",
    },
    "1.2.3": {
        "title": "MikroTik dan PCC dalam praktik",
        "file": "1.2.3_MikroTik_dan_PCC_praktik.md",
        "function": "Menunjukkan praktik PCC/MikroTik yang ada: rasio statis, failover, dan perbandingan ECMP, sebagai baseline implementasi.",
        "message": "Praktik PCC di MikroTik masih bertumpu pada rasio statis dan failover; belum ada ambang sadar biaya yang mengubah rasio secara terkendali.",
        "gap": "Belum ada implementasi PCC yang rasio-nya diturunkan dari biaya keputusan dan headroom kapasitas, serta diuji secara kuantitatif pada FO+LEO.",
        "sentence": "Implementasi PCC pada MikroTik umumnya menetapkan rasio dan aturan failover secara statis, sehingga kualitas pembagian beban bergantung pada konfigurasi awal dan tidak merespons degradasi parsial secara adaptif (Amalia et al., 2023; Putra et al., 2026).",
        "note": "Subbab ini sengaja hanya memuat dua paper yang lolos kriteria indeks. Dua paper praktik PCC Indonesia yang sangat relevan (Nugroho et al., 2026; Ahmadi et al., 2025) tidak dimasukkan karena status Scopus-nya belum terverifikasi; keduanya dapat dipakai sebagai “praktik lokal” dengan label jurnal nasional.",
    },
    "1.2.4": {
        "title": "PCC dan hash per-koneksi",
        "file": "1.2.4_PCC_dan_hash_per_koneksi.md",
        "function": "Landasan aktuator hash per-koneksi, kuantisasi rasio, dan stabilitas pemetaan saat bobot berubah.",
        "message": "Hash quantization sudah terbukti menjaga stabilitas dan meminimalkan remap, tetapi belum dipakai untuk menerjemahkan status jalur yang sadar SRLG menjadi rasio.",
        "gap": "Belum ada algoritma kuantisasi hash yang meminimalkan perubahan pemetaan sambil memperhitungkan risiko degradasi bersama antarjalur.",
        "sentence": "Kuantisasi hash dan consistent hashing telah terbukti menjaga stabilitas pemetaan serta meminimalkan migrasi saat kapasitas berubah (Levi & Keslassy, 2023; Dong et al., 2024), tetapi belum digunakan untuk menerjemahkan status degradasi jalur multi-WAN menjadi bobot yang sadar risiko bersama.",
    },
    "1.2.5": {
        "title": "Load balancing dan SD-WAN",
        "file": "1.2.5_Load_balancing_dan_SD-WAN.md",
        "function": "Membandingkan PCC/ECMP/NTH dengan SD-WAN dan metode adaptif, serta menunjukkan celah granularitas keputusan dan evaluasi.",
        "message": "SD-WAN adaptif sudah maju, tetapi keputusannya biasanya di tingkat overlay/site dan tidak menjelaskan bagaimana rasio hash per-koneksi diturunkan dari biaya.",
        "gap": "Belum ada perbandingan adil antara PCC statis, histeresis k-sampel, dan CUSUM asimetris pada metrik E/U/F yang sama.",
        "sentence": "SD-WAN adaptif dan pembelajaran penguatan telah menunjukkan perbaikan kinerja, tetapi keputusan umumnya berada pada tingkat overlay atau situs dan belum memberikan mekanisme ambang yang dapat dijelaskan untuk rasio hash per-koneksi (Troia et al., 2026; Botta et al., 2024; Cruvellier et al., 2025).",
    },
    "1.2.6": {
        "title": "Quickest change detection",
        "file": "1.2.6_Quickest_change_detection.md",
        "function": "Landasan teori deteksi perubahan sekuensial, CUSUM, ARL, dan asumsi yang perlu dilonggarkan untuk data jaringan.",
        "message": "QCD memberikan optimalitas statistik, tetapi ambangnya diturunkan dari batasan alarm palsu, bukan dari biaya keputusan asimetris dan komitmen koneksi.",
        "gap": "Asumsi i.i.d. dan ambang berbasis ARL belum tentu cocok untuk data jaringan yang berkorelasi dan mengalami degradasi bertahap.",
        "sentence": "CUSUM klasik optimal di bawah kriteria Lorden, tetapi jaminan tersebut bertumpu pada asumsi distribusi dan ambang alarm palsu, bukan pada biaya evakuasi versus pemulihan yang berbeda (Xie et al., 2023; Sun & Zou, 2024).",
    },
    "1.2.7": {
        "title": "CUSUM dua arah dan aplikasinya",
        "file": "1.2.7_CUSUM_dua_arah.md",
        "function": "Varian CUSUM dua arah, estimasi distribusi pasca-perubahan, dan bukti aplikasi pada monitoring jaringan.",
        "message": "CUSUM dua arah dapat mendeteksi naik/turun kualitas, tetapi perlu model pasca-perubahan yang tidak diketahui dan penanganan korelasi.",
        "gap": "Belum ada CUSUM dua arah yang ambang naik/turunnya diturunkan dari biaya asimetris dan diterjemahkan ke aksi hash.",
        "sentence": "Varian CUSUM dengan estimasi distribusi pasca-perubahan menunjukkan bahwa deteksi tetap dapat dilakukan ketika bentuk degradasi tidak diketahui sebelumnya (Liang & Veeravalli, 2024), dan CUSUM multivariat telah dipakai untuk monitoring jaringan kabel optik (Xu et al., 2025).",
    },
    "1.2.8": {
        "title": "Histeresis dan handover",
        "file": "1.2.8_Histeresis_dan_handover.md",
        "function": "Landasan histeresis, margin, time-to-trigger, dan biaya handover pada LEO/seluler.",
        "message": "Histeresis terbukti mengurangi handover yang tidak perlu, tetapi margin dan waktu tahan biasanya tetap atau dituning heuristik, bukan diturunkan dari biaya.",
        "gap": "Belum ada histeresis asimetris yang ambang evakuasi/pemulihannya merupakan fungsi biaya dan headroom pada multi-WAN.",
        "sentence": "Histeresis margin dan time-to-trigger efektif menekan handover yang tidak perlu (Eydian et al., 2025; Mbulwa et al., 2024), tetapi nilai margin umumnya ditetapkan tetap atau dioptimalkan secara heuristik, bukan diturunkan dari biaya keputusan dan headroom kapasitas.",
    },
    "1.2.9": {
        "title": "Komitmen koneksi dan biaya keputusan",
        "file": "1.2.9_Komitmen_koneksi_dan_biaya.md",
        "function": "Memodelkan komitmen per-koneksi, biaya keputusan salah, dan preseden desain ekonomi chart.",
        "message": "Desain ekonomi chart membuktikan parameter deteksi dapat dioptimalkan dari biaya; tetapi model yang ada belum memuat umur koneksi, porsi beban, dan headroom multi-WAN.",
        "gap": "Belum ada model biaya yang memuat komitmen per-koneksi (λ, w, L, G) dan menerjemahkannya menjadi ambang asimetris.",
        "sentence": "Desain ekonomi chart menunjukkan bahwa parameter deteksi dapat dipilih dengan meminimalkan biaya total, bukan hanya ARL (Shojaee et al., 2024; García-Bustos & Ramírez-Figueroa, 2023), tetapi model tersebut belum memuat komitmen umur koneksi dan porsi beban pada jaringan multi-WAN.",
    },
    "1.2.10": {
        "title": "Integrasi, SRLG, dan traffic engineering",
        "file": "1.2.10_Integrasi_SRLG_dan_TE.md",
        "function": "Menempatkan usulan pada literatur SRLG, routing satelit-terestrial, dan traffic engineering LEO, serta menunjukkan celah kuantisasi rasio.",
        "message": "SRLG dan TE LEO sudah maju, tetapi keduanya belum menyentuh keputusan rasio hash per-koneksi di sisi klien.",
        "gap": "Belum ada peta aksi SRLG-aware yang diterjemahkan menjadi bobot hash terkuantisasi dengan perubahan pemetaan minimal.",
        "sentence": "Literatur SRLG menyediakan jalur primer/backup yang disjoint dan literatur LEO menyediakan traffic engineering berbasis prediksi (Bérczi-Kovács et al., 2024; Matsuura et al., 2024; Kim et al., 2026), tetapi belum ada yang menerjemahkan risiko bersama tersebut menjadi rasio hash per-koneksi.",
    },
}

# ---------------------------------------------------------------------------
# Curated entries
# ---------------------------------------------------------------------------
ENTRIES = []


def E(pid, doi, section, tags, role, summary, relevance, usage, limitation,
      authors=None, title=None, venue=None, year=None, volume=None, issue=None,
      pages=None, dtype=None, publisher=None):
    ENTRIES.append({
        "id": pid, "doi": doi, "section": section, "tags": tags, "role": role,
        "summary": summary, "relevance": relevance, "usage": usage,
        "limitation": limitation, "authors": authors, "title": title,
        "venue": venue, "year": year, "volume": volume, "issue": issue,
        "pages": pages, "dtype": dtype, "publisher": publisher,
    })


# 1.2.1 QoS / QoE
E("P01", "10.1109/access.2023.3298556", "1.2.1", "1.2.1", "Pendukung",
  "Meninjau faktor QoE pada layanan multimedia di HetNet 5G (delay, jitter, throughput, konteks, dan faktor manusia) serta mengusulkan kerangka alokasi spektrum dan caching untuk layanan imersif.",
  "Menegaskan bahwa QoS jaringan saja tidak cukup dan metrik sisi pengguna perlu masuk ke evaluasi kebijakan alokasi.",
  "Dipakai di 1.2.1 untuk mendefinisikan dimensi QoS/QoE dan menjelaskan mengapa H2 memakai metrik sisi klien.",
  "Berfokus pada HetNet 5G dan layanan multimedia; tidak membahas multi-WAN, komitmen koneksi, atau ambang deteksi.",
  dtype="Artikel jurnal")

E("P02", "10.1016/j.simpat.2023.102771", "1.2.1", "1.2.1", "Pendukung",
  "Mengusulkan metode manajemen QoS pada jaringan nirkabel heterogen dengan teknologi Big Data dan aplikasi QoE mobile.",
  "Contoh pendekatan QoE-driven management yang menunjukkan kompleksitas parameter QoS di lingkungan heterogen.",
  "Dipakai di 1.2.1 sebagai pembanding pendekatan manajemen QoS; bukan acuan utama untuk model biaya.",
  "Tidak menyediakan model biaya atau ambang deteksi. Abstrak tidak tersedia dalam metadata daring; ringkasan ini perlu diverifikasi pada teks penuh.",
  dtype="Artikel jurnal")

E("P03", "10.1109/ton.2025.3638882", "1.2.1", "1.2.1", "Pendukung",
  "Mengusulkan Fabam, bidang kendali QoE-fairness lintas protokol congestion control, dengan virtual target per aliran video dan pemetaan berbasis DNN; melaporkan peningkatan QoE fairness 44,01% dan QoE efficiency 36,39%.",
  "Menunjukkan cara mengukur keadilan QoE antar-aliran dan relevansi QoE sebagai tujuan alokasi, meskipun konteksnya video streaming, bukan multi-WAN.",
  "Dipakai di 1.2.1 untuk metrik QoE fairness dan argumen bahwa alokasi bandwidth perlu mempertimbangkan hasil sisi pengguna.",
  "Tidak membahas kegagalan jalur, histeresis, atau biaya switching; mekanisme berada di lapisan transport/aplikasi.",
  dtype="Artikel jurnal", year=2026, volume="34", pages="2103-2118")

E("P04", "10.1016/j.comnet.2024.110186", "1.2.1", "1.2.1; 1.2.9", "Inti",
  "Mengembangkan packet scheduler untuk ATSSS 5G yang memanfaatkan informasi cross-layer dari congestion control untuk menghindari kongesti; emulasi menunjukkan penurunan excess delay hingga 34% dan perbaikan WebRTC/YouTube dibanding state of the art.",
  "Sangat dekat dengan gagasan cost-aware multipath: keputusan alokasi mempertimbangkan biaya tunda dan utilisasi jalur. Namun keputusannya per-paket, bukan komitmen per-koneksi.",
  "Dipakai di 1.2.1 dan 1.2.9 sebagai pembanding terdekat; menjadi titik pembeda untuk klaim komitmen per-koneksi dan kuantisasi hash.",
  "Tidak memodelkan umur koneksi, hash quantization, atau SRLG; fokus pada scheduling paket ATSSS.",
  authors=[("Pieskä", "Marcus"), ("Rabitsch", "Alexander"), ("Brunström", "Anna"),
           ("Kassler", "Andreas"), ("Amend", "Markus"), ("Bogenfeld", "Eckard")],
  dtype="Artikel jurnal", volume="241", pages="110186")

# 1.2.2 FO / LEO
E("P05", "10.1109/infocom53939.2023.10228912", "1.2.2", "1.2.2", "Inti",
  "Mengukur karakteristik end-to-end Starlink dari sisi pengguna dan menemukan throughput/latensi yang jauh lebih dinamis daripada jaringan terestrial, termasuk outage dan pengaruh terrain, badai matahari, hujan, awan, serta suhu.",
  "Memberi bukti empiris bahwa jalur LEO mengalami degradasi pada beberapa skala waktu, sehingga probe dan ambang harus mampu menangani dinamika tersebut.",
  "Dipakai di 1.2.2 untuk memotivasi pemilihan probe aktif dan menjelaskan pola degradasi LEO.",
  "Bersifat deskriptif dan tidak menghasilkan kebijakan alokasi; lokasi/temporal coverage terbatas.",
  dtype="Prosiding", volume="", pages="1-10")

E("P06", "10.1109/ojcoms.2025.3539836", "1.2.2", "1.2.2", "Inti",
  "Mengukur Starlink mobile sepanjang 300 km di Autobahn Jerman hingga 140 km/jam dan membandingkannya dengan pengukuran stasioner; obstruksi jembatan menyebabkan burst packet loss, lonjakan RTT, dan penurunan throughput yang signifikan.",
  "Menunjukkan bahwa gangguan singkat dapat menyebabkan burst loss dan penurunan kualitas, relevan untuk desain observasi multi-target dan durasi konfirmasi.",
  "Dipakai di 1.2.2 untuk menjelaskan pola gangguan LEO dan di 2.3.3 untuk memilih interval probe.",
  "Skenario mobile; belum tentu sama dengan RT/RW Net tetap; tidak membahas pembagian beban.",
  authors=[("Laniewski", "Dominic"), ("Lanfer", "Eric"), ("Aschenbruck", "Nils")],
  dtype="Artikel jurnal", volume="6", pages="1266-1283")

E("P07", "10.1109/icc51166.2024.10622394", "1.2.2", "1.2.2", "Pendukung",
  "Menganalisis sekitar 1,7 juta pengukuran crowdsourced dari 309 pengguna di 29 negara; median goodput unduh 100-200 Mbit/s, unggah 10-20 Mbit/s, RTT 40-50 ms, dan penurunan hingga 50 Mbit/s pada jam sibuk.",
  "Memberi rentang kapasitas dan latensi yang dapat dipakai untuk menetapkan parameter headroom dan skenario beban.",
  "Dipakai di 1.2.2 sebagai baseline kapasitas Starlink dan di 2.4 untuk spesifikasi skenario.",
  "Berbasis speed test, bukan probe kontinu; tidak mengukur korelasi antar-terminal atau kegagalan jangka panjang.",
  dtype="Prosiding", pages="5596-5603")

E("P08", "10.1145/3589334.3645328", "1.2.2", "1.2.2", "Inti",
  "Menganalisis 19,2 juta uji M-Lab dari 34 negara, kinerja Zoom dan Luna cloud gaming, probe RIPE Atlas, serta eksperimen terkontrol; menemukan interval rekonfigurasi global 15 detik yang menyebabkan variasi latensi dan throughput.",
  "Penting untuk memilih skala waktu sampling dan histeresis: rekonfigurasi periodik 15 detik dapat berinteraksi dengan CUSUM dan menyebabkan alarm berulang.",
  "Dipakai di 1.2.2 dan 2.3.3 untuk menjustifikasi interval probe serta analisis autokorelasi.",
  "Bersifat pengukuran, bukan kendali; agregat global dan tidak spesifik pada satu situs.",
  dtype="Prosiding", pages="2723-2734")

E("P09", "10.1109/infocom59046.2026.11571358", "1.2.2", "1.2.2", "Pendukung",
  "Melakukan pengukuran IPv6 skala besar terhadap Starlink: sekitar 5,98 juta alamat router pengguna di 208 region/165 negara, 49 PoP dan 98 tautan backbone, serta analisis latensi dan strategi penugasan alamat.",
  "Memberi gambaran topologi dan variasi latensi di tingkat backbone/PoP yang mendukung argumen bahwa dua terminal Starlink dapat berbagi risiko.",
  "Dipakai di 1.2.2 sebagai bukti terbaru tentang struktur jaringan Starlink dan keragaman jalur.",
  "Pengukuran backbone, bukan SLA akses; tidak membahas pembagian beban klien.",
  dtype="Prosiding", pages="1-10")

E("P10", "10.1109/pimrc56721.2023.10294034", "1.2.2", "1.2.2", "Latar",
  "Menjelaskan kampanye pengukuran Starlink yang mencakup jaringan akses satelit, gateway, PoP, serta koneksi backbone dan Internet, dan mengangkat tantangan penelitian jaringan terintegrasi.",
  "Latar belakang arsitektur LEO dan tantangan pengukuran; berguna untuk memperkenalkan istilah gateway/PoP.",
  "Dipakai di 1.2.2 sebagai rujukan latar, bukan sebagai bukti kuantitatif utama.",
  "Kampanye masih berlangsung dan hasil kuantitatif terbatas.",
  dtype="Prosiding", pages="1-6")

# 1.2.3 MikroTik / PCC practice
E("P11", "10.1109/iccsc71566.2026.11650293", "1.2.3", "1.2.3; 1.2.5", "Pendukung",
  "Membandingkan ECMP pada MikroTik dengan Smart Balancing pada Ruijie Reyee menggunakan pendekatan NDLC; melaporkan Smart Balancing lebih baik dalam status active-active, kecepatan switching ISP, dan stabilitas pada bandwidth rendah.",
  "Menunjukkan bahwa vendor lain sudah menawarkan smart balancing, sehingga model netral-vendor dan ambang yang dapat dijelaskan menjadi relevan.",
  "Dipakai di 1.2.3/1.2.5 sebagai pembanding praktis dan untuk menunjukkan kompetisi fitur vendor.",
  "Berbasis vendor dan konfigurasi tertentu; tidak menggunakan PCC atau ambang sadar biaya.",
  dtype="Prosiding", pages="1-6")

E("P12", "10.1016/j.procs.2022.12.116", "1.2.3", "1.2.3; 1.2.4", "Inti",
  "Merancang jaringan dua ISP dengan load balancing PCC dan failover pada MikroTik menggunakan NDLC; evaluasi QoS THIPON memperoleh nilai 3,75 pada jam sibuk dan 4 pada jam normal, dengan kuesioner meningkat dari 0,4 ke 0,89.",
  "Merupakan contoh langsung praktik PCC statis + failover yang menjadi baseline implementasi proposal.",
  "Dipakai di 1.2.3/1.2.4 untuk mendeskripsikan cara kerja PCC di MikroTik dan baseline yang akan diperbaiki.",
  "Dua ISP, rasio statis, tanpa LEO, tanpa pengukuran E/U/F, dan tanpa analisis statistik berulang.",
  dtype="Prosiding", volume="216", pages="103-111")

# 1.2.4 PCC / hashing
E("P13", "10.1109/icnp59255.2023.10355577", "1.2.4", "1.2.4", "Inti",
  "Mengusulkan kerangka quantized heterogeneous consistent hashing dengan virtual server dan algoritma pemetaan min-max fairness M3; memberikan syarat perlu dan cukup untuk stabilitas serta menunjukkan skalabilitas dan memori yang lebih baik.",
  "Paling dekat dengan komponen kuantisasi rasio: menunjukkan bahwa bobot heterogen dapat distabilkan dan dipetakan secara terkuantisasi. Namun tujuannya adalah heterogenitas server, bukan status jalur/SRLG.",
  "Dipakai di 1.2.4 dan 2.3.2 untuk merancang algoritma kuantisasi N bucket dan menganalisis stabilitas.",
  "Tidak memodelkan degradasi jalur, biaya keputusan, atau risiko bersama.",
  dtype="Prosiding", pages="1-12")

E("P14", "10.1145/3631708", "1.2.4", "1.2.4", "Inti",
  "Mengusulkan DxHash berbasis repeated pseudo-random number generation untuk memori rendah, lookup cepat, dan update minimal; menyediakan varian berbobot dan melaporkan pengurangan memori hingga 98,4% dibanding AnchorHash.",
  "Menunjukkan bahwa weighted consistent hashing dapat menangani kapasitas heterogen dengan perubahan pemetaan kecil, mendukung aktuator hash pada router.",
  "Dipakai di 1.2.4 untuk memilih struktur hash dan metrik remap; di 2.3.2 untuk implementasi.",
  "Berfokus pada datacenter/IoT; tidak ada status jalur atau SRLG.",
  dtype="Artikel jurnal", volume="24", issue="1", pages="1-22")

E("P15", "10.1109/eiecs59936.2023.10435520", "1.2.4", "1.2.4", "Pendukung",
  "Mengusulkan metode consistent hashing berbobot dinamis dengan optimasi heuristik yang menyesuaikan bobot node secara real-time; melaporkan perbaikan response time dan throughput dibanding bobot statis.",
  "Mendukung gagasan bobot hash yang berubah mengikuti kondisi, tetapi bobotnya didorong oleh beban node, bukan biaya jalur.",
  "Dipakai di 1.2.4 sebagai pembanding metode pembobotan dinamis.",
  "Tidak memberikan jaminan stabilitas formal dan tidak membahas kegagalan jaringan.",
  dtype="Prosiding", pages="492-496")



E("P16", "10.1002/nem.70033", "1.2.4", "1.2.4", "Pendukung",
  "Mengusulkan CHCA (consistent hashing with congestion awareness) pada switch P4, menggabungkan consistent hashing dengan least connections dan header khusus untuk mengurangi migrasi serta hot spot.",
  "Menggabungkan hash dengan kesadaran kongesti, sangat dekat dengan ide rasio sadar kondisi, tetapi pada load balancer server.",
  "Dipakai di 1.2.4 sebagai pembanding dan untuk menunjukkan bahwa kesadaran kongesti belum masuk ke multi-WAN.",
  "Berfokus pada data center/P4; tidak ada komitmen per-koneksi WAN atau SRLG.",
  year=2026, dtype="Artikel jurnal", volume="36", issue="1", pages="e70033")

E("P17", "10.1109/ispass57527.2023.00048", "1.2.4", "1.2.4", "Latar",
  "Mensurvei dan membandingkan algoritma consistent hashing (1997-2021) secara empiris; Jump, Anchor, dan Dx unggul pada metrik yang diuji, dan beberapa algoritma yang asimtotik cepat justru lebih lambat karena akses memori.",
  "Memberi dasar pemilihan algoritma hash dan metrik evaluasi (balance, remap, memori, lookup).",
  "Dipakai di 1.2.4 sebagai latar dan justifikasi pemilihan algoritma.",
  "Tidak membahas status jalur dinamis atau kuantisasi rasio multi-WAN.",
  authors=[("Coluzzi", "Massimo"), ("Brocco", "Amos"), ("Contu", "Patrizio"),
           ("Leidi", "Tiziano")],
  dtype="Prosiding", pages="346-348")

# 1.2.5 LB / SD-WAN
E("P18", "10.1109/comst.2025.3594678", "1.2.5", "1.2.5", "Inti",
  "Mensurvei ekosistem SD-WAN: arsitektur, CPE, overlay/underlay, controller, orkestrasi, traffic engineering, monitoring, dan celah penelitian.",
  "Memposisikan proposal dalam lini SD-WAN traffic engineering dan menunjukkan bahwa mekanisme keputusan adaptif masih menjadi celah.",
  "Dipakai di 1.2.5 untuk kerangka umum SD-WAN dan pernyataan celah.",
  "Survei; tidak mengusulkan mekanisme baru atau evaluasi empiris.",
  dtype="Artikel jurnal", year=2026, volume="28", pages="2805-2845")

E("P19", "10.1016/j.comnet.2024.110310", "1.2.5", "1.2.5", "Inti",
  "Mengusulkan bidang kendali SD-WAN terdesentralisasi dan orkestrasi cooperative multi-agent reinforcement learning untuk pemilihan overlay; memenuhi kebijakan QoS dan batasan biaya pada skenario multi-site.",
  "Paling dekat dengan SD-WAN sadar biaya, tetapi keputusannya di tingkat overlay/site, bukan rasio hash per-koneksi; tidak memakai CUSUM/histeresis.",
  "Dipakai di 1.2.5 sebagai pembanding utama dan untuk membedakan granularitas keputusan.",
  "Tidak mengevaluasi FO+LEO dengan SRLG; ambang keputusan tidak diturunkan dari biaya secara eksplisit.",
  dtype="Artikel jurnal", volume="243", pages="110310")

E("P20", "10.1109/globecom59602.2025.11432107", "1.2.5", "1.2.5", "Inti",
  "Mengusulkan kerangka deep reinforcement learning untuk kebijakan load balancing adaptif di SD-WAN; melaporkan perbaikan 48,94% dibanding baseline yang hanya memakai status trafik sesaat pada lingkungan bandwidth asimetris.",
  "Menunjukkan manfaat kebijakan adaptif dibanding statis, mendukung alternatif H0, tetapi solusinya black-box dan tidak memberikan ambang yang dapat dijelaskan.",
  "Dipakai di 1.2.5 sebagai pembanding DRL dan untuk menunjukkan pentingnya status dinamis.",
  "Simulasi; tidak memodelkan komitmen per-koneksi, biaya keputusan, atau kuantisasi hash.",
  dtype="Prosiding", pages="4053-4058")

E("P21", "10.1007/s10922-026-10066-1", "1.2.5", "1.2.5; 1.2.10", "Inti",
  "Mengusulkan monitoring aktif yang mengklasifikasikan overlay sebagai joint atau disjoint berdasarkan korelasi time series latensi probe; controller kemudian memilih overlay disjoint, dan evaluasi Mininet menunjukkan perbaikan throughput serta penurunan jitter/latensi.",
  "Sangat dekat dengan peta aksi SRLG-aware:mengidentifikasi bottleneck bersama dari korelasi, bukan hanya aturan kaku. Namun masih memilih overlay, bukan mengkuantisasi rasio hash.",
  "Dipakai di 1.2.5 dan 1.2.10 untuk mendukung deteksi risiko bersama berbasis korelasi dan desain aksi SRLG.",
  "Evaluasi Mininet; belum diuji pada FO+LEO nyata dan belum memuat biaya keputusan/histeresis.",
  authors=[("Botta", "Alessio"), ("Canonico", "Roberto"), ("Navarro", "Annalisa"),
           ("Pitacoro", "Lorenzo"), ("Stanco", "Giovanni"), ("Ventre", "Giorgio"),
           ("Zinno", "Stefania")],
  dtype="Artikel jurnal", volume="34", issue="3", pages="95")

E("P22", "10.1109/6gnet58894.2023.10317704", "1.2.5", "1.2.5", "Pendukung",
  "Mengusulkan arsitektur integrasi SD-WAN dan Satellite 6G untuk meningkatkan performa dan keandalan, terutama di daerah terpencil atau lingkungan latensi tinggi.",
  "Memposisikan integrasi SD-WAN+satelit sebagai arah yang relevan, tetapi masih konseptual.",
  "Dipakai di 1.2.5 sebagai latar integrasi SD-WAN dan satelit.",
  "Makalah arsitektur/posisi; tidak ada evaluasi mekanisme pembagian beban.",
  dtype="Prosiding", pages="1-4")

# 1.2.6 QCD
E("P23", "10.1109/tit.2024.3384510", "1.2.6", "1.2.6", "Inti",
  "Meneliti QCD pada model autoregresif (AR): sebelum perubahan observasi i.i.d., setelah perubahan mengikuti HMM kontinu; mengusulkan Ergodic CuSum yang rekursif dan asimtotik optimal, serta versi data-driven dengan gradient ascent dan batas ARL.",
  "Menjawab langsung kelemahan asumsi i.i.d. pada data jaringan yang berkorelasi; memberi alternatif model dan jaminan ARL.",
  "Dipakai di 1.2.6 dan 2.3.3 untuk membahas autokorelasi serta kemungkinan pengganti CUSUM i.i.d.",
  "Model AR tidak secara langsung memuat biaya asimetris atau aksi hash; kompleksitas implementasi perlu diuji.",
  dtype="Artikel jurnal", volume="70", issue="7", pages="5248-5268")

E("P24", "10.1109/tit.2023.3274646", "1.2.6", "1.2.6", "Inti",
  "Mengusulkan Window-Limited CUSUM yang menggabungkan CUSUM dengan estimasi parameter pasca-perubahan berbasis sliding window; memilih ukuran window optimal dan menunjukkan optimalitas asimtotik orde pertama dengan update rekursif.",
  "Relevan karena distribusi degradasi LEO tidak diketahui dan berubah; pendekatan ini menjaga deteksi tetap cepat tanpa mengasumsikan parameter pasca-perubahan diketahui.",
  "Dipakai di 1.2.6/1.2.7 untuk memperkuat desain CUSUM adaptif dan memilih window.",
  "Masih berasumsi i.i.d. bersyarat dan tidak memuat biaya keputusan.",
  dtype="Artikel jurnal", volume="69", issue="9", pages="5990-6005")

E("P25", "10.1109/tit.2023.3259185", "1.2.6", "1.2.6", "Pendukung",
  "Mengusulkan Spectral-CUSUM untuk mendeteksi perubahan struktur komunitas jaringan dari observasi bising, dengan karakterisasi ARL/EDD dan optimalitas asimtotik.",
  "Menunjukkan CUSUM dapat diperluas ke perubahan tingkat jaringan, tetapi belum pada pemilihan jalur multi-WAN.",
  "Dipakai di 1.2.6 sebagai contoh perluasan CUSUM ke struktur jaringan.",
  "Fokus pada graf/struktur, bukan kualitas jalur atau keputusan alokasi.",
  dtype="Artikel jurnal", volume="69", issue="7", pages="4691-4707")

E("P26", "10.1109/jsait.2024.3362324", "1.2.6", "1.2.6", "Pendukung",
  "Meneliti QCD dengan controlled sensing dan ketidakpastian parameter pasca-perubahan; merumuskan masalah dengan kriteria Lorden dan mengusulkan Windowed Chernoff-CuSum yang memilih aksi untuk memaksimalkan KL divergence.",
  "Menghubungkan deteksi dengan pemilihan aksi secara sekuensial, relevan dengan probe/aksi adaptif, meskipun aksinya masih abstrak.",
  "Dipakai di 1.2.6 untuk kerangka teoretis deteksi-kendali.",
  "Tidak memodelkan hash, komitmen koneksi, atau biaya switching.",
  authors=[("Veeravalli", "Venugopal V."), ("Fellouris", "Georgios"),
           ("Moustakides", "George V.")],
  dtype="Artikel jurnal", volume="5", pages="1-11")

E("P27", "10.1109/tit.2025.3566677", "1.2.6", "1.2.6", "Pendukung",
  "Mengusulkan QCD berbasis score yang robust terhadap ketidakpastian pre/post-change: memilih least-favorable distributions dari dua himpunan dan menurunkan metode estimasinya.",
  "Relevan untuk model mismatch dan ketidakpastian distribusi pada data jaringan nyata.",
  "Dipakai di 1.2.6 sebagai opsi robustness terhadap ketidakpastian model.",
  "Tidak membahas biaya asimetris atau aksi hash.",
  dtype="Artikel jurnal", volume="71", issue="7", pages="5539-5555")

E("P28", "10.1109/icassp49357.2023.10096555", "1.2.6", "1.2.6", "Pendukung",
  "Meneliti QCD data-driven pada model Markov ketika kernel transisi sebelum dan sesudah perubahan tidak diketahui; mengusulkan algoritma berbasis kernel yang rekursif dan efisien, dengan batas ARL dan detection delay.",
  "Alternatif untuk observasi yang bergantung waktu (Markov), mendukung diskusi asumsi i.i.d.",
  "Dipakai di 1.2.6 sebagai pembanding model dependen.",
  "Model Markov; tidak memuat biaya keputusan atau kuantisasi.",
  authors=[("Zhang", "Qi"), ("Sun", "Zhongchang"), ("Herrera", "Luis"),
           ("Zou", "Shaofeng")],
  dtype="Prosiding", pages="1-5")

# 1.2.7 CUSUM two-way
E("P29", "10.1109/tit.2024.3418379", "1.2.7", "1.2.7", "Inti",
  "Mengembangkan uji CUSUM non-parametrik dengan estimasi densitas pasca-perubahan (NGLR dan NWLA) yang tidak memerlukan sampel latih pasca-perubahan; membuktikan optimalitas asimtotik orde pertama.",
  "Paling relevan untuk kasus degradasi LEO yang bentuk distribusinya tidak diketahui; mengurangi ketergantungan pada asumsi q1 yang kaku.",
  "Dipakai di 1.2.7 untuk memperkuat model observation dan alternatif estimasi pasca-perubahan.",
  "Masih i.i.d.; tidak memuat biaya asimetris atau aksi hash.",
  dtype="Artikel jurnal", volume="70", issue="11", pages="8072-8086")

E("P30", "10.1109/tsp.2023.3256275", "1.2.7", "1.2.7", "Pendukung",
  "Meneliti deteksi anomali cepat pada jaringan sensor dengan sampel tanpa label; mengusulkan algoritma mixture likelihood ratio/MLE dan batas bawah detection delay untuk kasus anomali statis/dinamis.",
  "Relevan secara analogis untuk observasi multi-target yang ambigu atau tidak berlabel, tetapi bukan untuk pemilihan jalur.",
  "Dipakai di 1.2.7 sebagai dukungan teori deteksi dengan observasi tidak lengkap.",
  "Tidak membahas QoS, biaya, atau aktuator hash.",
  dtype="Artikel jurnal", volume="71", pages="873-887")

E("P31", "10.1109/icocn67308.2025.11145409", "1.2.7", "1.2.7", "Pendukung",
  "Mengusulkan monitoring kabel laut real-time dengan multivariate CUSUM dan sliding window; melaporkan akurasi 99,54% untuk 8 jenis anchor smash, 100% untuk 4 jenis anchor hook, false alarm <2%, dan latensi deteksi <0,2 detik.",
  "Bukti aplikasi CUSUM pada infrastruktur optik, mendukung kelayakan implementasi di jalur FO.",
  "Dipakai di 1.2.7 sebagai contoh aplikasi CUSUM pada jaringan optik.",
  "Berfokus klasifikasi event, bukan pembagian beban; tidak memuat biaya keputusan.",
  authors=[("Xu", "Chunying"), ("Chen", "Jianrong"), ("Fang", "Jingqi"),
           ("Xiao", "Keyan"), ("Xu", "Yuhong"), ("Chen", "Jiawang"),
           ("Wei", "Chuliang")],
  dtype="Prosiding", pages="1-3")

# 1.2.8 Hysteresis / handover
E("P32", "10.1109/ojcoms.2025.3541962", "1.2.8", "1.2.8", "Inti",
  "Mengusulkan strategi handover LEO berbasis weighted bipartite graph dan algoritma Kuhn-Munkres untuk pencocokan optimal, ditambah hysteresis margin untuk mengurangi handover yang tidak perlu; melaporkan penurunan handover rate, latensi, dan biaya.",
  "Paling dekat dengan komponen histeresis: menunjukkan margin mengurangi handover dan biaya, tetapi nilainya belum diturunkan dari biaya keputusan.",
  "Dipakai di 1.2.8 sebagai pembanding utama dan titik pembeda untuk ambang asimetris sadar biaya.",
  "Handover satelit, bukan rasio hash multi-WAN; tidak ada SRLG atau komitmen koneksi.",
  dtype="Artikel jurnal", volume="6", pages="1470-1484")

E("P33", "10.1109/access.2023.3346039", "1.2.8", "1.2.8", "Inti",
  "Mengusulkan self-optimization untuk threshold, hysteresis, dan time-to-trigger dengan mempertimbangkan kondisi kanal, profil mobilitas, dan parameter sistem; bertujuan mengurangi handover, ping-pong, dan failure.",
  "Menunjukkan bahwa tiga parameter histeresis dapat dioptimalkan bersama, tetapi pendekatannya analitik/heuristik dan tidak memakai biaya keputusan.",
  "Dipakai di 1.2.8 untuk menunjukkan kompleksitas tuning dan memperkenalkan TTT.",
  "Konteks 5G seluler; tidak membahas LEO atau hash quantization.",
  dtype="Artikel jurnal", year=2024, volume="12", pages="6117-6135")

E("P34", "10.1109/access.2024.3368503", "1.2.8", "1.2.8", "Inti",
  "Membandingkan tiga strategi handover (closest satellite, max visibility, CINR-based 3 dB) pada konstelasi LEO/MEO/HEO; untuk LEO besar, CINR-based memberi tradeoff terbaik antara efisiensi spektral, delay, dan handover rate.",
  "Menunjukkan bahwa margin 3 dB adalah praktik umum, sehingga kritik terhadap margin tetap/heuristik menjadi relevan.",
  "Dipakai di 1.2.8 untuk mendeskripsikan praktik hysteresis margin dan baseline.",
  "Simulasi konstelasi; tidak membahas multi-WAN atau biaya koneksi.",
  dtype="Artikel jurnal", volume="12", pages="31523-31537")

E("P35", "10.1109/i2cacis61270.2024.10649814", "1.2.8", "1.2.8", "Pendukung",
  "Mengevaluasi skema self-optimizing hysteresis dan time-to-trigger di 5G ultra-dense network; pendekatan analitik mencapai handover success 99,84%, diikuti fuzzy 67,10% dan regression 48,58%, dengan tradeoff terhadap efisiensi spektral.",
  "Mendukung gagasan bahwa tuning histeresis memengaruhi keberhasilan dan efisiensi, analog dengan tradeoff E/U.",
  "Dipakai di 1.2.8 sebagai bukti tradeoff kinerja parameter histeresis.",
  "Konteks seluler; tidak ada model biaya atau LEO.",
  dtype="Prosiding", pages="352-357")

E("P36", "10.1016/j.adhoc.2026.104378", "1.2.8", "1.2.8", "Pendukung",
  "Mengusulkan handover beam adaptif kecepatan untuk LEO dengan strategi keputusan kolaboratif DDQN dan TOPSIS.",
  "Menunjukkan tren terbaru penggunaan pembelajaran dan multi-kriteria dalam handover LEO.",
  "Dipakai di 1.2.8 sebagai pembanding pendekatan learning-based.",
  "Abstrak tidak tersedia dalam metadata; ringkasan berdasarkan judul dan perlu diverifikasi pada teks penuh.",
  dtype="Artikel jurnal", volume="193", pages="104378")

E("P37", "10.1109/tmc.2025.3582245", "1.2.8", "1.2.8", "Pendukung",
  "Mengusulkan PHandover, handover paralel berbasis perencanaan dan prediksi kekuatan sinyal untuk jaringan satelit mobile; melaporkan penurunan latensi handover hingga 21x dibanding skema NTN standar.",
  "Menunjukkan bahwa latensi handover dapat dikurangi dengan perencanaan, tetapi tidak membahas alokasi rasio.",
  "Dipakai di 1.2.8 sebagai dukungan pentingnya perencanaan waktu handover.",
  "Fokus akses satelit; tidak ada biaya keputusan atau hash.",
  dtype="Artikel jurnal", volume="24", issue="11", pages="11541-11554")

# 1.2.9 Commitment / cost
E("P38", "10.1016/j.comnet.2024.110218", "1.2.9", "1.2.9; 1.2.1", "Inti",
  "Mengatasi optimasi biaya scheduling multipath untuk VoD pada ATSSS 5G; menunjukkan Cheapest-Path-First dapat mengonsumsi hingga 90% kapasitas jalur mahal tanpa manfaat QoE, lalu mengusulkan Cost-Optimized-Multipath (COM) yang menyeimbangkan QoE dan biaya.",
  "Paling dekat dengan intuisi biaya proposal: alokasi ke jalur mahal harus memberi manfaat QoE. Namun keputusannya pada scheduling aliran, bukan komitmen hash per-koneksi.",
  "Dipakai di 1.2.9 sebagai pembanding utama untuk biaya dan QoE; di 1.2.1 untuk metrik.",
  "Konteks VoD/MP-TCP; tidak memakai CUSUM/histeresis atau SRLG.",
  dtype="Artikel jurnal", volume="242", pages="110218")

E("P39", "10.1016/j.cie.2023.109464", "1.2.9", "1.2.9", "Pendukung",
  "Mengusulkan desain ekonomi optimal untuk control chart LCP dua dimensi pada variabel Poisson yang berkorelasi.",
  "Preseden metodologis bahwa parameter chart dapat dioptimalkan dari biaya, termasuk saat observasi berkorelasi; mendukung gagasan ambang sadar biaya.",
  "Dipakai di 1.2.9 sebagai landasan teori desain ekonomi chart.",
  "Konteks manufaktur/kualitas; bukan jaringan. Abstrak tidak tersedia dalam metadata; verifikasi teks penuh diperlukan.",
  dtype="Artikel jurnal", volume="183", pages="109464")

E("P40", "10.1016/j.cie.2024.110401", "1.2.9", "1.2.9", "Inti",
  "Mengoptimalkan desain chart SVSSI-np dengan algoritma genetika dalam model ekonomi-statistik terpadu; melaporkan pengurangan biaya >10% dan perbaikan time-to-signal/false alarm >30% pada sebagian besar eksperimen, serta menunjukkan bahwa estimasi shift yang salah dapat merusak manfaat.",
  "Membuktikan bahwa desain yang mempertimbangkan biaya dapat mengalahkan desain statistik saja, dan bahwa kesalahan estimasi parameter adalah risiko nyata—analog dengan kesalahan estimasi q1/headroom.",
  "Dipakai di 1.2.9 untuk menjustifikasi penurunan ambang dari biaya dan analisis sensitivitas.",
  "Konteks quality control; tidak memuat komitmen koneksi atau aksi hash.",
  dtype="Artikel jurnal", volume="197", pages="110401")

E("P41", "10.3837/tiis.2026.10.023", "1.2.9", "1.2.9", "Pendukung",
  "Mengusulkan HARP, strategi load balancing sadar biaya untuk control plane SDN heterogen; memodelkan relief overload sebagai recovery rencana yang layak dan mempertimbangkan balancing gain, migration overhead, capacity safety, dan stabilitas.",
  "Menunjukkan bahwa biaya migrasi/rekonfigurasi dapat dimasukkan sebagai kriteria keputusan, mendukung metrik F.",
  "Dipakai di 1.2.9 sebagai dukungan untuk biaya rekonfigurasi dan stabilitas.",
  "Beban controller, bukan jalur WAN; tidak ada hash quantization.",
  authors=[("Ruan", "Chengqi"), ("Qi", "Qinglei"), ("Wang", "Yifang"),
           ("Li", "He"), ("Zhao", "Cong"), ("Li", "Zhenshuang")],
  dtype="Artikel jurnal", volume="20", issue="10", pages="")

# 1.2.10 Integration / SRLG / TE
E("P42", "10.1109/tnet.2024.3397613", "1.2.10", "1.2.10", "Pendukung",
  "Mengusulkan Dyna-STN, mekanisme routing wide-area berbasis dynamic discrete topology untuk satellite-terrestrial integrated network; menggunakan virtual overlay dan OSPF untuk menyembunyikan dinamika topologi serta menjaga kontinuitas layanan.",
  "Menunjukkan cara menangani topologi yang berubah cepat, tetapi pada level jaringan satelit-terestrial, bukan multi-WAN klien.",
  "Dipakai di 1.2.10 sebagai latar arsitektur STIN dan kontinuitas layanan.",
  "Tidak membahas rasio hash, biaya keputusan, atau histeresis.",
  dtype="Artikel jurnal", volume="32", issue="5", pages="3840-3853")

E("P43", "10.1109/jsac.2024.3365869", "1.2.10", "1.2.10", "Pendukung",
  "Mengusulkan CMADR, routing dinamis berbasis constrained multi-agent reinforcement learning untuk integrated satellite-terrestrial network; menurunkan packet delay minimal 21% dan 15% sambil memenuhi batas energi dan packet loss.",
  "Menunjukkan optimasi multi-objectif dengan batasan QoS; relevan sebagai pembanding, tetapi bukan keputusan per-koneksi.",
  "Dipakai di 1.2.10 sebagai pembanding routing adaptif.",
  "Simulasi; tidak ada hash actuator atau SRLG pada level klien.",
  dtype="Artikel jurnal", volume="42", issue="5", pages="1204-1218")

E("P44", "10.1016/j.comnet.2023.109823", "1.2.10", "1.2.10", "Pendukung",
  "Mempelajari joint optimization routing, alokasi bandwidth, user association, channel, dan power pada STIN untuk meminimalkan konsumsi daya satelit sambil memenuhi QoS; menyelesaikan masalah MINLP secara iteratif.",
  "Menunjukkan pentingnya joint optimization dan batasan kapasitas, tetapi solusinya terpusat/offline.",
  "Dipakai di 1.2.10 untuk dukungan model optimasi dan batasan kapasitas.",
  "Tidak membahas dinamika kegagalan atau histeresis; bukan implementasi per-koneksi.",
  authors=[("Yin", "Yabo"), ("Huang", "Chuanhe"), ("Xiong", "Naixue N."),
           ("Wu", "Dong-Fang"), ("Huang", "Shidong")],
  dtype="Artikel jurnal", volume="231", pages="109823")

E("P45", "10.1109/taes.2025.3571400", "1.2.10", "1.2.10", "Inti",
  "Mengusulkan DLBR, routing load-balancing LEO berbasis multiagent dueling double DQN dan prediksi trafik GCN-LSTM-Attention; hasilnya menurunkan utilisasi bandwidth maksimum dan rata-rata jalur.",
  "State of the art load balancing LEO, tetapi keputusannya di dalam konstelasi, bukan pembagian beban klien multi-WAN.",
  "Dipakai di 1.2.10 sebagai pembanding utama untuk load balancing LEO.",
  "Tidak memuat ambang sadar biaya, komitmen koneksi, atau SRLG.",
  dtype="Artikel jurnal", volume="61", issue="5", pages="11954-11970")

E("P46", "10.1016/j.icte.2026.08.003", "1.2.10", "1.2.10", "Inti",
  "Mengusulkan multipath traffic splitting berbasis utilisasi pada jalur LEO yang delay-feasible; memakai K-shortest path dan L2 splitting yang meminimalkan jumlah kuadrat utilisasi tautan; pada topologi 72 node, delay turun dari 74,85 ms ke 62,40 ms dan delivery ratio naik dari 72,6% ke 82,8% dibanding single-path.",
  "Sangat dekat dengan komponen penyesuaian rasio: menunjukkan splitting berbasis utilisasi memberi perbaikan besar. Namun masih di level jaringan/simulasi, bukan hash per-koneksi.",
  "Dipakai di 1.2.10 sebagai pembanding utama untuk rasio/splitting dan metrik delay/delivery.",
  "Simulasi; tidak membahas biaya keputusan, histeresis, atau kuantisasi hash.",
  authors=[("Kim", "Hyejin"), ("Baek", "Hyunchul"), ("Yoon", "Seunghyun"),
           ("Lim", "Hyuk")],
  dtype="Artikel jurnal", pages="in press")

E("P47", "10.1109/icccn65249.2025.11133958", "1.2.10", "1.2.10", "Pendukung",
  "Mengusulkan desain controller SDN untuk LEO dengan three-phase traffic engineering yang memanfaatkan trajektori satelit untuk penugasan jalur proaktif; melaporkan hingga dua kali residual bandwidth dan 95% dari residual bandwidth optimal.",
  "Menunjukkan nilai prediksi/proaktif dalam TE LEO, mendukung ide look-ahead, tetapi bukan keputusan klien.",
  "Dipakai di 1.2.10 sebagai dukungan perencanaan proaktif.",
  "Simulasi; tidak ada hash atau biaya keputusan.",
  dtype="Prosiding", pages="1-6")

E("P48", "10.1109/infocom52122.2024.10621256", "1.2.10", "1.2.10", "Inti",
  "Mempelajari region-disjoint survivable routing dan regional SRLG; mengusulkan kerangka algoritmik yang efisien dan mudah diimplementasikan, dengan kompleksitas near-linear expected time dan additive approximation untuk versi NP-hard.",
  "Memformalkan SRLG regional dan jalur disjoint, mendukung peta aksi yang sadar risiko bersama.",
  "Dipakai di 1.2.10 untuk landasan SRLG dan desain aksi.",
  "Routing backbone; tidak membahas kuantisasi rasio atau komitmen koneksi.",
  dtype="Prosiding", pages="951-960")

E("P49", "10.1364/jocn.525178", "1.2.10", "1.2.10", "Inti",
  "Memperluas algoritma k-SPF untuk menemukan pasangan rute primer/backup yang SRLG-disjoint pada jaringan optik; menemukan k pasangan dengan probabilitas lebih tinggi dan waktu lebih cepat, serta biaya rute mendekati minimum.",
  "Paling langsung untuk SRLG-disjoint path, tetapi hanya pasangan primer/backup, bukan N bucket rasio.",
  "Dipakai di 1.2.10 untuk mendukung peta aksi SRLG dan pemilihan jalur cadangan.",
  "Jaringan optik; tidak ada pembagian beban per-koneksi atau biaya keputusan.",
  dtype="Artikel jurnal", volume="16", issue="9", pages="E23")

E("P50", "10.1109/jlt.2023.3239743", "1.2.10", "1.2.10", "Pendukung",
  "Merancang shared backup path protection (SBPP) yang robust terhadap kegagalan SRLG pada SDM-EON; memformulasikan MILP dan heuristik, serta memakai Γ-robust optimization untuk ketidakpastian trafik.",
  "Menunjukkan pemodelan kegagalan SRLG dan robustness terhadap ketidakpastian, mendukung desain sadar risiko.",
  "Dipakai di 1.2.10 sebagai dukungan model SRLG dan robustness.",
  "Desain jaringan optik; tidak membahas hash atau keputusan klien.",
  dtype="Artikel jurnal", volume="41", issue="10", pages="2923-2939")

# ---------------------------------------------------------------------------
# Metadata helpers
# ---------------------------------------------------------------------------

def clean(s):
    if s is None:
        return ""
    s = html.unescape(str(s)).replace("\u2013", "-").replace("\u2014", "-")
    s = s.replace("\u2010", "-").replace("\u2011", "-").replace("\u00a0", " ")
    # Normalise Cyrillic look-alikes that occasionally appear in Crossref titles.
    s = s.translate(str.maketrans({"а": "a", "е": "e", "о": "o", "р": "p",
                                   "с": "c", "х": "x", "у": "y", "і": "i"}))
    return s


def initials(given):
    given = clean(given)
    parts = re.split(r"[\s\-]+", given)
    out = []
    for p in parts:
        if not p:
            continue
        out.append(p[0].upper() + ".")
    return " ".join(out)


def author_pairs(entry):
    if entry.get("authors"):
        return entry["authors"]
    doi = entry["doi"]
    csl = CSL.get(doi, {})
    authors = csl.get("author") or []
    pairs = []
    for a in authors:
        fam = clean(a.get("family", ""))
        giv = clean(a.get("given", ""))
        if fam:
            pairs.append((fam, giv))
        elif a.get("literal"):
            pairs.append((clean(a["literal"]), ""))
    if pairs:
        return pairs
    oa = OA.get(doi, {})
    for name in oa.get("authors", []):
        name = clean(name)
        if not name:
            continue
        bits = name.split()
        if len(bits) == 1:
            pairs.append((bits[0], ""))
        else:
            pairs.append((" ".join(bits[:-1]), bits[-1]))
    return pairs


def fmt_author(pair):
    fam, giv = pair
    if giv:
        return f"{fam}, {initials(giv)}"
    return fam


def fmt_authors(entry):
    pairs = author_pairs(entry)
    names = [fmt_author(p) for p in pairs]
    if not names:
        return "Penulis tidak tersedia"
    if len(names) == 1:
        return names[0]
    return ", ".join(names[:-1]) + ", & " + names[-1]


def fmt_authors_short(entry):
    pairs = author_pairs(entry)
    fams = [p[0] for p in pairs]
    if not fams:
        return "Penulis tidak tersedia"
    if len(fams) == 1:
        return fams[0]
    if len(fams) == 2:
        return f"{fams[0]} & {fams[1]}"
    return f"{fams[0]} et al."


def meta(entry):
    doi = entry["doi"]
    csl = CSL.get(doi, {})
    oa = OA.get(doi, {})
    title = entry.get("title") or clean(csl.get("title") or oa.get("title"))
    venue = entry.get("venue") or clean(csl.get("container-title") or oa.get("venue"))
    year = entry.get("year")
    if not year:
        dp = (csl.get("issued") or {}).get("date-parts")
        year = dp[0][0] if dp and dp[0] else oa.get("year")
    volume = entry.get("volume")
    if volume is None:
        volume = csl.get("volume") or (oa.get("biblio") or {}).get("volume") or ""
    issue = entry.get("issue")
    if issue is None:
        issue = csl.get("issue") or (oa.get("biblio") or {}).get("issue") or ""
    pages = entry.get("pages")
    if pages is None:
        pages = csl.get("page") or ""
        if not pages:
            b = oa.get("biblio") or {}
            fp, lp = b.get("first_page"), b.get("last_page")
            if fp and lp and fp != lp:
                pages = f"{fp}-{lp}"
            elif fp:
                pages = str(fp)
    pages = clean(pages)
    dtype = entry.get("dtype") or ("Artikel jurnal" if oa.get("type") == "article" else "Prosiding")
    publisher = entry.get("publisher")
    if not publisher:
        if doi.startswith("10.1109"):
            publisher = "IEEE Xplore"
        elif doi.startswith("10.1016"):
            publisher = "Elsevier ScienceDirect"
        elif doi.startswith("10.1145"):
            publisher = "ACM (Scopus)"
        elif doi.startswith("10.1007"):
            publisher = "Springer (Scopus)"
        elif doi.startswith("10.1002"):
            publisher = "Wiley (Scopus)"
        elif doi.startswith("10.1364"):
            publisher = "Optica (Scopus)"
        elif doi.startswith("10.3837"):
            publisher = "KSII (Scopus)"
        else:
            publisher = "Terindeks"
    oa_info = oa.get("open_access") or oa.get("oa") or {}
    oa_status = oa_info.get("oa_status") or ""
    oa_label = {
        "gold": "Open access (gold)",
        "hybrid": "Open access (hybrid)",
        "green": "Green OA (repositori)",
        "bronze": "Bronze OA",
        "diamond": "Open access (diamond)",
        "closed": "Berbayar/closed",
    }.get(oa_status, oa_status or "Tidak diketahui")
    return {
        "title": title, "venue": venue, "year": year, "volume": volume,
        "issue": issue, "pages": pages, "dtype": dtype,
        "publisher": publisher, "oa": oa_label,
    }


def cite(entry, short=False):
    m = meta(entry)
    authors = fmt_authors(entry)
    if short:
        first = author_pairs(entry)
        if first:
            fam = first[0][0]
            authors = fam + (" et al." if len(first) > 1 else "")
    s = f"{authors} ({m['year']}). {m['title']}. *{m['venue']}*"
    if m["volume"]:
        s += f", {m['volume']}"
        if m["issue"]:
            s += f"({m['issue']})"
    if m["pages"]:
        s += f", {m['pages']}"
    s += f". https://doi.org/{entry['doi']}"
    return s


def bib_key(entry):
    pairs = author_pairs(entry)
    fam = pairs[0][0] if pairs else "anon"
    fam = unicodedata.normalize("NFKD", fam).encode("ascii", "ignore").decode()
    fam = re.sub(r"[^A-Za-z]", "", fam).lower() or "anon"
    year = meta(entry)["year"]
    title = meta(entry)["title"]
    word = ""
    for w in re.findall(r"[A-Za-z]+", title):
        if w.lower() not in {"a", "an", "the", "of", "for", "on", "in", "and", "to", "with", "over", "via"}:
            word = w.lower()
            break
    return f"{fam}{year}{word}"


def bib_escape(s):
    s = clean(s)
    s = s.replace("\\", r"\textbackslash{}")
    for ch in ["&", "%", "#"]:
        s = s.replace(ch, "\\" + ch)
    s = s.replace("_", r"\_")
    return s


def bib_entry(entry):
    m = meta(entry)
    pairs = author_pairs(entry)
    authors = " and ".join(f"{fam}, {giv}" if giv else fam for fam, giv in pairs)
    key = bib_key(entry)
    pub = {
        "IEEE Xplore": "IEEE",
        "Elsevier ScienceDirect": "Elsevier",
        "ACM (Scopus)": "ACM",
        "Springer (Scopus)": "Springer",
        "Wiley (Scopus)": "Wiley",
        "Optica (Scopus)": "Optica Publishing Group",
        "KSII (Scopus)": "KSII",
    }.get(m["publisher"], m["publisher"])
    if m["dtype"].lower().startswith("prosiding"):
        lines = [f"@inproceedings{{{key},",
                 f"  author = {{{bib_escape(authors)}}},",
                 f"  title = {{{bib_escape(m['title'])}}},",
                 f"  booktitle = {{{bib_escape(m['venue'])}}},",
                 f"  year = {{{m['year']}}},"]
        if m["pages"]:
            lines.append(f"  pages = {{{bib_escape(m['pages']).replace('-', '--')}}},")
        lines += [f"  publisher = {{{bib_escape(pub)}}},",
                  f"  doi = {{{entry['doi']}}}", "}"]
    else:
        lines = [f"@article{{{key},",
                 f"  author = {{{bib_escape(authors)}}},",
                 f"  title = {{{bib_escape(m['title'])}}},",
                 f"  journal = {{{bib_escape(m['venue'])}}},",
                 f"  year = {{{m['year']}}},"]
        if m["volume"]:
            lines.append(f"  volume = {{{bib_escape(m['volume'])}}},")
        if m["issue"]:
            lines.append(f"  number = {{{bib_escape(m['issue'])}}},")
        if m["pages"]:
            lines.append(f"  pages = {{{bib_escape(m['pages']).replace('-', '--')}}},")
        lines += [f"  publisher = {{{bib_escape(pub)}}},",
                  f"  doi = {{{entry['doi']}}}", "}"]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Build outputs
# ---------------------------------------------------------------------------
by_section = {k: [] for k in SECTIONS}
for e in ENTRIES:
    by_section[e["section"]].append(e)

for k in by_section:
    by_section[k].sort(key=lambda x: (0 if x["role"] == "Inti" else 1 if x["role"] == "Pendukung" else 2, x["id"]))

counts = {
    "total": len(ENTRIES),
    "jurnal": sum(1 for e in ENTRIES if meta(e)["dtype"] == "Artikel jurnal"),
    "prosiding": sum(1 for e in ENTRIES if meta(e)["dtype"] == "Prosiding"),
    "ieee": sum(1 for e in ENTRIES if meta(e)["publisher"] == "IEEE Xplore"),
    "elsevier": sum(1 for e in ENTRIES if meta(e)["publisher"] == "Elsevier ScienceDirect"),
    "scopus_lain": sum(1 for e in ENTRIES if "(Scopus)" in meta(e)["publisher"]),
}
print(counts)

# README
readme = f"""# Review Jurnal 2023-2026 — Proposal Tesis Kasmil Papalia

Folder ini berisi **review literatur terstruktur** untuk proposal:

> *Pengembangan Histeresis Asimetris Sekuensial untuk Penyesuaian Rasio Dinamis Pembagian Beban Multi-WAN Fiber Optic dan Satelit LEO (Studi Kasus: PCC pada Router MikroTik).*

## 1. Isi folder

- **{counts['total']} paper** terbit 2023-2026.
- **{counts['jurnal']} artikel jurnal** dan **{counts['prosiding']} prosiding**.
- **{counts['ieee']} paper IEEE Xplore**, **{counts['elsevier']} paper Elsevier ScienceDirect**, dan **{counts['scopus_lain']} paper dari penerbit lain yang umumnya terindeks Scopus** (ACM, Springer, Wiley, Optica, KSII).
- Setiap paper diberi **tag subbab** 1.2.1-1.2.10, **peran** (Inti/Pendukung/Latar), ringkasan, alasan relevansi, cara pakai, dan keterbatasan.
- Metadata DOI diverifikasi pada **25 November 2026** melalui DOI content negotiation dan OpenAlex.
- Data mentah pencarian disimpan di `data_mentah/` agar dapat diaudit ulang tanpa mengganggu file review.

> Catatan: folder ini **tidak memuat PDF berbayar**. Setiap entri menyertakan DOI; unduh PDF melalui akses institusi atau akses terbuka yang disediakan penerbit.

## 2. Cara cepat memakai folder

1. Buka `00_RINGKASAN_REVIEW.md` untuk melihat temuan utama dan peta celah.
2. Buka `per_pembahasan/` sesuai subbab yang sedang ditulis.
3. Untuk menyalin sitasi, gunakan `03_DAFTAR_JURNAL.bib` (BibTeX) atau `01_DAFTAR_JURNAL.md`.
4. Untuk melihat paper mana yang mendukung klaim tertentu, buka `catatan/02_PETA_KUTIPAN.md`.
5. Untuk revisi proposal, buka `catatan/03_REVISI_YANG_DISARANKAN.md`.

## 3. Peta subbab

| Subbab | Topik | Paper inti | Jumlah |
|---|---|---|---|
| 1.2.1 | QoS dan QoE | P04 | {len(by_section['1.2.1'])} |
| 1.2.2 | FO dan LEO Starlink | P05, P06, P08 | {len(by_section['1.2.2'])} |
| 1.2.3 | MikroTik dan PCC praktik | P12 | {len(by_section['1.2.3'])} |
| 1.2.4 | PCC dan hash per-koneksi | P13, P14 | {len(by_section['1.2.4'])} |
| 1.2.5 | Load balancing dan SD-WAN | P18, P19, P20, P21 | {len(by_section['1.2.5'])} |
| 1.2.6 | Quickest change detection | P23, P24 | {len(by_section['1.2.6'])} |
| 1.2.7 | CUSUM dua arah | P29 | {len(by_section['1.2.7'])} |
| 1.2.8 | Histeresis dan handover | P32, P33, P34 | {len(by_section['1.2.8'])} |
| 1.2.9 | Komitmen koneksi dan biaya | P38, P40 | {len(by_section['1.2.9'])} |
| 1.2.10 | Integrasi, SRLG, dan TE | P45, P46, P48, P49 | {len(by_section['1.2.10'])} |

## 4. Sepuluh paper yang paling wajib dibaca

1. **P23** Sun & Zou (2024), *Quickest Change Detection in Autoregressive Models* — menjawab kritik asumsi i.i.d.
2. **P24** Xie, Moustakides & Xie (2023), *Window-Limited CUSUM* — CUSUM dengan parameter pasca-perubahan tidak diketahui.
3. **P13** Levi & Keslassy (2023), *Beyond the Ring: Quantized Heterogeneous Consistent Hashing* — dasar kuantisasi hash.
4. **P21** Botta et al. (2026), *Seeing Through the Overlay* — deteksi bottleneck bersama via korelasi latensi.
5. **P38** Amend & Rakocevic (2024), *Cost-efficient multipath scheduling* — biaya jalur mahal vs QoE.
6. **P40** Shojaee et al. (2024), *Economic-statistical design* — ambang dari biaya, bukan ARL saja.
7. **P32** Eydian et al. (2025), *Handover Strategy ... Hysteresis Margin* — histeresis di LEO.
8. **P45** Ju et al. (2025), *Dynamic Load-Balancing Routing Strategy for LEO* — state of the art LB LEO.
9. **P46** Kim et al. (2026), *Utilization-aware multipath traffic splitting* — splitting rasio di LEO.
10. **P12** Amalia et al. (2023), *PCC + failover pada MikroTik* — baseline PCC praktis.

## 5. Tiga klaim yang paling kuat didukung literatur

1. **Rasio statis tidak lagi memadai** ketika jalur LEO mengalami degradasi cepat dan kapasitas berubah (P05, P06, P08, P12, P18).
2. **Ambang deteksi dapat diturunkan dari biaya**, bukan hanya dari ARL, dan desain ekonomi chart sudah menunjukkan manfaatnya (P23, P24, P38, P40).
3. **Kuantisasi hash dan SRLG dapat dipertemukan**, tetapi belum ada yang melakukannya untuk rasio per-koneksi multi-WAN (P13, P14, P21, P48, P49).

## 6. Batasan folder ini

- Fokus pada paper 2023-2026; paper klasik (Page, Lorden, Moustakides, Duncan) tetap perlu dikutip dari sumber aslinya.
- Status Scopus untuk penerbit non-IEEE/Elsevier perlu dicek ulang di *Scopus Source List* institusi.
- Beberapa paper 2026 masih *early access* atau belum memiliki volume/halaman final.
- Paper tanpa abstrak daring ditandai eksplisit; ringkasannya harus diverifikasi pada teks penuh.
- Folder ini adalah alat bantu review, bukan pengganti membaca paper.

## 7. Struktur folder

```
review_jurnal_2023_2026/
├── README.md
├── 00_RINGKASAN_REVIEW.md
├── 01_DAFTAR_JURNAL.md
├── 02_DAFTAR_JURNAL.csv
├── 03_DAFTAR_JURNAL.bib
├── per_pembahasan/
│   ├── 1.2.1_QoS_dan_QoE.md
│   ├── 1.2.2_FO_dan_LEO_Starlink.md
│   ├── 1.2.3_MikroTik_dan_PCC_praktik.md
│   ├── 1.2.4_PCC_dan_hash_per_koneksi.md
│   ├── 1.2.5_Load_balancing_dan_SD-WAN.md
│   ├── 1.2.6_Quickest_change_detection.md
│   ├── 1.2.7_CUSUM_dua_arah.md
│   ├── 1.2.8_Histeresis_dan_handover.md
│   ├── 1.2.9_Komitmen_koneksi_dan_biaya.md
│   └── 1.2.10_Integrasi_SRLG_dan_TE.md
├── catatan/
│   ├── 01_MATRIKS_GAP.md
│   ├── 02_PETA_KUTIPAN.md
│   ├── 03_REVISI_YANG_DISARANKAN.md
│   ├── 04_KANDIDAT_DITOLAK_DAN_CATATAN.md
│   ├── 05_VERIFIKASI_METADATA.md
│   ├── 06_KALIMAT_SIAP_PAKAI.md
│   └── 07_DRAFT_KONTRIBUSI.md
└── data_mentah/
    ├── _selected_raw.json
    ├── _csl.json
    ├── _digest.txt
    ├── _targeted.json
    └── _raw_openalex.json
```
"""
with open(os.path.join(OUT, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme)

# Ringkasan review
ring = f"""# Ringkasan Review Literatur

**Tanggal review:** 25 November 2026  
**Cakupan:** {counts['total']} paper, 2023-2026, terbagi dalam 10 subbab proposal.

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
"""
with open(os.path.join(OUT, "00_RINGKASAN_REVIEW.md"), "w", encoding="utf-8") as f:
    f.write(ring)

# Daftar jurnal Markdown
lines = ["# Daftar Jurnal dan Prosiding 2023-2026", "",
         f"Total **{counts['total']}** paper. Tag subbab mengikuti struktur Bab I proposal.", "",
         "| ID | Tahun | Tipe | Judul | Venue | Penerbit/Indeks | Tag | Peran | DOI |",
         "|---|---|---|---|---|---|---|---|---|"]
for e in ENTRIES:
    m = meta(e)
    title = m["title"].replace("|", "\\|")
    venue = m["venue"].replace("|", "\\|")
    lines.append(f"| {e['id']} | {m['year']} | {m['dtype']} | {title} | {venue} | {m['publisher']} | {e['tags']} | {e['role']} | [{e['doi']}](https://doi.org/{e['doi']}) |")
lines += ["", "## Catatan", "",
          "- **Inti** = paper yang langsung dipakai untuk membangun argumen/novelty.",
          "- **Pendukung** = paper yang memperkuat konteks atau metodologi.",
          "- **Latar** = paper untuk definisi/istilah, bukan bukti utama.",
          "- Status akses dan abstrak ada di file per subbab dan CSV."]
with open(os.path.join(OUT, "01_DAFTAR_JURNAL.md"), "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

# CSV
with open(os.path.join(OUT, "02_DAFTAR_JURNAL.csv"), "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["id", "tahun", "tipe", "judul", "penulis", "venue", "volume",
                "nomor", "halaman", "penerbit_indeks", "tag_subbab", "peran",
                "doi", "url", "akses", "ringkasan_singkat"])
    for e in ENTRIES:
        m = meta(e)
        w.writerow([e["id"], m["year"], m["dtype"], m["title"], fmt_authors(e),
                    m["venue"], m["volume"], m["issue"], m["pages"],
                    m["publisher"], e["tags"], e["role"], e["doi"],
                    f"https://doi.org/{e['doi']}", m["oa"], e["summary"]])

# BibTeX
bibs = []
for e in ENTRIES:
    bibs.append(bib_entry(e))
with open(os.path.join(OUT, "03_DAFTAR_JURNAL.bib"), "w", encoding="utf-8") as f:
    f.write("\n\n".join(bibs) + "\n")

# Per-section files
for sec, info in SECTIONS.items():
    items = by_section[sec]
    n_core = sum(1 for x in items if x["role"] == "Inti")
    n_support = sum(1 for x in items if x["role"] == "Pendukung")
    n_bg = sum(1 for x in items if x["role"] == "Latar")
    cross = [e for e in ENTRIES
             if e["section"] != sec
             and sec in [t.strip() for t in e["tags"].split(";")]]
    out = [f"# {sec} {info['title']}", "",
           f"**Fungsi subbab:** {info['function']}", "",
           f"**Jumlah paper utama:** {len(items)} ({n_core} inti, {n_support} pendukung, {n_bg} latar)", "",
           f"**Rujukan lintas subbab:** {len(cross)} paper (dibahas di file subbab utamanya)", "",
           f"**Pesan kunci:** {info['message']}", ""]
    if info.get("note"):
        out += [f"**Catatan cakupan:** {info['note']}", ""]
    out += ["## Daftar paper", "",
           "| ID | Sitasi ringkas | Tahun | Venue | Peran |",
           "|---|---|---|---|---|"]
    for e in items:
        m = meta(e)
        out.append(f"| {e['id']} | {fmt_authors_short(e)} | {m['year']} | {m['venue']} | {e['role']} |")
    out += ["", "## Rujukan lintas subbab", ""]
    if cross:
        out += ["| ID | Sitasi ringkas | Tahun | Subbab utama | Peran |",
                "|---|---|---|---|---|"]
        for e in cross:
            m = meta(e)
            out.append(f"| {e['id']} | {fmt_authors_short(e)} | {m['year']} | {e['section']} | {e['role']} |")
        out += ["", "Paper di atas tidak diulang review-nya di sini; buka file subbab utamanya untuk ringkasan lengkap."]
    else:
        out += ["Tidak ada paper yang ditandai lintas ke subbab ini."]
    out += ["", "## Review per paper", ""]
    for e in items:
        m = meta(e)
        out += [f"### {e['id']} — {fmt_authors(e)} ({m['year']})", "",
                f"**Sitasi lengkap:** {cite(e)}", "",
                f"**Identitas:** {m['publisher']} · {m['dtype']} · {m['year']} · {m['oa']}", "",
                f"**Tag subbab:** `{e['tags']}`", "",
                f"**Peran:** **{e['role']}**", "",
                f"**Temuan/ringkasan:** {e['summary']}", "",
                f"**Mengapa relevan:** {e['relevance']}", "",
                f"**Cara memakainya di proposal:** {e['usage']}", "",
                f"**Keterbatasan / yang belum dijawab:** {e['limitation']}", "",
                "---", ""]
    out += ["## Celah yang belum dijawab subbab ini", "", info["gap"], "",
            "## Kalimat siap pakai", "", f"> {info['sentence']}", "",
            "## Catatan penulisan", "",
            "- Letakkan paper **Inti** lebih dulu dalam paragraf, lalu **Pendukung** sebagai penguat.",
            "- Jangan mengklaim bahwa paper ini sudah melakukan hal yang sama; gunakan kolom “Keterbatasan” untuk menunjukkan celah.",
            "- Untuk paper bertanda “abstrak tidak tersedia”, baca teks penuh sebelum mengutip angka atau klaim spesifik.", ""]
    with open(os.path.join(OUT, "per_pembahasan", info["file"]), "w", encoding="utf-8") as f:
        f.write("\n".join(out))

# ---------------------------------------------------------------------------
# Notes
# ---------------------------------------------------------------------------
gap = """# Matriks Gap → Kontribusi

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
"""
with open(os.path.join(OUT, "catatan", "01_MATRIKS_GAP.md"), "w", encoding="utf-8") as f:
    f.write(gap)

# Peta kutipan
peta = """# Peta Kutipan per Subbab

## 1. Matriks subbab → paper

| Subbab | Paper inti | Paper pendukung | Fungsi argumen |
|---|---|---|---|
| 1.2.1 QoS/QoE | P04 | P01, P02, P03 | Menetapkan metrik QoS/QoE dan biaya tunda |
| 1.2.2 FO/LEO | P05, P06, P08 | P07, P09, P10 | Menjelaskan dinamika LEO dan skala waktu probe |
| 1.2.3 MikroTik/PCC | P12 | P11 | Baseline PCC statis dan praktik vendor |
| 1.2.4 Hash | P13, P14 | P15, P16, P17 | Landasan kuantisasi dan stabilitas hash |
| 1.2.5 SD-WAN | P18, P19, P20, P21 | P22 | Celah granularitas keputusan dan evaluasi |
| 1.2.6 QCD | P23, P24 | P25, P26, P27, P28 | Asumsi i.i.d., ARL, dan model dependen |
| 1.2.7 CUSUM | P29 | P30, P31 | CUSUM dua arah dan estimasi pasca-perubahan |
| 1.2.8 Histeresis | P32, P33, P34 | P35, P36, P37 | Margin/TTT dan biaya handover |
| 1.2.9 Biaya | P38, P40 | P39, P41 | Economic design dan biaya keputusan |
| 1.2.10 SRLG/TE | P45, P46, P48, P49 | P42, P43, P44, P47, P50 | SRLG, TE LEO, dan kuantisasi rasio |

## 2. Indeks lengkap 50 paper

| ID | Sitasi ringkas | Tahun | Tag | Peran |
|---|---|---|---|---|
"""
for e in ENTRIES:
    m = meta(e)
    peta += f"| {e['id']} | {fmt_authors_short(e)} | {m['year']} | {e['tags']} | {e['role']} |\n"
peta += """
## 3. Urutan menulis paragraf literatur

1. **Mulai dari praktik** (P12/P11): PCC statis dan failover.
2. **Tunjukkan masalah** (P05/P06/P08): LEO dinamis, outage, rekonfigurasi 15 detik.
3. **Tunjukkan solusi yang sudah ada** (P18/P19/P20): SD-WAN/DRL adaptif, tetapi granularitasnya berbeda.
4. **Masuk ke teori deteksi** (P23/P24): CUSUM optimal, tetapi ambang ARL dan asumsi i.i.d.
5. **Tunjukkan preseden biaya** (P38/P40): desain ekonomi chart dan cost-aware multipath.
6. **Tutup dengan celah** (P13/P14/P21/P48/P49): hash quantization + SRLG belum dipertemukan.
7. **Baru masuk ke kontribusi** Anda: K1-K4.

## 4. Aturan sitasi

- Gunakan gaya yang diminta Universitas Hasanuddin (biasanya APA 7). File BibTeX sudah siap.
- Untuk klaim yang sangat spesifik (angka, persentase), kutip paper aslinya dan cantumkan halaman jika memungkinkan.
- Jangan mengutip paper yang hanya membaca abstrak. Untuk P02, P36, dan P39, baca teks penuh sebelum memakai klaim detail.
- Hindari sitasi berderet tanpa fungsi. Setiap sitasi harus menjawab: “paper ini mendukung klaim apa?”
"""
with open(os.path.join(OUT, "catatan", "02_PETA_KUTIPAN.md"), "w", encoding="utf-8") as f:
    f.write(peta)

# Revisi yang disarankan
revisi = """# Revisi yang Disarankan Berdasarkan Literatur

Diurutkan dari yang paling mendesak. Setiap butir menyebut paper pendukung.

## R1. Definisikan E, U, dan F secara formal (prioritas tertinggi)

Tambahkan definisi operasional sebelum masuk ke hipotesis:

- **E (exposure):** proporsi koneksi baru yang ditempatkan pada jalur berstatus terdegradasi, diukur pada jendela waktu yang sama dengan status jalur.
- **U (unused capacity):** kapasitas jalur sehat yang tidak terpakai karena rasio terlalu konservatif.
- **F (reconfiguration frequency):** jumlah perubahan bobot/status per jam, atau jumlah remap bucket per jam.

Paper: P04 (excess delay), P38 (biaya jalur mahal), P41 (migration overhead), P12 (QoS agregat).

Mengapa: tanpa definisi ini, klaim “E lebih rendah pada U setara” tidak dapat diuji dan mudah dibantah penguji.

## R2. Ganti “U setara” dengan uji frontier E–U

Jangan hanya membandingkan pada satu titik U. Buat kurva E–U dengan beberapa nilai ambang, lalu bandingkan:

- E pada U yang sama (matched-U), atau
- luas area di bawah frontier (semakin kecil semakin baik).

Paper: P40 (tradeoff ekonomi-statistik), P35 (tradeoff handover success vs spectral efficiency), P04 (delay vs utilization).

Mengapa: “U setara” adalah klaim kuat yang sulit dibuktikan dengan satu konfigurasi. Frontier lebih jujur dan lebih informatif.

## R3. Akui asumsi i.i.d. dan siapkan alternatif

Tambahkan satu paragraf:

> “CUSUM klasik mengasumsikan observasi i.i.d. sebelum perubahan. Data probe jaringan dapat berkorelasi karena rekonfigurasi periodik, cuaca, dan beban. Karena itu, penelitian ini (i) menguji autokorelasi residu, (ii) memakai window-limited CUSUM, dan (iii) menyiapkan AR-CuSum sebagai pembanding robustness.”

Paper: P23 (QCD AR), P24 (window-limited CUSUM), P27 (robust score-based), P28 (Markov), P29 (post-change estimation).

Mengapa: ini adalah kritik metodologis paling mungkin dari penguji QCD.

## R4. Perkuat model observasi M=2

Jelaskan:

- mengapa dua target cukup (biaya probe, independensi, cakupan),
- bagaimana menangani target yang mati,
- bagaimana menggabungkan dua target (AND/OR/median),
- uji sensitivitas terhadap jumlah target.

Paper: P05 (dynamics), P06 (obstruction/burst loss), P08 (15-s reconfiguration), P31 (multivariate CUSUM).

Mengapa: model observasi dua target dengan rolling median dan p1=0.25 terlihat rapuh; penguji akan bertanya apa yang terjadi jika satu target bias.

## R5. Tambahkan tabel aksi 8 status dan batasan SRLG

Buat tabel lengkap:

| Status FO | Status LEO A | Status LEO B | Bobot target | Catatan SRLG |
|---|---|---|---|---|
| baik | baik | baik | ... | ... |
| baik | buruk | baik | ... | ... |
| ... | ... | ... | ... | ... |

Paper: P21 (joint/disjoint overlay), P48 (regional SRLG), P49 (SRLG-disjoint path), P50 (SBPP).

Mengapa: proposal saat ini belum menunjukkan peta aksi lengkap; ini celah yang mudah dilihat penguji.

## R6. Jelaskan algoritma kuantisasi dan sapuan N

Tambahkan pseudocode:

1. Hitung bobot kontinu dari status jalur.
2. Kuantisasi ke N bucket.
3. Terapkan `keep-min(c_i, n_i)` untuk meminimalkan remap.
4. Ukur quantization error dan F.

Paper: P13 (quantized CH), P14 (weighted DxHash), P16 (CHCA), P17 (survey).

Mengapa: klaim “minimal remap” harus dibuktikan, bukan diasumsikan.

## R7. Tambahkan baseline A0–A7 dan protokol tuning yang adil

Minimal:

- A0: PCC statis 1:1:1.
- A1: PCC statis dengan rasio kapasitas.
- A2: failover reaktif.
- A3: histeresis k-sampel.
- A4: CUSUM simetris.
- A5: CUSUM asimetris tanpa SRLG.
- A6: CUSUM asimetris + SRLG, kuantisasi naif.
- A7: usulan lengkap (minimal-remap).

Paper: P12, P19, P20, P38, P40.

Mengapa: tanpa ablation, kontribusi K2 dan K3 tidak terpisahkan.

## R8. Tambahkan tabel parameter biaya dan analisis sensitivitas

Tabel: `C_salah`, `C_tunda`, `ν`, `Δt`, `λ`, `w`, `L`, `G`, `H`.

Lakukan sensitivitas ±25% dan tunjukkan perubahan `h*`.

Paper: P40 (sensitivity to shift misestimation), P39 (economic design), P38 (cost vs QoE).

Mengapa: rumus `h*` hanya kredibel jika parameter dan asumsinya jelas.

## R9. Perjelas evaluasi shadow-mode

Jelaskan:

- bagaimana trafik produksi dicatat,
- bagaimana keputusan shadow dibandingkan dengan keputusan aktual,
- bagaimana counterfactual dihitung,
- bagaimana menghindari selection bias.

Paper: P19 (SD-WAN testbed), P21 (Mininet + real topology), P12 (production deployment).

Mengapa: shadow-mode adalah bagian yang paling mudah dipertanyakan secara metodologis.

## R10. Perbaiki timeline 3 bulan

Timeline saat ini terlalu padat untuk:

- kalibrasi q0,
- replay,
- testbed,
- shadow,
- produksi,
- analisis.

Saran: tambahkan pilot 1-2 minggu dan buffer analisis; kurangi jumlah skenario jika perlu.

Paper: P12 (NDLC), P18 (SD-WAN deployment), P05 (measurement campaign).

## R11. Perbaiki inkonsistensi dokumen

- “VSAT/LEO”: VSAT umumnya GEO; pisahkan atau jelaskan.
- Heading 1.2.5 berbahasa Inggris: seragamkan ke Indonesia.
- Tabel State of the Art bernomor 12 tetapi tidak ada di Daftar Tabel.
- “keempat level” vs lima skenario A–E: samakan.
- Typo “kebururukan”, “single point  of failure”.
- Placeholder referensi `**` untuk Putra (2024) dan Ullah et al. (2025).
- Format nama “Duliades Mirsal & Herman Bedi Agtriadi”.
- “G. S. G.S. Kuo” duplikasi.

## R12. Tambahkan subbab 1.5 Kontribusi Penelitian

Lihat `catatan/07_DRAFT_KONTRIBUSI.md` untuk draft tiga paragraf dan tabel kontribusi → RQ → hipotesis → metrik.
"""
with open(os.path.join(OUT, "catatan", "03_REVISI_YANG_DISARANKAN.md"), "w", encoding="utf-8") as f:
    f.write(revisi)

# Kandidat ditolak
ditolak = """# Kandidat yang Tidak Masuk Folder Utama

Folder utama hanya memuat paper yang memenuhi tiga kriteria:

1. terbit 2023-2026;
2. dapat diverifikasi melalui DOI;
3. berasal dari IEEE Xplore, Elsevier ScienceDirect, atau penerbit yang umumnya terindeks Scopus.

## 1. Ditolak karena status indeks belum terverifikasi

| Paper | Alasan |
|---|---|
| Nugroho et al. (2026), *Quality Analysis of Service Load Balancing Using PCC, ECMP, and NTH Methods*, JANAPATI | Sangat relevan secara topik, tetapi status Scopus belum diverifikasi; jurnal nasional (SINTA) |
| Ahmadi et al. (2025), *Optimizing MikroTik Networks Using PCC Load Balancing with the PPDIOO Approach*, Jurnal Algoritma | Relevan sebagai praktik PCC, tetapi status Scopus belum diverifikasi |

Jika Anda ingin memasukkan dua paper Indonesia tersebut, letakkan di subbab 1.2.3 sebagai “praktik lokal” dan beri catatan “jurnal nasional, bukan Scopus”.

> Catatan: Putra et al. (2026), *Comparison of Load Balancing Performance Between Mikrotik ECMP and Ruijie Reyee Smart Balancing* (IEEE ICCSC) **tetap dimasukkan** sebagai P11 karena terbit di IEEE Xplore, meskipun fokusnya ECMP, bukan PCC.

## 2. Ditolak karena fokus/abstrak

| Paper | Alasan |
|---|---|
| Wan et al. (2024), *DeFlow: Differential flowlet switching for load balancing in datacenter networks*, Computer Networks | Fokus data center/flowlet, bukan multi-WAN; abstrak tidak tersedia saat verifikasi |
| Beberapa paper MikroTik 2023-2025 | Umumnya konfigurasi teknis tanpa evaluasi ilmiah yang kuat; tidak memenuhi kriteria kualitas |

## 3. Duplikasi

| Paper | Keputusan |
|---|---|
| Matsuura et al. (2023), GLOBECOM | Tidak dimasukkan karena merupakan versi konferensi dari P49 (JOCN 2024) |
| Mohan et al. (2024), WWW | Dimasukkan sebagai P08; versi arXiv tidak dihitung terpisah |
| Mbulwa et al. (2024), IEEE Access (P33) dan I2CACIS (P35) | Dua paper berbeda (optimasi parameter vs analisis kinerja), bukan duplikat; keduanya dipakai di 1.2.8 |

## 4. Paper dengan abstrak terbatas

| ID | Paper | Tindakan |
|---|---|---|
| P02 | Beshley et al. (2023), *Simulation Modelling Practice and Theory* | Baca teks penuh sebelum mengutip detail |
| P36 | Xie et al. (2026), *Ad Hoc Networks* | Baca teks penuh; ringkasan hanya berdasarkan judul |
| P39 | García-Bustos & Ramírez-Figueroa (2023), *Computers & Industrial Engineering* | Baca teks penuh; fokus pada metode economic design |

## 5. Mengapa tidak ada PDF

- Banyak paper IEEE/Elsevier berbayar; mengunduh dan mendistribusikan ulang PDF melanggar lisensi.
- Folder ini menyediakan DOI, metadata, dan catatan review; PDF dapat diunduh melalui akses institusi.
- Untuk paper open access, gunakan tombol “Download” pada halaman DOI.

## 6. Cara menambah paper baru

1. Cek DOI di `https://doi.org/...`.
2. Pastikan tahun 2023-2026.
3. Tambahkan entri ke `build_review.py` (atau buat file Markdown baru).
4. Perbarui `01_DAFTAR_JURNAL.md`, CSV, dan BibTeX.
5. Tandai subbab dan peran (Inti/Pendukung/Latar).
"""
with open(os.path.join(OUT, "catatan", "04_KANDIDAT_DITOLAK_DAN_CATATAN.md"), "w", encoding="utf-8") as f:
    f.write(ditolak)

# Verifikasi metadata
verif = f"""# Verifikasi Metadata

**Tanggal:** 25 November 2026  
**Jumlah paper:** {counts['total']}  
**Rentang:** 2023-2026

## 1. Metode

- DOI setiap paper diselesaikan melalui `https://doi.org/DOI` dengan content negotiation `application/vnd.citationstyles.csl+json`.
- Metadata pelengkap (abstrak, status OA, sitasi) diambil dari OpenAlex.
- Tahun yang dipakai adalah tahun terbit resmi pada record CSL/issue, bukan tahun unggah pertama.
- Tidak ada paper yang dimasukkan hanya berdasarkan judul tanpa DOI yang valid.

## 2. Komposisi

| Kategori | Jumlah |
|---|---|
| Total paper | {counts['total']} |
| Artikel jurnal | {counts['jurnal']} |
| Prosiding | {counts['prosiding']} |
| IEEE Xplore | {counts['ieee']} |
| Elsevier ScienceDirect | {counts['elsevier']} |
| Penerbit lain (Scopus) | {counts['scopus_lain']} |

## 3. Anomali metadata yang perlu diketahui

| ID | Isu | Tindakan |
|---|---|---|
| P03 | DOI 2025, tetapi issue resmi 2026 (vol. 34) | Gunakan 2026; cek halaman jurnal |
| P12 | DOI berakhiran 2022 dan daring Desember 2022, tetapi volume resmi 216 terbit 2023 | Gunakan 2023; sebut “daring 2022” bila perlu |
| P16 | Daring 30 November 2025, tetapi issue resmi Januari 2026 (vol. 36 no. 1) | Gunakan 2026 |
| P18 | DOI 2025, tetapi issue resmi 2026 (vol. 28) | Gunakan 2026; cek halaman jurnal |
| P33 | DOI 2023, tetapi issue resmi 2024 (vol. 12) | Gunakan 2024 |
| P41 | Halaman belum tersedia | Cantumkan volume/issue saja |
| P46 | Artikel in press, volume/halaman belum ada | Cantumkan “in press” |
| P49 | Halaman hanya tersedia sebagai nomor artikel E23 | Cantumkan E23, bukan rentang halaman |
| P02 | Abstrak tidak tersedia; judul mengandung karakter Cyrillic | Karakter dinormalisasi; verifikasi teks penuh |
| P36 | Abstrak tidak tersedia | Verifikasi teks penuh |
| P39 | Abstrak tidak tersedia | Verifikasi teks penuh |

## 4. Status indeks

- **IEEE Xplore** dan **Elsevier ScienceDirect** adalah sumber utama.
- **ACM, Springer, Wiley, Optica, KSII** umumnya terindeks Scopus, tetapi status final harus dicek di *Scopus Source List* institusi.
- Folder ini **tidak** mengklaim kuartil (Q1/Q2/Q3/Q4) karena kuartil berubah setiap tahun dan memerlukan akses Scimago/Scopus.

## 5. Cara mengecek ulang

1. Buka DOI.
2. Cocokkan judul, penulis, venue, tahun, volume, halaman.
3. Cek status indeks di Scopus Source List.
4. Cek apakah paper masih “early access” atau sudah final.
5. Untuk paper berbayar, gunakan akses perpustakaan kampus.

## 6. Yang belum diverifikasi

- Isi lengkap semua paper (baru abstrak/metadata).
- Kualitas metodologis secara rinci (sample size, validitas statistik).
- Status Scopus per paper (hanya level venue).
- Kesesuaian format sitasi dengan pedoman Universitas Hasanuddin.

> Gunakan file ini sebagai peta, bukan sebagai pengganti membaca paper.
"""
with open(os.path.join(OUT, "catatan", "05_VERIFIKASI_METADATA.md"), "w", encoding="utf-8") as f:
    f.write(verif)

# Kalimat siap pakai
kalimat = """# Kalimat Siap Pakai per Subbab

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
"""
with open(os.path.join(OUT, "catatan", "06_KALIMAT_SIAP_PAKAI.md"), "w", encoding="utf-8") as f:
    f.write(kalimat)

# Draft kontribusi
kontribusi = """# Draft Subbab 1.5 Kontribusi Penelitian

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
"""
with open(os.path.join(OUT, "catatan", "07_DRAFT_KONTRIBUSI.md"), "w", encoding="utf-8") as f:
    f.write(kontribusi)

print("done all outputs")
