"""Veelah MOMO/PChome 主圖卡（電商西班牙暖色風，跟官網米色風分開）。
主圖排法：1 白底 2 賣點 3 桶身比較 4 細節 5 品牌 6 場景"""
import sys, os, json
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
GK = 'C:/Users/User/AppData/Local/Temp/claude/ee212e1eeeb8db2e/4a4f221c-ec60-428d-8a3c-72ee0111d362/scratchpad/gweb'
VEE = 'C:/Users/User/AppData/Local/Temp/claude/ee212e1eeeb8db2e/ebab9218-68ed-4462-8e1b-e6e84aacc40f/scratchpad/vee/'
CUT = VEE + 'cut/'
SERIF = 'C:/Windows/Fonts/NotoSerifTC-VF.ttf'; SANS = 'C:/Windows/Fonts/NotoSansTC-VF.ttf'
SZ = 1000
CREAM = (255, 246, 232); GOLD = (242, 193, 78); TERRA = (200, 69, 42); BLUE = (31, 90, 168); DARK = (58, 22, 12)
SOFT = (251, 233, 210)


def fnt(p, s, w):
    f = ImageFont.truetype(p, s)
    try: f.set_variation_by_axes([w])
    except Exception: pass
    return f


def parts(im):
    a = np.asarray(im)[..., 3] > 128; w = a.sum(1).astype(float); H = len(w)
    top = int(np.argmax(w > 0)); hw = np.median(w[top + int(.02 * H):top + int(.08 * H)])
    he = top + int(.02 * H) + int(np.argmax(w[top + int(.02 * H):] < 0.6 * hw))
    nw = np.median(w[he + int(.03 * H):he + int(.15 * H)])
    bs = he + int(np.argmax(w[he:] > 2.5 * nw))
    bot = H - int(np.argmax(w[::-1] > 0)); bw = int(w[bs:bot].max())
    cols = np.where(a[bs:bot].any(0))[0]; cx = int((cols.min() + cols.max()) / 2)
    return top, he, bs, bot, bw, cx


def tiles(o):
    d = ImageDraw.Draw(o); cs = [TERRA, GOLD, BLUE, GOLD]
    for y in (0, SZ - 22):
        for i, x in enumerate(range(0, SZ, 26)):
            d.rectangle([x, y, x + 25, y + 21], fill=cs[i % 4])


def dark_bg(scene=None, alpha=0.78):
    if scene and os.path.exists(scene):
        b = Image.open(scene).convert('RGB').resize((SZ, SZ)).filter(ImageFilter.GaussianBlur(6))
    else:
        b = Image.new('RGB', (SZ, SZ), DARK)
    ov = Image.new('RGB', (SZ, SZ), (40, 14, 6))
    o = Image.blend(b, ov, alpha)
    # 暗角
    yy, xx = np.mgrid[0:SZ, 0:SZ] / SZ
    v = 1 - 0.45 * np.clip(((xx - .5) ** 2 + (yy - .5) ** 2) * 2.2, 0, 1)
    o = Image.fromarray((np.asarray(o).astype(float) * v[..., None]).clip(0, 255).astype(np.uint8))
    return o


def paste_fit(o, im, box, shadow=True):
    c = im.crop(im.getbbox()); x0, y0, x1, y1 = box
    s = min((x1 - x0) / c.width, (y1 - y0) / c.height)
    c = c.resize((max(1, int(c.width * s)), max(1, int(c.height * s))), Image.LANCZOS)
    px, py = x0 + (x1 - x0 - c.width) // 2, y0 + (y1 - y0 - c.height) // 2
    if shadow:
        sh = Image.new('L', o.size, 0); sh.paste(c.split()[3].point(lambda v: int(v * .55)), (px + 14, py + 16))
        o.paste(Image.new('RGB', o.size, (10, 3, 0)), (0, 0), sh.filter(ImageFilter.GaussianBlur(16)))
    o.paste(c, (px, py), c)
    return px, py, c.width, c.height


def fit_font(d, t, path, size, wt, maxw):
    f = fnt(path, size, wt)
    while d.textlength(t, font=f) > maxw and size > 16:
        size -= 1; f = fnt(path, size, wt)
    return f


def badge(o, text, xy):
    """附件徽章：紅底黃框（杰哥 11/20 附件徽章要亮眼，不寫贈送）"""
    d = ImageDraw.Draw(o); f = fnt(SANS, 30, 700)
    w = int(d.textlength(text, font=f)) + 56; x, y = xy
    d.rounded_rectangle([x, y, x + w, y + 64], 32, fill=TERRA, outline=GOLD, width=4)
    d.text((x + 28, y + 12), text, font=f, fill=(255, 255, 255))


# ---------------- 2 賣點 ----------------
def card_points(m, cutf, pts, accessory, scene, out):
    o = dark_bg(scene, .82); tiles(o); d = ImageDraw.Draw(o)
    im = Image.open(CUT + cutf).convert('RGBA')
    paste_fit(o, im, (40, 70, 400, 930))
    x = 440
    d.text((x, 90), 'Veelah', font=fnt('C:/Windows/Fonts/georgiai.ttf' if os.path.exists('C:/Windows/Fonts/georgiai.ttf') else SERIF, 40, 400), fill=GOLD)
    d.text((x, 140), m, font=fnt(SERIF, 76, 900), fill=CREAM)
    d.line([x, 250, x + 90, 250], fill=GOLD, width=4)
    y = 290
    for i, (t, sub) in enumerate(pts):
        d.ellipse([x, y + 4, x + 54, y + 58], fill=GOLD)
        n = str(i + 1); fn = fnt(SANS, 32, 800)
        d.text((x + 27 - d.textlength(n, font=fn) / 2, y + 8), n, font=fn, fill=DARK)
        f = fit_font(d, t, SERIF, 44, 800, 470)
        d.text((x + 74, y), t, font=f, fill=CREAM)
        d.text((x + 74, y + 62), sub, font=fit_font(d, sub, SANS, 27, 400, 470), fill=SOFT)
        y += 160
    badge(o, accessory, (x, 800))
    o.save(out, quality=93)


# ---------------- 3 桶身比較 ----------------
SHAPES = {
    'D': ('D 桶', 'DREADNOUGHT', ['音量大、低音厚', '刷和弦最有力', '自彈自唱首選']),
    'GA': ('GA 桶', 'GRAND AUDITORIUM', ['腰細好抱、聲音平衡', '指彈、刷扣都好聽', '大多數人都適合']),
    'T': ('旅行琴', 'TRAVEL 3/4', ['比一般吉他小一號', '手小、小朋友好按', '出門露營好帶']),
}


def silhouette(cutf, h, col):
    im = Image.open(CUT + cutf).convert('RGBA'); im = im.crop(im.getbbox())
    s = h / im.height; im = im.resize((int(im.width * s), int(h)), Image.LANCZOS)
    a = im.split()[3]; sil = Image.new('RGBA', im.size, col + (255,)); sil.putalpha(a)
    return sil, im


def card_compare(this_key, left, right, out, scene=None, note=None):
    """left/right = (key, cutout, 長度吋)；用實際長度比例縮放"""
    o = dark_bg(scene, .86); tiles(o); d = ImageDraw.Draw(o)
    t = '桶身怎麼選？'
    f = fnt(SERIF, 60, 900); d.text(((SZ - d.textlength(t, font=f)) / 2, 50), t, font=f, fill=CREAM)
    base = 600; mx = max(left[2], right[2])
    for (k, cutf, inch), cx in ((left, 270), (right, 730)):
        h = base * inch / mx
        mine = (k == this_key)
        _, im = silhouette(cutf, h, (0, 0, 0))
        y0 = 150 + (base - h)
        if mine:
            g = Image.new('L', o.size, 0); g.paste(im.split()[3], (int(cx - im.width / 2), int(y0)))
            o.paste(Image.new('RGB', o.size, GOLD), (0, 0), g.filter(ImageFilter.GaussianBlur(18)).point(lambda v: int(v * .7)))
            o.paste(im, (int(cx - im.width / 2), int(y0)), im)
        else:
            sil, _ = silhouette(cutf, h, (150, 110, 80))
            o.paste(sil, (int(cx - sil.width / 2), int(y0)), sil.split()[3].point(lambda v: int(v * .9)))
        name, en, lines = SHAPES[k]
        ty = 770
        fn = fnt(SERIF, 46, 900)
        lab = name + ('（這把）' if mine else '')
        col = GOLD if mine else SOFT
        d.text((cx - d.textlength(lab, font=fn) / 2, ty), lab, font=fn, fill=col)
        for j, ln in enumerate(lines):
            fl = fnt(SANS, 27, 500 if mine else 400)
            d.text((cx - d.textlength(ln, font=fl) / 2, ty + 64 + j * 38), ln, font=fl, fill=CREAM if mine else (200, 180, 160))
    d.line([500, 200, 500, 740], fill=(120, 80, 60), width=2)
    if note:
        fl = fnt(SANS, 20, 400); d.text(((SZ - d.textlength(note, font=fl)) / 2, 948), note, font=fl, fill=(190, 160, 140))
    o.save(out, quality=93)


# ---------------- 4 細節 ----------------
def card_detail(m, cutf, cutaway, out, scene=None, labels=None):
    o = dark_bg(scene, .88); tiles(o); d = ImageDraw.Draw(o)
    im = Image.open(CUT + cutf).convert('RGBA'); top, he, bs, bot, bw, cx = parts(im); bh = bot - bs
    t = '細節近看'; f = fnt(SERIF, 56, 900); d.text(((SZ - d.textlength(t, font=f)) / 2, 44), t, font=f, fill=CREAM)

    def rect(cy, wd, ht):
        return im.crop((int(cx - wd / 2), int(cy - ht / 2), int(cx + wd / 2), int(cy + ht / 2)))
    hs = he - top
    crops = [
        (rect((top + he) / 2 + .01 * im.height, hs * 1.2, hs * 1.2), labels[0] if labels else '琴頭'),
        (rect(bs + .36 * bh, bw * .6, bw * .6), labels[1] if labels else '音孔'),
        (rect(bs + .72 * bh, bw * .75, bw * .75), labels[2] if labels else '琴橋'),
        (im.crop((int(cx + .02 * bw), int(bs - .06 * bh), int(cx + .58 * bw), int(bs - .06 * bh + .56 * bw))) if cutaway else rect(bs + .02 * bh, bw * .7, bw * .7), labels[3] if labels else ('缺角設計' if cutaway else '琴頸接合')),
    ]
    W = 420; gap = 40; x0 = (SZ - 2 * W - gap) // 2; y0 = 140
    for i, (c, lab) in enumerate(crops):
        x = x0 + (i % 2) * (W + gap); y = y0 + (i // 2) * (W + 0)
        tile = Image.new('RGB', (W, W - 60), (238, 226, 206))
        cc = c.copy(); s = min(W / cc.width, (W - 60) / cc.height); cc = cc.resize((int(cc.width * s), int(cc.height * s)), Image.LANCZOS)
        tile.paste(cc, ((W - cc.width) // 2, (W - 60 - cc.height) // 2), cc)
        o.paste(tile, (x, y))
        d.rectangle([x, y, x + W - 1, y + W - 61], outline=GOLD, width=3)
        fl = fnt(SANS, 30, 700); d.text((x + (W - d.textlength(lab, font=fl)) / 2, y + W - 52), lab, font=fl, fill=GOLD)
    o.save(out, quality=93)


# ---------------- 5 品牌 ----------------
def card_brand(out, scene):
    o = dark_bg(scene, .72); tiles(o); d = ImageDraw.Draw(o)
    lg = Image.open(VEE + 'brand/logo.png').convert('RGBA'); lg = lg.crop(lg.getbbox())
    s = 300 / lg.width; lg = lg.resize((300, int(lg.height * s)), Image.LANCZOS)
    o.paste(lg, ((SZ - 300) // 2, 90), lg)
    t1 = '三代製琴家族的吉他'; f = fnt(SERIF, 62, 900); d.text(((SZ - d.textlength(t1, font=f)) / 2, 260), t1, font=f, fill=CREAM)
    t2 = 'Since 1971 · Third-generation luthiers'; f2 = fnt('C:/Windows/Fonts/georgiai.ttf' if os.path.exists('C:/Windows/Fonts/georgiai.ttf') else SERIF, 28, 400)
    d.text(((SZ - d.textlength(t2, font=f2)) / 2, 350), t2, font=f2, fill=GOLD)
    items = [('50+', '年', '1971 年開始做琴，傳到第三代'), ('12', '國', '台灣出發，12 個國家都有經銷'), ('唯一', '', '天然木紋＋拼花，沒有兩把一樣')]
    y = 450
    for big, unit, txt in items:
        d.rounded_rectangle([110, y, 890, y + 130], 18, fill=(70, 28, 14), outline=(160, 110, 60), width=2)
        fb = fnt(SERIF, 72, 900); bw = d.textlength(big, font=fb)
        d.text((150, y + 18), big, font=fb, fill=GOLD)
        d.text((150 + bw + 8, y + 58), unit, font=fnt(SANS, 30, 700), fill=GOLD)
        d.text((370, y + 42), txt, font=fit_font(d, txt, SANS, 34, 500, 490), fill=CREAM)
        y += 152
    o.save(out, quality=93)


def card_scene(src, out):
    im = Image.open(src).convert('RGB')
    w, h = im.size; s = min(w, h)
    im.crop(((w - s) // 2, (h - s) // 2, (w - s) // 2 + s, (h - s) // 2 + s)).resize((SZ, SZ), Image.LANCZOS).save(out, quality=93)


if __name__ == '__main__':
    os.makedirs('out', exist_ok=True)
    sc = VEE + 'out/V2-GAC_s5_wide.jpg'
    card_points('V2-GAC', 'V2-GAC_up.png',
                [('第一把單板琴的好選擇', '一萬出頭就有雲杉單板的清亮聲音'),
                 ('拿出來就很好看', '拼花音孔＋亮光漆，低調但有質感'),
                 ('GA 桶好抱好彈', '腰細不卡手，指彈刷扣都好聽')],
                '附 調音器・彈片・原廠琴袋', sc, 'out/V2-GAC_m2.jpg')
    card_compare('GA', ('D', 'V2-DCE_kr_up.png', 41), ('GA', 'V2-GAC_up.png', 40), 'out/V2-GAC_m3.jpg', sc,
                 note='同系列 D 桶與 GA 桶，依實際長度比例')
    card_detail('V2-GAC', 'V2-GAC_up.png', 1, 'out/V2-GAC_m4.jpg', sc, ['琴頭', '拼花音孔', '琴橋', '缺角設計'])
    card_brand('out/V2-GAC_m5.jpg', VEE + 'out/V8-D_s5_wide.jpg')
    card_scene(VEE + 'out/V2-GAC_s5_close.jpg', 'out/V2-GAC_m6.jpg')
