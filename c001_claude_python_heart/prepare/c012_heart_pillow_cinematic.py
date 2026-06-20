from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


WIDTH = 1280
HEIGHT = 720
FRAMES = 56
HEART_POINTS = 1550
SPARKS = 95
BG_TOP = (5, 8, 23)
BG_BOTTOM = (21, 12, 46)


def load_font(size: int) -> ImageFont.ImageFont:
    for font_path in (
        Path("C:/Windows/Fonts/msyh.ttc"),
        Path("C:/Windows/Fonts/simhei.ttf"),
        Path("C:/Windows/Fonts/simsun.ttc"),
    ):
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size=size)
    return ImageFont.load_default()


def heart_xy(t: float, scale: float) -> tuple[float, float]:
    x = 16 * math.sin(t) ** 3
    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )
    return x * scale, -y * scale


def make_heart_particles() -> list[tuple[float, float, float, float]]:
    rng = random.Random(20260621)
    particles: list[tuple[float, float, float, float]] = []
    for _ in range(HEART_POINTS):
        t = rng.random() * math.tau
        layer = rng.random() ** 0.48
        x, y = heart_xy(t, 18.6 * layer)
        jitter = 1.2 + 9.2 * (1 - layer)
        particles.append(
            (
                x + rng.uniform(-jitter, jitter),
                y + rng.uniform(-jitter, jitter),
                layer,
                rng.random() * math.tau,
            )
        )
    return particles


def make_sparks() -> list[tuple[float, float, float, float]]:
    rng = random.Random(2026)
    sparks: list[tuple[float, float, float, float]] = []
    for _ in range(SPARKS):
        angle = rng.random() * math.tau
        radius = rng.uniform(250, 560)
        speed = rng.uniform(0.25, 1.15)
        size = rng.uniform(1.4, 4.2)
        sparks.append((angle, radius, speed, size))
    return sparks


def draw_background(frame: int, sparks: list[tuple[float, float, float, float]]) -> Image.Image:
    image = Image.new("RGBA", (WIDTH, HEIGHT), BG_TOP + (255,))
    draw = ImageDraw.Draw(image)

    for y in range(HEIGHT):
        ratio = y / HEIGHT
        wave = 0.04 * math.sin(frame * 0.08 + ratio * math.tau)
        r = int(BG_TOP[0] * (1 - ratio) + BG_BOTTOM[0] * ratio + wave * 16)
        g = int(BG_TOP[1] * (1 - ratio) + BG_BOTTOM[1] * ratio + wave * 10)
        b = int(BG_TOP[2] * (1 - ratio) + BG_BOTTOM[2] * ratio + wave * 24)
        draw.line((0, y, WIDTH, y), fill=(r, g, b, 255))

    cx, cy = WIDTH / 2, HEIGHT / 2
    for index, (angle, radius, speed, size) in enumerate(sparks):
        theta = angle + frame * 0.012 * speed
        pulse = 0.55 + 0.45 * math.sin(frame * 0.18 + index)
        x = cx + math.cos(theta) * radius
        y = cy + math.sin(theta * 0.84) * radius * 0.52
        alpha = int(55 + 105 * pulse)
        draw.ellipse((x - size, y - size, x + size, y + size), fill=(111, 230, 255, alpha))

    return image


def draw_neon_heart_shell(center_x: float, center_y: float, beat: float) -> Image.Image:
    shell = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    draw = ImageDraw.Draw(shell)
    outline = []
    for i in range(420):
        t = i / 420 * math.tau
        x, y = heart_xy(t, 18.9 * beat)
        outline.append((center_x + x, center_y + y))

    draw.polygon(outline, fill=(255, 42, 138, 118))
    draw.line(outline + [outline[0]], fill=(255, 115, 190, 210), width=4, joint="curve")

    halo = shell.filter(ImageFilter.GaussianBlur(26))
    bright = shell.filter(ImageFilter.GaussianBlur(5))
    merged = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    merged.alpha_composite(halo)
    merged.alpha_composite(bright)
    merged.alpha_composite(shell)
    return merged


def draw_frame(
    heart_particles: list[tuple[float, float, float, float]],
    sparks: list[tuple[float, float, float, float]],
    frame: int,
) -> Image.Image:
    beat = 1 + 0.055 * math.sin(frame / FRAMES * math.tau)
    center_x = WIDTH / 2
    center_y = HEIGHT / 2 - 28
    image = draw_background(frame, sparks)

    image.alpha_composite(draw_neon_heart_shell(center_x, center_y, beat))

    beams = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    beams_draw = ImageDraw.Draw(beams)
    for i in range(28):
        angle = i / 28 * math.tau + frame * 0.018
        length = 70 + 42 * math.sin(frame * 0.11 + i)
        x1 = center_x + math.cos(angle) * 112
        y1 = center_y + math.sin(angle) * 64
        x2 = center_x + math.cos(angle) * (112 + length)
        y2 = center_y + math.sin(angle) * (64 + length * 0.52)
        beams_draw.line((x1, y1, x2, y2), fill=(130, 235, 255, 42), width=2)
    beams = beams.filter(ImageFilter.GaussianBlur(2))
    image.alpha_composite(beams)

    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    dots = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    dots_draw = ImageDraw.Draw(dots)

    for index, (x, y, depth, phase) in enumerate(heart_particles):
        drift = math.sin(frame * 0.19 + phase + index * 0.009)
        px = center_x + x * beat + drift * (1.0 + 3.2 * (1 - depth))
        py = center_y + y * beat + math.cos(frame * 0.15 + phase) * 1.25
        radius = 1.1 + depth * 3.0
        alpha = 125 + int(105 * depth)
        color = (255, 54 + int(76 * depth), 147 + int(76 * depth), alpha)
        dots_draw.ellipse((px - radius, py - radius, px + radius, py + radius), fill=color)
        glow_draw.ellipse((px - 9, py - 9, px + 9, py + 9), fill=(255, 64, 160, 24))

    image.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
    image.alpha_composite(dots)

    ring = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    ring_draw = ImageDraw.Draw(ring)
    ring_radius = 262 + 8 * math.sin(frame / FRAMES * math.tau)
    ring_draw.ellipse(
        (
            center_x - ring_radius,
            center_y - ring_radius * 0.72,
            center_x + ring_radius,
            center_y + ring_radius * 0.72,
        ),
        outline=(95, 232, 255, 78),
        width=2,
    )
    image.alpha_composite(ring.filter(ImageFilter.GaussianBlur(1)))

    draw = ImageDraw.Draw(image)
    title_font = load_font(48)
    subtitle_font = load_font(31)
    small_font = load_font(23)
    draw.text((WIDTH / 2, 68), "Claude + Python 爱心动画", fill=(255, 240, 250, 255), anchor="mm", font=title_font)
    draw.text((WIDTH / 2, HEIGHT - 82), "从第一行代码，到可以传播的视觉作品", fill=(192, 225, 255, 246), anchor="mm", font=subtitle_font)
    draw.text((WIDTH / 2, HEIGHT - 38), "大鹏AI教育", fill=(122, 255, 235, 240), anchor="mm", font=small_font)
    return image.convert("P", palette=Image.ADAPTIVE)


def main() -> None:
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    heart_particles = make_heart_particles()
    sparks = make_sparks()
    frames = [draw_frame(heart_particles, sparks, frame) for frame in range(FRAMES)]
    gif_path = output_dir / "c012_claude_python_heart_cinematic.gif"
    cover_path = output_dir / "c012_claude_python_heart_cinematic.png"
    frames[0].save(cover_path)
    frames[0].save(
        gif_path,
        save_all=True,
        append_images=frames[1:],
        duration=45,
        loop=0,
        optimize=True,
    )
    print("Saved:", gif_path)
    print("Saved:", cover_path)


if __name__ == "__main__":
    main()
