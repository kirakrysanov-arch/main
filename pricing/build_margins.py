"""Cost & margin sheet: purchase cost (from Ozon analytics report), Ozon vs website profit per unit.

Inputs:  report.xlsx (Товарная аналитика, Ozon, 01–24.11.2026) — path as argv[1]
         ../palitra-woocommerce.csv, ../palitra-ozon-prices.xlsx (Ozon + site prices)
Output:  ../palitra-prices-and-margins.xlsx
"""
import csv, os, re, sys, collections
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACQUIRING = 0.022   # Ozon Pay internet acquiring, top of the published range
SITE_TAX = 0.06     # tax on website revenue (report: tax ≈ 6% of what Ozon pays out)


def num(v):
    if v in (None, ''):
        return 0.0
    return float(str(v).replace(' ', '').replace('\xa0', '').replace(',', '.'))


def main(report_path):
    ws = openpyxl.load_workbook(report_path, data_only=True).active
    rows = list(ws.iter_rows(values_only=True))
    rep = [dict(zip(rows[0], r)) for r in rows[1:] if r[0]]
    by_sku = {str(r['SKU']).strip(): r for r in rep}
    by_art = {str(r['Артикул']).strip(): r for r in rep}

    cat = {c['SKU']: c for c in csv.DictReader(open(os.path.join(ROOT, 'palitra-woocommerce.csv'), encoding='utf-8-sig'))}
    pw = openpyxl.load_workbook(os.path.join(ROOT, 'palitra-ozon-prices.xlsx')).active
    items = []
    for r in pw.iter_rows(min_row=2, values_only=True):
        category, line, name, sku, ozon, site = r[:6]
        if 'Pocket Box' in line:
            line = 'Van Gogh Pocket Box (12 кювет)'
        c = cat[sku]
        rr = by_sku.get(str(c['Meta: ozon_sku']).strip()) or by_art.get(sku.strip())
        cost = num(rr['Себестоимость за шт (руб)']) if rr else 0.0
        it = dict(category=category, line=line, name=name, sku=sku, ozon=ozon, site=site,
                  cost=cost or None, cost_src='отчёт Ozon' if cost else '')
        # real Ozon result per unit, if it sold in the period
        units = num(rr['Продажи (шт.)']) if rr else 0
        if rr and units > 0:
            fees = sum(num(rr[k]) for k in ('Комиссия МП (руб.)', 'Логистика (руб.)', 'Хранение (руб.)', 'Штрафы (руб.)',
                                            'Приемка товара (руб.)', 'Реклама (руб.)', 'Прочие удержания (руб.)', 'Налог (руб.)'))
            fees -= num(rr['Доплаты МП(руб.)'])
            kept = (num(rr['Продажи (руб.)']) - fees) / units
            it['ozon_keep_ratio'] = kept / ozon  # share of the shop-window price you actually keep
            it['ozon_src'] = 'факт за ноябрь'
        items.append(it)

    # Fill missing cost from an identical product in the same line with the same Ozon price, else same line (median)
    line_costs = collections.defaultdict(list)
    for it in items:
        if it['cost']:
            line_costs[(it['line'], it['ozon'])].append(it['cost'])
            line_costs[(it['line'], None)].append(it['cost'] / it['ozon'])
    for it in items:
        if it['cost']:
            continue
        same = line_costs.get((it['line'], it['ozon']))
        if same:
            it['cost'] = round(sum(same) / len(same))
            it['cost_src'] = 'по аналогу (та же линейка и цена)'
        elif line_costs.get((it['line'], None)):
            ratios = sorted(line_costs[(it['line'], None)])
            it['cost'] = round(ratios[len(ratios) // 2] * it['ozon'])
            it['cost_src'] = 'оценка по линейке'
        else:
            it['cost_src'] = 'нет данных'

    # Ozon keep-ratio: product's own, else line average, else overall average
    allr = [it['ozon_keep_ratio'] for it in items if 'ozon_keep_ratio' in it]
    overall = sum(allr) / len(allr)
    line_r = collections.defaultdict(list)
    for it in items:
        if 'ozon_keep_ratio' in it:
            line_r[it['line']].append(it['ozon_keep_ratio'])
    for it in items:
        if 'ozon_keep_ratio' not in it:
            lr = line_r.get(it['line'])
            it['ozon_keep_ratio'] = sum(lr) / len(lr) if lr else overall
            it['ozon_src'] = 'среднее по линейке' if lr else 'среднее по магазину'
        it['ozon_keep'] = round(it['ozon'] * it['ozon_keep_ratio'])
        it['site_keep'] = round(it['site'] * (1 - ACQUIRING - SITE_TAX))
        if it['cost']:
            it['ozon_profit'] = it['ozon_keep'] - it['cost']
            it['site_profit'] = it['site_keep'] - it['cost']
            # costs per sale = purchase cost + channel fees (site: acquiring + tax; Ozon: all marketplace fees + tax)
            it['site_costs'] = it['cost'] + (it['site'] - it['site_keep'])
            it['ozon_costs'] = it['cost'] + (it['ozon'] - it['ozon_keep'])
            it['site_margin'] = it['site_profit'] / it['site_costs']
            it['ozon_margin'] = it['ozon_profit'] / it['ozon_costs']
        else:
            it['ozon_profit'] = it['site_profit'] = it['site_margin'] = it['ozon_margin'] = None
            it['site_costs'] = it['ozon_costs'] = None

    # ---- workbook
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = 'Цены и маржа'
    head = ['Себестоимость, ₽', 'Источник себестоимости', 'Категория', 'Линейка', 'Товар', 'Артикул',
            'Цена Ozon, ₽', 'Остаётся с Ozon, ₽', 'Прибыль Ozon, ₽', 'Маржа Ozon, % к затратам', 'Данные Ozon',
            'Цена на сайте, ₽', 'Затраты сайт (себест. + эквайринг + налог), ₽', 'Прибыль сайт, ₽', 'Маржа сайт, % к затратам', 'Сайт vs Ozon, ₽']
    ws.append(head)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True, vertical='top')
    warn = PatternFill('solid', fgColor='FCE4E4')
    est = PatternFill('solid', fgColor='FFF4D6')
    for it in items:
        diff = (it['site_profit'] - it['ozon_profit']) if it['cost'] else None
        ws.append([it['cost'], it['cost_src'], it['category'], it['line'], it['name'], it['sku'],
                   it['ozon'], it['ozon_keep'], it['ozon_profit'], it['ozon_margin'], it['ozon_src'],
                   it['site'], it['site_costs'], it['site_profit'], it['site_margin'], diff])
        r = ws.max_row
        for col in (10, 15):
            ws.cell(r, col).number_format = '0%'
        for col in (1, 7, 8, 9, 12, 13, 14, 16):
            ws.cell(r, col).number_format = '# ##0'
        if it['cost_src'] != 'отчёт Ozon':
            ws.cell(r, 1).fill = est
            ws.cell(r, 2).fill = est
        if it['site_margin'] is not None and it['site_margin'] < 0.2:
            for col in (14, 15):
                ws.cell(r, col).fill = warn
    widths = [14, 24, 24, 34, 70, 34, 12, 14, 13, 13, 18, 13, 18, 13, 13, 13]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = 'C2'
    ws.auto_filter.ref = ws.dimensions

    # summary per line
    s = wb.create_sheet('Сводка по линейкам')
    s.append(['Линейка', 'Товаров', 'Себестоимость, ₽', 'Цена Ozon, ₽', 'Прибыль Ozon, ₽', 'Маржа Ozon, % к затратам', 'Цена сайт, ₽', 'Прибыль сайт, ₽', 'Маржа сайт, % к затратам'])
    for c in s[1]:
        c.font = Font(bold=True)
    L = collections.OrderedDict()
    for it in items:
        L.setdefault(it['line'], []).append(it)
    summary = []
    for line, its in L.items():
        def rng(key):
            v = sorted({it[key] for it in its if it[key] is not None})
            if not v:
                return '—'
            f = lambda x: f'{int(round(x)):,}'.replace(',', ' ')
            return f(v[0]) if len(v) == 1 else f'{f(v[0])} – {f(v[-1])}'
        def pct(key):
            m = [it[key] for it in its if it[key] is not None]
            if not m:
                return '—'
            a, b = round(min(m) * 100), round(max(m) * 100)
            return f'{a}%' if a == b else f'{a}–{b}%'
        row = [line, len(its), rng('cost'), rng('ozon'), rng('ozon_profit'), pct('ozon_margin'), rng('site'), rng('site_profit'), pct('site_margin')]
        s.append(row)
        summary.append(row)
    for i, w in enumerate([42, 9, 18, 18, 18, 16, 18, 18, 16], 1):
        s.column_dimensions[get_column_letter(i)].width = w

    n = wb.create_sheet('Как считали')
    for line in [
        'Себестоимость — «Себестоимость за шт» из отчёта Ozon (01–24.11.2026), без логистики, таможни и доставки.',
        'Если товара нет в отчёте — себестоимость взята у такого же товара той же линейки и цены (жёлтая заливка), иначе «нет данных».',
        'Остаётся с Ozon — сколько вы реально получаете за 1 шт после комиссии, логистики, рекламы, прочих удержаний и налога: по факту продаж за ноябрь, иначе среднее по линейке/магазину.',
        f'Остаётся с сайта — цена на сайте минус эквайринг Ozon Pay {ACQUIRING*100:.1f}% и налог {SITE_TAX*100:.0f}%. Доставка не учтена.',
        'Прибыль = Остаётся − Себестоимость.',
        'Маржа, % к затратам = Прибыль ÷ (Себестоимость + эквайринг + налог) для сайта; для Ozon — Прибыль ÷ (Себестоимость + все удержания Ozon и налог).',
        'Пример: цена 12 000 ₽, себестоимость 6 277 ₽ → затраты 6 277 + 264 + 720 = 7 261 ₽, прибыль 4 739 ₽, маржа 4 739 ÷ 7 261 = 65%.',
        'Красная заливка — маржа на сайте ниже 20% к затратам.',
    ]:
        n.append([line])
    n.column_dimensions['A'].width = 140

    out = os.path.join(ROOT, 'palitra-prices-and-margins.xlsx')
    wb.save(out)
    srcs = collections.Counter(it['cost_src'] for it in items)
    print('saved', out, dict(srcs))
    print('overall Ozon keep ratio %.2f' % overall)
    for row in summary:
        print(' | '.join(str(x) for x in row))
    low = [it for it in items if it['site_margin'] is not None and it['site_margin'] < 0.2]
    print('low margin on site (<20% of costs):', [(it['name'][:50], round(it['site_margin'] * 100)) for it in low])
    better = sum(1 for it in items if it['cost'] and it['site_profit'] >= it['ozon_profit'])
    print('site profit >= ozon profit for', better, 'of', sum(1 for it in items if it['cost']))


if __name__ == '__main__':
    main(sys.argv[1])
