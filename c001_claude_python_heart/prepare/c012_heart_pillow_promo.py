from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1080
HEIGHT = 720
FRAMES = 42
POINT_COUNT = 1200
BACKGROUND = (7, 11, 24)


def load_font(size: int) -> ImageFont.ImageFont:
    for font_path in (
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ):
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def heart_position(t: float, scale: float) -> tuple[float, float]:
    x = 16 * math.sin(t) ** 3
    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )
    return x * scale, -y * scale


def build_particle_cloud() -> list[tuple[float, float, float, float]]:
    rng = random.Random(2026)
    particles: list[tuple[float, float, float, float]] = []
    for _ in range(POINT_COUNT):
        t = rng.random() * math.tau
        depth = rng.random() ** 0.52
        x, y = heart_position(t, 17.5 * depth)
        spread = 2.5 + 10 * (1 - depth)
        particles.append(
            (
                x + rng.uniform(-spread, spread),
                y + rng.uniform(-spread, spread),
                depth,
                rng.random() * math.tau,
            )
        )
    return particles


def draw_background() -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), BACKGROUND + (255,))
    draw = ImageDraw.Draw(image)
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        r = int(7 + 8 * ratio)
        g = int(11 + 5 * ratio)
        b = int(24 + 22 * ratio)
        draw.line((0, y, WIDTH, y), fill=(r, g, b, 255))
    return image


def draw_frame(particles: list[tuple[float, float, float, float]], frame: int) -> Image.Image:
    beat = 1 + 0.06 * math.sin(frame / FRAMES * math.tau)
    base = draw_background()
    fill_layer = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    dots = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    fill_draw = ImageDraw.Draw(fill_layer)
    glow_draw = ImageDraw.Draw(glow)
    dots_draw = ImageDraw.Draw(dots)

    center_x = WIDTH / 2
    center_y = HEIGHT / 2 - 40

    solid_points = []
    for i in range(240):
        t = i / 240 * math.tau
        x, y = heart_position(t, 17.4 * beat)
        solid_points.append((center_x + x, center_y + y))
    fill_draw.polygon(solid_points, fill=(245, 54, 135, 118))
    fill_layer = fill_layer.filter(ImageFilter.GaussianBlur(2))

    for index, (x, y, depth, phase) in enumerate(particles):
        shimmer = math.sin(frame * 0.22 + phase + index * 0.013)
        px = center_x + x * beat + shimmer * (1 + 2.8 * (1 - depth))
        py = center_y + y * beat + math.cos(frame * 0.18 + phase) * 1.4
        radius = 1.2 + depth * 3.2
        alpha = 120 + int(105 * depth)
        red = 235 + int(20 * depth)
        green = 55 + int(52 * depth)
        blue = 135 + int(70 * depth)
        color = (red, green, blue, alpha)
        dots_draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=color)
        glow_draw.ellipse((px - 8, py - 8, px + 8, py + 8), fill=(255, 60, 150, 26))

    outer_glow = fill_layer.filter(ImageFilter.GaussianBlur(24))
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    base.alpha_composite(outer_glow)
    base.alpha_composite(fill_layer)
    base.alpha_composite(glow)
    base.alpha_composite(dots)

    draw = ImageDraw.Draw(base)
    title_font = load_font(42)
    subtitle_font = load_font(30)
    small_font = load_font(22)
    draw.text((WIDTH / 2, 70), "Claude + Python 爱心动画", fill=(255, 238, 246, 255), anchor="mm", font=title_font)
    draw.text((WIDTH / 2, HEIGHT - 96), "用 AI 把第一行代码变成看得见的作品", fill=(185, 220, 255, 245), anchor="mm", font=subtitle_font)
    draw.text((WIDTH / 2, HEIGHT - 50), "大鹏AI教育", fill=(120, 245, 230, 230), anchor="mm", font=small_font)
    return base.convert("P", palette=Image.ADAPTIVE)


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    particles = build_particle_cloud()
    frames = [draw_frame(particles, frame) for frame in range(FRAMES)]
    gif_path = output_dir / "c012_claude_python_heart_promo.gif"
    cover_path = output_dir / "c012_claude_python_heart_promo.png"
    frames[0].save(cover_path)
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=50,
        loop=0,
        optimize=True,
    )
    print("Saved:", gif_path)
    print("Saved:", cover_path)


if __name__ == "__main__":
    main()
