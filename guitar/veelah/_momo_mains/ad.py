import numpy as np, sys
from PIL import Image, ImageFilter
import ec
G='C:/Users/User/AppData/Local/Temp/claude/ee212e1eeeb8db2e/ebab9218-68ed-4462-8e1b-e6e84aacc40f/scratchpad/vee/gift_cut.jpg'
src=Image.open(G).convert('RGB'); a=np.asarray(src).astype(float)
bgc=np.median(a[300:500,300:550].reshape(-1,3),0)
d=np.sqrt(((a-bgc)**2).sum(2)); al=np.clip((d-40)*4,0,255).astype(np.uint8)
rgba=src.copy(); rgba.putalpha(Image.fromarray(al).filter(ImageFilter.MinFilter(3)))
bag=rgba.crop((590,0,900,640)); bag=bag.crop(bag.getbbox())
tun=rgba.crop((0,0,300,330)); tun=tun.crop(tun.getbbox())
bag.save('bag_cut.png'); CASE=Image.open('case_cut3.png').convert('RGBA'); tun.save('tuner_cut.png')
def ad(m,cut,out,case=False):
    o=Image.new('RGB',(1000,1000),'white')
    g=Image.open(ec.CUT+cut).convert('RGBA'); g=g.crop(g.getbbox())
    h=860 if m.startswith('V') else int(860*34/41)
    gg=g.resize((int(g.width*h/g.height),h),Image.LANCZOS)
    t=tun.resize((int(tun.width*150/tun.height),150),Image.LANCZOS)
    if True:
        src=CASE if case else bag
        bh=int(h*(1.06 if case else 1.04)); b=src.resize((int(src.width*bh/src.height),bh),Image.LANCZOS)
        o.paste(b,(600-b.width//2+120,1000-60-bh),b)
        o.paste(gg,(330-gg.width//2,1000-60-h),gg)
        o.paste(t,((470 if case else 560),1000-60-150),t)
    o.save(out,quality=93)
CUTS={'V2-GAC':'V2-GAC_up.png','V2-DC':'V2-DCE_kr_up.png','V3-DC':'V3-DCE_th_up.png','V3-GAC':'V3-GAC_front_up.png','V5-D':'V5-D_up.png','V5-GAC':'V5-GACE_up.png','V5-GACE':'V5-GACE_up.png','V8-D':'V8-D_up.png','V8-GAC':'V8-GAC_up.png','TOGO-SE':'TOGO_S_Front_up.png','TOGO-ME':'Togo-ME_up.png'}
for m,c in CUTS.items(): ad(m,c,f'out/{m}_ad.jpg',case=m.startswith('V8'))
