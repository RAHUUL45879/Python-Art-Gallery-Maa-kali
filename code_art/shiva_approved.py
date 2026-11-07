"""Approved Mahadev BACK VIEW. All geometry is Python-drawn, no images."""

import math

from PIL import Image, ImageDraw, ImageFilter

W,H=432,768

GOLD=(230,158,70,255)

GOLD_LIGHT=(255,216,135,255)

def I(v):
    return int(round(v))

def curve(a,b,c,d, steps=32):
    return [((1-u)**3*a[0]+3*(1-u)**2*u*b[0]+3*(1-u)*u*u*c[0]+u**3*d[0],
             (1-u)**3*a[1]+3*(1-u)**2*u*b[1]+3*(1-u)*u*u*c[1]+u**3*d[1])
            for u in (k/steps for k in range(steps+1))]

def line(d, pts, fill, width=2):
    d.line(pts, fill=fill, width=width, joint="curve")

def ring(d, cx, cy, r, rgba, width=2, start=0, end=359):
    d.arc((cx-r, cy-r, cx+r, cy+r), start, end, fill=rgba, width=width)

def shaded_oval(d, box, colors, steps=7):
    """Quick painterly shading: inset ellipses instead of a flat block."""
    x0,y0,x1,y1=box
    d.ellipse(box,fill=colors[0])
    for j in range(1,steps+1):
        k=j/(steps+2)
        r=tuple(I(colors[0][n]*(1-k)+colors[1][n]*k) for n in range(3))+(255,)
        d.ellipse((x0+(x1-x0)*k*.45,y0+(y1-y0)*k*.23,
                   x1-(x1-x0)*k*.27,y1-(y1-y0)*k*.56),fill=r)

def shiva_figure(im, t):
    """Mahadev in lotus meditation, viewed entirely FROM BEHIND.

    Hand-built vector geometry: anatomy, jata, crescent, cobra, tiger-skin,
    rudraksha, trident, crossed legs, and calm breathing. No image assets.
    All dimensions are relative to the anchor, so the pose can be edited.
    """
    cx = 212.0
    # A restrained breathing cycle, so Shiva feels meditative, not restless.
    breath = math.sin(t * 1.1)
    cy = 616.0 + 0.8 * breath
    p = lambda x, y: (cx + x, cy + y)
    d = ImageDraw.Draw(im, 'RGBA')

    # A subdued reflected halo behind Shiva. Drawn using transparency only.
    aura = Image.new('RGBA', (W, H))
    ad = ImageDraw.Draw(aura, 'RGBA')
    ad.ellipse((cx-95, cy-146, cx+95, cy+38), fill=(217, 64, 37, 31))
    im.alpha_composite(aura.filter(ImageFilter.GaussianBlur(35)))
    d = ImageDraw.Draw(im, 'RGBA')

    # Stone ledge / ground shadow, then the tiger-hide meditation mat.
    d.ellipse((cx-113, cy+75, cx+114, cy+117), fill=(4, 7, 13, 255))
    d.ellipse((cx-96, cy+81, cx+99, cy+106), fill=(36, 21, 22, 255))
    d.polygon([p(-96, 88), p(-77, 74), p(-50, 75), p(-22, 61),
               p(26, 60), p(60, 76), p(95, 86), p(83, 106),
               p(-89, 105)], fill=(143, 83, 42, 255))
    for j in range(18):
        tx = -86 + (j*31) % 170
        ty = 84 + (j*19) % 19
        d.polygon([p(tx-5,ty-1),p(tx+3,ty-3),p(tx+8,ty+2),p(tx,ty+5)],
                  fill=(34, 23, 24, 255))
    d.line([p(-90,104),p(86,104)], fill=(230,142,70,190), width=2)

    # Crossed legs are drawn before the torso to make the lotus pose credible.
    # Rear bent thighs: broad at the knee, narrowing into the crossed shins.
    d.ellipse((cx-96,cy+45,cx+4,cy+110),fill=(19,26,37,255))
    d.ellipse((cx-2,cy+45,cx+99,cy+110),fill=(21,27,38,255))
    d.polygon([p(-86,61),p(-47,54),p(-1,78),p(19,92),p(-27,101),p(-99,90)],
              fill=(55,65,79,255))
    d.polygon([p(85,61),p(45,55),p(3,78),p(-18,93),p(30,102),p(100,90)],
              fill=(49,59,74,255))
    # Ash-coloured highlights make knees and calves read as real volumes.
    d.arc((cx-94,cy+54,cx-13,cy+102),193,335,fill=(102,112,117,170),width=3)
    d.arc((cx+12,cy+52,cx+97,cy+101),203,338,fill=(91,105,117,150),width=3)
    # Two small upward soles, where the folded feet emerge from the thighs.
    d.ellipse((cx-26,cy+74,cx+12,cy+101),fill=(66,81,92,255))
    d.ellipse((cx-13,cy+78,cx+30,cy+105),fill=(73,86,95,255))
    for j in range(4):
        x=-19+j*6
        d.line([p(x,82),p(x-1,89)],fill=(140,146,141,140),width=1)
    for j in range(4):
        x=10+j*6
        d.line([p(x,85),p(x+1,92)],fill=(148,147,137,140),width=1)

    # Bare muscular upper back: broad trapezius, natural waist taper,
    # visible scapulae, spine line and firelit left-side rim.
    shoulder_y = -44-1.7*breath
    d.polygon([p(-22,-67),p(-45,shoulder_y-6),p(-57,-23),p(-48,9),
               p(-38,48),p(-21,64),p(21,64),p(38,48),p(47,9),
               p(57,-23),p(44,shoulder_y-6),p(22,-67)],
              fill=(48,63,80,255))
    d.polygon([p(-48,-35),p(-58,-18),p(-39,42),p(-22,54),p(-17,-56)],
              fill=(96,109,118,205))
    d.polygon([p(44,-35),p(56,-18),p(39,41),p(21,56),p(15,-56)],
              fill=(17,30,49,190))
    # Back muscles / scapula and sternocleidomastoid contours.
    line(d, curve(p(-41,-33),p(-38,-9),p(-27,2),p(-9,7),18),
         (131,137,137,125),2)
    line(d, curve(p(41,-33),p(38,-8),p(27,0),p(9,7),18),
         (14,23,37,150),3)
    line(d, curve(p(-15,14),p(-21,31),p(-19,43),p(-9,53),16),
         (116,113,116,95),2)
    line(d, curve(p(15,14),p(21,31),p(19,43),p(9,53),16),
         (19,30,42,190),2)
    line(d,[p(0,-57),p(-1,-34),p(1,-4),p(0,28),p(0,54)],
         (108,113,119,125),2)
    for yy in (-26,-7,15,36):
        d.ellipse((cx-2,cy+yy,cx+2,cy+yy+4),fill=(131,137,136,65))

    # Shaded upper arms with elbows bent toward the knees; forearms remain
    # separate from torso, hands actually rest palm-up on the crossed legs.
    for side in (-1,1):
        start=p(side*46,-30)
        elbow=p(side*75,24)
        wrist=p(side*78,80)
        upper=curve(start,p(side*62,-24),p(side*74,-4),elbow,20)
        lower=curve(elbow,p(side*80,43),p(side*81,63),wrist,19)
        line(d,upper,(16,24,38,255),27)
        line(d,upper,(60,77,93,255),20)
        line(d,upper,(108,117,123,100),4)
        line(d,lower,(19,25,39,255),22)
        line(d,lower,(69,83,96,255),16)
        # Wrist bracelet, side-lit and anatomically placed.
        line(d,[p(side*72,65),p(side*82,67)],(157,90,48,255),5)
        line(d,[p(side*72,66),p(side*82,68)],(220,153,83,255),2)
        # Upward-open palm, thumb and subtle separated fingertip ridges.
        d.ellipse((wrist[0]-15,wrist[1]-5,wrist[0]+15,wrist[1]+12),
                  fill=(80,96,105,255),outline=(170,153,129,200),width=2)
        d.ellipse((wrist[0]-9,wrist[1],wrist[0]+10,wrist[1]+7),
                  fill=(115,125,127,150))
        for j in range(4):
            xx=wrist[0]-9+j*6
            d.arc((xx-4,wrist[1]-6,xx+5,wrist[1]+3),180,350,
                  fill=(159,164,157,135),width=1)
        d.ellipse((wrist[0]-3,wrist[1]+1,wrist[0]+3,wrist[1]+7),
                  fill=(226,167,96,210))

    # Tiger-skin drape falls over Shiva's RIGHT hip, leaving the back exposed.
    d.polygon([p(25,-37),p(39,-27),p(27,6),p(39,49),p(60,86),
               p(36,94),p(13,46),p(17,8)],fill=(189,94,48,246))
    d.polygon([p(30,-33),p(36,-20),p(27,3),p(40,49),p(54,83),
               p(38,80),p(25,40),p(22,0)],fill=(229,135,66,110))
    for j in range(12):
        sy=-27+j*9
        sx=29+9*math.sin(j*.54)
        d.polygon([p(sx-5,sy),p(sx+6,sy+5),p(sx+3,sy+9)],
                  fill=(42,24,29,210))

    # Neck rising into back-view jaw/occipital mass: NO forward-looking face.
    d.polygon([p(-15,-76),p(15,-76),p(22,-60),p(-22,-60)],
              fill=(46,57,75,255))
    shaded_oval(d,(cx-26,cy-127,cx+26,cy-69),
                ((22,32,48,255),(77,89,105,255)),8)
    # Ear contours are tiny; Shiva's FACE IS NEVER VISIBLE.
    for side in (-1,1):
        ex=cx+side*26
        d.ellipse((ex-5,cy-110,ex+5,cy-94),fill=(47,61,76,255))
        ring(d,ex,cy-95,5,(209,145,70,255),2)

    # Dense, braided jata hair covers the back of his head and flows down
    # the spine; matted topknot and a small crescent are identifiable.
    d.ellipse((cx-27,cy-134,cx+27,cy-91), fill=(13,14,23,255))
    d.ellipse((cx-20,cy-160,cx+20,cy-117),fill=(13,14,22,255))
    d.ellipse((cx-13,cy-172,cx+13,cy-141),fill=(16,16,23,255))
    for j in range(28):
        start=p(-24+(j*11)%49,-124+(j*7)%27)
        stop=p(-24+(j*17)%49+3*math.sin(t*.35+j),-56+(j*13)%74)
        pts=curve(start,p(start[0]-cx-8,-82),p(stop[0]-cx+9,-7),stop,20)
        line(d,pts,(13+j%5*5,13+j%4*3,22+j%3*3,240),2 if j%3 else 4)
        if j%6==0:
            line(d,pts,(124,68,40,125),1)
    # Crescent of Shiva, behind the topknot and illuminated by moonlight.
    d.arc((cx-18,cy-180,cx+22,cy-143),182,306,fill=(255,217,152,255),width=4)
    d.arc((cx-13,cy-175,cx+18,cy-149),183,304,fill=(99,70,58,140),width=1)

    # Cobra around his neck, visible from behind: two coiling paths and a
    # small raised hood at the left of his shoulder, never covering the pose.
    snake=curve(p(-12,-76),p(-48,-76),p(-48,-49),p(-35,-39),23)
    snake2=curve(p(-35,-39),p(-17,-27),p(7,-32),p(23,-48),22)
    line(d,snake+snake2,(20,26,29,255),12)
    line(d,snake+snake2,(111,104,81,255),7)
    line(d,snake+snake2,(209,172,102,185),2)
    # Raised, compact cobra hood (not a rectangular prop).
    hood=curve(p(-44,-75),p(-61,-97),p(-56,-108),p(-44,-105),18)
    line(d,hood,(41,46,43,255),10)
    d.ellipse((cx-57,cy-112,cx-39,cy-91),fill=(79,83,70,255),
              outline=(188,155,99,255),width=2)
    d.arc((cx-55,cy-109,cx-41,cy-94),180,345,fill=(147,133,97,255),width=2)
    d.ellipse((cx-45,cy-101,cx-42,cy-98),fill=(251,193,94,255))

    # Rudraksha collar and bracelets are modelled bead by bead.
    necklace=curve(p(-28,-69),p(-13,-60),p(12,-61),p(30,-70),25)
    line(d,necklace,(72,36,28,255),5)
    for j in range(11):
        point=necklace[j*2]
        x,y=point
        d.ellipse((x-3,y-3,x+3,y+3),fill=(153,81,46,255),
                  outline=(55,32,27,255),width=1)

    # Nearby Mahadev trident and tied damru, both hand-drawn.
    tx=67
    ty=474
    d.line((tx,ty+232,tx,ty+52),fill=(71,43,33,255),width=8)
    d.line((tx,ty+232,tx,ty+52),fill=(216,154,79,255),width=4)
    for side in (-1,1):
        pts=curve((tx,ty+75),(tx+side*31,ty+83),(tx+side*31,ty+33),
                  (tx+side*22,ty+2),20)
        line(d,pts,(222,156,80,255),5)
        line(d,pts,(248,208,129,210),2)
    d.polygon([(tx-4,ty+78),(tx+4,ty+78),(tx,ty)],fill=(244,195,100,255))
    # Damru in side silhouette, below the prongs.
    d.polygon([(tx+3,ty+115),(tx+24,ty+106),(tx+24,ty+131),(tx+3,ty+122)],
              fill=(130,67,42,255),outline=(229,161,79,255))
    d.polygon([(tx+3,ty+122),(tx+24,ty+106),(tx+24,ty+131),(tx+3,ty+115)],
              fill=(104,50,40,155))
    d.ellipse((tx+13,ty+118,tx+17,ty+123),fill=(234,164,83,255))
    d.line((tx+16,ty+124,tx+33,ty+132),fill=(222,155,71,210),width=1)

def fire_smoke(im,t):
    d=ImageDraw.Draw(im,'RGBA')
    smoke=Image.new('RGBA',(W,H))
    sd=ImageDraw.Draw(smoke,'RGBA')
    halo=Image.new('RGBA',(W,H))
    hd=ImageDraw.Draw(halo,'RGBA')
    for j,(x,y) in enumerate(((82,688),(351,695))):
        d.ellipse((x-29,y-6,x+29,y+10),fill=(76,38,29,255),outline=(171,104,60,255),width=2)
        d.polygon([(x-23,y+5),(x-16,y+24),(x+17,y+24),(x+23,y+5)],fill=(34,25,28,255))
        d.line((x-15,y+23,x+16,y+23),fill=(162,101,61,255),width=2)
        flick=6*math.sin(t*9+j*4)+4*math.sin(t*13+j*2)
        hd.ellipse((x-44,y-58,x+44,y+32),fill=(248,85,29,85))
        d.polygon([(x-8,y-5),(x-8,y-21),(x-2,y-35-flick),(x+2,y-18),
                   (x+8,y-28+flick*.5),(x+11,y-7)],fill=(230,84,31,255))
        d.polygon([(x-4,y-8),(x-1,y-23-flick*.3),(x+5,y-9)],fill=(255,219,115,245))
        for k in range(4):
            pts=[]
            for m in range(30):
                u=m/29
                yy=y-27-u*175-((t*12+k*7)%35)
                xx=x+(10+17*u)*math.sin(u*11+k*.8+t*.43)+(k-1.5)*4
                pts.append((xx,yy))
            line(sd,pts,(178,153,135,max(6,65-k*12)),2)
    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(20)))
    im.alpha_composite(smoke.filter(ImageFilter.GaussianBlur(4)))
