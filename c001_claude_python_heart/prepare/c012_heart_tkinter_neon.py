import math
import random
import tkinter as tk


WIDTH = 1000
HEIGHT = 680
PARTICLES = 900
SPARKS = 70


def heart_xy(t: float, scale: float) -> tuple[float, float]:
    x = 16 * math.sin(t) ** 3
    y = (
        13 * math.cos(t)
        - 5 * math.cos(2 * t)
        - 2 * math.cos(3 * t)
        - math.cos(4 * t)
    )
    return x * scale, -y * scale


def make_particles() -> list[dict[str, float]]:
    rng = random.Random(2026)
    points = []
    for _ in range(PARTICLES):
        t = rng.random() * math.tau
        layer = rng.random() ** 0.48
        x, y = heart_xy(t, 15.5 * layer)
        points.append(
            {
                "x": x + rng.uniform(-7, 7) * (1 - layer),
                "y": y + rng.uniform(-7, 7) * (1 - layer),
                "layer": layer,
                "phase": rng.random() * math.tau,
            }
        )
    return points


def make_sparks() -> list[dict[str, float]]:
    rng = random.Random(2027)
    return [
        {
            "angle": rng.random() * math.tau,
            "radius": rng.uniform(210, 470),
            "speed": rng.uniform(0.4, 1.3),
            "size": rng.uniform(1.0, 3.2),
        }
        for _ in range(SPARKS)
    ]


def rgb_to_hex(r: int, g: int, b: int) -> str:
    return f"#{r:02x}{g:02x}{b:02x}"


class NeonHeartApp:
    def __init__(self) -> None:
        self.root = tk.Tk()
        self.root.title("Claude + Python Tkinter Neon Heart")
        self.canvas = tk.Canvas(self.root, width=WIDTH, height=HEIGHT, bg="#070b18", highlightthickness=0)
        self.canvas.pack()
        self.particles = make_particles()
        self.sparks = make_sparks()
        self.frame = 0

    def draw_background(self) -> None:
        self.canvas.delete("all")
        for y in range(0, HEIGHT, 4):
            ratio = y / HEIGHT
            r = int(6 + 17 * ratio)
            g = int(9 + 5 * ratio)
            b = int(24 + 42 * ratio)
            self.canvas.create_rectangle(0, y, WIDTH, y + 4, fill=rgb_to_hex(r, g, b), outline="")

    def draw_shell(self, beat: float) -> None:
        cx = WIDTH / 2
        cy = HEIGHT / 2 - 20
        points = []
        for i in range(260):
            t = i / 260 * math.tau
            x, y = heart_xy(t, 15.9 * beat)
            points.extend((cx + x, cy + y))

        for width, color in ((18, "#2e123c"), (10, "#762064"), (5, "#ff78ce")):
            self.canvas.create_line(*points, fill=color, width=width, smooth=True)
        self.canvas.create_polygon(*points, fill="#e83d99", outline="#ff8bd8", width=2, smooth=True)

    def draw(self) -> None:
        self.draw_background()
        cx = WIDTH / 2
        cy = HEIGHT / 2 - 20
        beat = 1 + 0.065 * math.sin(self.frame * 0.11)

        for spark in self.sparks:
            angle = spark["angle"] + self.frame * 0.012 * spark["speed"]
            x = cx + math.cos(angle) * spark["radius"]
            y = cy + math.sin(angle * 0.84) * spark["radius"] * 0.52
            s = spark["size"]
            self.canvas.create_oval(x - s, y - s, x + s, y + s, fill="#55eaff", outline="")

        self.draw_shell(beat)

        for index, point in enumerate(self.particles):
            layer = point["layer"]
            drift = math.sin(self.frame * 0.16 + point["phase"] + index * 0.01)
            x = cx + point["x"] * beat + drift * (1.3 + 3 * (1 - layer))
            y = cy + point["y"] * beat + math.cos(self.frame * 0.13 + point["phase"]) * 1.2
            size = 1.2 + layer * 3.0
            color = "#ffb2ea" if layer > 0.72 else "#ff5db8"
            self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline="")

        self.canvas.create_text(WIDTH / 2, 62, text="Claude + Python 爱心动画", fill="#fff0fa", font=("Microsoft YaHei", 36))
        self.canvas.create_text(WIDTH / 2, HEIGHT - 76, text="不用复杂软件，也能做出吸引人的代码效果", fill="#d2e8ff", font=("Microsoft YaHei", 22))
        self.canvas.create_text(WIDTH / 2, HEIGHT - 38, text="大鹏AI教育", fill="#7dffe9", font=("Microsoft YaHei", 16))
        self.frame += 1
        self.root.after(33, self.draw)

    def run(self) -> None:
        self.draw()
        self.root.mainloop()


if __name__ == "__main__":
    NeonHeartApp().run()
