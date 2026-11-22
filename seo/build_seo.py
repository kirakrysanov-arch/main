"""Generate Russian SEO descriptions, titles and meta descriptions for the Palitra catalog.

Input:  ../palitra-woocommerce.csv, ../product-photos/*-map.json (official names),
        colours.json (colour families).
Output: palitra-seo-update.csv (WooCommerce importer, update existing by SKU).
"""
import csv, json, glob, re, hashlib, html, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# Brand facts kept deliberately general and well established.
BRANDS = {
    'Unison Colour': dict(ru='Юнисон Колор', alt='Unison, «Юнисон»', country='Великобритания',
        fact='Пастель Unison Colour изготавливают вручную в Нортумберленде (Англия) небольшими партиями; палитра славится сложными природными оттенками.'),
    'Terry Ludwig': dict(ru='Терри Людвиг', alt='«Терри Людвиг Пастелс»', country='США',
        fact='Terry Ludwig — американская мастерская ручной пастели; квадратные палочки с высокой концентрацией пигмента дают насыщенный бархатистый штрих.'),
    'Schmincke': dict(ru='Шминке', alt='«Шмике», «Шминк»', country='Германия',
        fact='Schmincke — немецкий производитель художественных красок, работающий с 1881 года; мягкая пастель Schmincke известна очень мягкой текстурой и чистотой цвета.'),
    'Sennelier': dict(ru='Сеннелье', alt='«Сенелье», «Сенилье»', country='Франция',
        fact='Sennelier — парижский дом художественных материалов, основанный в 1887 году; его краски и пастель ценят за яркость и плотность пигмента.'),
    'Rembrandt': dict(ru='Рембрандт', alt='Royal Talens Rembrandt', country='Нидерланды',
        fact='Rembrandt — профессиональная серия нидерландской компании Royal Talens; мягкая пастель Rembrandt отличается высокой светостойкостью и ровной мягкостью.'),
    'Royal Talens': dict(ru='Роял Таленс', alt='«Ройал Таленс», Talens', country='Нидерланды',
        fact='Royal Talens — нидерландский производитель художественных материалов, основанный в 1899 году (бренды Rembrandt, Van Gogh, Amsterdam, Cobra).'),
    'Van Gogh': dict(ru='Ван Гог', alt='Talens Van Gogh', country='Нидерланды',
        fact='Van Gogh — серия качественных материалов для художников от Royal Talens (Нидерланды).'),
    'Winsor&Newton': dict(ru='Винзор энд Ньютон', alt='Winsor & Newton, «Винзор и Ньютон», «Виндзор Ньютон»', country='Великобритания',
        fact='Winsor & Newton — британская компания, производящая краски для художников с 1832 года.'),
    'Michael Harding': dict(ru='Майкл Хардинг', alt='«Майкл Хардин»', country='Великобритания',
        fact='Michael Harding — лондонский производитель профессиональных масляных и акварельных красок с высокой концентрацией пигмента.'),
    'PanPastel': dict(ru='ПанПастель', alt='Pan Pastel, «Пан Пастель»', country='США',
        fact='PanPastel — сухая пастель в формате кювет: наносится спонжами и инструментами Sofft и смешивается почти как краска, давая минимум пыли.'),
    'Jack Richeson': dict(ru='Джек Ричесон', alt='Richeson, «Ричесон»', country='США',
        fact='Jack Richeson & Co. — американский производитель художественных материалов; ручные пастели Richeson Handrolled собраны в наборы по тону и цвету.'),
    'Holbein': dict(ru='Хольбейн', alt='«Холбейн»', country='Япония',
        fact='Holbein — японский производитель профессиональных красок; гуашь серии Irodori передаёт традиционные японские цвета.'),
    'Art Spectrum': dict(ru='Арт Спектрум', alt='«Артспектрум»', country='Австралия',
        fact='Art Spectrum — австралийский производитель художественных материалов, известный пастелью и пастельной бумагой Colourfix.'),
    'Old Holland': dict(ru='Олд Холланд', alt='«Олд Холанд»', country='Нидерланды',
        fact='Old Holland — нидерландский производитель масляных красок высшего класса по классическим рецептурам.'),
    'Daniel Smith': dict(ru='Дэниел Смит', alt='«Даниэль Смит»', country='США',
        fact='Daniel Smith — американский производитель акварели (Сиэтл), известный необычными минеральными и гранулирующими пигментами.'),
    'J. Luda': dict(ru='Джей Люда', alt='J.Luda, «Люда»', country='',
        fact='J. Luda — мягкая пастель ручной работы с плотным насыщенным пигментом; наборы подобраны по тону и настроению.'),
    'Mount Vision': dict(ru='Маунт Вижн', alt='«Маунт Вижен»', country='Непал',
        fact='Mount Vision — мягкая пастель ручной работы из Непала, крупные палочки с щедрым количеством пигмента.'),
    'Lyra': dict(ru='Лира', alt='LYRA', country='Германия',
        fact='LYRA — немецкий производитель карандашей и материалов для рисования, работающий с 1806 года.'),
    "General's": dict(ru='Дженералс', alt='General Pencil, «Дженерал»', country='США',
        fact="General's (General Pencil Company) — американский производитель карандашей для художников, работающий с 1889 года."),
}

COLOUR_TEXT = {
    'Красные': 'красные', 'Оранжевые': 'оранжевые', 'Жёлтые': 'жёлтые', 'Зелёные': 'зелёные',
    'Бирюзовые': 'бирюзовые', 'Синие': 'синие', 'Фиолетовые': 'фиолетовые', 'Розовые': 'розовые',
    'Коричневые и земляные': 'коричневые и земляные', 'Серые': 'серые', 'Белые': 'белые',
    'Тёмные': 'тёмные', 'Светлые': 'светлые', 'Разноцветные': 'разнообразные',
}

USE = {
    'Мягкая пастель': [
        'Мягкая пастель даёт бархатистый матовый штрих, легко растушёвывается и хорошо ложится слоями.',
        'Подходит для пейзажа, портрета и натюрморта на пастельной бумаге с зерном (Sennelier La Carte, Pastelmat, UART, Colourfix).',
        'Готовую работу удобно защищать фиксативом и оформлять под стекло.'],
    'Сухая пастель PanPastel': [
        'Пастель наносится спонжами Sofft, аппликаторами или кистью и смешивается прямо на бумаге, как краска.',
        'Подходит для живописи, тонировки фона, смешанной техники и работы поверх акварели и графики.',
        'Кювета 9 мл расходуется очень экономно, а пыли почти нет.'],
    'Масляная пастель': [
        'Масляная пастель даёт яркий насыщенный штрих, хорошо перекрывает и смешивается пальцем или растворителем.',
        'Подходит для бумаги, картона, холста и дерева.'],
    'Масляные краски': [
        'Масляные краски подходят для живописи на холсте, картоне и дереве, а также для лессировок и пастозной техники.',
        'Для разбавления используют разбавители и медиумы на основе масла.'],
    'Акварель': [
        'Акварель подходит для пейзажей, ботанической иллюстрации, скетчинга и работы на природе.',
        'Лучше всего раскрывается на хлопковой акварельной бумаге плотностью от 300 г/м².'],
    'Гуашь': [
        'Гуашь даёт плотные матовые заливки и хорошо перекрывает предыдущие слои.',
        'Подходит для иллюстрации, дизайна, леттеринга и живописи на бумаге и картоне.'],
    'Акрил': [
        'Акриловые краски быстро сохнут, подходят для холста, картона, дерева и смешанной техники.',
        'Разбавляются водой, а после высыхания становятся водостойкими.'],
    'Бумага': [
        'Бумага с зерном удерживает несколько слоёв пастели и хорошо подходит для растушёвки.'],
    'Карандаши и кисти': [
        'Подходят для рисунка, скетчинга, графики и смешанной техники.'],
}

OILSTICK = ['Масляная краска в форме стика: рисуете как пастелью, а получаете фактуру масляной живописи.',
            'Подходит для холста, картона и бумаги для масла, смешивается с обычными масляными красками и медиумами.',
            'Стик со временем покрывается защитной плёнкой, которую легко снять салфеткой.']
BRUSH = ['Кисти для акварели с упругим ворсом хорошо держат форму кончика и подходят для деталей и тонких линий.']
PENCIL = ['Подходят для рисунка, тонального эскиза и графики; водорастворимые грифели можно размывать кистью.']


TYPE_RU = {'Мягкая пастель': 'Пастель', 'Сухая пастель PanPastel': 'Пастель', 'Масляная пастель': 'Масляная пастель',
           'Масляные краски': 'Масляные краски', 'Акварель': 'Акварель', 'Гуашь': 'Гуашь', 'Акрил': 'Акриловые краски',
           'Бумага': 'Бумага для пастели', 'Карандаши и кисти': 'Карандаши'}

GENERIC = [r'\bUnison\b', r'Пастель', r'пастели', r'кистей', r'Кисти для акварели', r'Бумага для пастели', r'Карандаши', r'Набор\w*', r'мягкой', r'масляной', r'масляных', r'акварельных', r'акриловых', r'гуаши', r'красок',
           r'Масляная краска в форме стика', r'Масляная краска', r'Акварельные краски', r'Художественн\w*,?', r'мягкая',
           r'Мягкая художественная', r'Профессиональная пастель', r'Сухая', r'Великобритания', r'США', r'Нидерланды',
           r'\(?половин\w*\)?', r'\d+\s*цвет\w*', r'по \d+\s*мл', r'\d+x\d+ ?ml', r'\d+шт', r'\(\d+ шт\)', r'\(\d+ цвет\w*\)',
           r'Soft Pastel', r'\bMini\b', r'\bSET\b', r'\bSet\b', r'Extra-fine', r'Artists', r'professional', r'\(Терри Людвиг\)',
           r'Talens', r'Pastels?']

def set_label(name, brand):
    s = name
    for b in (brand, brand.replace('&', ' & '), 'Winsor & Newton', 'Royal Talens', 'Van Gogh', 'UNISON COLOUR HANDMADE SOFT PASTELS', 'ART SPECTRUM', 'LYRA'):
        s = re.sub(re.escape(b), ' ', s, flags=re.I)
    for g in GENERIC:
        s = re.sub(g, ' ', s, flags=re.I)
    s = re.sub(r'[()]', ' ', s)
    s = re.sub(r'\s+', ' ', s).strip(' -,')
    if s.isupper() or (s.upper() == s and len(s) > 3):
        s = s.title()
    s = s.replace('Introductory', 'Introductory').replace('Brownintroductory', 'Brown Introductory').replace('Michieintroductory', 'Michie Introductory')
    return s

PP_SUFFIX = {'1': 'экстра-тёмный оттенок (Extra Dark)', '3': 'затемнённый оттенок (Shade)', '5': 'чистый цвет',
             '7': 'осветлённый оттенок', '8': 'светлый оттенок (Tint)'}


def pick(key, options):
    h = int(hashlib.md5(key.encode()).hexdigest(), 16)
    return options[h % len(options)]


def short_name(name):
    n = re.sub(r'\s*Художественн\w*.*$|\s*Мягкая художественная.*$|\s*Профессиональная пастель.*$', '', name).strip()
    return n


def plural(n, one, few, many):
    n = int(n)
    if n % 10 == 1 and n % 100 != 11:
        return one
    if 2 <= n % 10 <= 4 and not 12 <= n % 100 <= 14:
        return few
    return many


def load():
    rows = list(csv.DictReader(open(os.path.join(ROOT, 'palitra-woocommerce.csv'), encoding='utf-8-sig')))
    src = {}
    for f in glob.glob(os.path.join(ROOT, 'product-photos', '*-map.json')):
        for k, v in json.load(open(f)).items():
            src[k] = v.get('src', '')
    colours = json.load(open(os.path.join(HERE, 'colours.json')))
    return rows, src, colours


def build(r, src, colours):
    name = r['Name']
    brand = r['Brands']
    b = BRANDS[brand]
    kind = r['Attribute 2 value(s)']
    cat = r['Categories']
    count = r['Attribute 3 value(s)']
    fam = [COLOUR_TEXT[c] for c in colours.get(r['SKU'], []) if c in COLOUR_TEXT]
    sname = short_name(name)
    brand_both = f'{b["ru"]} ({brand.replace("&", " & ")})'
    is_half = 'половин' in name.lower() or 'half' in src.get(r['SKU'], '').lower()
    oilstick = 'стика' in name
    lower = name.lower()

    # --- what it is
    label = set_label(name, brand)
    if count:
        label = re.sub(r'\s+' + re.escape(str(count)) + r'$', '', label).strip()
    type_ru = 'Масляные краски в стиках' if oilstick else TYPE_RU.get(kind, TYPE_RU.get(cat.split(' > ')[0], ''))
    if 'Кисти' in name:
        type_ru = 'Кисти для акварели'
    if 'Карандаш' in name:
        type_ru = re.sub(r'\s*(LYRA|General.s)\s*\d*шт.*$', '', name).replace('Набор карандашей', 'Карандаши').strip()
        label = ''
    label = re.sub(r'\s*\d+-$', '', label).strip()
    if '1-18' in name and '1-18' not in label:
        label = re.sub(r'\s1$', ' 1-18', label)
    # special cases
    if 'Бумага' in name:
        type_ru, label = 'Бумага для пастели', 'Naples Yellow, 6 листов 30×40 см'
    if brand == "General's":
        type_ru, label = 'Карандаши', 'Black & White'
    if 'Michael Harding 60ml' in name:
        type_ru, label = 'Масляная краска', re.sub(r'.*60ml\s*', '', name) + ', 60 мл'
    if brand == 'Van Gogh':
        label = 'серия 191 (000, 0, 2), 3 шт'
    if brand == 'Royal Talens':
        label = 'Van Gogh ' + label
    size = ''
    if count and 'Кисти' not in name:
        size = f'{count} {plural(count, "половинка", "половинки", "половинок")}' if is_half else f'{count} {plural(count, "цвет", "цвета", "цветов")}'
        if 'карандаш' in name.lower():
            size = f'{count} шт'
        if '(3 шт)' in name:
            size = '3 палочки'
    pp_name = ''
    if brand == 'PanPastel':
        code = re.search(r'PanPastel (\d{3}(?:\.\d)?)', name).group(1)
        off = re.sub(r'\s*\(\d.*$', '', src.get(r['SKU'], '')).strip()
        pp_name = f'{code} {off}'.strip()
        tone = PP_SUFFIX.get(code.split('.')[-1], '') if '.' in code else ''
        if code == '010':
            what = 'ПанПастель (PanPastel) 010 Colorless Blender — бесцветный блендер в кювете 9 мл. Помогает смягчать переходы, высветлять цвет и создавать прозрачные тонкие слои.'
        elif code == '011':
            what = 'ПанПастель (PanPastel) 011 Pearl Medium White Fine — перламутровый медиум в кювете 9 мл. Добавляет мелкое мерцание поверх любого цвета или смешивается с пастелью.'
        else:
            what = f'Сухая пастель ПанПастель (PanPastel) {pp_name} — кювета 9 мл' + (f', {tone}.' if tone else '.')
    elif '(3 шт)' in name:
        what = f'Мягкая пастель Шминке (Schmincke) {label}: упаковка из 3 палочек одного цвета. Удобно докупить любимый оттенок, который быстро расходуется.'
    elif oilstick:
        what = f'Набор масляных красок в форме стиков {brand_both} «{label}».'
    elif 'Кисти' in name:
        what = f'Набор из 3 кистей для акварели {brand_both}, серия 191, размеры 000, 0 и 2.'
    else:
        what = (f'{type_ru} {brand_both} «{label}»' if label else f'{type_ru} {brand_both}') + (f' — {size}.' if size else '.')
    title_core = (f'{type_ru} {brand.replace("&", " & ")} {pp_name or label}').strip()
    title_core = re.sub(r'\s+', ' ', title_core)
    parts = [what]
    if fam and brand != 'PanPastel' and 'Кисти' not in name and 'карандаш' not in name.lower():
        if fam == ['разнообразные']:
            parts.append('Набор собран из гармоничных оттенков разных цветовых групп.')
        else:
            parts.append('Цветовая гамма: ' + ', '.join(f for f in fam if f != 'разнообразные') + ' оттенки.')
    parts.append(b['fact'])

    if oilstick:
        use = OILSTICK
    elif 'Кисти' in name:
        use = BRUSH
    elif 'Карандаш' in name:
        use = PENCIL
    else:
        use = USE.get(kind) or USE.get(cat.split(' > ')[0]) or []
    body = ' '.join(use)

    alt = f'Бренд также ищут как {b["alt"]}.' if b.get('alt') else ''
    country = f'Страна производителя: {b["country"]}.' if b['country'] else ''
    buy = pick(r['SKU'], [
        'В магазине «Палитра» — только оригинальная продукция, отправка за 1–2 дня и доставка по всей России.',
        'Купить с доставкой по всей России в магазине художественных материалов «Палитра». Только оригинальная продукция.',
        'Заказывайте в интернет-магазине «Палитра»: оригинальные материалы, быстрая отправка и доставка по России.'])

    desc_html = (
        f'<p>{html.escape(" ".join(parts), quote=False)}</p>\n'
        + (f'<p>{html.escape(body, quote=False)}</p>\n' if body else '')
        + '<ul>'
        + f'<li>Бренд: {html.escape(brand_both, quote=False)}</li>'
        + (f'<li>{html.escape(country[:-1], quote=False)}</li>' if country else '')
        + (f'<li>Количество в наборе: {count}{" (половинки)" if is_half else ""}</li>' if count and 'Кисти' not in name else '')
        + (f'<li>Цвет: {html.escape(", ".join(fam), quote=False)}</li>' if fam and 'Кисти' not in name and 'карандаш' not in name.lower() else '')
        + '</ul>\n'
        + f'<p>{html.escape(alt + " " + buy, quote=False).strip()}</p>'
    )

    short = ' '.join(parts[:1]) + (' ' + parts[1] if len(parts) > 2 and len(parts[0]) < 140 else '')
    short = short[:300]

    title_tail = (f', {size}' if size and brand != 'PanPastel' else '') + f' ({b["ru"]})'
    seo_title = f'{title_core}{title_tail} — купить | Палитра'
    fam_txt = [f for f in fam if f != 'разнообразные']
    meta = f'{title_core}' + (f', {size}' if size and brand != 'PanPastel' else '') + f' — {b["ru"]}'
    if fam_txt and 'Кисти' not in name and 'карандаш' not in name.lower():
        meta += ', ' + ', '.join(fam_txt[:2]) + ' оттенки'
    meta += '. ' + pick(r['SKU'] + 'm', ['Оригинал, доставка по России.', 'Отправка за 1–2 дня, доставка по России.', 'Только оригинал. Доставка по всей России.'])
    if len(meta) > 160:
        meta = meta[:157].rsplit(' ', 1)[0] + '…'
    tags = [t.strip() for t in r['Tags'].split(',') if t.strip()]
    for t in (b['ru'].lower(), kind.lower() if kind else ''):
        if t and t not in tags:
            tags.append(t)
    return {
        'SKU': r['SKU'],
        'Description': desc_html,
        'Short description': short,
        'Tags': ', '.join(tags),
        'Meta: pl_seo_title': seo_title,
        'Meta: pl_seo_description': meta,
    }


def main():
    rows, src, colours = load()
    out = [build(r, src, colours) for r in rows]
    cols = ['SKU', 'Description', 'Short description', 'Tags', 'Meta: pl_seo_title', 'Meta: pl_seo_description']
    with open(os.path.join(ROOT, 'palitra-seo-update.csv'), 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(out)
    lens = [len(re.sub('<[^>]+>', '', o['Description'])) for o in out]
    print('rows', len(out), 'desc chars min/avg/max', min(lens), sum(lens) // len(lens), max(lens))
    descs = [re.sub('<[^>]+>', '', o['Description']) for o in out]
    print('unique descriptions', len(set(descs)))
    for o in out[:: max(1, len(out) // 6)]:
        print('\n=== ', o['SKU'])
        print('TITLE:', o['Meta: pl_seo_title'])
        print('META :', o['Meta: pl_seo_description'])
        print('SHORT:', o['Short description'])
        print(o['Description'])


if __name__ == '__main__':
    main()
