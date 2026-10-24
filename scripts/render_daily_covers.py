#!/usr/bin/env python3
"""Build permanent daily PNG covers from public archived article metadata.

No secrets, remote image dependencies or platform login state.
Use one filename per YYYY-MM-DD, so older posted article images don't break.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

WIDTH, HEIGHT = 1200, 675
ROOT = Path(__file__).resolve().parents[1]
ARTICLES = ROOT / "articles"
OUTPUT = ROOT / "images"

FONT_PATHS = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
FONT_PATH = next((path for path in FONT_PATHS if Path(path).exists()), None)
if FONT_PATH is None:
    raise SystemExit("No Chinese-capable TrueType font found")

def font(size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(FONT_PATH, size)

def fit_lines(draw: ImageDraw.ImageDraw, title: str, max_width: int, max_lines: int = 3):
    # Greedy width-based CJK and ASCII wrapping; shrink to fit.
    title = re.sub(r"\s+", " ", title).strip()
    for fontsize in (52, 49, 46, 43, 40):
        fnt = font(fontsize)
        lines, current = [], ""
        for character in title:
            candidate = current + character
            bbox = draw.textbbox((0, 0), candidate, font=fnt)
            if bbox[2] <= max_width or not current:
                current = candidate
            else:
                lines.append(current)
                current = character
        if current:
            lines.append(current)
        if len(lines) <= max_lines:
            return lines, fnt, fontsize
    return lines[:max_lines - 1] + [lines[max_lines - 1][:18] + "…"], font(40), 40

def create(meta: dict):
    date = meta.get("date", "")
    if not re.fullmatch(r"20\d{2}-\d{2}-\d{2}", date):
        raise ValueError("Invalid ISO date in article metadata")
    title = str(meta.get("title", "")).strip()
    if len(title) < 5:
        raise ValueError("Missing article title")
    im = Image.new("RGB", (WIDTH, HEIGHT), "#f6faff")
    d = ImageDraw.Draw(im)
    # Clear photo-free B2B editorial artwork, deliberately no invented instruments.
    d.rectangle((0, 0, WIDTH, 17), fill="#1982b7")
    d.rounded_rectangle((36, 55, 1161, 621), radius=29, fill="#ffffff", outline="#d4e5f5", width=3)
    d.rounded_rectangle((70, 94, 410, 150), radius=11, fill="#e1f1fb")
    d.text((95, 106), "科学仪器行业 · 营销观察", font=font(25), fill="#114b75")
    d.text((85, 167), date.replace("-", " / "), font=font(23), fill="#5a829f")
    lines, fnt, fontsize = fit_lines(d, title, 690)
    y = 217
    for line in lines:
        d.text((83, y), line, fill="#113b5c", font=fnt)
        y += fontsize + 22
    d.rounded_rectangle((85, 481, 663, 548), radius=14, fill="#e6f3fc")
    d.text((107, 495), "获客 · 品牌 · 销售转化 · AI营销", font=font(26), fill="#1d6797")
    # Neutral vector motif: instruments / sample flow / lead funnel.
    d.rounded_rectangle((802, 178, 1112, 525), radius=24, fill="#e7f4fc", outline="#b7d9ef", width=4)
    d.rounded_rectangle((839, 224, 1080, 287), radius=12, fill="#1b78ad")
    d.text((860, 231), "B2B 增长", fill="#ffffff", font=font(31))
    d.rounded_rectangle((845, 326, 915, 402), radius=13, fill="#ffffff", outline="#89b8d4", width=3)
    d.rounded_rectangle((934, 326, 1049, 402), radius=13, fill="#cde5f5", outline="#89b8d4", width=3)
    d.line((875, 418, 875, 472), fill="#5a9fc7", width=6)
    d.line((993, 418, 993, 472), fill="#5a9fc7", width=6)
    d.line((874, 467, 996, 467), fill="#5a9fc7", width=6)
    d.text((75, 635), "仪器信息网  |  科学仪器行业营销解决方案", font=font(21), fill="#456f8f")
    OUTPUT.mkdir(exist_ok=True)
    dst = OUTPUT / f"article-cover-{date}.png"
    im.quantize(colors=64, method=Image.Quantize.FASTOCTREE).save(dst, optimize=True)
    if dst.stat().st_size < 3000:
        raise RuntimeError("Unexpectedly small image produced")
    print("Rendered", dst.name, dst.stat().st_size, "bytes")

def main():
    sources = sorted(ARTICLES.glob("20??-??-??.json"))
    latest = ARTICLES / "latest.json"
    if latest.exists():
        sources.append(latest)
    seen = set()
    for path in sources:
        article = json.loads(path.read_text(encoding="utf-8"))
        date = article.get("date")
        if date in seen:
            continue
        create(article)
        seen.add(date)

if __name__ == "__main__":
    main()
