import numpy as np, math
from PIL import Image, ImageDraw, ImageFilter
from scipy.spatial import ConvexHull
def shape(W,H):
    pts=[]
    for (cx,cy,r) in ((W*0.27,H*0.25,W*0.27),(W*0.73,H*0.25,W*0.27),(W*0.5,H*0.93,W*0.07)):
        for a in np.linspace(0,2*math.pi,90): pts.append((cx+r*math.cos(a),cy+r*math.sin(a)))
    pts=np.array(pts); h=ConvexHull(pts); return [tuple(p) for p in pts[h.vertices]]
def tex(H,W,scale,seed):
    rng=np.random.default_rng(seed); n=rng.random((H//scale+2,W//scale+2))
    return np.array(Image.fromarray((n*255).astype(np.uint8)).resize((W,H),Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale/3))).astype(float)/255
def pick(color,seed,W=400):
    H=int(W*1.15)
    m=Image.new('L',(W*4,H*4),0); ImageDraw.Draw(m).polygon([(x*4,y*4) for x,y in shape(W,H)],fill=255); m=m.resize((W,H),Image.LANCZOS)
    t=np.clip(0.6*tex(H,W,40,seed)+0.4*tex(H,W,12,seed+5),0,1); t=(t-t.min())/(t.max()-t.min())
    t=(np.sin(t*math.pi*1.6)*0.5+0.5)*0.7+0.15   # pearl swirl bands
    c=np.array(color,float); light=np.minimum(c*1.3+35,255)
    rgb=c*(1-t[...,None])+light*t[...,None]
    yy,xx=np.mgrid[0:H,0:W]; sh=1.05-0.35*(((xx/W-0.4)**2+(yy/H-0.3)**2))
    rgb=np.clip(rgb*sh[...,None],0,255)
    im=Image.fromarray(rgb.astype(np.uint8)); im.putalpha(m); return im.crop(im.getbbox())
a=pick((100,45,150),1); b=pick((35,120,80),2)
c=Image.new('RGBA',(int(a.width*1.75),int(a.height*1.2)),(0,0,0,0))
c.alpha_composite(b.rotate(-12,expand=True,resample=Image.BICUBIC),(int(a.width*0.6),int(a.height*0.12)))
sh=Image.new('RGBA',c.size,(0,0,0,0))
ar=a.rotate(10,expand=True,resample=Image.BICUBIC)
s=Image.new('RGBA',ar.size,(0,0,0,90)); s.putalpha(ar.split()[3].point(lambda v:int(v*0.35)))
c.alpha_composite(s.filter(ImageFilter.GaussianBlur(6)),(14,14)); c.alpha_composite(ar,(0,0))
c=c.crop(c.getbbox()); c.save('picks2.png')
w=Image.new('RGB',c.size,'white'); w.paste(c,(0,0),c); w.save('picks_chk.jpg')
