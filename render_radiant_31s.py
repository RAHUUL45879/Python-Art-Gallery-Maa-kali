"""Python Art Gallery — Maa Kali: approved radiant-reveal 31-second edition.

Python renders and encodes every output frame. Opening, closing, Mahadev,
embers and overlays are Python-drawn. The Maa Kali character/background in
Scene 2 uses the USER-APPROVED animation GIF as a visual asset, because this
mode explicitly prioritizes faithfully preserving that artwork. This is a
Python-produced video, NOT a 100%-procedural character drawing.

The render never imports a pre-made MP4. To change the GIF, replace the file
under assets/; neither previous scripts nor videos are overwritten.

Usage:
  python render_radiant_31s.py --still 320
  python render_radiant_31s.py --preview
  python render_radiant_31s.py
"""
from __future__ import annotations

import argparse
import math
import random
import sys
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'code_art'))  # supports existing scene modules
from code_art import scene1, scene3
from code_art import eyes_shiva as E

W, H = 432, 768
FPS = 20
OPENING = 152   # 7.6 s
MIDDLE = 354    # 17.7 s
ENDING = 114    # 5.7 s
FRAMES = OPENING + MIDDLE + ENDING  # 620 = 31 s
ASSET = ROOT / 'assets' / 'maa_kali_radiant_reveal.gif'


def smooth(a: float, b: float, t: float) -> float:
    x = min(1., max(0., (t-a)/(b-a)))
    return x*x*(3-2*x)


def load_reference_frames() -> tuple[Image.Image, ...]:
    """Read ONLY the approved scene-2 GIF, scale to the project format."""
    if not ASSET.exists():
        raise FileNotFoundError(f'Approved Kali GIF missing: {ASSET}')
    result = []
    with Image.open(ASSET) as gif:
        for f in range(getattr(gif, 'n_frames', 1)):
            gif.seek(f)
            frame = gif.convert('RGB')
            result.append(frame.resize((W,H), Image.Resampling.LANCZOS))
    if len(result) < 2:
        raise ValueError('Expected multi-frame Maa Kali GIF')
    return tuple(result)


# Exactly 16 artist-provided animation frames, displayed over 17.7 seconds.
# The early dark-eye sequence gets enough time; full sari reveal is held.
CUES = (
    (0.0, 0.0), (1.3, 1.3), (2.4, 2.9),
    (3.8, 4.4), (5.5, 5.8), (7.2, 6.8),
    (9.5, 8.6), (12.3, 10.5), (14.7, 12.7), (17.7, 15.0),
)


def asset_position(t: float) -> float:
    for (a, fa), (b, fb) in zip(CUES, CUES[1:]):
        if t <= b:
            return fa + (fb-fa)*smooth(a,b,t)
    return float(CUES[-1][1])


_KALI_FRAMES: tuple[Image.Image, ...] | None = None


def animation_frames() -> tuple[Image.Image, ...]:
    global _KALI_FRAMES
    if _KALI_FRAMES is None:
        _KALI_FRAMES = load_reference_frames()
    return _KALI_FRAMES


_P = random.Random(62123)
SPARKS = [(_P.uniform(0,W), _P.uniform(0,H), _P.uniform(6,27),
           _P.uniform(0,6.28), _P.choice([1,1,2])) for _ in range(58)]


@lru_cache(maxsize=48)
def shiva_layer(half_second: int) -> Image.Image:
    # A meditating Shiva is almost stationary. Cache two drawn poses each second
    # so Python does not redraw the same anatomy hundreds of times.
    layer = Image.new('RGBA',(W,H),(0,0,0,0))
    E.shiva_foreground(layer,half_second/2)
    return layer


def middle_frame(index: int) -> Image.Image:
    """Python-composite the approved GIF, with procedural atmospheric effects
    and the previously approved, code-drawn Mahadev in the foreground.
    """
    if not 0 <= index < MIDDLE:
        raise ValueError('Middle frame index out of range')
    t = index/FPS
    frames = animation_frames()
    p = asset_position(t)
    low = min(len(frames)-1,int(p))
    high = min(low+1,len(frames)-1)
    alpha = p-low
    # Interpolate artist's source drawings instead of showing GIF at 2 FPS.
    base = Image.blend(frames[low],frames[high],alpha) if high!=low else frames[low].copy()
    image = base.convert('RGBA')

    # Very light code-generated moving embers over the animated red sky.
    embers = Image.new('RGBA',(W,H),(0,0,0,0))
    draw = ImageDraw.Draw(embers,'RGBA')
    for px,py,speed,phase,r in SPARKS:
        x = px + 6*math.sin(t*.38+phase)
        y = (py-speed*t)%H
        a = int(18+38*(.5+.5*math.sin(t*1.1+phase)))
        if y < 600:
            draw.ellipse((x-r,y-r,x+r,y+r),fill=(255,137,61,a))
    image.alpha_composite(embers)

    # Soft floor mist visually separates Shiva (foreground) from Kali.
    floor = Image.new('RGBA',(W,H),(0,0,0,0))
    fd = ImageDraw.Draw(floor,'RGBA')
    fd.ellipse((-30,564,W+30,852),fill=(9,7,14,78))
    image.alpha_composite(floor.filter(ImageFilter.GaussianBlur(25)))

    # The approved back-facing Mahadev is DRAWN by Python for every frame,
    # from the very beginning, and without changing his design.
    image.alpha_composite(shiva_layer(int(t*2)))

    # Soft crossfade only at the opening of Scene 2; opening video is unchanged.
    intro_mix = smooth(0.0,.60,t)
    if intro_mix < .999:
        start = E.render_frame(min(119,index)) .convert('RGBA')
        image = Image.blend(start,image,intro_mix)
    return image.convert('RGB')


def render_frame(index: int) -> Image.Image:
    if not 0 <= index < FRAMES:
        raise ValueError(f'Frame {index} outside 0..{FRAMES-1}')
    if index < OPENING:
        return scene1.render_frame(index)
    if index < OPENING+MIDDLE:
        t = index-OPENING
        frame = middle_frame(t)
        if t>=MIDDLE-13:  # very short handoff to the ending
            amt = smooth(MIDDLE-13,MIDDLE-1,t)
            return Image.blend(frame,scene3.render_frame(0),amt)
        return frame
    return scene3.render_frame(index-OPENING-MIDDLE)


def render_video(path: Path, indices) -> None:
    path.parent.mkdir(parents=True,exist_ok=True)
    indices = list(indices)
    writer = imageio_ffmpeg.write_frames(
        str(path), (W,H),fps=FPS,codec='libx264',
        pix_fmt_in='rgb24',pix_fmt_out='yuv420p',
        output_params=['-crf','18','-preset','medium','-movflags','+faststart'],
        macro_block_size=16
    )
    writer.send(None)
    try:
        for j,i in enumerate(indices,1):
            writer.send(render_frame(i).tobytes())
            if j%50==0 or j==len(indices):
                print(f'Rendered {j}/{len(indices)} frames',flush=True)
    finally:
        writer.close()
    print(f'PASS: {path}\nDuration: {len(indices)/FPS:.1f}s | {FPS} FPS | {W}x{H}')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--still',type=int,help='Save one generated video frame to PNG')
    p.add_argument('--preview',action='store_true',help='Render 4-second reveal excerpt')
    p.add_argument('--output',type=Path)
    args=p.parse_args()
    if args.still is not None:
        path=args.output or ROOT/'output'/f'radiant_frame_{args.still:03}.png'
        path.parent.mkdir(parents=True,exist_ok=True)
        render_frame(args.still).save(path)
        print(f'PASS: {path}')
        return
    path=args.output or ROOT/'output'/('Radiant_Reveal_4s_Preview.mp4' if args.preview else 'Maa_Kali_Radiant_31s_Python.mp4')
    indices=range(OPENING+110, OPENING+190) if args.preview else range(FRAMES)
    render_video(path,indices)

if __name__=='__main__':
    main()
