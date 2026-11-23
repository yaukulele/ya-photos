import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage
from ec import *
im=Image.open(r'C:\Users\User\.claude\channels\discord-jian-b\inbox\1795270836073-1573704671250354344.webp').convert('RGB')
c=im.crop((150,330,2470,1720)); a=np.asarray(c).astype(float)
d0=np.sqrt(((a-250)**2).sum(2)); m=d0>22
m=ndimage.binary_opening(m,np.ones((5,5))); lab,n=ndimage.label(m); sz=ndimage.sum(m,lab,range(1,n+1)); m=lab==(np.argmax(sz)+1)
al=Image.fromarray((m*255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1)); oc=c.copy(); oc.putalpha(al); oc=oc.crop(oc.getbbox())
cl=Image.open('case_cut3.png').convert('RGBA'); tun=Image.open('tuner_cut.png').convert('RGBA')
o=dark_bg(VEE+'out/V8-D_s5_wide.jpg',.86); tiles(o); d=ImageDraw.Draw(o)
t='購琴就附'; f=fnt(SERIF,78,900); d.text(((SZ-d.textlength(t,font=f))/2,60),t,font=f,fill=CREAM)
t2='V8 全單系列 原廠豪華硬盒'; f2=fnt(SANS,32,500); d.text(((SZ-d.textlength(t2,font=f2))/2,165),t2,font=f2,fill=GOLD)
paste_fit(o,cl,(60,240,330,900)); paste_fit(o,oc,(330,250,960,640)); paste_fit(o,tun,(560,700,720,850))
fl=fnt(SANS,28,700)
for txt,cx,y in (('原廠豪華硬盒',195,905),('打開：絨布內襯・可上鎖',645,650),('夾式調音器・彈片',640,870)):
    d.text((cx-d.textlength(txt,font=fl)/2,y),txt,font=fl,fill=GOLD)
n='※ 配件以實際出貨為主'; fn=fnt(SANS,24,400); d.text(((SZ-d.textlength(n,font=fn))/2,945),n,font=fn,fill=SOFT)
o.save('out/V8_gift.jpg',quality=93)
