"""Apply the All Steel attribution directly to public product photos."""

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "dist" / "assets" if (ROOT / "dist" / "assets").exists() else ROOT / "assets"
PHOTOS = (
    "caminhao-betoneira.jpg",
    "betoneira-pecas.jpg",
    "bomba-concreto.jpg",
    "motor-redutor.webp",
    "cabos-comando.webp",
    "guarnicao.webp",
    "rolo-apoio.webp",
)
FONT = next(
    (
        path
        for path in (
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        )
        if Path(path).exists()
    ),
    None,
)


def get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return ImageFont.truetype(FONT, size) if FONT else ImageFont.load_default(size=size)


def watermark(path: Path) -> None:
    source = Image.open(path).convert("RGBA")
    width, height = source.size
    hero = path.name == "caminhao-betoneira.jpg"
    caption = "© ALL STEEL" if hero else "© ALL STEEL SOLUTIONS"
    size = 18 if hero else max(16, round(min(width, height) * 0.078))
    font = get_font(size)
    box = ImageDraw.Draw(source).textbbox((0, 0), caption, font=font, stroke_width=1)
    text_width, text_height = box[2] - box[0], box[3] - box[1]
    text_layer = Image.new("RGBA", (text_width + 30, text_height + 30))
    draw = ImageDraw.Draw(text_layer)
    draw.text(
        (15 - box[0], 15 - box[1]),
        caption,
        font=font,
        fill=(255, 255, 255, 136),
        stroke_width=2,
        stroke_fill=(12, 22, 28, 165),
    )
    text_layer = text_layer.rotate(16 if hero else 22, expand=True, resample=Image.Resampling.BICUBIC)
    x = (width - text_layer.width) // 2
    y = (height - text_layer.height) // 2
    source.alpha_composite(text_layer, (x, y))

    label = "© All Steel Solutions"
    label_font = get_font(max(11, round(width * 0.027)))
    label_box = ImageDraw.Draw(source).textbbox((0, 0), label, font=label_font)
    label_width = label_box[2] - label_box[0]
    label_height = label_box[3] - label_box[1]
    padding = max(8, round(width * 0.018))
    label_x = width - label_width - padding * 2
    label_y = height - label_height - padding * 2
    badge = Image.new("RGBA", source.size)
    badge_draw = ImageDraw.Draw(badge)
    badge_draw.rounded_rectangle(
        (label_x - padding, label_y - padding, width - padding, height - padding),
        radius=4,
        fill=(12, 22, 28, 190),
    )
    badge_draw.text(
        (label_x, label_y - label_box[1]),
        label,
        font=label_font,
        fill=(244, 194, 21, 245),
    )
    source.alpha_composite(badge)

    if path.suffix == ".jpg":
        source.convert("RGB").save(path, format="JPEG", quality=92, subsampling=0)
    else:
        source.convert("RGB").save(path, format="WEBP", quality=92)


for filename in (sys.argv[1:] or PHOTOS):
    watermark(ASSETS / filename)
