from __future__ import annotations

import math
import random
from pathlib import Path

import pygame
from PIL import Image


WIDTH = 1280
HEIGHT = 720
FPS = 60
PARTICLES = 1800
SPARKS = 160
PREVIEW_FRAMES = 72


def heart_xy(t: float, scale: float) -> tuple[float, float]:
    x = 16 * math.sin(t) ** 3
    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )
    return x * scale, -y * scale


def make_heart_particles() -> list[dict[str, float]]:
    rng = random.Random(20260621)
    items: list[dict[str, float]] = []
    for _ in range(PARTICLES):
        t = rng.random() * math.tau
        layer = rng.random() ** 0.46
        x, y = heart_xy(t, 19.2 * layer)
        items.append(
            {
                "x": x + rng.uniform(-8, 8) * (1 - layer),
                "y": y + rng.uniform(-8, 8) * (1 - layer),
                "layer": layer,
                "phase": rng.random() * math.tau,
                "twinkle": rng.uniform(0.7, 1.35),
            }
        )
    return items


def make_sparks() -> list[dict[str, float]]:
    rng = random.Random(2026)
    sparks: list[dict[str, float]] = []
    for _ in range(SPARKS):
        sparks.append(
            {
                "angle": rng.random() * math.tau,
                "radius": rng.uniform(230, 610),
                "speed": rng.uniform(0.35, 1.45),
                "size": rng.uniform(1.1, 3.8),
                "phase": rng.random() * math.tau,
            }
        )
    return sparks


def draw_text(surface: pygame.Surface, text: str, size: int, y: int, color: tuple[int, int, int]) -> None:
    font_path = "C:/Windows/Fonts/msyh.ttc"
    if not Path(font_path).exists():
        font_path = "C:/Windows/Fonts/simhei.ttf"
    font = pygame.font.Font(font_path if Path(font_path).exists() else None, size)
    image = font.render(text, True, color)
    rect = image.get_rect(center=(WIDTH // 2, y))
    surface.blit(image, rect)


def draw_gradient(surface: pygame.Surface, frame: int) -> None:
    for y in range(HEIGHT):
        ratio = y / HEIGHT
        wave = math.sin(frame * 0.025 + ratio * math.tau) * 8
        r = int(5 * (1 - ratio) + 22 * ratio + wave)
        g = int(9 * (1 - ratio) + 12 * ratio + wave * 0.4)
        b = int(25 * (1 - ratio) + 55 * ratio + wave * 1.2)
        pygame.draw.line(surface, (max(0, r), max(0, g), max(0, b)), (0, y), (WIDTH, y))


def draw_heart_shell(surface: pygame.Surface, center: tuple[int, int], beat: float) -> None:
    cx, cy = center
    points = []
    for i in range(420):
        t = i / 420 * math.tau
        x, y = heart_xy(t, 19.5 * beat)
        points.append((cx + x, cy + y))

    shell = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    pygame.draw.polygon(shell, (255, 42, 148, 126), points)
    pygame.draw.lines(shell, (255, 118, 205, 230), True, points, 5)
    glow1 = pygame.transform.smoothscale(shell, (WIDTH // 4, HEIGHT // 4))
    glow1 = pygame.transform.smoothscale(glow1, (WIDTH, HEIGHT))
    glow1.set_alpha(115)
    surface.blit(glow1, (0, 0), special_flags=pygame.BLEND_ADD)
    surface.blit(shell, (0, 0), special_flags=pygame.BLEND_PREMULTIPLIED)


def draw_scene(
    surface: pygame.Surface,
    heart_particles: list[dict[str, float]],
    sparks: list[dict[str, float]],
    frame: int,
) -> None:
    draw_gradient(surface, frame)
    center = (WIDTH // 2, HEIGHT // 2 - 24)
    cx, cy = center
    beat = 1 + 0.072 * math.sin(frame * 0.105)

    for spark in sparks:
        angle = spark["angle"] + frame * 0.012 * spark["speed"]
        radius = spark["radius"] + 16 * math.sin(frame * 0.035 + spark["phase"])
        x = cx + math.cos(angle) * radius
        y = cy + math.sin(angle * 0.84) * radius * 0.52
        alpha = int(80 + 145 * (0.5 + 0.5 * math.sin(frame * 0.11 + spark["phase"])))
        color = (80, 232, 255, alpha)
        size = spark["size"]
        dot = pygame.Surface((16, 16), pygame.SRCALPHA)
        pygame.draw.circle(dot, color, (8, 8), int(size))
        surface.blit(dot, (x - 8, y - 8), special_flags=pygame.BLEND_ADD)

    draw_heart_shell(surface, center, beat)

    particle_layer = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    for index, particle in enumerate(heart_particles):
        layer = particle["layer"]
        drift = math.sin(frame * 0.16 + particle["phase"] + index * 0.006)
        px = cx + particle["x"] * beat + drift * (1.5 + 3 * (1 - layer))
        py = cy + particle["y"] * beat + math.cos(frame * 0.13 + particle["phase"]) * 1.2
        pulse = 0.58 + 0.42 * math.sin(frame * 0.22 * particle["twinkle"] + particle["phase"])
        radius = max(1, int(1 + layer * 4 + pulse * 1.5))
        color = (
            255,
            int(62 + layer * 88),
            int(145 + layer * 86),
            int(132 + layer * 115),
        )
        pygame.draw.circle(particle_layer, color, (int(px), int(py)), radius)
    surface.blit(particle_layer, (0, 0), special_flags=pygame.BLEND_ADD)

    draw_text(surface, "Claude + Python 爱心动画", 54, 64, (255, 242, 250))
    draw_text(surface, "AI 编程课也可以一眼心动", 34, HEIGHT - 84, (202, 229, 255))
    draw_text(surface, "大鹏AI教育", 24, HEIGHT - 38, (126, 255, 235))


def surface_to_pil(surface: pygame.Surface) -> Image.Image:
    raw = pygame.image.tobytes(surface, "RGB")
    return Image.frombytes("RGB", surface.get_size(), raw)


def export_preview(heart_particles: list[dict[str, float]], sparks: list[dict[str, float]]) -> None:
    output_dir = Path(__file__).resolve().parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    pygame.init()
    pygame.font.init()
    surface = pygame.Surface((WIDTH, HEIGHT))
    frames: list[Image.Image] = []
    for frame in range(PREVIEW_FRAMES):
        draw_scene(surface, heart_particles, sparks, frame)
        frames.append(surface_to_pil(surface))

    cover_path = output_dir / "c012_claude_python_heart_pygame_neon.png"
    gif_path = output_dir / "c012_claude_python_heart_pygame_neon.gif"
    frames[0].save(cover_path)
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=42, loop=0, optimize=True)
    pygame.quit()
    print("Saved:", cover_path)
    print("Saved:", gif_path)


def run_live(heart_particles: list[dict[str, float]], sparks: list[dict[str, float]]) -> None:
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Claude + Python Neon Heart")
    clock = pygame.time.Clock()
    frame = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
        draw_scene(screen, heart_particles, sparks, frame)
        pygame.display.flip()
        frame += 1
        clock.tick(FPS)
    pygame.quit()


def main() -> None:
    heart_particles = make_heart_particles()
    sparks = make_sparks()
    run_live(heart_particles, sparks)


if __name__ == "__main__":
    main()
