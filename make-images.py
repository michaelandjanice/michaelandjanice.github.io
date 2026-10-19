"""Render the save-the-date as images (4:5 and square, English and Korean) from the hero photo.

    python3 make-images.py          # needs Pillow:  pip install pillow

Output: images/save-the-date-{en,ko}-{4x5,square}.jpg
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = Path(__file__).resolve().parent
FONTS, OUT = HERE / "fonts", HERE / "images"
PHOTO = HERE / "photos" / "hero.jpg"
SIZES = {"4x5": (1080, 1350), "square": (1080, 1080)}
WHITE, BLUSH = (255, 255, 255), (243, 232, 226)

TEXT = {
    "en": dict(eyebrow="SAVE THE DATE", names=("Michael", "Janice"), date="Friday, October 8, 2027",
               place="San Francisco", serif="CormorantGaramond-Light.ttf", tracking=True),
    "ko": dict(eyebrow="초대합니다", names=("이진섭", "이나현"), date="2027년 10월 8일 금요일",
               place="샌프란시스코", serif="GowunBatang-Regular.ttf", tracking=False),
}


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(str(FONTS / name), size)


def cover(img: Image.Image, w: int, h: int, focus_y: float = 0.55) -> Image.Image:
    """Scale to cover w x h, cropping around a vertical focal point (0 = top, 1 = bottom)."""
    scale = max(w / img.width, h / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    x = (img.width - w) // 2
    y = min(max(round(img.height * focus_y - h / 2), 0), img.height - h)
    return img.crop((x, y, x + w, y + h))


def overlay(img: Image.Image) -> Image.Image:
    """Same gradient as the website hero: darker top and bottom, lighter middle, plus a touch of grain."""
    w, h = img.size
    mask = Image.new("L", (1, h))
    for y in range(h):
        t = y / (h - 1)
        a = 0.30 + (0.12 - 0.30) * (t / 0.5) if t < 0.5 else 0.12 + (0.55 - 0.12) * ((t - 0.5) / 0.5)
        mask.putpixel((0, y), round(a * 255))
    mask = mask.resize((w, h))
    img = Image.composite(Image.new("RGB", (w, h), (50, 30, 25)), img, mask)
    noise = Image.effect_noise((w, h), 14).convert("L")
    return Image.blend(img, Image.merge("RGB", (noise, noise, noise)), 0.05)


def width(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, tracking: float = 0) -> float:
    return sum(draw.textlength(c, font=f) for c in text) + tracking * (len(text) - 1)


def tracked(draw: ImageDraw.ImageDraw, cx: float, y: float, text: str, f: ImageFont.FreeTypeFont,
            tracking: float, fill=WHITE) -> None:
    x = cx - width(draw, text, f, tracking) / 2
    for c in text:
        draw.text((x, y), c, font=f, fill=fill)
        x += draw.textlength(c, font=f) + tracking


def render(lang: str, size_name: str) -> Path:
    t = TEXT[lang]
    w, h = SIZES[size_name]
    img = overlay(cover(ImageOps.exif_transpose(Image.open(PHOTO)).convert("RGB"), w, h, focus_y=0.58))
    draw = ImageDraw.Draw(img)
    cx = w / 2
    s = w / 1080  # scale factor if sizes change

    f_eyebrow = font(t["serif"] if lang == "ko" else "CormorantGaramond-Light.ttf", round((30 if lang == "ko" else 28) * s))
    f_names = font(t["serif"], round((104 if lang == "ko" else 122) * s))
    f_amp = font("CormorantGaramond-LightItalic.ttf", round((84 if lang == "ko" else 66) * s))
    f_date = font(t["serif"], round((44 if lang == "ko" else 48) * s))
    f_place = font("CormorantGaramond-LightItalic.ttf" if lang == "en" else t["serif"], round((38 if lang == "en" else 34) * s))

    # Vertical layout: the block sits a little above centre so it clears the couple low in the frame.
    y = h * (0.30 if size_name == "4x5" else 0.26)
    tracked(draw, cx, y, t["eyebrow"], f_eyebrow, tracking=(9 if t["tracking"] else 4) * s, fill=(255, 255, 255, 230))
    y += f_eyebrow.size * 1.9

    n1, n2 = t["names"]
    gap = 26 * s
    total = draw.textlength(n1, font=f_names) + gap + draw.textlength("&", font=f_amp) + gap + draw.textlength(n2, font=f_names)
    x = cx - total / 2
    base = y + f_names.size * 0.95  # align everything on a shared baseline
    draw.text((x, base), n1, font=f_names, fill=WHITE, anchor="ls")
    x += draw.textlength(n1, font=f_names) + gap
    draw.text((x, base - f_names.size * 0.06), "&", font=f_amp, fill=BLUSH, anchor="ls")
    x += draw.textlength("&", font=f_amp) + gap
    draw.text((x, base), n2, font=f_names, fill=WHITE, anchor="ls")
    y = base + f_names.size * 0.42

    tracked(draw, cx, y, t["date"], f_date, tracking=(3 if t["tracking"] else 1) * s)
    y += f_date.size * 1.5
    tracked(draw, cx, y, t["place"], f_place, tracking=(1 if t["tracking"] else 0.5) * s, fill=(255, 255, 255, 235))

    OUT.mkdir(exist_ok=True)
    out = OUT / f"save-the-date-{lang}-{size_name}.jpg"
    img.save(out, "JPEG", quality=92, optimize=True, progressive=True)
    return out


if __name__ == "__main__":
    for lang in TEXT:
        for size_name in SIZES:
            p = render(lang, size_name)
            print(p.relative_to(HERE), f"{p.stat().st_size // 1024}KB")
