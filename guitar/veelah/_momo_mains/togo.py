import ec
from ec import *
from PIL import Image, ImageDraw
def card(this, out):
    o = dark_bg(VEE + f'out/{this}_s11_wide.jpg' if this=='TOGO-SE' else VEE + 'out/TOGO-ME_s14_wide.jpg', .86); tiles(o); d = ImageDraw.Draw(o)
    t = 'TOGO-SE 還是 TOGO-ME？'; f = fnt(SERIF, 52, 900); d.text(((SZ - d.textlength(t, font=f)) / 2, 44), t, font=f, fill=CREAM)
    t2 = '同一個琴身，差在面板木頭'; f2 = fnt(SANS, 26, 400); d.text(((SZ - d.textlength(t2, font=f2)) / 2, 112), t2, font=f2, fill=SOFT)
    for m, cutf, cx in (('TOGO-SE', 'TOGO_S_Front_up.png', 250), ('TOGO-ME', 'Togo-ME_up.png', 750)):
        im = Image.open(CUT + cutf).convert('RGBA'); im = im.crop(im.getbbox()); h = 380; im = im.resize((int(im.width * h / im.height), h), Image.LANCZOS)
        x = int(cx - im.width / 2); y = 165
        if m == this:
            g = Image.new('L', o.size, 0); g.paste(im.split()[3], (x, y))
            o.paste(Image.new('RGB', o.size, GOLD), (0, 0), g.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * .7)))
        o.paste(im, (x, y), im)
        lab = m + ('（這把）' if m == this else ''); fl = fnt(SERIF, 36, 900)
        d.text((cx - d.textlength(lab, font=fl) / 2, 556), lab, font=fl, fill=GOLD if m == this else SOFT)
    rows = [('面板', '雲杉單板', '桃花心木單板'), ('音色', '明亮清脆、刷起來有亮度', '溫暖圓潤、中音比較厚'),
            ('外觀', '淺色原木、清爽', '深咖啡木紋、復古'), ('適合', '刷和弦、自彈自唱', '指彈、輕輕唱歌')]
    y = 620
    for k, a, b in rows:
        d.rounded_rectangle([60, y, 940, y + 60], 12, fill=(70, 28, 14))
        fk = fnt(SANS, 26, 700); d.text((500 - d.textlength(k, font=fk) / 2, y + 13), k, font=fk, fill=GOLD)
        for txt, cx, mine in ((a, 250, this == 'TOGO-SE'), (b, 750, this == 'TOGO-ME')):
            ft = fit_font(d, txt, SANS, 27, 600 if mine else 400, 360)
            d.text((cx - d.textlength(txt, font=ft) / 2, y + 13), txt, font=ft, fill=CREAM if mine else (205, 185, 165))
        y += 72
    t3 = '兩支都一樣：34 吋小琴身・插電款・鐵木指板・附原廠厚琴袋'; f3 = fit_font(d, t3, SANS, 24, 500, 880)
    d.text(((SZ - d.textlength(t3, font=f3)) / 2, 922), t3, font=f3, fill=GOLD)
    o.save(out, quality=93)
for m in ('TOGO-SE', 'TOGO-ME'): card(m, f'out/{m}_mse.jpg')
