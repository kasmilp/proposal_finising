# -*- coding: utf-8 -*-
"""Build the architecture comparison deck (old vs proposed) for the thesis proposal.

Run:  python build_ppt_arsitektur.py
Out:  Arsitektur_Lama_vs_Baru_PCC.pptx
"""
import os
import math
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR
from pptx.enum.dml import MSO_LINE_DASH_STYLE
from pptx.oxml.ns import qn
from lxml import etree

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, "assets_ppt")
OUT = os.path.join(BASE, "Arsitektur_Lama_vs_Baru_PCC.pptx")

# ---------------------------------------------------------------------------
# Design tokens
# ---------------------------------------------------------------------------
NAVY = "0B1B2B"
INK = "14263A"
SLATE = "536579"
MUTED = "8795A4"
LINE = "DCE4EC"
BG = "F6F8FA"
WHITE = "FFFFFF"
TEAL = "0E8F8F"
TEAL_DARK = "0A6E6E"
TEAL_LIGHT = "E7F4F3"
TEAL_PALE = "F1F9F8"
AMBER = "D98A2B"
AMBER_DARK = "A96317"
AMBER_LIGHT = "FBF1E3"
AMBER_PALE = "FDF8F1"
RED = "C65454"
RED_LIGHT = "F9E9E9"
GREEN = "2E9E6B"
GREEN_LIGHT = "E8F6EF"
INDIGO = "4C5FD5"
INDIGO_LIGHT = "ECEEFB"
INDIGO_PALE = "F5F6FE"

FONT = "Segoe UI"
FONT_B = "Segoe UI Semibold"
MONO = "Consolas"

SW, SH = 13.333, 7.5
M = 0.6


def rgb(hexstr):
    return RGBColor.from_string(hexstr)


def set_bg(slide, color):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = rgb(color)


def add_text(slide, x, y, w, h, text, size=12, color=INK, bold=False,
             font=FONT, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP,
             line_spacing=1.0, margins=(0, 0, 0, 0), italic=False,
             spacing=None, wrap=True):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = wrap
    tf.auto_size = None
    tf.margin_left = Inches(margins[0])
    tf.margin_right = Inches(margins[1])
    tf.margin_top = Inches(margins[2])
    tf.margin_bottom = Inches(margins[3])
    tf.vertical_anchor = valign
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = line_spacing
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = font
    r.font.color.rgb = rgb(color)
    if spacing is not None:
        r._r.get_or_add_rPr().set("spc", str(spacing))
    return box


def add_lines(slide, x, y, w, h, lines, size=11, color=INK, font=FONT,
              align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, line_spacing=1.05,
              space_after=0, margins=(0, 0, 0, 0), bold=False):
    """lines: list of str or (str, dict overrides)."""
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.margin_left = Inches(margins[0])
    tf.margin_right = Inches(margins[1])
    tf.margin_top = Inches(margins[2])
    tf.margin_bottom = Inches(margins[3])
    tf.vertical_anchor = valign
    for i, item in enumerate(lines):
        if isinstance(item, tuple):
            txt, ov = item
        else:
            txt, ov = item, {}
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = ov.get("align", align)
        p.line_spacing = ov.get("line_spacing", line_spacing)
        p.space_after = Pt(ov.get("space_after", space_after))
        p.space_before = Pt(ov.get("space_before", 0))
        r = p.add_run()
        r.text = txt
        r.font.size = Pt(ov.get("size", size))
        r.font.bold = ov.get("bold", bold)
        r.font.italic = ov.get("italic", False)
        r.font.name = ov.get("font", font)
        r.font.color.rgb = rgb(ov.get("color", color))
        if ov.get("spacing") is not None:
            r._r.get_or_add_rPr().set("spc", str(ov["spacing"]))
    return box


def add_rect(slide, x, y, w, h, fill=WHITE, line=None, radius=None,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE, line_w=1.0, dash=None):
    if shape == MSO_SHAPE.ROUNDED_RECTANGLE:
        shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        shp.adjustments[0] = 0.08 if radius is None else radius
    else:
        shp = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    if fill is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = rgb(fill)
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = rgb(line)
        shp.line.width = Pt(line_w)
        if dash is not None:
            shp.line.dash_style = dash
    shp.shadow.inherit = False
    shp.text_frame.text = ""
    return shp


def add_pill(slide, x, y, w, h, text, fill, color=WHITE, size=9.5, bold=True,
             line=None):
    shp = add_rect(slide, x, y, w, h, fill=fill, line=line, radius=0.5)
    tf = shp.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.04)
    tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0)
    tf.margin_bottom = Inches(0)
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = FONT
    r.font.color.rgb = rgb(color)
    return shp


def add_badge(slide, x, y, d, text, fill=TEAL, color=WHITE, size=10):
    shp = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x), Inches(y), Inches(d), Inches(d))
    shp.fill.solid()
    shp.fill.fore_color.rgb = rgb(fill)
    shp.line.fill.background()
    shp.shadow.inherit = False
    tf = shp.text_frame
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = True
    r.font.name = FONT
    r.font.color.rgb = rgb(color)
    return shp


def add_arrow(slide, x1, y1, x2, y2, color=TEAL, width=1.5, dash=None,
              head=True, tail=False):
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                   Inches(x2), Inches(y2))
    c.line.color.rgb = rgb(color)
    c.line.width = Pt(width)
    if dash is not None:
        c.line.dash_style = dash
    ln = c.line._get_or_add_ln()
    if head:
        he = etree.SubElement(ln, qn("a:headEnd"))
        he.set("type", "none")
    # DrawingML: headEnd = start, tailEnd = end
    if head:
        he = ln.find(qn("a:headEnd"))
        if he is not None:
            he.set("type", "none")
    if tail:
        te = etree.SubElement(ln, qn("a:tailEnd"))
        te.set("type", "triangle")
        te.set("w", "med")
        te.set("len", "med")
    return c


def add_polyline_arrow(slide, pts, color=TEAL, width=1.5, dash=None, arrow_end=True):
    """Draw a polyline as connected straight connectors; arrow on the last segment."""
    for i in range(len(pts) - 1):
        add_arrow(slide, pts[i][0], pts[i][1], pts[i + 1][0], pts[i + 1][1],
                  color=color, width=width, dash=dash,
                  head=False, tail=(arrow_end and i == len(pts) - 2))


def header(slide, section, title, subtitle=None, number=None):
    # left accent tick
    add_rect(slide, M, 0.42, 0.07, 0.22, fill=TEAL, line=None, radius=0.5)
    add_text(slide, M + 0.16, 0.38, 9.0, 0.28, section.upper(), size=9.5,
             color=TEAL_DARK, bold=True, spacing=120)
    add_text(slide, M, 0.65, 12.1, 0.52, title, size=26, color=NAVY, bold=True,
             line_spacing=0.95)
    if subtitle:
        add_text(slide, M, 1.14, 12.1, 0.3, subtitle, size=10.5, color=SLATE,
                 line_spacing=1.0)
        line_y = 1.46
    else:
        line_y = 1.32
    add_rect(slide, M, line_y, SW - 2 * M, 0.012, fill=LINE, line=None,
             shape=MSO_SHAPE.RECTANGLE)
    if number is not None:
        add_text(slide, SW - M - 0.5, 7.13, 0.5, 0.22, f"{number:02d}", size=8,
                 color=MUTED, align=PP_ALIGN.RIGHT)
        add_text(slide, M, 7.13, 6.5, 0.22,
                 "Arsitektur Lama vs Baru · Proposal Tesis 2026", size=8, color=MUTED)


def card(slide, x, y, w, h, fill=WHITE, line=LINE, accent=None, accent_w=0.07):
    add_rect(slide, x, y, w, h, fill=fill, line=line, radius=0.06)
    if accent:
        add_rect(slide, x, y, accent_w, h, fill=accent, line=None, radius=0.5)


def table_no_style(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    for el in list(tblPr):
        if el.tag == qn("a:tableStyleId"):
            tblPr.remove(el)
    style = etree.SubElement(tblPr, qn("a:tableStyleId"))
    style.text = "{2D5ABB26-0587-4C30-8999-92F81FD0307C}"


def cell_fill(cell, color):
    cell.fill.solid()
    cell.fill.fore_color.rgb = rgb(color)


def cell_text(cell, text, size=10, color=INK, bold=False, font=FONT,
              align=PP_ALIGN.LEFT):
    cell.margin_left = Inches(0.09)
    cell.margin_right = Inches(0.07)
    cell.margin_top = Inches(0.03)
    cell.margin_bottom = Inches(0.03)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    p.line_spacing = 0.95
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.name = font
    r.font.color.rgb = rgb(color)


# ---------------------------------------------------------------------------
# Assets
# ---------------------------------------------------------------------------
def make_cover_bg(path):
    W, H = 2560, 1440
    img = Image.new("RGB", (W, H), "#07131F")
    px = img.load()
    for yy in range(H):
        for xx in range(W):
            t = (xx / W) * 0.55 + (yy / H) * 0.45
            r = int(7 + 10 * t)
            g = int(19 + 27 * t)
            b = int(31 + 35 * t)
            px[xx, yy] = (r, g, b)

    # faint technical grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(grid)
    step = 80
    for xx in range(0, W, step):
        gd.line([(xx, 0), (xx, H)], fill=(120, 190, 200, 8), width=1)
    for yy in range(0, H, step):
        gd.line([(0, yy), (W, yy)], fill=(120, 190, 200, 8), width=1)
    img = Image.alpha_composite(img.convert("RGBA"), grid)

    # soft glows on the right
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((1600, 250, 2450, 1100), fill=(14, 143, 143, 22))
    gd.ellipse((1850, 600, 2650, 1400), fill=(217, 138, 43, 16))
    glow = glow.filter(ImageFilter.GaussianBlur(120))
    img = Image.alpha_composite(img, glow)

    # network motif on the right
    net = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    nd = ImageDraw.Draw(net)

    def bez(p0, p1, p2, p3, n=120):
        pts = []
        for i in range(n + 1):
            t = i / n
            x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
            y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
            pts.append((x, y))
        return pts

    sources = [(1810, 300, (14, 143, 143)), (2070, 430, (217, 138, 43)), (1900, 610, (14, 143, 143))]
    hub = (2180, 760)
    clients = [(2320, 1030), (2440, 900), (2240, 1120)]
    for sx, sy, col in sources:
        pts = bez((sx, sy), (sx + 90, sy + 100), (hub[0] - 130, hub[1] - 90), hub)
        nd.line(pts, fill=col + (90,), width=3)
        for p in pts[::8]:
            nd.ellipse((p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2), fill=col + (45,))
    for cx, cy in clients:
        pts = bez(hub, (hub[0] + 60, hub[1] + 80), (cx - 40, cy - 80), (cx, cy))
        nd.line(pts, fill=(120, 205, 205, 70), width=2)
    # nodes
    for sx, sy, col in sources:
        nd.ellipse((sx - 13, sy - 13, sx + 13, sy + 13), fill=col + (255,))
        nd.ellipse((sx - 30, sy - 30, sx + 30, sy + 30), outline=col + (80,), width=2)
    nd.ellipse((hub[0] - 28, hub[1] - 28, hub[0] + 28, hub[1] + 28), fill=(230, 245, 245, 255))
    nd.ellipse((hub[0] - 46, hub[1] - 46, hub[0] + 46, hub[1] + 46), outline=(120, 220, 220, 100), width=3)
    for cx, cy in clients:
        nd.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=(120, 205, 205, 210))
        nd.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), outline=(120, 205, 205, 70), width=2)

    net = net.filter(ImageFilter.GaussianBlur(0.6))
    img = Image.alpha_composite(img, net)

    # subtle vignette
    vig = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vig)
    vd.ellipse((-W * 0.25, -H * 0.3, W * 1.15, H * 1.2), fill=255)
    vig = vig.filter(ImageFilter.GaussianBlur(200))
    black = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    img = Image.composite(img, black, vig)
    img.convert("RGB").save(path, quality=95)


# ---------------------------------------------------------------------------
# Slide builders
# ---------------------------------------------------------------------------
def slide_cover(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.shapes.add_picture(os.path.join(ASSETS, "cover_bg.png"), 0, 0,
                         width=Inches(SW), height=Inches(SH))

    # left accent
    add_rect(s, 0.86, 1.18, 0.06, 2.35, fill=TEAL, line=None, radius=0.5)
    add_text(s, 1.08, 1.10, 7.0, 0.3, "PROPOSAL TESIS  ·  2026", size=10.5,
             color="9FD7D4", bold=True, spacing=180)
    add_text(s, 1.08, 1.48, 7.6, 1.9,
             "Arsitektur Lama\nvs Arsitektur Baru", size=42, color=WHITE,
             bold=True, line_spacing=0.92)
    add_rect(s, 1.10, 3.35, 1.5, 0.045, fill=AMBER, line=None, shape=MSO_SHAPE.RECTANGLE)
    add_text(s, 1.08, 3.58, 7.1, 1.05,
             "Dari PCC statis 1:1:1 menuju histeresis asimetris sekuensial "
             "sadar biaya keputusan pada pembagian beban FO–LEO",
             size=16.5, color="C9D6E2", line_spacing=1.12)

    add_text(s, 1.08, 5.18, 7.0, 0.3, "Kasmil Papalia  ·  D082252011", size=13,
             color=WHITE, bold=True)
    add_text(s, 1.08, 5.52, 7.4, 0.55,
             "Program Studi Magister Teknik Informatika\nFakultas Teknik · Universitas Hasanuddin",
             size=10.5, color="9FB0C0", line_spacing=1.2)

    # pills
    pills = [("MikroTik PCC", 1.08, 1.55), ("FO + Starlink LEO", 2.82, 1.95),
             ("CUSUM dua arah", 4.95, 1.55)]
    for txt, x, w in pills:
        add_pill(s, x, 6.48, w, 0.36, txt, fill="133344", color="CFE9E7", size=9)

    # logo card
    add_rect(s, 11.55, 0.72, 1.02, 1.18, fill=WHITE, line=None, radius=0.10)
    s.shapes.add_picture(os.path.join(ASSETS, "logo_unhas.png"), Inches(11.67),
                         Inches(0.80), height=Inches(1.02))


def slide_summary(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Ringkasan", "Satu jaringan, dua cara mengambil keputusan",
           "Arsitektur lama bereaksi saat link putus; arsitektur baru bereaksi "
           "terhadap bukti degradasi dan biaya.", 2)

    # old card
    card(s, M, 1.68, 5.55, 4.12, accent=AMBER)
    add_text(s, 0.88, 1.88, 4.6, 0.25, "ARSITEKTUR LAMA", size=9, color=AMBER_DARK,
             bold=True, spacing=120)
    add_text(s, 0.88, 2.14, 4.9, 0.45, "PCC statis 1:1:1", size=22, color=NAVY, bold=True)
    add_text(s, 0.88, 2.62, 4.95, 0.3, "Baseline eksisting · Skenario A", size=9.5,
             color=SLATE)
    items_old = [
        ("Rasio tetap", "Tidak ada umpan balik kualitas jalur."),
        ("Reaktif saat putus", "Degradasi parsial tidak memicu keputusan."),
        ("Manual", "Operator mengubah rasio saat gangguan terasa."),
    ]
    yy = 3.12
    for i, (t, d) in enumerate(items_old):
        add_badge(s, 0.88, yy + 0.03, 0.22, str(i + 1), fill=AMBER, size=8.5)
        add_text(s, 1.22, yy - 0.02, 4.55, 0.25, t, size=11.5, color=NAVY, bold=True)
        add_text(s, 1.22, yy + 0.22, 4.55, 0.26, d, size=9.5, color=SLATE)
        yy += 0.82

    # new card
    card(s, 7.18, 1.68, 5.55, 4.12, accent=TEAL)
    add_text(s, 7.46, 1.88, 4.6, 0.25, "ARSITEKTUR BARU", size=9, color=TEAL_DARK,
             bold=True, spacing=120)
    add_text(s, 7.46, 2.14, 4.9, 0.45, "Kontroler adaptif", size=22, color=NAVY, bold=True)
    add_text(s, 7.46, 2.62, 4.95, 0.3, "Usulan · Skenario D", size=9.5, color=SLATE)
    items_new = [
        ("Probe + CUSUM", "Bukti degradasi diakumulasi lintas waktu."),
        ("Ambang sadar biaya keputusan", "h↓ dan h↑ diturunkan dari biaya serta headroom."),
        ("Aktuator minimal", "Hanya bucket yang berubah; koneksi lama tetap."),
    ]
    yy = 3.12
    for i, (t, d) in enumerate(items_new):
        add_badge(s, 7.46, yy + 0.03, 0.22, str(i + 1), fill=TEAL, size=8.5)
        add_text(s, 7.80, yy - 0.02, 4.55, 0.25, t, size=11.5, color=NAVY, bold=True)
        add_text(s, 7.80, yy + 0.22, 4.55, 0.26, d, size=9.5, color=SLATE)
        yy += 0.82

    # bottom notes inside cards
    add_rect(s, 0.88, 5.36, 4.95, 0.008, fill=AMBER_LIGHT, line=None, shape=MSO_SHAPE.RECTANGLE)
    add_text(s, 0.88, 5.44, 4.95, 0.28,
             "Konsekuensi: kualitas bergantung pada konfigurasi awal.",
             size=8.6, color=AMBER_DARK, italic=True)
    add_rect(s, 7.46, 5.36, 4.95, 0.008, fill=TEAL_LIGHT, line=None, shape=MSO_SHAPE.RECTANGLE)
    add_text(s, 7.46, 5.44, 4.95, 0.28,
             "Konsekuensi: kualitas mengikuti bukti dan biaya.",
             size=8.6, color=TEAL_DARK, italic=True)

    # center arrow
    add_text(s, 6.17, 3.15, 0.8, 0.25, "evolusi", size=8, color=MUTED, align=PP_ALIGN.CENTER)
    add_rect(s, 6.30, 3.42, 0.55, 0.55, fill=TEAL, line=None,
             shape=MSO_SHAPE.RIGHT_ARROW)

    # bottom agenda chips
    chips = [
        ("01", "Mengapa lama tidak cukup?", "Lima titik buta dan akar masalahnya"),
        ("02", "Bagaimana baru bekerja?", "Kontroler, CUSUM, dan aktuator"),
        ("03", "Bagaimana dibuktikan?", "Skenario A–E, metrik E/U/F"),
    ]
    x = M
    for num, txt, sub in chips:
        add_rect(s, x, 5.96, 3.85, 0.72, fill=WHITE, line=LINE, radius=0.08)
        add_text(s, x + 0.16, 6.04, 0.35, 0.3, num, size=10, color=TEAL, bold=True)
        add_text(s, x + 0.56, 6.03, 3.1, 0.28, txt, size=9.3, color=NAVY, bold=True)
        add_text(s, x + 0.56, 6.33, 3.1, 0.22, sub, size=7.4, color=SLATE)
        x += 4.14


def slide_context(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Konteks", "Tiga jalur WAN, dua rezim risiko",
           "FO stabil tetapi terbatas; dua Starlink dinamis dan saling berkorelasi.", 3)

    # diagram card
    add_rect(s, M, 1.66, 6.95, 5.05, fill=WHITE, line=LINE, radius=0.05)
    add_text(s, 0.86, 1.76, 4.0, 0.25, "TOPOLOGI EKSISTING", size=8.5, color=MUTED,
             bold=True, spacing=110)

    isps = [
        ("FO · IndiHome", "WAN1 · latensi rendah", 1.98, TEAL),
        ("Starlink A · LEO", "WAN2 · dinamis", 2.86, AMBER),
        ("Starlink B · LEO", "WAN3 · dinamis", 3.74, AMBER),
    ]
    for title, sub, y, col in isps:
        add_rect(s, 0.86, y, 2.12, 0.64, fill=WHITE, line=col, radius=0.10)
        add_rect(s, 0.86, y, 0.07, 0.64, fill=col, line=None, radius=0.5)
        add_text(s, 1.04, y + 0.08, 1.85, 0.24, title, size=9.8, color=NAVY, bold=True)
        add_text(s, 1.04, y + 0.33, 1.85, 0.2, sub, size=8, color=SLATE)

    # router
    add_rect(s, 3.55, 2.38, 2.65, 1.42, fill=WHITE, line=NAVY, radius=0.06, line_w=1.2)
    add_rect(s, 3.55, 2.38, 2.65, 0.07, fill=NAVY, line=None, radius=0.5)
    add_text(s, 3.72, 2.54, 2.3, 0.25, "MikroTik RB1100AHx4", size=10.5, color=NAVY, bold=True)
    add_text(s, 3.72, 2.84, 2.3, 0.6,
             "PCC · mangle routing-mark\nNAT/conntrack · failover",
             size=8.8, color=SLATE, line_spacing=1.15)

    # switch + client
    add_rect(s, 3.86, 4.48, 2.02, 0.55, fill=WHITE, line=LINE, radius=0.10)
    add_text(s, 3.96, 4.59, 1.85, 0.25, "Switch client 24 port", size=8.8, color=NAVY,
             bold=True, align=PP_ALIGN.CENTER)
    add_rect(s, 4.02, 5.38, 1.70, 0.52, fill=NAVY, line=None, radius=0.5)
    add_text(s, 4.12, 5.49, 1.5, 0.22, "Pelanggan RT/RW Net", size=8.3, color=WHITE,
             bold=True, align=PP_ALIGN.CENTER)

    # arrows
    for _, _, y, col in isps:
        add_arrow(s, 2.98, y + 0.32, 3.55, 2.95, color=col, width=1.3, dash=None)
    add_arrow(s, 4.87, 3.80, 4.87, 4.48, color=TEAL, width=1.5)
    add_arrow(s, 4.87, 5.03, 4.87, 5.38, color=TEAL, width=1.5)

    # right side
    x = 7.95
    blocks = [
        ("Heterogen", "FO unggul pada latensi dan loss; LEO berubah pada skala detik–menit."),
        ("Shared risk", "Starlink A dan B terkena hujan, obstruksi, dan rekonfigurasi yang sama."),
        ("Komitmen per-koneksi", "NAT/conntrack mengikat koneksi lama; hanya koneksi baru dapat dipindah."),
    ]
    yy = 1.72
    for i, (t, d) in enumerate(blocks):
        add_badge(s, x, yy + 0.02, 0.32, str(i + 1), fill=TEAL, size=10)
        add_text(s, x + 0.46, yy, 4.25, 0.28, t, size=12.5, color=NAVY, bold=True)
        add_text(s, x + 0.46, yy + 0.29, 4.25, 0.65, d, size=10, color=SLATE,
                 line_spacing=1.12)
        yy += 1.18

    # stat cards
    stats = [("3 WAN", "1 FO · 2 LEO"), ("Δt ≈ 2,3 s", "siklus probe"), ("M = 2", "target per jalur")]
    sx = 7.95
    for i, (v, l) in enumerate(stats):
        add_rect(s, sx, 5.58, 1.48, 0.78, fill=TEAL_PALE, line=TEAL_LIGHT, radius=0.08)
        add_text(s, sx + 0.10, 5.68, 1.3, 0.25, v, size=12, color=TEAL_DARK, bold=True)
        add_text(s, sx + 0.10, 5.96, 1.3, 0.2, l, size=8, color=SLATE)
        sx += 1.60


def slide_old(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Arsitektur lama", "PCC statis: sederhana, tetapi buta kondisi",
           "Rasio 1:1:1 ditetapkan di router; tidak ada control plane yang mengamati "
           "kualitas jalur.", 4)

    # diagram
    add_rect(s, M, 1.66, 8.05, 5.0, fill=WHITE, line=LINE, radius=0.05)
    add_text(s, 0.86, 1.76, 4.0, 0.25, "BASELINE · SKENARIO A", size=8.5, color=AMBER_DARK,
             bold=True, spacing=110)

    isps = [
        ("FO · IndiHome", "WAN1", 0.92, TEAL),
        ("Starlink A", "WAN2", 3.00, AMBER),
        ("Starlink B", "WAN3", 5.08, AMBER),
    ]
    for title, sub, x, col in isps:
        add_rect(s, x, 1.98, 1.90, 0.66, fill=WHITE, line=col, radius=0.10)
        add_rect(s, x, 1.98, 1.90, 0.06, fill=col, line=None, radius=0.5)
        add_text(s, x + 0.12, 2.08, 1.65, 0.24, title, size=9.8, color=NAVY, bold=True)
        add_text(s, x + 0.12, 2.34, 1.65, 0.2, sub, size=8, color=SLATE)

    # router
    add_rect(s, 2.35, 3.12, 3.35, 1.40, fill=WHITE, line=NAVY, radius=0.05, line_w=1.3)
    add_rect(s, 2.35, 3.12, 3.35, 0.08, fill=AMBER, line=None, radius=0.5)
    add_text(s, 2.52, 3.28, 3.0, 0.26, "Router MikroTik", size=11.5, color=NAVY, bold=True)
    add_text(s, 2.52, 3.58, 3.0, 0.78,
             "PCC statis 1:1:1 · mangle\nrouting-mark → gateway\nNAT/conntrack",
             size=9.2, color=SLATE, line_spacing=1.18)

    # no control plane box
    add_rect(s, 6.35, 3.12, 1.95, 1.40, fill=AMBER_PALE, line=AMBER, radius=0.05, dash=MSO_LINE_DASH_STYLE.DASH)
    add_text(s, 6.48, 3.42, 1.70, 0.7, "Tidak ada\ncontrol plane", size=10, color=AMBER_DARK,
             bold=True, align=PP_ALIGN.CENTER, line_spacing=1.1)

    # switch + clients
    add_rect(s, 2.85, 4.92, 2.35, 0.56, fill=WHITE, line=LINE, radius=0.10)
    add_text(s, 2.95, 5.04, 2.15, 0.25, "Switch client", size=9, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER)
    add_rect(s, 3.05, 5.82, 1.95, 0.50, fill=NAVY, line=None, radius=0.5)
    add_text(s, 3.15, 5.93, 1.75, 0.22, "Pelanggan", size=8.5, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER)

    for _, _, x, col in isps:
        add_arrow(s, x + 0.95, 2.64, 3.55, 3.12, color=col, width=1.3)
    add_arrow(s, 4.02, 4.52, 4.02, 4.92, color=TEAL, width=1.5)
    add_arrow(s, 4.02, 5.48, 4.02, 5.82, color=TEAL, width=1.5)

    # right column
    x = 8.95
    add_text(s, x, 1.70, 3.7, 0.28, "Cara kerja", size=12, color=NAVY, bold=True)
    steps = [
        ("Koneksi baru di-hash", "PCC memilih bucket berdasarkan src/dst/port."),
        ("Bucket → routing mark", "Mangle menandai koneksi ke gateway tujuan."),
        ("Koneksi lama tetap", "Conntrack menahan koneksi pada jalur awal."),
        ("Rasio diubah manual", "Operator menyesuaikan saat gangguan terasa."),
    ]
    yy = 2.10
    for i, (t, d) in enumerate(steps):
        add_badge(s, x, yy + 0.02, 0.26, str(i + 1), fill=AMBER, size=8.5)
        add_text(s, x + 0.38, yy - 0.02, 3.25, 0.24, t, size=10.5, color=NAVY, bold=True)
        add_text(s, x + 0.38, yy + 0.21, 3.25, 0.42, d, size=9, color=SLATE, line_spacing=1.05)
        yy += 0.87

    add_rect(s, x, 5.75, 3.45, 0.62, fill=AMBER_LIGHT, line=None, radius=0.08)
    add_text(s, x + 0.14, 5.85, 3.2, 0.4,
             "Keputusan hanya berubah saat operator turun tangan.",
             size=9.2, color=AMBER_DARK, bold=True, line_spacing=1.0)


def slide_limits(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Keterbatasan", "Lima titik buta arsitektur lama",
           "Bukan karena PCC buruk, tetapi karena keputusan rasio tidak punya model "
           "observasi dan biaya.", 5)

    cards = [
        ("01", "Buta degradasi parsial", "Failover hanya saat link down; loss dan RTT yang naik tidak memicu apa pun.",
         "Dampak: degradasi lolos tanpa alarm."),
        ("02", "Rasio tidak representatif", "1:1:1 statis tidak mengikuti kapasitas dan kualitas jalur yang berubah.",
         "Dampak: kapasitas tidak terpakai optimal."),
        ("03", "Shared risk diabaikan", "Memindahkan Starlink A ke B saat hujan justru memindahkan masalah.",
         "Dampak: evakuasi tidak benar-benar aman."),
        ("04", "Flapping & intervensi manual", "Perubahan rasio manual; otomasi naif dapat berosilasi.",
         "Dampak: osilasi dan intervensi berulang."),
        ("05", "Tanpa dasar biaya", "Kapasitas mahal bisa terbuang, atau jalur sehat justru overload.",
         "Dampak: biaya dan QoS tidak seimbang."),
    ]
    coords = [(M, 1.68), (4.68, 1.68), (8.76, 1.68), (M, 3.82), (4.68, 3.82)]
    for (num, t, d, impact), (x, y) in zip(cards, coords):
        card(s, x, y, 3.95, 1.92, accent=AMBER)
        add_text(s, x + 0.24, y + 0.16, 0.5, 0.25, num, size=9, color=AMBER_DARK, bold=True)
        add_text(s, x + 0.24, y + 0.44, 3.4, 0.3, t, size=12.5, color=NAVY, bold=True)
        add_text(s, x + 0.24, y + 0.86, 3.4, 0.55, d, size=9.8, color=SLATE, line_spacing=1.12)
        add_text(s, x + 0.24, y + 1.53, 3.4, 0.22, impact, size=8.4, color=AMBER_DARK,
                 bold=True, italic=True)

    # root cause card
    x, y = 8.76, 3.82
    add_rect(s, x, y, 3.95, 1.92, fill=NAVY, line=None, radius=0.06)
    add_text(s, x + 0.24, y + 0.16, 0.6, 0.25, "AKAR", size=9, color="9FD7D4", bold=True, spacing=120)
    add_text(s, x + 0.24, y + 0.44, 3.45, 0.3, "Tidak ada loop umpan balik", size=12.5,
             color=WHITE, bold=True)
    add_text(s, x + 0.24, y + 0.86, 3.45, 0.8,
             "Ukur → akumulasi bukti → putuskan → audit. Semuanya masih dilakukan manusia.",
             size=9.8, color="C9D6E2", line_spacing=1.12)

    add_text(s, M, 6.10, 12.1, 0.4,
             "Kebutuhan sebenarnya: keputusan rasio yang sadar bukti, sadar risiko, dan sadar biaya.",
             size=12.5, color=TEAL_DARK, bold=True, italic=True)


def slide_principles(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Prinsip desain", "Lima pergeseran menuju arsitektur baru",
           "Router tetap menjadi eksekutor; kecerdasan dipindahkan ke kontroler eksternal.", 6)

    # left dark panel
    add_rect(s, M, 1.68, 4.25, 4.95, fill=NAVY, line=None, radius=0.05)
    add_text(s, 0.88, 1.92, 3.6, 0.25, "PRINSIP UTAMA", size=9, color="9FD7D4",
             bold=True, spacing=120)
    add_text(s, 0.88, 2.30, 3.55, 1.75,
             "“Bukan mengganti router, tetapi menambah lapisan keputusan di atasnya.”",
             size=19, color=WHITE, bold=True, line_spacing=1.12)
    add_rect(s, 0.90, 4.10, 1.0, 0.04, fill=AMBER, line=None, shape=MSO_SHAPE.RECTANGLE)
    add_text(s, 0.88, 4.32, 3.5, 1.0,
             "Data plane tetap sederhana dan cepat. Kontroler yang mengamati, menghitung, "
             "dan menulis keputusan.",
             size=10.5, color="C9D6E2", line_spacing=1.18)

    # small amati -> putuskan -> eksekusi strip
    add_text(s, 0.88, 5.44, 3.5, 0.2, "ALUR KEPUTUSAN", size=7.5, color="9FD7D4",
             bold=True, spacing=100)
    steps = [("Amati", 0.95), ("Putuskan", 1.25), ("Eksekusi", 1.15)]
    sx = 0.88
    for i, (t, wd) in enumerate(steps):
        add_rect(s, sx, 5.76, wd, 0.34, fill="123344", line=TEAL, radius=0.5, line_w=0.8)
        add_text(s, sx + 0.04, 5.84, wd - 0.08, 0.2, t, size=7.4, color="CFE9E7",
                 bold=True, align=PP_ALIGN.CENTER)
        sx += wd
        if i < len(steps) - 1:
            add_arrow(s, sx + 0.03, 5.93, sx + 0.17, 5.93, color=TEAL, width=0.9)
            sx += 0.20

    items = [
        ("Pisahkan control plane", "Probe dan keputusan di server; forwarding tetap di router."),
        ("Ukur kualitas, bukan status", "Loss dan RTT per target, bukan hanya link up/down."),
        ("Akumulasi bukti", "CUSUM dua arah, bukan threshold satu sampel."),
        ("Turunkan ambang dari biaya", "C_salah, C_tunda, dan headroom H — bukan angka tebakan."),
        ("Ubah sesedikit mungkin", "Event-driven, kuantisasi bucket, tulis hanya bila berubah."),
    ]
    x = 5.20
    yy = 1.72
    for i, (t, d) in enumerate(items):
        add_badge(s, x, yy + 0.02, 0.34, str(i + 1), fill=TEAL, size=9.5)
        add_text(s, x + 0.48, yy - 0.02, 7.1, 0.28, t, size=12.5, color=NAVY, bold=True)
        add_text(s, x + 0.48, yy + 0.27, 7.1, 0.38, d, size=9.8, color=SLATE, line_spacing=1.05)
        yy += 0.97


def slide_new(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Arsitektur baru", "Kontroler di luar data plane, aktuator tetap di router",
           "Tiga jalur produksi, satu kontroler, dan gateway uji paralel untuk pembanding.", 7)

    # big diagram card
    add_rect(s, M, 1.62, 12.13, 5.05, fill=WHITE, line=LINE, radius=0.04)
    add_text(s, 0.86, 1.78, 4.0, 0.25, "ZONA PRODUKSI", size=8.5, color=TEAL_DARK,
             bold=True, spacing=110)
    add_text(s, 8.70, 1.78, 3.8, 0.25, "ZONA UJI", size=8.5, color=AMBER_DARK,
             bold=True, spacing=110)

    # production ISPs
    isps = [
        ("FO · IndiHome", "WAN1", 0.85, TEAL),
        ("Starlink A · LEO", "WAN2", 2.75, AMBER),
        ("Starlink B · LEO", "WAN3", 4.65, AMBER),
    ]
    for title, sub, x, col in isps:
        add_rect(s, x, 2.05, 1.75, 0.66, fill=WHITE, line=col, radius=0.10)
        add_rect(s, x, 2.05, 1.75, 0.06, fill=col, line=None, radius=0.5)
        add_text(s, x + 0.11, 2.14, 1.55, 0.24, title, size=9.0, color=NAVY, bold=True)
        add_text(s, x + 0.11, 2.40, 1.55, 0.2, sub, size=8, color=SLATE)

    # router
    add_rect(s, 2.30, 3.10, 3.00, 1.20, fill=WHITE, line=NAVY, radius=0.05, line_w=1.2)
    add_rect(s, 2.30, 3.10, 3.00, 0.07, fill=TEAL, line=None, radius=0.5)
    add_text(s, 2.46, 3.24, 2.7, 0.25, "Router MikroTik produksi", size=10.2, color=NAVY, bold=True)
    add_lines(s, 2.46, 3.52, 2.7, 0.70,
              ["PCC N bucket · NAT/conntrack",
               "routing-mark per bucket",
               "REST API untuk baca/tulis"],
              size=8.4, color=SLATE, line_spacing=1.15)

    # client switch + clients
    add_rect(s, 0.85, 4.38, 1.40, 0.55, fill=WHITE, line=LINE, radius=0.10)
    add_text(s, 0.92, 4.49, 1.26, 0.25, "Switch client", size=8.5, color=NAVY, bold=True,
             align=PP_ALIGN.CENTER)
    add_rect(s, 0.90, 5.15, 1.30, 0.48, fill=NAVY, line=None, radius=0.5)
    add_text(s, 0.98, 5.25, 1.14, 0.22, "Pelanggan", size=8.1, color=WHITE, bold=True,
             align=PP_ALIGN.CENTER)

    # controller
    add_rect(s, 2.30, 4.52, 3.00, 1.00, fill=INDIGO_PALE, line=INDIGO, radius=0.05, line_w=1.2)
    add_text(s, 2.46, 4.64, 2.7, 0.25, "Server Controller", size=10.2, color=INDIGO, bold=True)
    add_lines(s, 2.46, 4.90, 2.7, 0.55,
              ["probe · CUSUM · ambang sadar biaya keputusan",
               "peta aksi · Q_N · log keputusan"],
              size=8.1, color=SLATE, line_spacing=1.12)

    # test gateway + clients
    add_rect(s, 8.95, 3.10, 2.55, 1.05, fill=AMBER_PALE, line=AMBER, radius=0.05,
             dash=MSO_LINE_DASH_STYLE.DASH, line_w=1.2)
    add_text(s, 9.10, 3.22, 2.25, 0.25, "Gateway uji paralel", size=10.0, color=AMBER_DARK, bold=True)
    add_lines(s, 9.10, 3.48, 2.25, 0.58,
              ["MikroTik kedua / mini-PC nftables",
               "injeksi tc/netem"],
              size=8.1, color=SLATE, line_spacing=1.12)
    add_rect(s, 9.20, 4.38, 2.00, 0.55, fill=WHITE, line=AMBER, radius=0.10,
             dash=MSO_LINE_DASH_STYLE.DASH)
    add_text(s, 9.28, 4.49, 1.84, 0.25, "Klien uji", size=8.5, color=AMBER_DARK, bold=True,
             align=PP_ALIGN.CENTER)

    # data arrows
    add_arrow(s, 1.72, 2.71, 2.95, 3.10, color=TEAL, width=1.3)
    add_arrow(s, 3.62, 2.71, 3.80, 3.10, color=AMBER, width=1.3)
    add_arrow(s, 5.52, 2.71, 4.65, 3.10, color=AMBER, width=1.3)
    add_polyline_arrow(s, [(2.30, 3.70), (2.05, 3.70), (2.05, 4.65), (2.25, 4.65)],
                       color=TEAL, width=1.4)
    add_arrow(s, 1.55, 4.93, 1.55, 5.15, color=TEAL, width=1.4)

    # controller to router (probe/API)
    add_arrow(s, 3.80, 4.52, 3.80, 4.30, color=INDIGO, width=1.4,
              dash=MSO_LINE_DASH_STYLE.ROUND_DOT)
    add_text(s, 3.90, 4.32, 1.55, 0.2, "probe + API", size=7.4, color=INDIGO, bold=True)

    # backup LAN bus to test gateway
    add_polyline_arrow(s, [(6.42, 2.38), (7.72, 2.38), (7.72, 3.30), (8.95, 3.30)],
                       color=AMBER, width=0.9, dash=MSO_LINE_DASH_STYLE.DASH)
    add_text(s, 6.52, 2.12, 1.45, 0.18, "3× port LAN cadangan", size=7.0,
             color=AMBER_DARK, bold=True)

    add_arrow(s, 10.22, 4.15, 10.22, 4.38, color=AMBER, width=1.2,
              dash=MSO_LINE_DASH_STYLE.DASH)

    # notes in empty space
    add_text(s, 2.30, 5.66, 3.0, 0.38,
             "Kontroler membaca dan menulis via API.", size=7.8, color=INDIGO,
             bold=True, line_spacing=1.0)
    add_rect(s, 9.00, 5.12, 2.40, 0.46, fill=AMBER_PALE, line=None, radius=0.08)
    add_text(s, 9.10, 5.18, 2.22, 0.34,
             "Pembanding: k-sampel / CUSUM simetris", size=7.2, color=AMBER_DARK,
             bold=True, line_spacing=1.0)

    # legend
    add_arrow(s, 0.90, 6.38, 1.30, 6.38, color=TEAL, width=1.4)
    add_text(s, 1.38, 6.30, 1.5, 0.2, "data produksi", size=7.8, color=SLATE)
    add_arrow(s, 3.10, 6.38, 3.50, 6.38, color=INDIGO, width=1.4,
              dash=MSO_LINE_DASH_STYLE.ROUND_DOT)
    add_text(s, 3.58, 6.30, 1.7, 0.2, "probe / API", size=7.8, color=SLATE)
    add_arrow(s, 5.55, 6.38, 5.95, 6.38, color=AMBER, width=1.2,
              dash=MSO_LINE_DASH_STYLE.DASH)
    add_text(s, 6.03, 6.30, 2.1, 0.2, "jalur uji / port cadangan", size=7.8, color=SLATE)

    add_text(s, 8.95, 6.28, 3.55, 0.28,
             "Data plane tetap di router.", size=8.2, color=INDIGO, bold=True,
             align=PP_ALIGN.RIGHT)


def slide_components(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Komponen", "Enam komponen, satu alur keputusan",
           "Dari sampel probe hingga perubahan routing-mark yang dapat diaudit.", 8)

    comps = [
        ("01", "Probe aktif", "M = 2 target per jalur; Δt ≈ 2,3 s.", "Pola 00 / 10 / 01 / 11"),
        ("02", "Model observasi", "q₀ normal vs q₁ degradasi.", "LLR ℓ(yₖ) = ln q₁/q₀"),
        ("03", "CUSUM dua arah", "S↓ untuk degradasi, S↑ untuk pemulihan.", "Reset saat transisi status"),
        ("04", "Ambang sadar biaya keputusan", "h↓, h↑ = f(C_salah, C_tunda, D).", "Diperbarui dari headroom H"),
        ("05", "Peta aksi & kuantisasi", "Status → bobot target; N bucket.", "Minimal remap, event-driven"),
        ("06", "Aktuator & audit", "RouterOS routing-mark / nftables.", "Log keputusan + metrik"),
    ]
    coords = [(M, 1.68), (4.68, 1.68), (8.76, 1.68), (M, 3.86), (4.68, 3.86), (8.76, 3.86)]
    for (num, t, d, f), (x, y) in zip(comps, coords):
        card(s, x, y, 3.95, 1.98, accent=TEAL)
        add_text(s, x + 0.24, y + 0.16, 0.55, 0.25, num, size=9, color=TEAL_DARK, bold=True)
        add_text(s, x + 0.24, y + 0.44, 3.4, 0.3, t, size=12.5, color=NAVY, bold=True)
        add_text(s, x + 0.24, y + 0.84, 3.4, 0.35, d, size=9.8, color=SLATE, line_spacing=1.05)
        add_rect(s, x + 0.24, y + 1.40, 3.45, 0.36, fill=TEAL_PALE, line=None, radius=0.10)
        add_text(s, x + 0.34, y + 1.46, 3.25, 0.24, f, size=8.4, color=TEAL_DARK, bold=True,
                 font=MONO)

    add_text(s, M, 6.18, 12.1, 0.3,
             "Setiap komponen punya peran tunggal; tidak ada keputusan yang disembunyikan di router.",
             size=11, color=SLATE, italic=True)


def slide_loops(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Alur kerja", "Dua loop: cepat untuk status, lambat untuk biaya",
           "Loop cepat berjalan setiap siklus probe; loop lambat memperbarui parameter "
           "dari tabel koneksi.", 9)

    # fast band
    add_rect(s, M, 1.66, 12.13, 2.22, fill=TEAL_PALE, line=TEAL_LIGHT, radius=0.05)
    add_text(s, 0.86, 1.80, 5.0, 0.25, "LOOP CEPAT  ·  Δt ≈ 2,3 s", size=8.5,
             color=TEAL_DARK, bold=True, spacing=110)
    fast = [
        ("Probe M target", "routing per WAN"),
        ("Pola yₖ → LLR", "q₀ vs q₁"),
        ("CUSUM S↓ / S↑", "akumulasi bukti"),
        ("Transisi status", "SEHAT / DIEVAKUASI"),
        ("Peta aksi + Q_N", "bobot → bucket"),
        ("Tulis routing-mark", "hanya bila berubah"),
    ]
    x0, y0, w, h, gap = 0.86, 2.20, 1.70, 0.92, 0.20
    for i, (t, d) in enumerate(fast):
        x = x0 + i * (w + gap)
        add_rect(s, x, y0, w, h, fill=WHITE, line=TEAL, radius=0.08)
        add_text(s, x + 0.10, y0 + 0.13, w - 0.20, 0.38, t, size=8.8, color=NAVY, bold=True,
                 align=PP_ALIGN.CENTER, line_spacing=0.95)
        add_text(s, x + 0.10, y0 + 0.55, w - 0.20, 0.25, d, size=7.4, color=SLATE,
                 align=PP_ALIGN.CENTER)
        if i < len(fast) - 1:
            add_arrow(s, x + w, y0 + h / 2, x + w + gap, y0 + h / 2, color=TEAL, width=1.2)

    # loop back
    add_polyline_arrow(s, [(11.42, 3.12), (11.42, 3.38), (1.71, 3.38), (1.71, 3.12)],
                       color=TEAL, width=1.0, arrow_end=True)
    add_text(s, 5.9, 3.50, 1.2, 0.2, "siklus berikutnya", size=7.4, color=TEAL_DARK,
             align=PP_ALIGN.CENTER)

    # slow band
    add_rect(s, M, 4.18, 12.13, 2.10, fill=AMBER_PALE, line=AMBER_LIGHT, radius=0.05)
    add_text(s, 0.86, 4.32, 5.0, 0.25, "LOOP LAMBAT  ·  setiap beberapa menit", size=8.5,
             color=AMBER_DARK, bold=True, spacing=110)
    slow = [
        ("Tabel koneksi", "cuplikan per menit"),
        ("λ · umur · headroom H", "laju & komitmen"),
        ("Hitung ulang h↓ / h↑", "struktur biaya"),
        ("Update ambang", "loop cepat berikutnya"),
    ]
    x0, y0, w, h, gap = 0.86, 4.72, 2.10, 0.92, 0.26
    for i, (t, d) in enumerate(slow):
        x = x0 + i * (w + gap)
        add_rect(s, x, y0, w, h, fill=WHITE, line=AMBER, radius=0.08)
        add_text(s, x + 0.10, y0 + 0.15, w - 0.20, 0.3, t, size=9.2, color=NAVY, bold=True,
                 align=PP_ALIGN.CENTER)
        add_text(s, x + 0.10, y0 + 0.55, w - 0.20, 0.22, d, size=7.6, color=SLATE,
                 align=PP_ALIGN.CENTER)
        if i < len(slow) - 1:
            add_arrow(s, x + w, y0 + h / 2, x + w + gap, y0 + h / 2, color=AMBER, width=1.2)

    add_text(s, 10.28, 4.74, 1.95, 0.88,
             "Kalibrasi hanya dari data berlabel; parameter tidak ditebak.",
             size=7.8, color=AMBER_DARK, bold=True, line_spacing=1.05)

    add_text(s, 0.86, 5.82, 9.2, 0.26,
             "Output loop lambat: pasangan ambang (h↓, h↑) yang dipakai loop cepat pada siklus berikutnya.",
             size=8.2, color=AMBER_DARK, italic=True)

    add_text(s, M, 6.45, 12.1, 0.3,
             "Penulisan ke router bersifat event-driven: hanya saat pemetaan bucket benar-benar berubah.",
             size=10.5, color=SLATE, italic=True)


def slide_hysteresis(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Mekanisme kunci", "Histeresis asimetris: evakuasi cepat, pemulihan hati-hati",
           "Dua ambang, dua struktur biaya, satu zona penyangga untuk menahan flapping.", 10)

    # left state machine
    add_rect(s, M, 1.66, 6.55, 4.95, fill=WHITE, line=LINE, radius=0.05)
    add_text(s, 0.86, 1.84, 4.0, 0.25, "MESIN STATUS", size=8.5, color=TEAL_DARK,
             bold=True, spacing=110)

    add_pill(s, 1.05, 2.22, 1.70, 0.55, "SEHAT", fill=GREEN, color=WHITE, size=11)
    add_pill(s, 4.45, 2.22, 1.95, 0.55, "DIEVAKUASI", fill=AMBER, color=WHITE, size=11)

    # transition arrows
    add_arrow(s, 2.75, 2.38, 4.45, 2.38, color=AMBER, width=1.5)
    add_text(s, 2.80, 2.02, 1.65, 0.25, "S↓ ≥ h↓", size=8.5, color=AMBER_DARK, bold=True,
             font=MONO, align=PP_ALIGN.CENTER)
    add_text(s, 2.80, 2.62, 1.65, 0.22, "evakuasi cepat", size=7.8, color=SLATE,
             align=PP_ALIGN.CENTER)
    add_arrow(s, 4.45, 3.02, 2.75, 3.02, color=TEAL, width=1.5)
    add_text(s, 2.80, 3.08, 1.65, 0.25, "S↑ ≥ h↑", size=8.5, color=TEAL_DARK, bold=True,
             font=MONO, align=PP_ALIGN.CENTER)
    add_text(s, 2.80, 3.34, 1.65, 0.22, "pemulihan hati-hati", size=7.8, color=SLATE,
             align=PP_ALIGN.CENTER)

    # threshold gauge
    add_text(s, 0.90, 4.02, 2.0, 0.22, "Ambang statistik", size=8.2, color=SLATE, bold=True)
    gx0, gx1, gy = 1.00, 5.95, 4.55
    add_rect(s, gx0, gy, gx1 - gx0, 0.12, fill="E9EEF3", line=None, radius=0.5)
    add_rect(s, gx0 + 1.55, gy, 3.00, 0.12, fill=TEAL_LIGHT, line=None, radius=0.5)
    add_rect(s, gx0 + 1.53, gy - 0.10, 0.05, 0.32, fill=AMBER, line=None, shape=MSO_SHAPE.RECTANGLE)
    add_rect(s, gx0 + 4.50, gy - 0.10, 0.05, 0.32, fill=TEAL, line=None, shape=MSO_SHAPE.RECTANGLE)
    add_text(s, gx0 + 1.10, gy + 0.18, 1.2, 0.2, "h↓", size=9, color=AMBER_DARK, bold=True,
             font=MONO)
    add_text(s, gx0 + 4.20, gy + 0.18, 1.2, 0.2, "h↑", size=9, color=TEAL_DARK, bold=True,
             font=MONO)
    add_text(s, gx0 + 2.15, gy + 0.18, 2.1, 0.2, "zona penyangga", size=8, color=SLATE,
             align=PP_ALIGN.CENTER)
    add_text(s, 0.90, 4.95, 5.85, 0.55,
             "Selama kedua statistik berada di bawah ambangnya, status terakhir dipertahankan.",
             size=9.2, color=SLATE, line_spacing=1.05)
    add_rect(s, 0.90, 5.62, 3.55, 0.42, fill=TEAL_PALE, line=None, radius=0.10)
    add_text(s, 1.02, 5.70, 3.3, 0.24, "h↑ = m · h↓   dengan m > 1", size=9.5, color=TEAL_DARK,
             bold=True, font=MONO)

    # right cost cards
    x, w = 7.40, 5.30
    add_rect(s, x, 1.66, w, 1.72, fill=AMBER_PALE, line=AMBER_LIGHT, radius=0.06)
    add_text(s, x + 0.20, 1.80, 4.9, 0.25, "EVAKUASI  ·  SEHAT → DIEVAKUASI", size=8.5,
             color=AMBER_DARK, bold=True, spacing=80)
    add_text(s, x + 0.20, 2.10, 4.9, 0.28, "C_salah: kapasitas sehat menganggur", size=10.2,
             color=NAVY, bold=True)
    add_text(s, x + 0.20, 2.40, 4.9, 0.28, "C_tunda: koneksi baru ke jalur buruk", size=10.2,
             color=NAVY, bold=True)
    add_text(s, x + 0.20, 2.78, 4.9, 0.45,
             "Headroom besar → false alarm murah → h↓ rendah, evakuasi cepat.",
             size=8.8, color=AMBER_DARK, line_spacing=1.05)

    add_rect(s, x, 3.55, w, 1.72, fill=TEAL_PALE, line=TEAL_LIGHT, radius=0.06)
    add_text(s, x + 0.20, 3.69, 4.9, 0.25, "PEMULIHAN  ·  DIEVAKUASI → SEHAT", size=8.5,
             color=TEAL_DARK, bold=True, spacing=80)
    add_text(s, x + 0.20, 3.99, 4.9, 0.28, "C_salah: koneksi tertambat di jalur buruk", size=10.2,
             color=NAVY, bold=True)
    add_text(s, x + 0.20, 4.29, 4.9, 0.28, "C_tunda: kapasitas sehat tertahan", size=10.2,
             color=NAVY, bold=True)
    add_text(s, x + 0.20, 4.67, 4.9, 0.45,
             "Headroom langka → asimetri mengecil → pemulihan tidak terlalu konservatif.",
             size=8.8, color=TEAL_DARK, line_spacing=1.05)

    add_rect(s, x, 5.45, w, 0.62, fill=NAVY, line=None, radius=0.08)
    add_text(s, x + 0.18, 5.53, w - 0.36, 0.42,
             "h↓, h↑ = f(C_salah, C_tunda, D)   ·   diperbarui pada loop lambat",
             size=8.8, color=WHITE, bold=True, font=MONO, align=PP_ALIGN.CENTER)


def slide_compare(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Perbandingan", "Apa yang berubah, dan mengapa itu penting",
           "Sepuluh dimensi keputusan: dari konfigurasi statis ke kebijakan adaptif "
           "yang dapat diaudit.", 11)

    rows = [
        ("Sumber keputusan", "Konfigurasi statis; tanpa umpan balik kualitas", "Probe aktif + statistik koneksi + log"),
        ("Pemicu perubahan", "Link putus atau operator turun tangan", "Bukti CUSUM cukup (Δt ≈ 2,3 s)"),
        ("Bentuk keputusan", "Rasio tetap 1:1:1", "Bobot per bucket; hanya koneksi baru"),
        ("Degradasi parsial", "Tidak terdeteksi", "Loss & RTT per target probe"),
        ("Risiko bersama", "Tidak dipertimbangkan", "Evakuasi Starlink → FO"),
        ("Flapping", "Rawan; bergantung pada operator", "CUSUM + histeresis asimetris"),
        ("Dasar biaya", "Tidak eksplisit", "C_salah, C_tunda, headroom H"),
        ("Perubahan config", "Manual, menyentuh seluruh router", "Event-driven, minimal remap"),
        ("Peran operator", "Intervensi rutin", "Supervisi + rollback"),
        ("Audit", "Log router terbatas", "Log keputusan + basis data metrik"),
    ]
    nrows, ncols = len(rows) + 1, 3
    left, top, width, height = M, 1.62, 12.13, 5.12
    gf = s.shapes.add_table(nrows, ncols, Inches(left), Inches(top), Inches(width), Inches(height))
    table = gf.table
    table_no_style(table)
    table.first_row = False
    table.horz_banding = False
    widths = [3.00, 4.40, 4.73]
    for i, wd in enumerate(widths):
        table.columns[i].width = Inches(wd)
    table.rows[0].height = Inches(0.52)
    for i in range(1, nrows):
        table.rows[i].height = Inches(0.46)

    heads = ["Dimensi", "Arsitektur lama", "Arsitektur baru"]
    head_colors = [NAVY, AMBER, TEAL]
    for j, h in enumerate(heads):
        c = table.cell(0, j)
        cell_fill(c, head_colors[j])
        cell_text(c, h, size=10.5, color=WHITE, bold=True)

    for i, (dim, old, new) in enumerate(rows, start=1):
        fill = WHITE if i % 2 == 1 else "F1F5F9"
        c0, c1, c2 = table.cell(i, 0), table.cell(i, 1), table.cell(i, 2)
        for c in (c0, c1, c2):
            cell_fill(c, fill)
        cell_text(c0, dim, size=9.6, color=NAVY, bold=True)
        cell_text(c1, old, size=9.3, color="6B4A22")
        cell_text(c2, new, size=9.3, color="0B5E5E")

    add_text(s, M, 6.86, 12.1, 0.2,
             "Baseline: PCC statis 1:1:1.  Usulan: CUSUM dua arah + ambang asimetris sadar biaya keputusan.",
             size=8, color=MUTED, italic=True)


def slide_eval(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Pembuktian", "Membandingkan kebijakan pada input yang sama",
           "Lima skenario, tiga tingkat pengujian, empat metrik utama.", 12)

    rows = [
        ("A", "PCC statis 1:1:1", "Baseline eksisting"),
        ("B", "Histeresis k-sampel berturut", "Praktik failover umum"),
        ("C", "CUSUM simetris", "Ablasi efek asimetri"),
        ("D", "CUSUM asimetris sadar biaya keputusan", "Usulan"),
        ("E", "Starlink diminimalkan", "Acuan batas"),
    ]
    nrows, ncols = len(rows) + 1, 3
    left, top, width, height = M, 1.66, 7.25, 3.55
    gf = s.shapes.add_table(nrows, ncols, Inches(left), Inches(top), Inches(width), Inches(height))
    table = gf.table
    table_no_style(table)
    table.first_row = False
    table.horz_banding = False
    for i, wd in enumerate([0.85, 3.55, 2.85]):
        table.columns[i].width = Inches(wd)
    table.rows[0].height = Inches(0.46)
    for i in range(1, nrows):
        table.rows[i].height = Inches(0.60)
    for j, h in enumerate(["Skenario", "Kebijakan", "Peran"]):
        c = table.cell(0, j)
        cell_fill(c, NAVY)
        cell_text(c, h, size=9.8, color=WHITE, bold=True)
    for i, (sc, pol, role) in enumerate(rows, start=1):
        fill = WHITE if i % 2 == 1 else "F1F5F9"
        c0, c1, c2 = table.cell(i, 0), table.cell(i, 1), table.cell(i, 2)
        for c in (c0, c1, c2):
            cell_fill(c, fill)
        cell_text(c0, sc, size=10.5, color=TEAL_DARK if sc == "D" else NAVY, bold=True,
                  align=PP_ALIGN.CENTER)
        cell_text(c1, pol, size=9.4, color=NAVY, bold=(sc == "D"))
        cell_text(c2, role, size=9.2, color=SLATE)

    # right: test ladder
    x, w = 8.15, 4.55
    add_text(s, x, 1.68, w, 0.25, "TIGA TINGKAT PENGUJIAN", size=8.5, color=TEAL_DARK,
             bold=True, spacing=100)
    ladder = [
        ("1", "Replay offline", "Semua kebijakan pada rekaman probe identik."),
        ("2", "Gateway uji paralel", "Kondisi jalur sama; tanpa trafik pelanggan."),
        ("3", "Produksi", "Shadow mode, lalu fungsi tulis + rollback."),
    ]
    yy = 2.02
    for num, t, d in ladder:
        add_badge(s, x, yy + 0.02, 0.28, num, fill=TEAL, size=9)
        add_text(s, x + 0.40, yy - 0.02, w - 0.45, 0.24, t, size=10.5, color=NAVY, bold=True)
        add_text(s, x + 0.40, yy + 0.22, w - 0.45, 0.45, d, size=8.8, color=SLATE,
                 line_spacing=1.05)
        yy += 0.78

    # metrics
    add_text(s, x, 4.48, w, 0.25, "EMPAT METRIK", size=8.5, color=TEAL_DARK,
             bold=True, spacing=100)
    metrics = [("E", "paparan jalur"), ("U", "kapasitas tertahan"),
               ("F", "frekuensi rekonfigurasi"), ("QoS", "sisi klien")]
    mx, my = x, 4.80
    for i, (m, d) in enumerate(metrics):
        xx = mx + (i % 2) * 2.22
        yy2 = my + (i // 2) * 0.62
        add_rect(s, xx, yy2, 2.08, 0.52, fill=TEAL_PALE, line=TEAL_LIGHT, radius=0.08)
        add_text(s, xx + 0.10, yy2 + 0.07, 0.45, 0.22, m, size=10, color=TEAL_DARK, bold=True)
        add_text(s, xx + 0.50, yy2 + 0.08, 1.48, 0.22, d, size=7.8, color=SLATE)

    # hypotheses strip
    add_rect(s, M, 5.62, 7.25, 0.84, fill=WHITE, line=LINE, radius=0.06)
    add_text(s, 0.78, 5.72, 0.55, 0.22, "H1", size=9, color=TEAL_DARK, bold=True)
    add_text(s, 1.18, 5.72, 6.3, 0.3,
             "D vs B/C: E dan F lebih rendah pada U setara.", size=9.5, color=NAVY, bold=True)
    add_text(s, 0.78, 6.02, 0.55, 0.22, "H2", size=9, color=TEAL_DARK, bold=True)
    add_text(s, 1.18, 6.02, 6.3, 0.3,
             "D vs A: E lebih rendah dan QoS klien lebih baik.", size=9.5, color=NAVY, bold=True)

    add_text(s, 8.15, 6.20, 4.55, 0.45,
             "Taraf signifikansi α = 0,05; ukuran efek dan bootstrap 95% dilaporkan.",
             size=7.8, color=MUTED, italic=True, line_spacing=1.05)


def slide_evidence(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Sinyal awal", "CUSUM sudah menunjukkan kurva yang lebih baik",
           "Studi pendahuluan: trade-off paparan vs kapasitas tertahan pada rekaman "
           "13–17 November 2026.", 13)

    # image card
    add_rect(s, M, 1.66, 7.45, 4.78, fill=WHITE, line=LINE, radius=0.04)
    s.shapes.add_picture(os.path.join(ASSETS, "tradeoff.png"), Inches(0.72),
                         Inches(1.78), width=Inches(7.20))

    # right stats
    x, w = 8.35, 4.35
    stats = [
        ("2,39% → 0,26%", "paparan E saat rasio 1 → 4"),
        ("12,8 → 1,6 /jam", "perubahan status"),
        ("1,2% → 4,6%", "kapasitas tertahan U"),
    ]
    yy = 1.72
    for i, (v, d) in enumerate(stats):
        add_rect(s, x, yy, w, 0.74, fill=WHITE, line=LINE, radius=0.08)
        add_text(s, x + 0.16, yy + 0.10, w - 0.30, 0.30, v, size=13.5, color=TEAL_DARK, bold=True)
        add_text(s, x + 0.16, yy + 0.43, w - 0.30, 0.22, d, size=8.3, color=SLATE)
        yy += 0.86

    add_text(s, x, 4.42, w, 0.25, "Yang ditunjukkan data", size=9, color=NAVY, bold=True)
    add_text(s, x, 4.72, w, 0.95,
             "• CUSUM berada di bawah kurva k-sampel untuk setiap tingkat U.\n"
             "• Di atas rasio 4, perbaikan E hampir habis dan U melonjak 17,8%.",
             size=8.8, color=SLATE, line_spacing=1.18)
    add_rect(s, x, 5.82, w, 0.62, fill=TEAL_LIGHT, line=None, radius=0.08)
    add_text(s, x + 0.16, 5.91, w - 0.32, 0.42,
             "Karena itu ambang harus adaptif, bukan rasio tetap.",
             size=9.2, color=TEAL_DARK, bold=True, line_spacing=1.0)

    add_text(s, M, 6.55, 12.1, 0.22,
             "Sumber: studi pendahuluan proposal; parameter akan dikalibrasi ulang pada prototipe.",
             size=7.8, color=MUTED, italic=True)


def slide_risk(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    set_bg(s, BG)
    header(s, "Risiko & dampak", "Manfaat yang diharapkan, risiko yang dikendalikan",
           "Arsitektur baru harus lebih baik, tetapi juga aman diterapkan di jaringan produksi.", 14)

    # left impact
    add_text(s, M, 1.68, 5.7, 0.25, "DAMPAK YANG DIHARAPKAN", size=8.5, color=TEAL_DARK,
             bold=True, spacing=100)
    impacts = [
        ("H1", "E dan F turun pada U setara", "Dibanding histeresis k-sampel dan CUSUM simetris.",
         "Metrik: E dan F pada U setara."),
        ("H2", "E turun dan QoS klien membaik", "Dibanding baseline PCC statis 1:1:1.",
         "Metrik: E, U, dan QoS klien."),
        ("OPS", "Rasio tidak lagi ditebak", "Keputusan dapat dijelaskan dan diaudit.",
         "Metrik: audit log dan jumlah intervensi."),
    ]
    yy = 2.02
    for tag, t, d, metric in impacts:
        card(s, M, yy, 5.75, 1.18, accent=TEAL)
        add_pill(s, 0.80, yy + 0.16, 0.60, 0.28, tag, fill=TEAL, color=WHITE, size=7.5)
        add_text(s, 1.52, yy + 0.14, 4.55, 0.28, t, size=11, color=NAVY, bold=True)
        add_text(s, 1.52, yy + 0.47, 4.55, 0.30, d, size=8.8, color=SLATE, line_spacing=1.05)
        add_text(s, 1.52, yy + 0.82, 4.55, 0.24, metric, size=7.8, color=TEAL_DARK,
                 bold=True, italic=True)
        yy += 1.36

    # right risks
    x = 6.75
    add_text(s, x, 1.68, 5.9, 0.25, "RISIKO & MITIGASI", size=8.5, color=AMBER_DARK,
             bold=True, spacing=100)
    risks = [
        ("Controller / API gagal", "Shadow mode + rollback ke rasio nominal."),
        ("Keamanan API", "Management VLAN + pembatasan akses."),
        ("Kalibrasi bergeser", "Loop lambat + kalibrasi berlabel."),
        ("Cakupan terbatas", "3 WAN, 1 lokasi; generalisasi diuji lanjut."),
    ]
    yy = 2.02
    for i, (t, d) in enumerate(risks):
        add_rect(s, x, yy, 5.95, 0.94, fill=WHITE, line=LINE, radius=0.06)
        add_badge(s, x + 0.18, yy + 0.29, 0.28, str(i + 1), fill=AMBER, size=8)
        add_text(s, x + 0.58, yy + 0.15, 2.1, 0.25, t, size=9.8, color=NAVY, bold=True)
        add_text(s, x + 0.58, yy + 0.43, 5.1, 0.38, d, size=8.6, color=SLATE, line_spacing=1.02)
        yy += 1.06

    # success strip
    add_rect(s, M, 6.18, 12.1, 0.55, fill=NAVY, line=None, radius=0.08)
    add_text(s, 0.80, 6.29, 11.7, 0.3,
             "Kriteria sukses:  E ↓  ·  F ↓  ·  QoS tidak memburuk  ·  rollback tersedia",
             size=9.5, color=WHITE, bold=True, align=PP_ALIGN.CENTER)


def slide_closing(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.shapes.add_picture(os.path.join(ASSETS, "cover_bg.png"), 0, 0,
                         width=Inches(SW), height=Inches(SH))
    add_rect(s, 0.86, 0.82, 0.06, 2.9, fill=TEAL, line=None, radius=0.5)
    add_text(s, 1.08, 0.76, 6.0, 0.3, "PENUTUP", size=10, color="9FD7D4",
             bold=True, spacing=180)
    add_text(s, 1.08, 1.12, 8.5, 0.6, "Tiga hal yang perlu diingat", size=32,
             color=WHITE, bold=True)

    items = [
        ("01", "Lama: statis, reaktif, manual.",
         "PCC 1:1:1 tidak melihat degradasi parsial dan risiko bersama."),
        ("02", "Baru: kontroler + CUSUM + biaya.",
         "Bukti diakumulasi, ambang diturunkan dari biaya, keputusan dapat diaudit."),
        ("03", "Perubahan dijaga minimal.",
         "Hanya koneksi baru, hanya bucket yang berubah, dengan rollback."),
    ]
    yy = 2.20
    for num, t, d in items:
        add_text(s, 1.08, yy, 0.6, 0.3, num, size=10, color=AMBER, bold=True)
        add_text(s, 1.55, yy - 0.04, 7.5, 0.32, t, size=14, color=WHITE, bold=True)
        add_text(s, 1.55, yy + 0.30, 7.2, 0.45, d, size=9.8, color="B8C8D6", line_spacing=1.1)
        yy += 1.02

    add_text(s, 1.08, 5.72, 6.0, 0.45, "Terima kasih", size=26, color=WHITE, bold=True)
    add_text(s, 1.08, 6.22, 7.2, 0.55,
             "Kasmil Papalia · D082252011\nMagister Teknik Informatika · Universitas Hasanuddin",
             size=9.5, color="9FB0C0", line_spacing=1.2)

    # small old -> new motif
    add_text(s, 8.85, 5.55, 1.2, 0.22, "statis", size=8, color="D9A45C", bold=True,
             align=PP_ALIGN.CENTER)
    add_rect(s, 9.70, 5.86, 0.85, 0.05, fill="6F8494", line=None, shape=MSO_SHAPE.RECTANGLE)
    add_text(s, 10.55, 5.55, 1.2, 0.22, "adaptif", size=8, color="7FD1CB", bold=True,
             align=PP_ALIGN.CENTER)
    add_pill(s, 8.85, 5.86, 0.72, 0.30, "lama", fill="6B4A22", color=WHITE, size=7.5)
    add_pill(s, 10.62, 5.86, 0.80, 0.30, "baru", fill=TEAL, color=WHITE, size=7.5)

    add_rect(s, 11.55, 0.72, 1.02, 1.18, fill=WHITE, line=None, radius=0.10)
    s.shapes.add_picture(os.path.join(ASSETS, "logo_unhas.png"), Inches(11.67),
                         Inches(0.80), height=Inches(1.02))


def main():
    os.makedirs(ASSETS, exist_ok=True)
    cover = os.path.join(ASSETS, "cover_bg.png")
    if not os.path.exists(cover):
        print("generating cover background...")
        make_cover_bg(cover)

    prs = Presentation()
    prs.slide_width = Inches(SW)
    prs.slide_height = Inches(SH)

    slide_cover(prs)
    slide_summary(prs)
    slide_context(prs)
    slide_old(prs)
    slide_limits(prs)
    slide_principles(prs)
    slide_new(prs)
    slide_components(prs)
    slide_loops(prs)
    slide_hysteresis(prs)
    slide_compare(prs)
    slide_eval(prs)
    slide_evidence(prs)
    slide_risk(prs)
    slide_closing(prs)

    notes = [
        "Deck ini membandingkan arsitektur PCC statis yang berjalan saat ini dengan arsitektur yang diusulkan. Fokusnya bukan mengganti router, tetapi menambahkan lapisan keputusan yang mengamati kualitas jalur dan biaya.",
        "Ringkasan satu slide: arsitektur lama memakai rasio tetap dan bereaksi saat link putus; arsitektur baru memakai probe, CUSUM, dan ambang yang diturunkan dari biaya. Tiga pertanyaan di bagian bawah menjadi alur presentasi.",
        "Konteks jaringan: satu FO IndiHome dan dua Starlink LEO. FO relatif stabil; kedua Starlink dinamis dan saling berkorelasi. Karena NAT/conntrack, keputusan hanya memengaruhi koneksi baru.",
        "Arsitektur lama: koneksi baru di-hash ke bucket PCC, lalu ditandai routing-mark. Rasio 1:1:1 statis dan tidak ada control plane yang memantau kualitas jalur. Perubahan hanya terjadi saat operator turun tangan.",
        "Lima titik buta: degradasi parsial tidak terlihat, rasio tidak representatif, shared risk diabaikan, flapping/ intervensi manual, dan tidak ada dasar biaya. Akar masalahnya adalah tidak ada loop umpan balik yang utuh.",
        "Lima prinsip desain: pisahkan control plane, ukur kualitas, akumulasi bukti, turunkan ambang dari biaya, dan ubah sesedikit mungkin. Router tetap menjadi eksekutor; kontroler berada di luar data plane.",
        "Arsitektur baru: kontroler mengirim probe melalui setiap WAN, membaca statistik koneksi, dan menulis pemetaan bucket melalui API. Gateway uji paralel menjalankan kebijakan pembanding tanpa menyentuh trafik pelanggan.",
        "Enam komponen: probe, model observasi/LLR, CUSUM dua arah, ambang sadar biaya keputusan, peta aksi/kuantisasi, dan aktuator/audit. Setiap komponen punya peran tunggal sehingga keputusan dapat ditelusuri.",
        "Dua loop: loop cepat setiap siklus probe menentukan status jalur; loop lambat setiap beberapa menit memperbarui parameter biaya dan headroom. Penulisan ke router hanya dilakukan bila pemetaan berubah.",
        "Histeresis asimetris: evakuasi memakai ambang rendah karena false alarm relatif murah saat headroom besar; pemulihan memakai ambang tinggi karena koneksi yang tertambat di jalur buruk lebih mahal. Saat headroom langka, asimetri mengecil.",
        "Tabel perbandingan merangkum sepuluh dimensi: sumber keputusan, pemicu, bentuk keputusan, degradasi parsial, shared risk, flapping, dasar biaya, perubahan konfigurasi, peran operator, dan audit.",
        "Pembuktian memakai lima skenario A–E dan tiga tingkat pengujian: replay offline, gateway uji paralel, lalu produksi dengan shadow mode. Metrik utamanya E, U, F, dan QoS klien.",
        "Studi pendahuluan menunjukkan CUSUM berada di bawah kurva k-sampel. Saat rasio dinaikkan dari 1 ke 4, E turun dari 2,39% ke 0,26% dan perubahan status turun dari 12,8 ke 1,6 per jam, dengan U naik dari 1,2% ke 4,6%. Di atas rasio 4, U melonjak 17,8%.",
        "Manfaat yang diharapkan: H1 menurunkan E dan F pada U setara; H2 menurunkan E dan memperbaiki QoS klien. Risiko utama adalah kegagalan controller/API, keamanan API, pergeseran kalibrasi, dan cakupan yang terbatas; semuanya punya mitigasi.",
        "Tiga hal yang perlu diingat: arsitektur lama statis dan reaktif; arsitektur baru mengakumulasi bukti dan menurunkan ambang dari biaya; perubahan dijaga minimal dengan rollback. Terima kasih.",
    ]
    for slide, note in zip(prs.slides, notes):
        slide.notes_slide.notes_text_frame.text = note

    prs.save(OUT)
    print("saved:", OUT, "slides:", len(prs.slides))


if __name__ == "__main__":
    main()
