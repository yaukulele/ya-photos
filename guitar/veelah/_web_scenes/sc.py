import sys, os
from PIL import Image
V='C:/Users/User/AppData/Local/Temp/claude/ee212e1eeeb8db2e/ebab9218-68ed-4462-8e1b-e6e84aacc40f/scratchpad/vee'
sys.path.insert(0,V)
from gcomp import comp
CUT=V+'/cut/'
# key: (room, cx, base, h_104cm, floor, shadow, tint, dim, warm, rot)
SC={
 'beach':('rooms/beach.png',880,1215,486,1200,(40,-4,.32),.30,.85,.14,3,720),
 'camp':('rooms/camp.png',760,1335,625,None,(0,0,0),.30,.55,.16,3,1150),
 'roof':('rooms/roof.png',1000,1190,440,1170,(30,-4,.25),.30,.70,.14,3,None),
 'park':('rooms/park.png',1000,1092,460,None,(0,0,0),.25,.95,.10,2,None),
 'dock':('rooms/dock.png',720,1205,540,None,(0,0,0),.25,.90,.10,2,None),
 'cabin':('rooms/cabin.png',1097,1250,465,1247,(35,-4,.30),.30,.80,.16,3,None),
 'cafe':('rooms/cafe.png',880,1215,480,1211,(30,-4,.25),.28,.92,.12,3,None),
 'living':('rooms/living.png',1463,1085,400,1075,(30,-4,.22),.20,.95,.10,3,1330),
 'studio':('rooms/studio.png',1463,1080,383,1075,(25,-4,.30),.30,.60,.18,3,1250),
 'maple':('rooms/maple.png',1000,930,315,900,(30,-4,.25),.30,.85,.14,3,None),
 'meadow':('rooms/meadow.png',878,1430,620,None,(0,0,0),.22,.97,.08,2,None),
 'brick':('rooms/brick.png',1317,1140,528,1135,(35,-4,.30),.28,.90,.14,3,1100),
}
from PIL import ImageDraw, ImageFont
def label(im):
    d=ImageDraw.Draw(im); f=ImageFont.truetype('C:/Windows/Fonts/msjh.ttc',26)
    t='示意圖'; x,y=28,im.height-52
    d.text((x+1,y+1),t,font=f,fill=(0,0,0)); d.text((x,y),t,font=f,fill=(255,255,255))
    return im
def render(cut,key,out,scale=1.0):
    r,cx,base,h,fl,sh,tint,dim,warm,rot,ccx=SC[key]; hh=int(h*scale)
    im=comp(r,CUT+cut,cx=cx,base=base,height=hh,shadow=sh,floor=fl,tint=tint,dim=dim,warm=warm,rot=rot)
    W,H=im.size; side=min(H,int(max(h/0.55,600 if h<340 else 900)))
    x0=int(min(max((ccx or cx)-side/2,0),W-side)); y1=min(H,base+int(side*0.2)); y0=max(0,y1-side)
    im2=im.crop((x0,y0,x0+side,y0+side)).resize((1200,1200),Image.LANCZOS); label(im2).save(out,quality=90)
if __name__=='__main__':
    os.makedirs('out',exist_ok=True)
    for k in (sys.argv[1:] or SC): render('V5-D_up.png',k,f'out/V5-D_{k}.jpg')
