#!/usr/bin/env python3
"""README visuals for dsh-finops-suite, derived from what the suite really does.

Every number, name and code below is read from the checked-in manifests:
`package.json` (four exact dependency pins), `cordis.patch.yml` (four insert
rows), `samples/quickstart/input/profile.json` (four synthetic rows) and
`src/members.mjs` (the three E_ codes). Nothing here is invented.

  hero 1440x576 (Pillow, zh/en x light/dark, four WebP files)
      Left column: kicker / wordmark / two value lines / one subtitle / one
      meta line / footer.  Right side: ONE PIN SET beam clamped onto a
      four-row rack (member id, exact version, resolution source), closed by a
      4/4 tally band, so the picture says "four members, one version set,
      read from three local files".

  flow 1100x660 (hand-written SVG, light/dark)
      Grammar: a STAIRCASE -- three ascending gates that a suite must climb
      before it may print its verdict, each step carrying the failure code it
      raises, ending on a tall verdict bench that shows 4/4 resolved.  Not a
      row of arrowed boxes: the steps are diagonally offset treads wired by
      short risers, and the bench is the landing platform.
      (1) manifests readable  -> E_SUITE_MANIFEST_MISSING
      (2) rows match the pins   -> E_SUITE_PATCH_MISMATCH
      (3) versions stay locked  -> E_SUITE_VERSION_MISMATCH

Run once:  python scripts/gen-readme-assets.py
Requires:  Pillow, and the Windows fonts msyh.ttc / msyhbd.ttc / consola*.ttf.
"""
from __future__ import annotations

import json
import os
import re
from html import escape

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs", "assets")
NAME = "dsh-finops-suite"

FONT_FILES = {
    "cjk": r"C:\Windows\Fonts\msyh.ttc",
    "cjk_bold": r"C:\Windows\Fonts\msyhbd.ttc",
    "mono": r"C:\Windows\Fonts\consola.ttf",
    "mono_bold": r"C:\Windows\Fonts\consolab.ttf",
}
for _kind, _path in FONT_FILES.items():
    if not os.path.exists(_path):
        raise SystemExit(f"FATAL: font missing: {_path}")
os.makedirs(OUT, exist_ok=True)

RADIUS = 20
SHADOW = 24

SKIN = {
    "light": dict(
        bg_from="#f9f6fd", bg_to="#e4eaf8",
        card="#ffffff", edge="#e6e2ef",
        text="#141419", sub="#4d5261", faint="#8f94a4",
        accent="#4B67B4", pill="#ece7f9", band="#f5f2fb",
        grid="#e7e4f0", warm="#b45309", warm_bg="#fdf3e9",
        ok="#15803d", ok_bg="#eaf6ee",
        shadow=(38, 30, 72), glow=34, dots="#e7e4f0", shade="#2b2440",
    ),
    "dark": dict(
        bg_from="#131a2a", bg_to="#0c1016",
        card="#1b2231", edge="#2e374b",
        text="#f0f3f9", sub="#a8b1c4", faint="#737b8d",
        accent="#8496f5", pill="#242d42", band="#202839",
        grid="#262f42", warm="#d9a441", warm_bg="#2a2216",
        ok="#3fb950", ok_bg="#16281c",
        shadow=(0, 0, 0), glow=48, dots="#1d2434", shade="#000000",
    ),
}


def font(size: int, kind: str = "cjk") -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_FILES[kind], int(round(size)))


def hx(color: str) -> tuple[int, int, int]:
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def gradient(w: int, h: int, top: str, bottom: str) -> Image.Image:
    base = Image.new("RGB", (w, h))
    draw = ImageDraw.Draw(base)
    a, b = hx(top), hx(bottom)
    for y in range(h):
        t = 0.12 * (y / h) + 0.88 * (y / h) ** 1.3
        draw.line([(0, y), (w, y)],
                  fill=tuple(int(p + (q - p) * t) for p, q in zip(a, b)))
    return base


def glow(img: Image.Image, cx: int, cy: int, r: int, color: str,
         alpha: int) -> Image.Image:
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    rgb = hx(color)
    for i in range(10, 0, -1):
        rr = r * i / 10
        d.ellipse([cx - rr, cy - rr, cx + rr, cy + rr],
                  fill=rgb + (int(alpha * (1 - i / 11)),))
    return Image.alpha_composite(img.convert("RGBA"),
                                 layer.filter(ImageFilter.GaussianBlur(26))
                                 ).convert("RGB")


def shadow_card(img: Image.Image, box: tuple[int, int, int, int], s: dict,
                radius: int = RADIUS, shadow: int = SHADOW,
                fill: str | None = None, edge: str | None = None,
                width: int = 2) -> Image.Image:
    x0, y0, x1, y1 = box
    sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
    sd = ImageDraw.Draw(sh)
    for i in range(shadow, 0, -2):
        sd.rounded_rectangle([x0 - i // 6, y0 + i // 2, x1 + i // 6, y1 + i],
                             radius=radius + i // 6,
                             fill=s["shadow"] + (int(10 * (1 - i / shadow)),))
    base = Image.alpha_composite(img.convert("RGBA"),
                                 sh.filter(ImageFilter.GaussianBlur(11)))
    d = ImageDraw.Draw(base)
    d.rounded_rectangle(box, radius=radius, fill=hx(fill or s["card"]),
                        outline=hx(edge or s["edge"]), width=width)
    return base.convert("RGB")


_MEASURE = ImageDraw.Draw(Image.new("RGB", (8, 8)))


def measure(text: str, size: float, kind: str) -> float:
    return _MEASURE.textlength(text, font=font(int(round(size)), kind))


def require_w(text: str, size: float, kind: str, max_w: float,
              what: str) -> None:
    got = measure(text, size, kind)
    if got > max_w + 0.4:
        raise SystemExit(f"FATAL: {what} overflows: {text!r} needs "
                         f"{got:.1f}px > {max_w:.0f}px")


def fit(text: str, kind: str, max_w: float, start: int, minimum: int) -> int:
    size = start
    while size > minimum and measure(text, size, kind) > max_w:
        size -= 1
    if measure(text, size, kind) > max_w:
        raise SystemExit(f"FATAL: {text!r} cannot fit {max_w}px even at "
                         f"{minimum}px")
    return size


def fit_lines(lines: list[str], kind: str, max_w: float, start: int,
              minimum: int) -> int:
    size = start
    while size > minimum and any(measure(l, size, kind) > max_w
                                 for l in lines):
        size -= 1
    if any(measure(l, size, kind) > max_w for l in lines):
        raise SystemExit(f"FATAL: value line cannot fit {max_w}px at "
                         f"{minimum}px")
    return size


def pill(img: Image.Image, x: int, top: int, label: str, s: dict,
         size: float = 15.5, kind: str = "cjk", height: int | None = None,
         pad: int = 15, fg: str | None = None, bg: str | None = None,
         edge: str | None = None) -> tuple[Image.Image, int]:
    f = font(size, kind)
    h = height or int(size * 2.15)
    w = measure(label, size, kind) + pad * 2
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([x, top, x + w, top + h], radius=h / 2,
                        fill=hx(bg or s["pill"]),
                        outline=hx(edge) if edge else None,
                        width=2 if edge else 0)
    d.text((x + pad, top + h / 2 + 1), label, font=f,
           fill=hx(fg or s["accent"]), anchor="lm")
    return img, int(w)


def check_mark(d: ImageDraw.ImageDraw, cx: int, cy: int, scale: float,
               color: str, width: int) -> None:
    d.line([(cx - 9 * scale, cy - 1 * scale),
            (cx - 2 * scale, cy + 6 * scale),
            (cx + 11 * scale, cy - 9 * scale)],
           fill=hx(color), width=width, joint="curve")


# ---------------------------------------------------------------------------
# suite data: the manifests are the only source of truth.
# ---------------------------------------------------------------------------
ERROR_CODES = (
    "E_SUITE_MANIFEST_MISSING",
    "E_SUITE_PATCH_MISMATCH",
    "E_SUITE_VERSION_MISMATCH",
)


def load_suite() -> dict:
    with open(os.path.join(ROOT, "package.json"), encoding="utf-8") as fh:
        pkg = json.load(fh)
    with open(os.path.join(ROOT, "cordis.patch.yml"), encoding="utf-8") as fh:
        patch_text = fh.read()
    with open(os.path.join(ROOT, "samples", "quickstart", "input",
                           "profile.json"), encoding="utf-8") as fh:
        profile = json.load(fh)
    with open(os.path.join(ROOT, "src", "members.mjs"), encoding="utf-8") as fh:
        members_src = fh.read()

    if pkg.get("name") != NAME:
        raise SystemExit("FATAL: package.json name changed")
    if pkg.get("dsh", {}).get("bundle", {}).get("patch") != "./cordis.patch.yml":
        raise SystemExit("FATAL: dsh.bundle.patch changed")

    rows: list[dict] = []
    current = None
    for line in patch_text.replace("\r\n", "\n").split("\n"):
        m = re.match(r"^\s*-\s+id:\s*([^\s#]+)\s*$", line)
        if m:
            current = {"id": m.group(1), "name": None}
            rows.append(current)
            continue
        m = re.match(r"^\s+name:\s*([^\s#]+)\s*$", line)
        if m and current is not None:
            current["name"] = m.group(1)

    deps = pkg.get("dependencies", {})
    if len(rows) != 4:
        raise SystemExit(f"FATAL: cordis.patch.yml has {len(rows)} members, "
                         "expected 4")
    if len(deps) != 4:
        raise SystemExit(f"FATAL: package.json has {len(deps)} deps, "
                         "expected 4")
    if {r["id"] for r in rows} != set(deps):
        raise SystemExit("FATAL: patch member set != dependency set")
    for row in rows:
        if row["name"] != row["id"]:
            raise SystemExit(f"FATAL: patch row {row['id']} lacks a matching "
                             "name")
    for code in ERROR_CODES:
        if code not in members_src:
            raise SystemExit(f"FATAL: {code} is not raised by src/members.mjs")

    sample_rows = {row["id"]: row for row in profile.get("rows", [])}
    members = []
    for row in rows:
        member = row["id"]
        version = deps[member]
        sample = sample_rows.get(member)
        if sample is None:
            raise SystemExit(f"FATAL: profile sample lacks {member}")
        if sample.get("version") != version:
            raise SystemExit(f"FATAL: profile sample pins {member} at "
                             f"{sample.get('version')}, manifest pins "
                             f"{version}")
        if sample.get("enabled") is not True:
            raise SystemExit(f"FATAL: profile sample does not enable {member}")
        members.append({"id": member, "version": version})
    return {
        "version": pkg["version"],
        "members": members,
        "profile": str(profile.get("profile", "synthetic")),
    }


HERO = {
    "zh": dict(
        kicker="DeepSeek Harness 插件 · 安装型套件",
        value=["一条命令装齐财务运营四件套", "四个成员锁在同一组精确版本"],
        sub="只安装，不处理单据：插四行、钉四版、核对 4/4 解析。",
        meta="4/4 resolved · 4 pins · 0 tools · network: false",
        foot="Apache-2.0 · 零工具面 · 不读单据 · 不联网",
        cmd_note="一条命令 · 4 个成员",
        beam="同一组精确版本 · ",
        rack_title="成员 · 精确版本",
        rack_note="由 cordis.patch.yml 插入",
        band_note="profile：4/4 行已启用",
        facts1="reads 3 files · writes 0 · network: false",
        facts2="由 samples/quickstart/run.mjs 离线核对",
        src="[manifest pin]",
        src_ok="profile: enabled",
        verdict="4/4 resolved",
        roles={
            "dsh-einvoice": "电子发票",
            "dsh-bankrec": "银行对账",
            "dsh-ap-three-way": "三单匹配",
            "dsh-travel-recon": "差旅对账",
        },
    ),
    "en": dict(
        kicker="DeepSeek Harness plugin · install-only suite",
        value=["Four members, one install", "four exact pins, one set"],
        sub="Install-only: insert four rows, pin four versions, verify 4/4.",
        meta="4/4 resolved · 4 pins · 0 tools · network: false",
        foot="Apache-2.0 · zero tool surface · no writes · no network",
        cmd_note="one command · 4 members",
        beam="ONE PIN SET · ",
        rack_title="MEMBERS · EXACT PINS",
        rack_note="inserted by cordis.patch.yml",
        band_note="profile: 4/4 rows enabled",
        facts1="reads 3 files · writes 0 · network: false",
        facts2="checked offline by samples/quickstart/run.mjs",
        src="[manifest pin]",
        src_ok="profile: enabled",
        verdict="4/4 resolved",
        roles={
            "dsh-einvoice": "e-invoicing",
            "dsh-bankrec": "bank reconciliation",
            "dsh-ap-three-way": "three-way match",
            "dsh-travel-recon": "travel reconciliation",
        },
    ),
}


# ---------------------------------------------------------------------------
# hero 1440x576
# ---------------------------------------------------------------------------
def hero(lang: str, skin: str, suite: dict) -> None:
    s = SKIN[skin]
    h = HERO[lang]
    members = suite["members"]
    W, H = 1440, 576
    img = gradient(W, H, s["bg_from"], s["bg_to"])
    img = glow(img, 1120, 70, 430, s["accent"], s["glow"])
    img = glow(img, 140, 552, 300, s["accent"], max(8, s["glow"] // 3))
    d = ImageDraw.Draw(img)
    m = 56
    col_w = 556

    # ---- left column --------------------------------------------------------
    img, _ = pill(img, m, 62, h["kicker"], s, size=15.5)
    d = ImageDraw.Draw(img)

    title_size = fit(NAME, "mono_bold", col_w, 58, 48)
    if title_size < 48:
        raise SystemExit("FATAL: hero title below 48px")
    d.text((m - 1, 124), NAME, font=font(title_size, "mono_bold"),
           fill=hx(s["text"]))
    require_w(NAME, title_size, "mono_bold", col_w, "hero title")

    value_size = fit_lines(h["value"], "cjk_bold", col_w, 38, 30)
    for i, line in enumerate(h["value"]):
        d.text((m, 228 + i * 54), line, font=font(value_size, "cjk_bold"),
               fill=hx(s["text"]))
        require_w(line, value_size, "cjk_bold", col_w, "hero value line")

    sub_size = fit(h["sub"], "cjk", col_w, 22, 18)
    require_w(h["sub"], sub_size, "cjk", col_w, "hero subtitle")
    d.text((m, 344), h["sub"], font=font(sub_size, "cjk"), fill=hx(s["sub"]))

    meta_size = fit(h["meta"], "mono", col_w, 18, 14)
    d.text((m + 1, 398), h["meta"], font=font(meta_size, "mono"),
           fill=hx(s["faint"]))

    d.line([m + 1, 452, m + col_w - 4, 452], fill=hx(s["grid"]), width=2)
    require_w(h["foot"], 16, "cjk", col_w, "hero footer")
    d.text((m + 1, 470), h["foot"], font=font(16, "cjk"), fill=hx(s["faint"]))

    # ---- right: install command --------------------------------------------
    cmd = "dsh plugin --profile <profile> add dsh-finops-suite"
    img, cmd_w = pill(img, 620, 54, cmd, s, size=13, kind="mono",
                      height=34, pad=15, fg=s["text"], bg=s["card"],
                      edge=s["edge"])
    d = ImageDraw.Draw(img)
    note_x = 620 + cmd_w + 14
    note_w = 1384 - note_x
    note_size = fit(h["cmd_note"], "cjk", note_w, 11, 9)
    require_w(h["cmd_note"], note_size, "cjk", note_w, "hero command note")
    d.text((1384, 71), h["cmd_note"], font=font(note_size, "cjk"),
           fill=hx(s["faint"]), anchor="rm")

    # ---- right: ONE PIN SET beam + the four-row rack ------------------------
    beam_x0, beam_x1 = 620, 648
    rack_x0, rack_x1 = 664, 1380
    rack_y0, rack_y1 = 126, 466
    beam_label = h["beam"] + suite["version"]
    require_w(beam_label, 11, "cjk", 260, "hero beam label")
    d.text((620, 100), beam_label, font=font(11, "cjk_bold"),
           fill=hx(s["accent"]))
    d.rounded_rectangle([beam_x0, rack_y0, beam_x1, rack_y1], radius=14,
                        fill=hx(s["pill"]), outline=hx(s["accent"]), width=2)
    # a version-set "clamp" glyph at the top of the beam
    cx = (beam_x0 + beam_x1) // 2
    d.line([cx - 5, rack_y0 + 22, cx + 5, rack_y0 + 22], fill=hx(s["accent"]),
           width=2)
    d.line([cx - 5, rack_y0 + 30, cx + 5, rack_y0 + 30], fill=hx(s["accent"]),
           width=2)

    img = shadow_card(img, (rack_x0, rack_y0, rack_x1, rack_y1), s,
                      radius=22, shadow=22)
    d = ImageDraw.Draw(img)
    require_w(h["rack_title"], 11, "cjk", 300, "hero rack title")
    d.text((rack_x0 + 18, rack_y0 + 18), h["rack_title"],
           font=font(11, "cjk_bold"), fill=hx(s["accent"]))
    require_w(h["rack_note"], 11, "cjk", 280, "hero rack note")
    d.text((rack_x1 - 18, rack_y0 + 18), h["rack_note"],
           font=font(11, "cjk"), fill=hx(s["faint"]), anchor="ra")
    d.line([rack_x0 + 18, rack_y0 + 36, rack_x1 - 18, rack_y0 + 36],
           fill=hx(s["grid"]), width=1)

    row_y0 = rack_y0 + 44
    row_h = 60
    for i, member in enumerate(members):
        top = row_y0 + i * row_h
        cy = top + row_h // 2
        # clamp tick from the beam into the row
        d.line([beam_x1 + 2, cy, rack_x0 + 6, cy], fill=hx(s["accent"]),
               width=2)
        d.ellipse([beam_x0 + 6, cy - 4, beam_x0 + 14, cy + 4],
                  fill=hx(s["accent"]))
        d.text((rack_x0 + 18, top + 16), f"{i + 1:02d}",
               font=font(10.5, "mono"), fill=hx(s["faint"]))
        require_w(member["id"], 15, "mono_bold", 300, "hero member id")
        d.text((rack_x0 + 50, top + 14), member["id"],
               font=font(15, "mono_bold"), fill=hx(s["text"]))
        require_w(member["version"], 17, "mono_bold", 200,
                  "hero member version")
        d.text((rack_x1 - 18, top + 12), member["version"],
               font=font(17, "mono_bold"), fill=hx(s["text"]), anchor="ra")
        # ledger leader between the id and its exact pin
        id_w = measure(member["id"], 15, "mono_bold")
        ver_w = measure(member["version"], 17, "mono_bold")
        lead_x0 = rack_x0 + 50 + id_w + 16
        lead_x1 = rack_x1 - 18 - ver_w - 16
        if lead_x1 > lead_x0 + 8:
            step = 6
            x = lead_x0
            while x < lead_x1:
                d.line([x, top + 21, min(x + 2, lead_x1), top + 21],
                       fill=hx(s["grid"]), width=2)
                x += step
        # second line: role, then the resolution source, then the profile row
        role = h["roles"][member["id"]]
        require_w(role, 11, "cjk", 260, "hero member role")
        d.text((rack_x0 + 50, top + 38), role, font=font(11, "cjk"),
               fill=hx(s["sub"]))
        ok_w = measure(h["src_ok"], 10.5, "mono")
        d.text((rack_x1 - 18 - ok_w, top + 38), h["src_ok"],
               font=font(10.5, "mono"), fill=hx(s["ok"]))
        d.text((rack_x1 - 18 - ok_w - 16, top + 38), h["src"],
               font=font(10.5, "mono"), fill=hx(s["faint"]), anchor="ra")
        if i < len(members) - 1:
            d.line([rack_x0 + 18, top + row_h - 2, rack_x1 - 18,
                    top + row_h - 2], fill=hx(s["grid"]), width=1)

    # ---- right: 4/4 tally band ---------------------------------------------
    band_y0 = row_y0 + 4 * row_h + 10
    band_h = 32
    d.rounded_rectangle([rack_x0 + 14, band_y0, rack_x1 - 14, band_y0 + band_h],
                        radius=12, fill=hx(s["ok_bg"]))
    dot_x = rack_x0 + 30
    for _ in range(4):
        d.ellipse([dot_x - 4, band_y0 + 12, dot_x + 4, band_y0 + 20],
                  fill=hx(s["ok"]))
        dot_x += 16
    require_w(h["verdict"], 12.5, "mono_bold", 150, "hero tally")
    d.text((dot_x + 10, band_y0 + 9), h["verdict"],
           font=font(12.5, "mono_bold"), fill=hx(s["ok"]))
    require_w(h["band_note"], 11, "cjk", 240, "hero band note")
    d.text((rack_x1 - 28, band_y0 + 10), h["band_note"],
           font=font(11, "cjk"), fill=hx(s["ok"]), anchor="ra")

    # ---- right: what was read, and what was not written ---------------------
    require_w(h["facts1"], 12, "mono", 700, "hero facts 1")
    d.text((rack_x0 + 2, 490), h["facts1"], font=font(12, "mono"),
           fill=hx(s["sub"]))
    require_w(h["facts2"], 12, "cjk", 700, "hero facts 2")
    d.text((rack_x0 + 2, 512), h["facts2"], font=font(12, "cjk"),
           fill=hx(s["sub"]))

    path = os.path.join(OUT, f"{NAME}-hero-{lang}-{skin}.webp")
    img.save(path, "WEBP", quality=90, method=6)


# ---------------------------------------------------------------------------
# flow 1100x660: staircase of three gates -> verdict bench
# ---------------------------------------------------------------------------
MONO = "Consolas,'Microsoft YaHei',ui-monospace,monospace"
SANS = ("'Microsoft YaHei','Segoe UI','PingFang SC','Noto Sans CJK SC',"
        "sans-serif")


def adv(text: str, size: float, mono: bool = True) -> float:
    total = 0.0
    for ch in text:
        total += size if ord(ch) > 0x2E80 else size * 0.55
    return total


def gate(code: str) -> str:
    if code not in ERROR_CODES:
        raise SystemExit(f"FATAL: unknown code {code}")
    return code


def flow_svg(skin: str, suite: dict) -> str:
    s = SKIN[skin]
    members = suite["members"]
    W, H = 1100, 660
    P: list[str] = []

    def text(x: float, y: float, value: str, size: float, fill: str,
             mono: bool = True, weight: int = 400, anchor: str = "start",
             ls: float | None = None, maxw: float | None = None,
             what: str = "text") -> None:
        width = adv(value, size, mono)
        if ls:
            width += ls * max(len(value) - 1, 0)
        if maxw is not None and width > maxw + 0.5:
            raise SystemExit(f"FATAL: {what} overflows: {value!r} needs "
                             f"{width:.1f}px > {maxw:.0f}px")
        fam = MONO if mono else SANS
        extra = f' font-weight="{weight}"' if weight != 400 else ""
        extra += f' letter-spacing="{ls}"' if ls else ""
        extra += f' text-anchor="{anchor}"' if anchor != "start" else ""
        P.append(f'<text x="{x:g}" y="{y:g}" fill="{fill}" '
                 f'font-family="{fam}" font-size="{size:g}"{extra}>'
                 f'{escape(value)}</text>')

    # ---- shell --------------------------------------------------------------
    P.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" '
             f'height="{H}" viewBox="0 0 {W} {H}" role="img" '
             f'aria-labelledby="title desc">')
    P.append('<title id="title">dsh-finops-suite structure: a three-step '
             'staircase to one 4/4 verdict</title>')
    desc = (
        "A staircase, not a row of arrowed boxes. Three ascending treads are "
        "the three gates the suite must pass, and the tall panel on the right "
        "is the landing platform where the verdict is printed. The cluster at "
        "the top left is the only input: package.json (four exact pins), "
        "cordis.patch.yml (four insert rows) and the synthetic "
        "samples/quickstart/input/profile.json (four enabled rows). Step 1 "
        "checks that both manifests and the bundle patch are readable; its "
        "failure code is E_SUITE_MANIFEST_MISSING. Step 2 checks that the "
        "patch rows and the dependency pins name the same four members, with "
        "id equal to name and no duplicates; its failure code is "
        "E_SUITE_PATCH_MISMATCH. Step 3 checks that every member resolves at "
        "its pin, whether the version comes from node_modules or from the "
        "manifest pin, and that the profile row carries the same version; its "
        "failure code is E_SUITE_VERSION_MISMATCH. The risers between treads "
        "are the only arrows: a gate is climbed, not skipped. The landing "
        "prints 4/4 resolved for " + ", ".join(m["id"] for m in members) +
        " at " + ", ".join(m["version"] for m in members) +
        ", with network false, zero writes, zero tools and zero config keys. "
        "Every name, version and count is read from the checked-in manifests.")
    P.append(f'<desc id="desc">{escape(desc)}</desc>')
    P.append('<defs>')
    P.append(f'<linearGradient id="bg" x1="0" y1="0" x2="0.2" y2="1">'
             f'<stop offset="0" stop-color="{s["bg_from"]}"/>'
             f'<stop offset="1" stop-color="{s["bg_to"]}"/></linearGradient>')
    P.append('<filter id="soft" x="-30%" y="-30%" width="160%" height="180%">'
             '<feDropShadow dx="0" dy="8" stdDeviation="10" '
             f'flood-color="{s["shade"]}" flood-opacity="0.13"/></filter>')
    P.append(f'<pattern id="dots" width="24" height="24" '
             f'patternUnits="userSpaceOnUse"><circle cx="1.2" cy="1.2" '
             f'r="1.2" fill="{s["dots"]}"/></pattern>')
    P.append(f'<marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" '
             f'markerWidth="6" markerHeight="6" orient="auto-start-reverse">'
             f'<path d="M0 0 L10 5 L0 10 z" fill="{s["accent"]}"/></marker>')
    P.append('</defs>')
    P.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
    P.append(f'<rect width="{W}" height="{H}" fill="url(#dots)" '
             'opacity="0.55"/>')

    # ---- header -------------------------------------------------------------
    kicker = "INSTALL-ONLY BUNDLE · 4 MEMBERS"
    kw = adv(kicker, 11) + len(kicker) + 28
    P.append(f'<rect x="44" y="28" width="{kw:.0f}" height="26" rx="13" '
             f'fill="{s["pill"]}"/>')
    text(58, 46, kicker, 11, s["accent"], weight=700, ls=1, maxw=kw - 28,
         what="kicker")

    text(44, 84, NAME, 30, s["text"], mono=True, weight=700, maxw=380,
         what="flow title")
    text(44, 108, "One install pins four finance members; the suite is done "
                  "only at 4/4.", 13.5, s["sub"], mono=False, maxw=700,
         what="flow subtitle")
    pill_label = "suite " + suite["version"]
    pw = adv(pill_label, 11) + 28
    P.append(f'<rect x="{1056 - pw:.0f}" y="28" width="{pw:.0f}" height="26" '
             f'rx="13" fill="{s["pill"]}"/>')
    text(1056 - pw + 14, 46, pill_label, 11, s["accent"], weight=700,
         maxw=pw - 26, what="suite pill")
    text(1056, 84, "3 gates · 4 members · 1 verdict", 11, s["faint"],
         anchor="end", maxw=300, what="header note")
    text(1056, 108, "reads 3 files · writes 0 · network: false", 11, s["faint"],
         anchor="end", maxw=300, what="header scope")
    P.append(f'<line x1="44" y1="126" x2="1056" y2="126" stroke="{s["grid"]}" '
             'stroke-width="1" opacity="0.8"/>')

    # ---- entry: the one install command and the only three files it reads ---
    P.append(f'<rect x="44" y="146" width="280" height="146" rx="14" '
             f'fill="{s["card"]}" stroke="{s["grid"]}" stroke-width="1"/>')
    text(58, 168, "ENTRY · ONE COMMAND", 11, s["accent"], weight=700,
         ls=1, maxw=180, what="entry label")
    text(310, 168, "READS 3 FILES", 11, s["faint"], anchor="end", maxw=100,
         what="entry reads")
    P.append(f'<line x1="50" y1="180" x2="50" y2="216" stroke="{s["accent"]}" '
             'stroke-width="2" opacity="0.45"/>')
    text(58, 194, "dsh plugin --profile <profile>", 11.5, s["text"], maxw=252,
         what="entry command 1")
    text(58, 214, "add dsh-finops-suite", 11.5, s["text"], maxw=252,
         what="entry command 2")
    P.append(f'<line x1="58" y1="226" x2="310" y2="226" stroke="{s["grid"]}" '
             'stroke-width="1"/>')
    text(58, 246, "package.json · 4 pins", 11, s["sub"], maxw=252,
         what="entry read 1")
    text(58, 264, "cordis.patch.yml · 4 insert rows", 11, s["sub"], maxw=252,
         what="entry read 2")
    text(58, 282, "profile.json · 4 rows (synthetic)", 11, s["sub"], maxw=252,
         what="entry read 3")
    P.append(f'<path d="M184 292 V452" stroke="{s["accent"]}" '
             'stroke-width="2" stroke-dasharray="5 6" opacity="0.8" '
             'marker-end="url(#arr)"/>')

    # ---- staircase: three treads -------------------------------------------
    cards = [
        dict(x=44, y=460, step="01", title="Manifests are readable",
             d1="package.json → dsh.bundle.patch",
             d2="cordis.patch.yml · 4 id/name rows",
             code=gate("E_SUITE_MANIFEST_MISSING")),
        dict(x=214, y=296, step="02", title="Rows match the pins",
             d1="patch {4 ids} == deps {4 pins}",
             d2="no duplicate id · id == name",
             code=gate("E_SUITE_PATCH_MISMATCH")),
        dict(x=384, y=132, step="03", title="Versions stay locked",
             d1="installed == pin, else manifest pin",
             d2="profile.json row == pin · enabled",
             code=gate("E_SUITE_VERSION_MISMATCH")),
    ]
    cw, ch = 330, 140
    for c in cards:
        x, y = c["x"], c["y"]
        P.append(f'<rect x="{x}" y="{y}" width="{cw}" height="{ch}" rx="18" '
                 f'fill="{s["card"]}" stroke="{s["edge"]}" '
                 'stroke-width="1.5" filter="url(#soft)"/>')
        P.append(f'<circle cx="{x + 32:g}" cy="{y + 29:g}" r="15" '
                 f'fill="{s["accent"]}"/>')
        text(x + 32, y + 34, c["step"], 13, "#ffffff" if skin == "light"
             else "#0c1016", weight=700, anchor="middle", maxw=24,
             what="step badge")
        text(x + 58, y + 34, "STEP " + c["step"] + " · GATE", 11,
             s["accent"], weight=700, ls=1.1, maxw=240, what="step kicker")
        text(x + 18, y + 71, c["title"], 15.5, s["text"], mono=False,
             weight=700, maxw=296, what="step title")
        text(x + 18, y + 94, c["d1"], 11.5, s["sub"], maxw=296,
             what="step detail 1")
        text(x + 18, y + 111, c["d2"], 11.5, s["sub"], maxw=296,
             what="step detail 2")
        cw_chip = adv(c["code"], 11) + 24
        P.append(f'<rect x="{x + 18}" y="{y + 117}" width="{cw_chip:.0f}" '
                 f'height="20" rx="10" fill="{s["warm_bg"]}" '
                 f'stroke="{s["warm"]}" stroke-width="1" opacity="0.95"/>')
        text(x + 30, y + 131, c["code"], 11, s["warm"], weight=700,
             maxw=cw_chip - 20, what="failure code")

    # risers: the only arrows in the figure — a gate is climbed, not skipped
    P.append(f'<path d="M374 458 V438" stroke="{s["accent"]}" stroke-width="2.4" '
             'marker-end="url(#arr)"/>')
    P.append(f'<path d="M544 294 V274" stroke="{s["accent"]}" stroke-width="2.4" '
             'marker-end="url(#arr)"/>')

    # ---- landing: the verdict bench ----------------------------------------
    bx0, by0, bx1, by1 = 740, 132, 1056, 600
    P.append(f'<path d="M714 202 H736" stroke="{s["accent"]}" '
             'stroke-width="2.4" marker-end="url(#arr)"/>')
    P.append(f'<rect x="{bx0}" y="{by0}" width="{bx1 - bx0}" '
             f'height="{by1 - by0}" rx="20" fill="{s["card"]}" '
             f'stroke="{s["edge"]}" stroke-width="1.5" filter="url(#soft)"/>')
    text(bx0 + 22, by0 + 30, "VERDICT · run.mjs", 11, s["accent"],
         weight=700, ls=1.1, maxw=200, what="bench kicker")
    text(bx1 - 22, by0 + 30, "exit 0", 11, s["ok"], anchor="end", maxw=80,
         what="bench exit")
    text(bx0 + 22, by0 + 84, "4/4", 44, s["ok"], weight=700, maxw=140,
         what="bench tally")
    text(bx0 + 22, by0 + 106, "members resolved", 11.5, s["faint"], mono=False,
         maxw=200, what="bench tally label")
    P.append(f'<line x1="{bx0 + 22}" y1="{by0 + 120}" x2="{bx1 - 22}" '
             f'y2="{by0 + 120}" stroke="{s["grid"]}" stroke-width="1"/>')

    for i, member in enumerate(members):
        top = by0 + 132 + i * 42
        P.append(f'<circle cx="{bx0 + 36:g}" cy="{top + 9:g}" r="8" '
                 f'fill="{s["ok_bg"]}" stroke="{s["ok"]}" stroke-width="1.5"/>')
        P.append(f'<path d="M{bx0 + 31:g} {top + 9:g} l4 4 l8 -9" fill="none" '
                 f'stroke="{s["ok"]}" stroke-width="2.2" stroke-linecap="round" '
                 'stroke-linejoin="round"/>')
        text(bx0 + 54, top + 13, member["id"], 13, s["text"], maxw=190,
             what="bench member id")
        text(bx1 - 22, top + 13, member["version"], 11, s["faint"],
             anchor="end", maxw=110, what="bench member version")
        text(bx0 + 54, top + 31, "manifest pin · profile enabled", 11,
             s["faint"], mono=False, maxw=230, what="bench member source")

    P.append(f'<line x1="{bx0 + 22}" y1="{by0 + 306}" x2="{bx1 - 22}" '
             f'y2="{by0 + 306}" stroke="{s["grid"]}" stroke-width="1"/>')
    facts = ("network: false", "writes: 0 · reads: 3 files",
             "tools: 0 · config keys: 0")
    for i, fact in enumerate(facts):
        text(bx0 + 22, by0 + 326 + i * 18, fact, 11, s["sub"], maxw=270,
             what="bench fact")
    text(bx0 + 22, by0 + 384, NAME + " " + suite["version"], 11, s["accent"],
         weight=700, maxw=280, what="bench suite version")
    text(bx0 + 22, by0 + 402, "profile: " + suite["profile"] + " · 4/4 rows",
         11, s["faint"], maxw=280, what="bench profile")
    P.append(f'<rect x="{bx0 + 14}" y="{by0 + 418}" width="{bx1 - bx0 - 28}" '
             f'height="28" rx="12" fill="{s["warm_bg"]}" '
             f'stroke="{s["warm"]}" stroke-width="1"/>')
    text(bx0 + 28, by0 + 436, "fail closed on any drift", 11, s["warm"],
         weight=700, maxw=270, what="bench fail-closed")

    # ---- footer -------------------------------------------------------------
    text(44, 626, "src/members.mjs · readManifest → inspectMembers", 11,
         s["faint"], maxw=380, what="footer left")
    text(520, 626, "4 inserts == 4 pins", 11, s["faint"], maxw=220,
         what="footer mid")
    text(1056, 626, NAME + " " + suite["version"] + " · 3 codes · 0 tools", 11,
         s["faint"], anchor="end", maxw=380, what="footer right")
    P.append('</svg>')
    return "\n".join(P) + "\n"


def main() -> None:
    suite = load_suite()
    for lang in ("zh", "en"):
        for skin in ("light", "dark"):
            hero(lang, skin, suite)
    for skin in ("light", "dark"):
        path = os.path.join(OUT, f"{NAME}-flow-v5-{skin}.svg")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(flow_svg(skin, suite))
    print("wrote 4 hero webp + 2 flow svg to docs/assets/")


if __name__ == "__main__":
    main()
