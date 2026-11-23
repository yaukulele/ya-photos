import re,requests,io,json,base64,sys,os
from PIL import Image
import ec
app=io.open('D:/Coding/yu-toolbox/app.py',encoding='utf-8').read()
TOK=re.search(r'token=([A-Za-z0-9_-]+)',app).group(1)
B='https://momo-integration-production.up.railway.app'
def api(m,p,**kw):
    return requests.request(m,f'{B}{p}?token={TOK}',timeout=180,**kw).json()
CUT={'V2-DC':'V2-DCE_kr_up.png','V3-DC':'V3-DCE_th_up.png','V5-GAC':'V5-GACE_up.png','V5-GACE':'V5-GACE_up.png','V2-GAC':'V2-GAC_up.png','V3-GAC':'V3-GAC_front_up.png','V5-D':'V5-D_up.png','V8-D':'V8-D_up.png','V8-GAC':'V8-GAC_up.png','TOGO-SE':'TOGO_S_Front_up.png','TOGO-ME':'Togo-ME_up.png'}
items=[p for p in api('GET','/api/listing/products')['items'] if p.get('brand')=='Veelah']
json.dump(items,open('backup_listing_imgs.json','w',encoding='utf-8'),ensure_ascii=False)
only=sys.argv[1:]
for p in items:
    m=p['model']; pid=p['id']
    if only and m not in only: continue
    imgs=p['images']; mains=[i for i in imgs if i['role']=='main']; rest=[i for i in imgs if i['role']!='main']
    white=[i for i in mains if i.get('name')=='white.jpg']
    def up(path,fn):
        r=api('POST',f'/api/listing/images/{pid}',json={'base64':base64.b64encode(open(path,'rb').read()).decode(),'mime':'image/jpeg','filename':fn,'role':'main'})
        assert r.get('ok'),r; return r['product']['images'][-1]['id']
    if white: wid=white[0]['id']
    else:
        im=Image.open(ec.CUT+CUT[m]).convert('RGBA'); im=im.crop(im.getbbox()); s=900/im.height
        im=im.resize((int(im.width*s),900),Image.LANCZOS); o=Image.new('RGB',(1000,1000),'white'); o.paste(im,((1000-im.width)//2,50),im)
        o.save(f'out/{m}_m1.jpg',quality=93); wid=up(f'out/{m}_m1.jpg','white.jpg')
    for i in mains:
        if i['id']!=wid:
            r=api('DELETE',f'/api/listing/images/{pid}/{i["id"]}'); assert r.get('ok'),r
    new=[up(f'out/{m}_m{k}.jpg',f'{m}_m{k}.jpg') for k in (2,3,4,5,6)]
    r=api('PUT',f'/api/listing/images/{pid}/order',json={'order':[wid]+new+[i['id'] for i in rest],'mainId':wid}); assert r.get('ok'),r
    fin=r['product']['images']; print(pid,m,'mains',[x['name'] for x in fin if x['role']=='main'],'others',len([x for x in fin if x['role']!='main']),'white_new' if not white else '')
