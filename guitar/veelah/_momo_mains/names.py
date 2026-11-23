import re, requests, io, json, sys
app = io.open('D:/Coding/yu-toolbox/app.py', encoding='utf-8').read()
TOK = re.search(r'token=([A-Za-z0-9_-]+)', app).group(1)
B = 'https://momo-integration-production.up.railway.app'
W = lambda s: sum(2 if ord(c) > 127 else 1 for c in s)

BAG, CASE, THICK = '原廠琴袋', '原廠硬盒', '原廠厚琴袋'
# model: (MOMO 品名(不含品牌), MOMO 特色標語<=15, PC 前台品名(含品牌), 主賣點1/2/3, 第一段, 適合誰)
D = {
 'V2-GAC': ('V2-GAC 面單吉他 木吉他 40吋 GA桶缺角 雲杉單板 桃花心木背側 附琴袋（民謠吉他 拼花音孔 進階 社團）',
            '拼花音孔 亮光漆面單琴',
            'Veelah V2-GAC 雲杉面單板 民謠吉他 木吉他 40吋 GA桶缺角 桃花心木背側 附原廠琴袋',
            ['第一把單板琴的好選擇 雲杉單板聲音清亮', '拼花音孔＋亮光漆 低調有質感', 'GA桶腰細好抱 指彈刷扣都好聽 附原廠琴袋'],
            '想換第一把單板琴、又想要外觀有質感的人：從入門琴升級、社團練團、自彈自唱、指彈都適合。'),
 'V2-DC': ('V2-DC 面單吉他 木吉他 41吋 D桶缺角 雲杉單板 桃花心木背側 附琴袋（民謠吉他 拼花音孔 進階 社團）',
           '拼花音孔 亮光漆面單琴',
           'Veelah V2-DC 雲杉面單板 民謠吉他 木吉他 41吋 D桶缺角 桃花心木背側 附原廠琴袋',
           ['第一把單板琴的好選擇 雲杉單板聲音清亮', '拼花音孔＋亮光漆 低調有質感', 'D桶聲音大 刷和弦有力 附原廠琴袋'],
           '想換第一把單板琴、又想要外觀有質感的人：從入門琴升級、社團練團、刷和弦自彈自唱都適合。'),
 'V3-DC': ('V3-DC 面單吉他 木吉他 41吋 D桶缺角 雲杉單板 非洲胡桃木背側 附琴袋（民謠吉他 溫潤 進階 社團）',
           '非洲胡桃木 溫潤好聽',
           'Veelah V3-DC 雲杉面單板 民謠吉他 木吉他 41吋 D桶缺角 非洲胡桃木背側 附原廠琴袋',
           ['想要溫暖音色選這把 非洲胡桃木背側聲音溫潤', '霧面消光塗裝 低調耐看 手感自然', 'D桶聲音大 刷和弦有力 附原廠琴袋'],
           '喜歡溫暖、厚一點的聲音，想從入門琴升級的人：社團、自彈自唱、刷和弦都適合。'),
 'V3-GAC': ('V3-GAC 面單吉他 木吉他 40吋 GA桶缺角 雲杉單板 非洲胡桃木背側 附琴袋（民謠吉他 溫潤 進階 社團）',
            '非洲胡桃木 溫潤好聽',
            'Veelah V3-GAC 雲杉面單板 民謠吉他 木吉他 40吋 GA桶缺角 非洲胡桃木背側 附原廠琴袋',
            ['想要溫暖音色選這把 非洲胡桃木背側聲音溫潤', '霧面消光塗裝 低調耐看 手感自然', 'GA桶腰細好抱 指彈刷扣都好聽 附原廠琴袋'],
            '喜歡溫暖、厚一點的聲音，想從入門琴升級的人：指彈、自彈自唱、社團都適合，GA 桶抱起來不卡手。'),
 'V5-D': ('V5-D 面單吉他 木吉他 41吋 D桶 雲杉單板 玫瑰木背側 黑檀指板 附原廠琴袋（民謠吉他 進階 自彈自唱）',
          '雲杉配玫瑰木 經典面單',
          'Veelah V5-D 雲杉面單板 民謠吉他 木吉他 41吋 D桶 玫瑰木背側 黑檀指板 附原廠琴袋',
          ['經典配方 一把用很久 雲杉單板＋玫瑰木背側', '進階換琴的首選 黑檀木指板與琴橋手感更順', 'D桶聲音大 刷和弦有力 附原廠琴袋'],
          '已經彈一陣子、想換一把可以用很久的琴的人：自彈自唱、刷和弦特別有感。'),
 'V5-GAC': ('V5-GAC 面單吉他 木吉他 40吋 GA桶缺角 雲杉單板 玫瑰木背側 黑檀指板 附原廠琴袋（民謠吉他 進階 指彈）',
            '雲杉配玫瑰木 經典面單',
            'Veelah V5-GAC 雲杉面單板 民謠吉他 木吉他 40吋 GA桶缺角 玫瑰木背側 黑檀指板 附原廠琴袋',
            ['經典配方 一把用很久 雲杉單板＋玫瑰木背側', '進階換琴的首選 黑檀木指板與琴橋手感更順', 'GA桶腰細好抱 指彈刷扣都好聽 附原廠琴袋'],
            '已經彈一陣子、想換一把可以用很久的琴的人：指彈、自彈自唱都好聽，GA 桶抱起來舒服。'),
 'V5-GACE': ('V5-GACE 插電木吉他 電木吉他 面單 40吋 GA桶缺角 雲杉單板 玫瑰木背側 附琴袋（民謠吉他 拾音器 表演）',
             '插電面單 接音箱就能彈',
             'Veelah V5-GACE 插電木吉他 雲杉面單板 民謠吉他 40吋 GA桶缺角 玫瑰木背側 內建拾音器 附原廠琴袋',
             ['想上台的人選這把 插電款接音箱就能表演', '經典配方 雲杉單板＋玫瑰木背側 聲音飽滿', 'GA桶缺角好抱 高把位好按 附原廠琴袋'],
             '想上台、街頭、教會或咖啡廳表演的人：不插電是一把好聽的面單吉他，插上音箱就能直接用。'),
 'V8-D': ('V8-D 全單吉他 木吉他 41吋 D桶 雲杉 玫瑰木 全單板 附原廠硬盒（民謠吉他 鮑魚貝音孔 進階 收藏）',
          '全單板 鮑魚貝音孔',
          'Veelah V8-D 全單板 民謠吉他 木吉他 41吋 D桶 雲杉面板 玫瑰木單板背側 鮑魚貝音孔 附原廠硬盒',
          ['Veelah 頂級系列 雲杉＋玫瑰木全單板 越彈越開', '收藏等級外觀 鮑魚貝音孔＋虎紋楓木滾邊', 'D桶聲音大 低音厚 附原廠硬盒'],
          '想要一把全單板、聲音和外觀都到位的人：進階玩家換琴、收藏、自彈自唱都適合。'),
 'V8-GAC': ('V8-GAC 全單吉他 木吉他 40吋 GA桶缺角 雲杉 玫瑰木 全單板 附原廠硬盒（民謠吉他 鮑魚貝音孔 進階 收藏）',
            '全單板 鮑魚貝音孔',
            'Veelah V8-GAC 全單板 民謠吉他 木吉他 40吋 GA桶缺角 雲杉面板 玫瑰木單板背側 鮑魚貝音孔 附原廠硬盒',
            ['Veelah 頂級系列 雲杉＋玫瑰木全單板 越彈越開', '收藏等級外觀 鮑魚貝音孔＋虎紋楓木滾邊', 'GA桶缺角好抱 指彈表現細膩 附原廠硬盒'],
            '想要一把全單板、聲音和外觀都到位的人：進階玩家換琴、收藏、指彈都適合。'),
 'TOGO-SE': ('TOGO-SE 旅行吉他 插電木吉他 34吋 雲杉面單 內建拾音器 附原廠厚琴袋（民謠吉他 小尺寸 兒童 露營）',
             '34吋插電旅行吉他',
             'Veelah TOGO-SE 旅行吉他 插電木吉他 34吋 雲杉面單板 內建拾音器 民謠吉他 附原廠厚琴袋',
             ['出門帶得走的吉他 34吋小琴身好背好收', '插電款 內建拾音器 接音箱就能表演', '手小、小朋友、初學都好按 附原廠厚琴袋'],
             '想出門、露營、旅行帶著彈的人，或手比較小、小朋友第一把琴：琴身小、好按，在家當練習琴也好用。'),
 'TOGO-ME': ('TOGO-ME 旅行吉他 插電木吉他 34吋 桃花心木面單 內建拾音器 附原廠厚琴袋（民謠吉他 小尺寸 兒童 露營）',
             '34吋插電旅行吉他',
             'Veelah TOGO-ME 旅行吉他 插電木吉他 34吋 桃花心木面單板 內建拾音器 民謠吉他 附原廠厚琴袋',
             ['出門帶得走的吉他 34吋小琴身好背好收', '桃花心木面單 聲音溫暖不單薄', '插電款 內建拾音器 附原廠厚琴袋'],
             '想出門、露營、旅行帶著彈的人，或手比較小、小朋友第一把琴：喜歡溫暖、柔和的聲音選這支。'),
}
bad = []
for m, (mn, hl, pc, sl, who) in D.items():
    if len(mn) > 60: bad.append((m, 'momo name', len(mn)))
    if len(hl) > 15: bad.append((m, 'headline', len(hl)))
    if W(pc) > 96: bad.append((m, 'pc name', W(pc)))
    for i, x in enumerate(sl):
        if W(x) > 82: bad.append((m, f'slogan{i+1}', W(x)))
    for w in ('最', '第一名', '冠軍', '贈'):
        for t in [mn, hl, pc, who] + sl:
            if w in t: bad.append((m, 'word', w, t))
if bad:
    for b in bad: print('BAD', b)
    sys.exit(1)
if '--go' not in sys.argv:
    print('check ok'); sys.exit()
items = requests.get(f'{B}/api/listing/products?token={TOK}', timeout=60).json()['items']
json.dump([p for p in items if p.get('brand') == 'Veelah'], open('backup_names_1121.json', 'w', encoding='utf-8'), ensure_ascii=False)
for p in items:
    m = p.get('model')
    if m not in D or p.get('brand') != 'Veelah': continue
    mn, hl, pc, sl, who = D[m]
    desc = p.get('description') or ''
    desc = desc.replace('36吋', '34吋').replace('36 吋', '34 吋')
    first = desc.split('\n\n')[0]
    kw = pc.replace('Veelah ', 'Veelah ', 1) + '。'
    if first.startswith('Veelah ' + m): rest = desc.split('\n\n', 1)[1] if '\n\n' in desc else ''
    else: rest = desc
    desc = kw + '\n\n適合誰：' + who + '\n\n' + rest
    patch = dict(name='【Veelah】' + mn, headline=hl, salesName=pc, tagLine=sl[0], slogan2=sl[1], slogan3=sl[2], description=desc)
    if p.get('spec'): patch['spec'] = p['spec'].replace('36吋', '34吋').replace('36 吋', '34 吋')
    r = requests.put(f'{B}/api/listing/products/{p["id"]}?token={TOK}', json=patch, timeout=60).json()
    q = r['product']
    print(p['id'], m, r.get('ok'), all(q.get(k) == v for k, v in patch.items()), '36吋' in json.dumps(q, ensure_ascii=False))
