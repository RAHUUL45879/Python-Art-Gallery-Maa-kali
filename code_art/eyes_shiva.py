"""Approved luminous-eyes and Mahadev beat; procedural background for full movie.

No imported artwork, fonts, background images, masks, videos, or AI visuals.
Only Pillow drawing primitives and math generate the visuals. The established
Shiva back-view renderer in scene2_base_approved.py is reused unchanged.

This is a 6-second *visual approval test*, NOT the complete 17.7-second scene.
Run: python code_art/shadow_shiva_v4.py
     python code_art/shadow_shiva_v4.py --still 45
"""
from __future__ import annotations
import math, random, argparse
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg
import shiva_approved as base

W,H,FPS,DURATION=432,768,20,6.0
FRAMES=int(FPS*DURATION)
PI=math.pi

def clamp(v):return max(0.,min(1.,v))
def smooth(a,b,t):
    x=clamp((t-a)/(b-a))
    return x*x*(3-2*x)
def draw_line(draw,pts,color,width=2):
    draw.line([(int(x),int(y)) for x,y in pts],fill=color,width=width,joint='curve')

def smoke_paths(im,t):
    veil=Image.new('RGBA',(W,H));d=ImageDraw.Draw(veil,'RGBA')
    for k in range(17):
        x0=75+17*k
        phase=k*2.19
        xy=[]
        for u in range(28):
            yy=720-u*8.3 + k*4
            xx=x0+17*math.sin(u*.17+t*.55+phase)+u*0.7*math.sin(phase)
            xy.append((xx,yy))
        draw_line(d,xy,(126,73,75,13 if k%3 else 24),1+(k%3))
    im.alpha_composite(veil.filter(ImageFilter.GaussianBlur(8)))

def background(t):
    im=Image.new('RGBA',(W,H),(0,0,0,255));d=ImageDraw.Draw(im)
    # Low-contrast gradient: Shiva stays visible even in the first frame.
    for y in range(H):
        eye_zone=math.exp(-((y-294)/206)**2)
        floor_zone=math.exp(-((y-650)/180)**2)
        r=int(5+12*eye_zone+17*floor_zone)
        g=int(4+2*eye_zone+5*floor_zone)
        b=int(10+4*eye_zone+6*floor_zone)
        d.line((0,y,W,y),fill=(r,g,b,255))
    # Crimson celestial shimmer, left deliberately subtle.
    m=Image.new('RGBA',(W,H));md=ImageDraw.Draw(m,'RGBA')
    rr=109+9*math.sin(t*.3)
    md.ellipse((216-rr,277-rr,216+rr,277+rr),fill=(113,8,19,37))
    m=m.filter(ImageFilter.GaussianBlur(47));im.alpha_composite(m)
    # Dark lower terrain and water; no Kali figure or lion in this preview.
    d=ImageDraw.Draw(im,'RGBA')
    for k in range(4):
        pts=[(0,H)]
        for x in range(0,W+12,12):
            yy=555+23*k+9*math.sin(x*.02+k*1.35)+5*math.sin(x*.09+k)
            pts.append((x,yy))
        pts.append((W,H))
        d.polygon(pts,fill=[(12,11,20,170),(10,10,18,180),(6,8,15,225),(5,7,13,245)][k])
    d.line((0,614,W,614),fill=(122,39,38,105),width=1)
    for k in range(26):
        y=626+k*5
        cx=214+12*math.sin(y*.07+t*.6)
        wd=6+k*.85
        d.line((cx-wd,y,cx+wd,y),fill=(128,37,37,max(5,66-k*2)),width=1)
    # Moving glowing embers, deterministic from seeded locations.
    random.seed(143)
    for k in range(105):
        x=random.uniform(0,W);y=random.uniform(0,H);rad=random.uniform(.45,1.8)
        ph=random.uniform(0,2*PI); sp=random.uniform(4,19)
        xx=x+6*math.sin(t*.4+ph);yy=(y-t*sp)%H
        a=int(60+72*(.5+.5*math.sin(t*1.6+ph)))
        d.ellipse((xx-rad,yy-rad,xx+rad,yy+rad),fill=(236,101,51,a))
    smoke_paths(im,t)
    return im

def eyes(im,t):
    intensity=smooth(.38,2.05,t)
    if intensity==0:return
    cx,cy=216,286
    glow=Image.new('RGBA',(W,H));g=ImageDraw.Draw(glow,'RGBA')
    for s in (-1,1):
        ex=cx+s*53
        g.ellipse((ex-32,cy-22,ex+32,cy+22),fill=(240,14,32,int(182*intensity)))
    im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(19)))
    d=ImageDraw.Draw(im,'RGBA')
    # One natural blink, layered glow, asymmetrical eyelid curvature.
    blink=1-.93*math.exp(-((t-3.9)/.105)**2)
    eye_h=7.6*blink
    for side in (-1,1):
        x=cx+53*side
        aperture=[(x-29,cy+1),(x-18,cy-eye_h*.62),(x-4,cy-eye_h),
                  (x+11,cy-eye_h*.7),(x+25,cy+1),(x+10,cy+eye_h*.7),
                  (x-7,cy+eye_h*.75)]
        d.polygon(aperture,fill=(10,2,8,int(245*intensity)))
        if eye_h>1.4:
            d.ellipse((x-12,cy-eye_h*.72,x+12,cy+eye_h*.75),fill=(211,29,40,int(255*intensity)))
            d.ellipse((x-6,cy-eye_h*.64,x+6,cy+eye_h*.7),fill=(255,137,88,int(255*intensity)))
            d.ellipse((x-2,cy-eye_h*.6,x+2,cy+eye_h*.6),fill=(31,7,14,int(255*intensity)))
            d.ellipse((x-4,cy-eye_h*.6,x-1,cy-eye_h*.22),fill=(255,221,183,int(215*intensity)))
        eyelid=[(x-29,cy-3),(x-18,cy-10*blink),(x,cy-12*blink),(x+20,cy-5*blink),(x+27,cy-2)]
        draw_line(d,eyelid,(128,39,43,int(130*intensity)),2)

def shadow_hint(im,t):
    # A backlit silhouette only near the end; deliberately no badly rendered face.
    alpha=smooth(4.4,6.0,t)*.35
    if alpha<=0:return
    x=216;y=285
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer,'RGBA')
    a=int(185*alpha)
    # Dark long hair mass framing eyes, no clownlike face features.
    d.polygon([(x-41,y-110),(x+39,y-115),(x+84,y-62),(x+103,y+88),
               (x+146,y+190),(x+56,y+152),(x+31,y+111),
               (x-36,y+112),(x-66,y+162),(x-147,y+185),(x-105,y+56),(x-86,y-62)],fill=(9,7,15,a))
    for k in range(34):
        side=1 if k%2 else -1
        st=(x+side*(40+(k*7)%24),y-92+(k*11)%60)
        dest=(x+side*(92+(k*17)%69)+12*math.sin(t*.57+k),y+93+(k*29)%122)
        pts=base.curve(st,(st[0]+side*51,y-40), (dest[0]-side*19,dest[1]-50),dest,22)
        draw_line(d,pts,(65,17,23,int(124*alpha)),1+(k%2))
    # Underlayer is intentionally behind eye drawing; avoids re-covering eyes.
    im.alpha_composite(layer)

def shiva_foreground(im,t):
    # The exact approved back-facing Mahadev drawing is used from FRAME ZERO.
    # He is drawn over the dark base so the outline remains readable.
    base.shiva_figure(im,t)
    base.fire_smoke(im,t)

def render_frame(index):
    if not (0<=index<FRAMES):
        raise ValueError('Frame must be in 0..119')
    t=index/FPS
    im=background(t)
    shadow_hint(im,t)
    eyes(im,t)
    shiva_foreground(im,t)
    return im.convert('RGB')

def render_video(out):
    out=Path(out);out.parent.mkdir(exist_ok=True,parents=True)
    writer=imageio_ffmpeg.write_frames(str(out),(W,H),fps=FPS,codec='libx264',
        pix_fmt_in='rgb24',pix_fmt_out='yuv420p',
        output_params=['-crf','19','-movflags','+faststart'],macro_block_size=16)
    writer.send(None)
    try:
        for i in range(FRAMES):
            writer.send(render_frame(i).tobytes())
            if (i+1)%40==0 or i+1==FRAMES:
                print(f'Rendered {i+1}/{FRAMES} frames',flush=True)
    finally:writer.close()
    print(f'PASS: {out} | 6.0 seconds | 20 FPS | Python drawing only')

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--still',type=int)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent.parent
    if args.still is not None:
        out=args.output or root/'output'/f'shadow_shiva_v4_{args.still:03}.png'
        out.parent.mkdir(parents=True,exist_ok=True)
        render_frame(args.still).save(out);print(f'PASS: {out}')
    else:
        render_video(args.output or root/'output'/'shadow_shiva_v4_6s_preview.mp4')
if __name__=='__main__':main()
