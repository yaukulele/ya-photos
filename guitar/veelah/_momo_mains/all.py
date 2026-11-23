import glob, os, sys
import ec
from ec import VEE
ec.SHAPES['STD'] = ('標準吉他', '41 吋', ['一般成人尺寸', '音量、低音比較足', '放家裡、上課用'])
ec.SHAPES['T'] = ('旅行琴', 'TRAVEL', ['34 吋，小一號', '手小、小朋友好按', '出門、露營好帶'])

V2P = [('第一把單板琴的好選擇', '一萬出頭就有雲杉單板的清亮聲音'), ('拿出來就很好看', '拼花音孔＋亮光漆，低調但有質感')]
V3P = [('想要溫暖音色選這把', '非洲胡桃木背側，聲音溫潤有厚度'), ('霧面質感 低調耐看', '消光塗裝，手感自然不黏手')]
V5P = [('經典配方 一把用很久', '雲杉單板＋玫瑰木背側，聲音飽滿'), ('進階換琴的首選', '黑檀木指板與琴橋，手感更順')]
V8P = [('Veelah 最高階 全單板', '雲杉＋玫瑰木全單，越彈聲音越開'), ('收藏等級的外觀', '鮑魚貝音孔＋虎紋楓木滾邊')]
DPT = ('D 桶聲音大', '刷和弦有力，自彈自唱最適合')
GAPT = ('GA 桶好抱好彈', '腰細不卡手，指彈刷扣都好聽')
BAG = '附 調音器・彈片・原廠琴袋'
# model: cutout, points, accessory, this_key, (left), (right), cutaway, rosette label
M = {
 'V2-DC': ('V2-DCE_kr_up.png', V2P + [DPT], BAG, 'D', ('D', 'V2-DCE_kr_up.png', 41), ('GA', 'V2-GAC_up.png', 40), 1, '拼花音孔'),
 'V3-DC': ('V3-DCE_th_up.png', V3P + [DPT], BAG, 'D', ('D', 'V3-DCE_th_up.png', 41), ('GA', 'V3-GAC_front_up.png', 40), 1, '音孔'),
 'V3-GAC': ('V3-GAC_front_up.png', V3P + [GAPT], BAG, 'GA', ('D', 'V3-DCE_th_up.png', 41), ('GA', 'V3-GAC_front_up.png', 40), 1, '音孔'),
 'V5-D': ('V5-D_up.png', V5P + [DPT], BAG, 'D', ('D', 'V5-D_up.png', 41), ('GA', 'V5-GACE_up.png', 40), 0, '音孔'),
 'V5-GAC': ('V5-GACE_up.png', V5P + [GAPT], BAG, 'GA', ('D', 'V5-D_up.png', 41), ('GA', 'V5-GACE_up.png', 40), 1, '音孔'),
 'V5-GACE': ('V5-GACE_up.png', [('想上台的人選這把', '插電款，接音箱就能表演'), V5P[0], ('GA 桶缺角好抱好按', '腰細不卡手，高把位也好按')], BAG, 'GA',
             ('D', 'V5-D_up.png', 41), ('GA', 'V5-GACE_up.png', 40), 1, '音孔'),
 'V8-D': ('V8-D_up.png', V8P + [DPT], '附 調音器・彈片・原廠硬盒', 'D', ('D', 'V8-D_up.png', 41), ('GA', 'V8-GAC_up.png', 40), 0, '鮑魚貝音孔'),
 'V8-GAC': ('V8-GAC_up.png', V8P + [GAPT], '附 調音器・彈片・原廠硬盒', 'GA', ('D', 'V8-D_up.png', 41), ('GA', 'V8-GAC_up.png', 40), 1, '鮑魚貝音孔'),
 'TOGO-SE': ('TOGO_S_Front_up.png', [('出門帶得走的吉他', '34 吋小尺寸，好背好收'), ('插電款 隨時能表演', '內建拾音器，接音箱就能彈'), ('手小、初學也好按', '琴身小、弦長短，按和弦不吃力')],
             '附 調音器・彈片・原廠厚琴袋', 'T', ('STD', 'V1-DC-2_up.png', 41), ('T', 'TOGO_S_Front_up.png', 34), 0, '音孔'),
 'TOGO-ME': ('Togo-ME_up.png', [('出門帶得走的吉他', '34 吋小尺寸，好背好收'), ('插電款 隨時能表演', '內建拾音器，接音箱就能彈'), ('桃花心木 溫暖音色', '琴身小但聲音不單薄')],
             '附 調音器・彈片・原廠厚琴袋', 'T', ('STD', 'V1-DC-2_up.png', 41), ('T', 'Togo-ME_up.png', 34), 0, '音孔'),
}
NOTE = {'V2-DC': '※ 照片為插電款，外觀相同（側邊沒有前級）', 'V3-DC': '※ 照片為插電款，外觀相同（側邊沒有前級）', 'V5-GAC': '※ 照片為插電款，外觀相同（側邊沒有前級）'}

os.makedirs('out', exist_ok=True)
ec.card_brand('out/brand.jpg', VEE + 'out/V8-D_s5_wide.jpg')
for m in (sys.argv[1:] or M):
    cut, pts, acc, key, L, R, ca, ros = M[m]
    wide = sorted(glob.glob(VEE + f'out/{m}_s*_wide.jpg')); close = sorted(glob.glob(VEE + f'out/{m}_s*_close.jpg'))
    sc = wide[0]
    ec.card_points(m, cut, pts, acc, sc, f'out/{m}_m2.jpg')
    cmpnote = '標準吉他與旅行琴，依實際長度比例' if key == 'T' else '同系列 D 桶與 GA 桶，依實際長度比例'
    ec.card_compare(key, L, R, f'out/{m}_m3.jpg', sc, note=cmpnote)
    ec.card_detail(m, cut, ca, f'out/{m}_m4.jpg', sc, ['琴頭', ros, '琴橋', '缺角設計' if ca else '琴頸接合'])
    import shutil; shutil.copy('out/brand.jpg', f'out/{m}_m5.jpg')
    ec.card_scene(close[0], f'out/{m}_m6.jpg')
    print(m, 'ok', os.path.basename(close[0]))
from PIL import Image, ImageDraw
for m, t in NOTE.items():
    if sys.argv[1:] and m not in sys.argv[1:]: continue
    p = f'out/{m}_m2.jpg'; o = Image.open(p); d = ImageDraw.Draw(o); f = ec.fnt(ec.SANS, 20, 400)
    d.text((440, 900), t, font=f, fill=(200, 175, 150)); o.save(p, quality=93)
for m in (sys.argv[1:] or M):
    p = f'out/{m}_m2.jpg'; o = Image.open(p); d = ImageDraw.Draw(o); f = ec.fnt(ec.SANS, 20, 400)
    d.text((440, 932), '※ 配件以實際出貨為主', font=f, fill=(200, 175, 150)); o.save(p, quality=93)
