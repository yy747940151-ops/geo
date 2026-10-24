#!/usr/bin/env python3
"""Render a deterministic 1200x675 PNG cover for the article. No third-party image URLs."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 675
im = Image.new("RGB", (W, H), "#f7faff")
d = ImageDraw.Draw(im)
NAVY = "#113d63"
BLUE = "#1679b7"
LIGHT = "#e4f3ff"
font_candidates = [
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc",
    "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
font_path = next((p for p in font_candidates if Path(p).is_file()), font_candidates[-1])
def font(size):
    return ImageFont.truetype(font_path, size)

d.rectangle((0, 0, W, 18), fill=BLUE)
d.rounded_rectangle((47, 70, 1154, 615), radius=26, fill="#ffffff", outline="#cbdff0", width=3)
d.rounded_rectangle((72, 100, 380, 156), radius=11, fill=LIGHT)
d.text((94, 109), "科学仪器企业 · 营销增长", font=font(25), fill=NAVY)
d.text((87, 202), "花大价钱参加仪器展会", font=font(55), fill=NAVY)
d.text((87, 294), "为什么最后没几单？", font=font(62), fill=BLUE)
d.rectangle((87, 393, 645, 399), fill="#7cc6eb")
d.text((90, 437), "客户加了不少，转化到底卡在哪一步", font=font(29), fill=NAVY)
d.rounded_rectangle((760, 180, 1100, 530), radius=16, fill="#e6f3fc", outline="#bbd9ee", width=4)
d.rectangle((790, 216, 1070, 256), fill=BLUE)
d.text((842, 220), "仪器展会", font=font(26), fill="white")
d.rectangle((794, 294, 922, 428), fill="white", outline="#7baacf", width=4)
d.rectangle((953, 299, 1057, 428), fill="#c9e6f7", outline="#7baacf", width=4)
for cx in [822, 914, 1025]:
    d.ellipse((cx-21, 450, cx+21, 492), fill=BLUE)
    d.rounded_rectangle((cx-29, 491, cx+29, 563), radius=13, fill=NAVY)
d.rounded_rectangle((89, 543, 617, 597), radius=11, fill=LIGHT)
d.text((115, 551), "展后转化才是真正的战场", font=font(28), fill=NAVY)
d.text((63, 630), "仪器信息网 · 科学仪器行业营销方法参考", font=font(20), fill=NAVY)

out = Path("images") / "expo-single-cover.png"
out.parent.mkdir(parents=True, exist_ok=True)
im.quantize(colors=16, method=Image.Quantize.FASTOCTREE).save(out, optimize=True)
print(f"Created {out} ({out.stat().st_size} bytes)")
