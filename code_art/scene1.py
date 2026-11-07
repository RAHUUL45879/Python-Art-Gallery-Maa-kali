"""Mitratics code-art: Scene 1 / 100% drawn with Python.

No image or video assets are loaded. Every pixel originates from Pillow
shapes, curves, gradients and generated particles. The output is an MP4.

Run:
    python code_art/scene1.py
    python code_art/scene1.py --preview   # quick 1-second motion check

Requirements: Pillow>=10.4, imageio-ffmpeg>=0.5
"""

from __future__ import annotations

import argparse
import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

W, H = 432, 768
FPS = 20
DURATION = 7.6
TOTAL_FRAMES = int(FPS * DURATION)
CX, CY = W // 2, 364


def smoothstep(edge0: float, edge1: float, x: float) -> float:
    u = max(0.0, min(1.0, (x - edge0) / (edge1 - edge0)))
    return u * u * (3 - 2 * u)


def cubic(p0, p1, p2, p3, steps=45):
    """Sample a Bezier curve using Python maths (not an imported image)."""
    result = []
    for i in range(steps + 1):
        t = i / steps
        q = 1 - t
        result.append((
            round(q**3*p0[0] + 3*q*q*t*p1[0] + 3*q*t*t*p2[0] + t**3*p3[0]),
            round(q**3*p0[1] + 3*q*q*t*p1[1] + 3*q*t*t*p2[1] + t**3*p3[1]),
        ))
    return result


def path(*segments):
    out = []
    for segment in segments:
        c = cubic(*segment)
        out.extend(c if not out else c[1:])
    return out


def draw_partial(draw, coords, fraction, color, width):
    if fraction <= 0:
        return
    count = max(2, min(len(coords), round(fraction * len(coords))))
    draw.line(coords[:count], fill=color, width=width, joint='curve')


def make_background():
    """One-time per-pixel radial gradient created with Python, no pictures."""
    image = Image.new('RGB', (W, H))
    pixels = image.load()
    for y in range(H):
        for x in range(W):
            dx = (x - CX) / W
            dy = (y - CY - 10) / H
            warm = max(0, 1 - math.sqrt((dx*1.5)**2 + (dy*1.55)**2) * 2.1)
            horizon = max(0, 1 - abs(y - 585)/280) * 0.22
            n = (math.sin(x*0.052+y*0.034) + math.sin(x*0.018-y*0.025)) * 1.5
            pixels[x, y] = (
                int(max(0, 8 + 38*warm + 9*horizon + n)),
                int(max(0, 3 + 4*warm + n*0.25)),
                int(max(0, 7 + 7*warm + n*0.3)),
            )
    return image


BACKGROUND = make_background()
RNG = random.Random(26011)
PARTICLES = [
    (RNG.randrange(W), RNG.randrange(H), RNG.uniform(5, 29),
     RNG.uniform(0.6, 2.1), RNG.uniform(0, 2*math.pi))
    for _ in range(90)
]

# Branded letter geometry authored entirely with mathematical Bézier paths.
# No logo files, image overlays, or external video assets are read.
# The two long, mirrored ribbons create a genuinely balanced M monogram.
LEFT_RIBBON = path(
    ((104, 293), (116, 292), (138, 299), (152, 326)),
    ((152, 326), (180, 379), (134, 419), (119, 444)),
    ((119, 444), (106, 467), (124, 478), (144, 465)),
    ((144, 465), (167, 450), (192, 422), (216, 394)),
)
RIGHT_RIBBON = [(W-x, y) for x, y in LEFT_RIBBON]
LEFT_CREST = path(
    ((104, 293), (139, 284), (177, 321), (216, 364)),
)
RIGHT_CREST = [(W-x, y) for x, y in LEFT_CREST]
INNER_LEFT = path(
    ((123, 300), (148, 338), (152, 385), (126, 428)),
)
INNER_RIGHT = [(W-x, y) for x, y in INNER_LEFT]
# One graceful lower ribbon flows through the analytics bars (not across the M tip).
LOWER_SWEEP = path(
    ((135, 463), (172, 471), (189, 451), (222, 431)),
    ((222, 431), (261, 410), (290, 374), (303, 333)),
)
ROOTS = [
    [(216, 478), (216, 495), (201, 505), (195, 514)],
    [(216, 491), (232, 503), (240, 515)],
    [(216, 493), (216, 517)],
    [(211, 499), (201, 501), (190, 500)],
    [(222, 499), (234, 500), (245, 496)],
]


def rich_stroke(draw: ImageDraw.ImageDraw, coords, fraction: float, alpha=255, width=10):
    """Procedural layered metal stroke, drawn only with Pillow primitives."""
    if fraction <= 0:
        return
    count = max(2, min(len(coords), round(fraction * len(coords))))
    points = coords[:count]
    draw.line(points, fill=(78, 22, 5, alpha), width=width + 6, joint='curve')
    draw.line(points, fill=(199, 78, 18, alpha), width=width + 3, joint='curve')
    draw.line(points, fill=(255, 162, 42, alpha), width=width, joint='curve')
    draw.line(points, fill=(255, 225, 140, alpha), width=max(2, width//3), joint='curve')


def draw_capital_m(draw: ImageDraw.ImageDraw, opacity: float):
    """Draw a legible serif letter M via code-defined line strokes and serifs."""
    if opacity <= 0:
        return
    a = round(opacity * 255)
    strokes = [
        ([(136, 422), (136, 301)], 16),
        ([(136, 301), (216, 389)], 17),
        ([(216, 389), (296, 301)], 17),
        ([(296, 301), (296, 422)], 16),
        ([(122, 296), (153, 296)], 8),
        ([(279, 296), (311, 296)], 8),
        ([(122, 428), (157, 428)], 8),
        ([(275, 428), (310, 428)], 8),
    ]
    for pts, thick in strokes:
        rich_stroke(draw, pts, 1, a, thick)



def render_frame(frame: int) -> Image.Image:
    t = frame / FPS
    base = BACKGROUND.copy().convert('RGBA')

    # Slow luminous smoke: procedurally drawn moving elliptical clouds.
    smoke = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    sd = ImageDraw.Draw(smoke, 'RGBA')
    for k in range(9):
        phase = k * 0.85 + t * 0.35
        px = CX + math.sin(phase * 1.7) * (93 + 5*k)
        py = CY + math.cos(phase * 1.05) * (97 + 7*k)
        sz = 47 + k * 10
        sd.ellipse((int(px-sz), int(py-sz*0.47), int(px+sz), int(py+sz*0.47)),
                   fill=(139, 19 + k*2, 11, 8 + k))
    smoke = smoke.filter(ImageFilter.GaussianBlur(25))
    base = Image.alpha_composite(base, smoke)

    # Traces in a second layer make it possible to glow without image assets.
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, 'RGBA')

    # Rotating/drawing orbital arcs, one stroke at a time.
    for i, radius in enumerate((154, 175, 195)):
        start = -120 + 15*i + t * (13 if i % 2 == 0 else -9)
        end = start + (105 + 95*smoothstep(0.0, 3.0, t))
        d.arc((CX-radius, CY-radius, CX+radius, CY+radius),
              start=start, end=end, fill=(231, 68+25*i, 29, 65+i*15), width=2)

    # The trident-like geometric starter symbol appears then dissolves.
    old_alpha = 1 - smoothstep(1.4, 3.5, t)
    if old_alpha > 0:
        a = round(220 * old_alpha)
        orange = (255, 110, 42, a)
        d.line([(CX, CY+87), (CX, CY-46)], fill=orange, width=4)
        d.line([(CX-63, CY-67), (CX-62, CY-13), (CX, CY+7),
                (CX+62, CY-13), (CX+63, CY-67)], fill=orange, width=4, joint='curve')
        d.line([(CX-63, CY-67), (CX-49, CY-44), (CX-46, CY-23)], fill=orange, width=3)
        d.line([(CX+63, CY-67), (CX+49, CY-44), (CX+46, CY-23)], fill=orange, width=3)

    # Distinct two-stage reveal: clearly readable M, then the branded monogram.
    # These are distinct compositions built from geometry in every frame.
    letter_alpha = smoothstep(1.55, 2.45, t) * (1-smoothstep(3.5, 4.6, t))
    draw_capital_m(d, letter_alpha)

    reveal = smoothstep(3.75, 6.7, t)
    for coords, begin, end in (
        (LEFT_RIBBON, 0.0, 0.80), (RIGHT_RIBBON, 0.03, 0.83),
        (LEFT_CREST, 0.06, 0.76), (RIGHT_CREST, 0.08, 0.78),
        (INNER_LEFT, 0.23, 0.91), (INNER_RIGHT, 0.27, 0.92),
        (LOWER_SWEEP, 0.57, 1.0),
    ):
        rich_stroke(d, coords, smoothstep(begin, end, reveal), width=8)

    # Warm vertical growth bars are kept behind the monogram's lower swoop.
    for i, h in enumerate((22, 33, 42, 50, 63, 72, 82)):
        progress = smoothstep(4.75 + 0.12*i, 5.45 + 0.12*i, t)
        if progress:
            x = 156 + i*17
            top = 454 - int(h*progress)
            d.rounded_rectangle((x, top, x+8, 454), radius=2,
                                fill=(189, 80, 18, round(230*progress)))
            d.line([(x+2, top+1), (x+2, 453)],
                   fill=(255, 194, 83, round(220*progress)), width=2)

    # Redraw main ribbon over bars for a clean layered 3D silhouette.
    rich_stroke(d, LOWER_SWEEP, smoothstep(5.1, 6.7, t), width=8)

    for i, rpath in enumerate(ROOTS):
        draw_partial(d, rpath, smoothstep(5.8 + i*0.1, 7.1 + i*0.06, t),
                     (255, 171, 67, 225), 2)

    # One Gaussian-blurred duplicate is a procedural glow, not an external image.
    glow = layer.filter(ImageFilter.GaussianBlur(10))
    base = Image.alpha_composite(base, glow)
    base = Image.alpha_composite(base, layer)

    # Generated embers drifting upward, different each frame.
    dots = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dd = ImageDraw.Draw(dots, 'RGBA')
    for x, y, speed, radius, phase in PARTICLES:
        px = x + math.sin(t*0.55 + phase)*11
        py = (y - t*speed*5.0) % H
        flicker = (1 + math.sin(t*2.3 + phase)) / 2
        alpha = int(70 + flicker * 155)
        r = max(1, round(radius))
        dd.ellipse((px-r, py-r, px+r, py+r), fill=(255, 126, 32, alpha))
        if r > 1:
            dd.point((px, py), fill=(255, 224, 152, 255))
    base = Image.alpha_composite(base, dots)
    return base.convert('RGB')


def main():
    parser = argparse.ArgumentParser(description='100% Python-generated Mitratics Scene 1')
    parser.add_argument('--preview', action='store_true',
                        help='Render only first 1 second to verify encoding')
    parser.add_argument('--output', type=Path, default=None,
                        help='Optional custom output MP4 path')
    args = parser.parse_args()

    output = args.output or Path(__file__).resolve().parents[1] / 'output' / (
        'code_art_scene1_test.mp4' if args.preview else 'code_art_scene1_opening.mp4')
    output.parent.mkdir(parents=True, exist_ok=True)
    count = FPS if args.preview else TOTAL_FRAMES

    writer = imageio_ffmpeg.write_frames(
        str(output), (W, H), fps=FPS, codec='libx264',
        pix_fmt_in='rgb24', pix_fmt_out='yuv420p',
        output_params=['-crf', '21', '-movflags', '+faststart'],
        macro_block_size=16,
    )
    writer.send(None)
    try:
        for i in range(count):
            writer.send(render_frame(i).tobytes())
            if (i + 1) % 40 == 0 or i + 1 == count:
                print(f'Rendered {i+1}/{count} frames', flush=True)
    finally:
        writer.close()
    print(f'PASS: {output}')
    print(f'{count/FPS:.1f} seconds | {FPS} FPS | {W} x {H} | fully code-drawn')


if __name__ == '__main__':
    main()
