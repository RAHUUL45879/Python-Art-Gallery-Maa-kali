"""Closing sequence: code-drawn Happy Kali Puja + Mitratics M + Coming Soon.
No imported images or video. The approved vector M is redrawn via scene1 geometry.
"""
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import scene1
import eyes_shiva as E
from shiva_approved import shiva_figure

W,H,FPS,FRAMES=432,768,20,114


def smooth(a,b,t):
    u=max(0.,min(1.,(t-a)/(b-a)))
    return u*u*(3-2*u)


def get_font(size=28,serif=True):
    # Rendering text with an available local font is still Python-drawn text.
    if serif:
        candidates=('C:/Windows/Fonts/georgia.ttf',
                    'C:/Windows/Fonts/times.ttf',
                    '/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf')
    else:
        candidates=('C:/Windows/Fonts/arial.ttf',
                    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')
    for p in candidates:
        if Path(p).exists():
            return ImageFont.truetype(p,size)
    return ImageFont.load_default(size=size)


def center_text(im,text,at_y,size,color,opacity=255):
    lay=Image.new('RGBA',(W,H));d=ImageDraw.Draw(lay,'RGBA')
    font=get_font(size)
    bbox=d.textbbox((0,0),text,font=font)
    tw=bbox[2]-bbox[0]
    x=(W-tw)/2
    d.text((x,at_y),text,font=font,anchor='lt',fill=(*color,opacity),stroke_width=0)
    im.alpha_composite(lay.filter(ImageFilter.GaussianBlur(5)))
    im.alpha_composite(lay)


def make_logo():
    """Only curves and metal strokes from the approved Python code, no image import."""
    layer=Image.new('RGBA',(W,H));d=ImageDraw.Draw(layer,'RGBA')
    for path in (scene1.LEFT_RIBBON,scene1.RIGHT_RIBBON,
                 scene1.LEFT_CREST,scene1.RIGHT_CREST,
                 scene1.INNER_LEFT,scene1.INNER_RIGHT):
        scene1.rich_stroke(d,path,1,width=8)
    for i,h in enumerate((22,33,42,50,63,72,82)):
        x=156+i*17
        d.rounded_rectangle((x,454-h,x+8,454),radius=2,fill=(215,120,28,230))
    scene1.rich_stroke(d,scene1.LOWER_SWEEP,1,width=8)
    for pts in scene1.ROOTS:
        scene1.draw_partial(d,pts,1,(255,180,65,235),2)
    crop=layer.crop((85,275,348,528))
    return crop.resize((194,186),Image.Resampling.LANCZOS)

LOGO=make_logo()


def shiva_bottom(im,t):
    lay=Image.new('RGBA',(W,H))
    shiva_figure(lay,t)
    obj=lay.crop((82,427,339,743)).resize((158,196),Image.Resampling.LANCZOS)
    # Shiva is kept small and downstage, so no conflicts with the text/logo.
    im.alpha_composite(obj,(137,572))


def render_frame(i):
    if not 0<=i<FRAMES:raise ValueError('Scene3 frame index out of range')
    t=i/FPS
    im=E.background(17.7+t)
    d=ImageDraw.Draw(im,'RGBA')
    p=smooth(0,1.8,t)
    # Original rotating fiery rings and a small sun/moon over the greeting.
    pulse=.5+.5*math.sin(t*1.4)
    for r in (154,173,190):
        st=-105+t*7+r*.2
        d.arc((216-r,380-r,216+r,380+r),st,st+245,
              fill=(235,94,47,int(p*(53+23*pulse))),width=2)
    d.ellipse((140,56,292,208),fill=(73,9,21,int(p*100)),outline=(192,36,30,int(p*90)),width=1)
    # Thin decorative lotus filigree drawn with lines, not an imported icon.
    for side in (-1,1):
        linepts=[(216,298),(216+side*17,281),(216+side*30,297),(216+side*11,305),(216,298)]
        d.line(linepts,fill=(231,132,60,int(p*154)),width=2)
    if p:
        center_text(im,'Happy',189,31,(255,224,177),int(p*238))
        center_text(im,'KALI PUJA',231,37,(241,137,75),int(p*243))
        # Glow around the dynamically drawn logo, then the crisp actual path artwork.
        logo=LOGO.copy()
        # Slight breathing pulse only, not jitter or zooming into a poster.
        g=logo.filter(ImageFilter.GaussianBlur(8))
        g.putalpha(g.getchannel('A').point(lambda a:int(a*.47*p)))
        im.alpha_composite(g,(118,328))
        logo.putalpha(logo.getchannel('A').point(lambda a:int(a*p)))
        im.alpha_composite(logo,(118,328))
    if t>=1.2:
        q=smooth(1.2,3.3,t)
        d=ImageDraw.Draw(im,'RGBA')
        d.line((104,526,328,526),fill=(178,92,48,int(q*130)),width=1)
        center_text(im,'Coming Soon',540,28,(255,208,149),int(q*235))
    shiva_bottom(im,17.7+t)
    # Embers and muted smoke generated through the existing background every frame.
    return im.convert('RGB')
