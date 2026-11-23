from sc import render
from PIL import Image
import os
CUTS={'V1-DC':'V1-DC-2_up.png','V2-DC':'V2-DCE_kr_up.png','V3-DC':'V3-DCE_th_up.png','V3-GAC':'V3-GAC_front_up.png','V5-D':'V5-D_up.png','V5-GAC':'V5-GACE_up.png','V5-GACE':'V5-GACE_up.png','V8-D':'V8-D_up.png','V8-GAC':'V8-GAC_up.png','TOGO-SE':'TOGO_S_Front_up.png','TOGO-ME':'Togo-ME_up.png'}
PLAN={'V1-DC':('park','living'),'V2-DC':('cafe','beach'),'V3-DC':('cabin','park'),'V3-GAC':('maple','dock'),'V5-D':('roof','meadow'),
 'V5-GAC':('living','cabin'),'V5-GACE':('studio','roof'),'V8-D':('studio','brick'),'V8-GAC':('cafe','dock'),'TOGO-SE':('camp','beach'),'TOGO-ME':('camp','meadow')}
os.makedirs('final',exist_ok=True)
for m,ks in PLAN.items():
    for k in ks:
        render(CUTS[m],k,f'final/{m}_{k}.jpg',scale=34/41 if m.startswith('TOGO') else 1.0)
fs=sorted(os.listdir('final'))
for i in range(0,len(fs),12):
    S=Image.new('RGB',(4*400,3*400),'white')
    for j,f in enumerate(fs[i:i+12]): S.paste(Image.open('final/'+f).resize((400,400)),((j%4)*400,(j//4)*400))
    S.save(f'chk_{i//12}.jpg',quality=85)
print(len(fs))
