import os as _o
def _find_repo():
    d = _o.path.dirname(_o.path.abspath(__file__))
    while d and not _o.path.isdir(_o.path.join(d, "08_Jordanian_Unemployment_Truth")):
        nd = _o.path.dirname(d)
        if nd == d: break
        d = nd
    return d
REPO = _o.environ.get("REPO_ROOT") or _find_repo()
"""Generates pbip/JordanUnemployment.SemanticModel (TMDL): tables from ../data/*.csv, DAX SVG measures. Kill Desktop (own instance) before running."""
import os, json, csv, uuid, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA = os.path.join(ROOT, 'data')
SM = os.path.join(ROOT, 'pbip', 'JordanUnemployment.SemanticModel')
NS = uuid.UUID('9e1d7a44-0c1e-4a6e-9d51-7a0f2b2c9e55'); tag = lambda s: str(uuid.uuid5(NS, s))

INT = {'Quarter': ['Order'], 'Annual': ['Year', 'Unemployed', 'Employed', 'LabourForce'],
       'DimGov': ['Order', 'Unemployed', 'LabourForce'], 'Dots': ['Idx', 'Row', 'Col'], 'LegendKey': ['GroupOrder', 'Count'], 'Lens': ['LensOrder']}
DBL = {'Quarter': ['Total', 'Male', 'Female', 'HotX', 'HotY'], 'Annual': ['RateDerived'], 'DimGov': ['Rate', 'Share', 'CX', 'CY', 'R', 'RowY', 'HotMapY', 'HotRowY', 'HotRowX'], 'LegendKey': ['MidY'], 'Facts': ['Value']}
TABLES = ['Quarter', 'Annual', 'DimGov', 'Dots', 'LegendKey', 'Lens', 'Facts']

INK = 'rgb(28,27,25)'; CLAY = 'rgb(181,71,46)'; SLATE = 'rgb(62,76,82)'; MUTE = 'rgb(64,55,47)'; SAND = 'rgb(216,200,168)'; RULE = 'rgb(207,198,179)'; PAPER = 'rgb(241,236,226)'; MIST = 'rgb(230,223,208)'
PCT = '&%2337;'
URI = '"data:image/svg+xml;utf8,"'
def svg(w, h, body): return f'{URI} & "<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'{w}\' height=\'{h}\' viewBox=\'0 0 {w} {h}\'>" & {body} & "</svg>"'
def F(x): return x if x >= 18 else round(x * 1.13, 1)
def T(x, y, txt, size, fill, font='Segoe UI', weight=400, anchor='start', ls=0):
    size = F(size)
    """static text element as a DAX string literal; txt may be a DAX expression if wrapped by caller via TD"""
    return f'"<text x=\'{x}\' y=\'{y}\' font-family=\'{font}\' font-size=\'{size}\' font-weight=\'{weight}\' fill=\'{fill}\' text-anchor=\'{anchor}\' letter-spacing=\'{ls}\'>{txt}</text>"'
def TD(x, y, expr, size, fill, font='Segoe UI', weight=400, anchor='start'):
    size = F(size)
    """dynamic text: expr is a DAX expression"""
    return f'"<text x=\'{x}\' y=\'{y}\' font-family=\'{font}\' font-size=\'{size}\' font-weight=\'{weight}\' fill=\'{fill}\' text-anchor=\'{anchor}\'>" & ({expr}) & "</text>"'
def chip(x, y, label, kind):
    w = int(len(label) * 8.0 + 24)
    fills = {'pub': (INK, PAPER), 'der': (CLAY, PAPER), 'lim': (SAND, INK)}[kind]
    return f'"<rect x=\'{x}\' y=\'{y - 14}\' width=\'{w}\' height=\'20\' fill=\'{fills[0]}\'/><text x=\'{x + 11}\' y=\'{y}\' font-family=\'Segoe UI Semibold\' font-size=\'12.4\' fill=\'{fills[1]}\' letter-spacing=\'0.4\'>{label}</text>"', w
FACT = lambda k: f'LOOKUPVALUE(Facts[Value], Facts[Key], "{k}")'

MEAS = []
def M(name, expr, fmt=None, cat=None, folder=None): MEAS.append(dict(name=name, expr=expr, fmt=fmt, cat=cat, folder=folder))

# =========================================================== PAGE 1
M('SelQ', 'SELECTEDVALUE(Quarter[Order], 18)', folder='1 Number')
M('SelQ Label', 'LOOKUPVALUE(Quarter[Label], Quarter[Order], [SelQ])', folder='1 Number')
c1, w1 = chip(0, 112, 'DoS PUBLISHED', 'pub'); c2, w2 = chip(w1 + 8, 112, 'JORDANIAN CITIZENS ONLY', 'lim')
HERO = f'''VAR o = [SelQ]
VAR lab = [SelQ Label]
VAR v = LOOKUPVALUE(Quarter[Total], Quarter[Order], o)
RETURN {svg(700, 130, ' & '.join([TD(0, 72, 'FORMAT(v, "0.0") & "' + PCT + '"', 64, CLAY, 'Georgia', 700), T(240, 48, 'of Jordanian citizens in the labour force', 14, INK, 'Segoe UI Semibold', 600), TD(240, 70, '"were unemployed in " & lab & " (age 15+)."', 14, MUTE), c1, c2]))}'''
M('Hero SVG', HERO, cat='ImageUrl', folder='1 Number')

# chart geometry (local): x 22..772, y: 15% -> 314, 36% -> 24
X = lambda o: f'(22 + ({o} - 1) * 718 / 17)'
Y = lambda v: f'(314 - ({v} - 15) * 290 / 21)'
def series(col, stroke, w):
    return (f'"<path d=\'" & CONCATENATEX(ALL(Quarter), IF(Quarter[Order] = 1, "M", "L") & ROUND({X("Quarter[Order]")}, 1) & "," & ROUND({Y("Quarter[" + col + "]")}, 1), " ", Quarter[Order]) '
            f'& "\' fill=\'none\' stroke=\'{stroke}\' stroke-width=\'{w}\' stroke-linejoin=\'round\'/>"')
def hollow(col, basis, stroke):
    return (f'CONCATENATEX(FILTER(ALL(Quarter), Quarter[{basis}] = "chart label"), "<circle cx=\'" & ROUND({X("Quarter[Order]")}, 1) & "\' cy=\'" & ROUND({Y("Quarter[" + col + "]")}, 1) & "\' r=\'4\' fill=\'{PAPER}\' stroke=\'{stroke}\' stroke-width=\'1.6\'/>", "", Quarter[Order])')
def seldot(col, stroke, r):
    return f'"<circle cx=\'" & ROUND({X("o")}, 1) & "\' cy=\'" & ROUND({Y("LOOKUPVALUE(Quarter[" + col + "], Quarter[Order], o)")}, 1) & "\' r=\'{r}\' fill=\'{stroke}\'/>"'
GRID = '"' + ''.join(f"<line x1='22' y1='{314 - (v - 15) * 290 / 21:.1f}' x2='740' y2='{314 - (v - 15) * 290 / 21:.1f}' stroke='{RULE}' stroke-width='0.8'/><text x='17' y='{314 - (v - 15) * 290 / 21 + 4:.1f}' font-family='Segoe UI' font-size='13.0' text-anchor='end' fill='{MUTE}'>{v}</text>" for v in (15, 20, 25, 30, 35)) + ''.join(f"<text x='{22 + i * 718 / 17:.1f}' y='340' font-family='Segoe UI' font-size='12.4' text-anchor='middle' fill='{MUTE}'>{lab}</text>" for i, lab in ((0, 'Q1 2022'), (3, 'Q4 2022'), (6, 'Q3 2023'), (9, 'Q2 2024'), (12, 'Q1 2025'), (15, 'Q4 2025'))) + '"'
CHART = f'''VAR o = [SelQ]
VAR plateau = FILTER(ALL(Quarter), Quarter[Order] >= 9)
VAR mn = MINX(plateau, Quarter[Total])
VAR mx = MAXX(plateau, Quarter[Total])
VAR n = COUNTROWS(plateau)
VAR lastT = LOOKUPVALUE(Quarter[Total], Quarter[Order], 18)
VAR lastM = LOOKUPVALUE(Quarter[Male], Quarter[Order], 18)
VAR lastF = LOOKUPVALUE(Quarter[Female], Quarter[Order], 18)
VAR yb = {Y("mx")} - 38
RETURN {svg(900, 344, ' & '.join([
    GRID,
    f'"<rect x=\'" & ROUND({X(9)}, 1) & "\' y=\'" & ROUND({Y("mx")}, 1) & "\' width=\'" & ROUND({X(18)} - {X(9)}, 1) & "\' height=\'" & ROUND({Y("mn")} - {Y("mx")}, 1) & "\' fill=\'{SAND}\'/>"',
    f'"<line x1=\'" & ROUND({X('o')}, 1) & "\' y1=\'24\' x2=\'" & ROUND({X('o')}, 1) & "\' y2=\'314\' stroke=\'{RULE}\' stroke-width=\'1.5\' stroke-dasharray=\'3 3\'/>"',
    series('Female', CLAY, 1.6), series('Male', SLATE, 1.6), series('Total', INK, 3.6),
    hollow('Female', 'FemaleBasis', CLAY), hollow('Male', 'MaleBasis', SLATE),
    seldot('Female', CLAY, 5), seldot('Male', SLATE, 5), seldot('Total', INK, 6.5),
    f'"<line x1=\'" & ROUND({X(9)}, 1) & "\' y1=\'" & ROUND(yb, 1) & "\' x2=\'" & ROUND({X(18)}, 1) & "\' y2=\'" & ROUND(yb, 1) & "\' stroke=\'{INK}\'/><line x1=\'" & ROUND({X(9)}, 1) & "\' y1=\'" & ROUND(yb - 5, 1) & "\' x2=\'" & ROUND({X(9)}, 1) & "\' y2=\'" & ROUND(yb + 5, 1) & "\' stroke=\'{INK}\'/><line x1=\'" & ROUND({X(18)}, 1) & "\' y1=\'" & ROUND(yb - 5, 1) & "\' x2=\'" & ROUND({X(18)}, 1) & "\' y2=\'" & ROUND(yb + 5, 1) & "\' stroke=\'{INK}\'/>"',
    f'"<text x=\'" & ROUND(({X(9)} + {X(18)}) / 2, 1) & "\' y=\'" & ROUND(yb - 10, 1) & "\' font-family=\'Segoe UI Semibold\' font-size=\'13.6\' font-weight=\'700\' text-anchor=\'middle\' fill=\'{INK}\'>" & n & " quarters between " & FORMAT(mn, "0.0") & "{PCT} and " & FORMAT(mx, "0.0") & "{PCT}</text>"',
    f'"<text x=\'752\' y=\'" & ROUND({Y("lastF")} + 4, 1) & "\' font-family=\'Segoe UI Semibold\' font-size=\'13.6\' font-weight=\'700\' fill=\'{CLAY}\'>Women " & FORMAT(lastF, "0.0") & "</text><text x=\'752\' y=\'" & ROUND({Y("lastT")} + 4, 1) & "\' font-family=\'Segoe UI Semibold\' font-size=\'13.6\' font-weight=\'700\' fill=\'{INK}\'>All Jordanians " & FORMAT(lastT, "0.0") & "</text><text x=\'752\' y=\'" & ROUND({Y("lastM")} + 4, 1) & "\' font-family=\'Segoe UI Semibold\' font-size=\'13.6\' font-weight=\'700\' fill=\'{SLATE}\'>Men " & FORMAT(lastM, "0.0") & "</text>"',
    f'"<text x=\'" & ROUND({X('o')} + (IF(o > 14, -8, 8)), 1) & "\' y=\'16\' font-family=\'Segoe UI Semibold\' font-size=\'13.6\' font-weight=\'700\' text-anchor=\'" & IF(o > 14, "end", "start") & "\' fill=\'{INK}\'>" & [SelQ Label] & "  ·  " & FORMAT(LOOKUPVALUE(Quarter[Total], Quarter[Order], o), "0.0") & "{PCT}  ·  men " & FORMAT(LOOKUPVALUE(Quarter[Male], Quarter[Order], o), "0.0") & "  ·  women " & FORMAT(LOOKUPVALUE(Quarter[Female], Quarter[Order], o), "0.0") & "</text>"',
]))}'''
M('Chart SVG', CHART, cat='ImageUrl', folder='1 Number')

# ruler (local 432 x 520): rows at y=70,198,326
def row(i, title, sub, key, hl):
    y = 60 + i * 112
    col = CLAY if hl else INK
    parts = []
    if hl: parts.append(f'"<rect x=\'24\' y=\'{y - 34}\' width=\'400\' height=\'104\' fill=\'{SAND}\' opacity=\'0.6\'/>"')
    parts += [T(40, y, title, 18, INK, 'Georgia', 700), T(40, y + 20, sub, 12, MUTE),
              f'"<line x1=\'40\' y1=\'{y + 48}\' x2=\'400\' y2=\'{y + 48}\' stroke=\'{RULE}\' stroke-width=\'1.2\'/><line x1=\'40\' y1=\'{y + 48}\' x2=\'" & ROUND(40 + 360 * {FACT(key)} / 35, 1) & "\' y2=\'{y + 48}\' stroke=\'{col}\' stroke-width=\'3\'/><circle cx=\'" & ROUND(40 + 360 * {FACT(key)} / 35, 1) & "\' cy=\'{y + 48}\' r=\'7\' fill=\'{col}\'/>"',
              TD(400, y + 14, f'FORMAT({FACT(key)}, "0.0") & "{PCT}"', 24, col, 'Georgia', 700, 'end')]
    return parts
cr, wr_ = chip(40, 446, 'DoS PUBLISHED  ·  Q2 2026', 'pub')
RULER = f'''{svg(432, 470, ' & '.join(row(0, 'All residents', 'Jordanians and non-Jordanians together', 'AllRes', False) + row(1, 'Jordanians', 'citizens, age 15+', 'Jord', True) + row(2, 'Jordanian women', 'citizens, age 15+', 'JordWomen', False) + [
    TD(40, 372, f'"Non-Jordanian residents: " & FORMAT({FACT("NonJord")}, "0.0") & "{PCT}."', 12, MUTE),
    TD(40, 392, f'"Expatriate workers are " & FORMAT({FACT("ExpatShare")}, "0") & "{PCT} of the employed"', 12, MUTE),
    TD(40, 412, '"(Q2 2026), so the all-resident rate is lower."', 12, MUTE), cr]))}'''
M('Ruler SVG', RULER, cat='ImageUrl', folder='1 Number')
AY = lambda y, col: f'LOOKUPVALUE(Annual[{col}], Annual[Year], {y})'
cp, wp = chip(40, 146, 'DERIVED FROM DoS COUNTS', 'der')
PEOPLE = f'''VAR dE = {AY(2025, 'Employed')} - {AY(2020, 'Employed')}
VAR dU = {AY(2025, 'Unemployed')} - {AY(2020, 'Unemployed')}
RETURN {svg(432, 150, ' & '.join([
    TD(40, 44, '"+" & FORMAT(dE, "#,0")', 34, INK, 'Georgia', 700), T(230, 44, 'more Jordanians employed', 13, MUTE),
    TD(40, 88, '"+" & FORMAT(dU, "#,0")', 34, CLAY, 'Georgia', 700), T(230, 88, 'more Jordanians unemployed', 13, MUTE),
    TD(40, 118, f'"Rate over the same years: " & FORMAT({AY(2020, "RateDerived")}, "0.0") & "{PCT} to " & FORMAT({AY(2025, "RateDerived")}, "0.0") & "{PCT}."', 12.5, MUTE), cp]))}'''
M('People SVG', PEOPLE, cat='ImageUrl', folder='1 Number')

# =========================================================== PAGE 2
M('SelLens', 'SELECTEDVALUE(Lens[Lens], "Sex")', folder='2 People')
DOTS = f'''VAR lens = [SelLens]
VAR dots = CONCATENATEX(FILTER(ALL(Dots), Dots[Lens] = lens), "<circle cx='" & (Dots[Col] * 29 + 11) & "' cy='" & (Dots[Row] * 29 + 11) & "' r='11' fill='" & Dots[Rgb] & "'/>", "", Dots[Idx])
VAR labels = CONCATENATEX(FILTER(ALL(LegendKey), LegendKey[Lens] = lens), "<text x='318' y='" & (LegendKey[MidY] + 14) & "' font-family='Georgia' font-weight='700' font-size='40.0' fill='" & LegendKey[TextRgb] & "'>" & LegendKey[Count] & "</text><text x='398' y='" & (LegendKey[MidY] + 12) & "' font-family='Segoe UI Semibold' font-size='16.9' fill='{INK}'>" & LegendKey[Label] & "</text>", "", LegendKey[GroupOrder])
VAR cap = SELECTEDVALUE(Lens[Caption], "")
RETURN {URI} & "<svg xmlns='http://www.w3.org/2000/svg' width='640' height='360' viewBox='0 0 640 360'>" & dots & labels & "<text x='0' y='334' font-family='Segoe UI' font-size='14.1' fill='{MUTE}'>Of every 100 unemployed Jordanians. " & cap & "</text></svg>"'''
M('Dots SVG', DOTS, cat='ImageUrl', folder='2 People')
def g2(x, key, col, lab):
    n = f'ROUND({FACT(key)}, 0)'
    return (f'CONCATENATEX(GENERATESERIES(1, 100), "<circle cx=\'" & ({x} + MOD([Value] - 1, 10) * 24 + 9) & "\' cy=\'" & (INT(([Value] - 1) / 10) * 24 + 9) & "\' r=\'9\' fill=\'" & IF([Value] <= {n}, "{col}", "{MIST}") & "\'/>", "", [Value])'), n
parts = []
for x, key, col, lab in ((0, 'MenRate', SLATE, 'men'), (290, 'WomenRate', CLAY, 'women')):
    gs, n = g2(x, key, col, lab)
    parts += [gs, TD(x, 292, n, 48, col, 'Georgia', 700), T(x + 62, 262, f'of 100 {lab}', 14, INK, 'Segoe UI Semibold', 600),
              T(x + 62, 281, 'in the labour force', 13, MUTE),
              TD(x + 62, 300, f'"unemployed: " & FORMAT({FACT(key)}, "0.00") & "{PCT}"', 13, INK)]
RATE = f'''{svg(620, 320, ' & '.join(parts))}'''
M('Rate SVG', RATE, cat='ImageUrl', folder='2 People')

# =========================================================== PAGE 3
M('SelGov', 'SELECTEDVALUE(DimGov[Name], "")', folder='3 Places')
leg = ''.join(f"<rect x='{480 + i * 12}' y='398' width='12' height='10' fill='RAMP{i}'/>" for i in range(15))
RAMP = ["rgb(216,200,168)", "rgb(212,193,160)", "rgb(207,186,152)", "rgb(203,178,144)", "rgb(198,171,137)", "rgb(194,164,129)", "rgb(190,156,121)", "rgb(185,149,113)", "rgb(181,142,106)", "rgb(181,126,96)", "rgb(181,110,86)", "rgb(181,95,76)", "rgb(160,70,50)", "rgb(130,50,35)", "rgb(110,36,23)"]
import sys
sys.path.insert(0, _o.path.join(REPO, *r"09_Jordanian_Unemployment_Experience\01_Design".split("\\")))
from common import ramp
def rgbs(h): return "rgb(%d,%d,%d)" % tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
legend_static = ''.join(f"<rect x='{480 + i * 12}' y='398' width='12' height='10' fill='{rgbs(ramp(15 + i))}'/>" for i in range(15))
legend_static += f"<text x='480' y='428' font-family='Segoe UI' font-size='12.4' fill='{MUTE}'>15%</text><text x='660' y='428' font-family='Segoe UI' font-size='12.4' text-anchor='end' fill='{MUTE}'>29%</text>"
legend_static += f"<text x='480' y='388' font-family='Segoe UI Semibold' font-size='12.4' font-weight='700' letter-spacing='1' fill='{MUTE}'>RATE</text>"
legend_static += f"<circle cx='490' cy='462' r='3.5' fill='{INK}'/><circle cx='516' cy='462' r='7.1' fill='{INK}'/><text x='532' y='466' font-family='Segoe UI' font-size='12.4' fill='{MUTE}'>5k / 20k people</text>"
MAP = f'''VAR sel = [SelGov]
VAR paths = CONCATENATEX(ALL(DimGov), "<path d='" & DimGov[PathD] & "' fill='" & DimGov[Fill] & "' stroke='{PAPER}' stroke-width='1.4' opacity='" & IF(sel = "" || sel = DimGov[Name], "1", "0.4") & "'/>", "", DimGov[Order])
VAR topPath = CONCATENATEX(FILTER(ALL(DimGov), DimGov[Name] = sel), "<path d='" & DimGov[PathD] & "' fill='none' stroke='{INK}' stroke-width='3'/>", "", DimGov[Order])
VAR discs = CONCATENATEX(ALL(DimGov), "<circle cx='" & DimGov[CX] & "' cy='" & DimGov[CY] & "' r='" & (DimGov[R] + 2) & "' fill='{PAPER}' opacity='0.9'/><circle cx='" & DimGov[CX] & "' cy='" & DimGov[CY] & "' r='" & DimGov[R] & "' fill='" & IF(sel = DimGov[Name], "{CLAY}", "{INK}") & "' opacity='0.9'/>", "", DimGov[Order])
RETURN {URI} & "<svg xmlns='http://www.w3.org/2000/svg' width='700' height='500' viewBox='0 0 700 500'>" & paths & topPath & discs & "{legend_static}</svg>"'''
M('Map SVG', MAP, cat='ImageUrl', folder='3 Places')
LEDGER = f'''VAR sel = [SelGov]
VAR rws = CONCATENATEX(ALL(DimGov), IF(sel = DimGov[Name], "<rect x='0' y='" & (DimGov[RowY] - 21) & "' width='560' height='30' fill='{SAND}' opacity='0.75'/>", "")
  & "<circle cx='14' cy='" & DimGov[RowY] & "' r='8' fill='none' stroke='{INK}' stroke-width='1.2'/>"
  & "<rect x='38' y='" & (DimGov[RowY] - 6) & "' width='12' height='12' fill='" & DimGov[Fill] & "'/>"
  & "<text x='60' y='" & (DimGov[RowY] + 5) & "' font-family='Segoe UI' font-size='15.8' font-weight='" & IF(sel = DimGov[Name], "700", "400") & "' fill='{INK}'>" & DimGov[Name] & "</text>"
  & "<text x='262' y='" & (DimGov[RowY] + 6) & "' font-family='Georgia' font-weight='700' font-size='18.1' text-anchor='end' fill='" & IF(DimGov[Rate] >= 24, "{CLAY}", "{INK}") & "'>" & FORMAT(DimGov[Rate], "0.0") & "{PCT}</text>"
  & "<text x='396' y='" & (DimGov[RowY] + 5) & "' font-family='Segoe UI' font-size='14.7' text-anchor='end' fill='{INK}'>" & FORMAT(DimGov[Unemployed], "#,0") & "</text>"
  & "<rect x='412' y='" & (DimGov[RowY] - 4) & "' width='" & MAX(2, ROUND(DimGov[Unemployed] / 155900 * 100, 1)) & "' height='9' fill='{INK}'/>"
  & "<text x='556' y='" & (DimGov[RowY] + 5) & "' font-family='Segoe UI' font-size='14.7' text-anchor='end' fill='{MUTE}'>" & FORMAT(DimGov[Share] * 100, "0") & "{PCT}</text>", "", DimGov[Order])
RETURN {svg(560, 412, 'rws')}'''
M('Ledger SVG', LEDGER, cat='ImageUrl', folder='3 Places')
NAT_R = AY(2025, 'RateDerived'); NAT_U = AY(2025, 'Unemployed')
FRAME = '"' + "<rect x='1' y='1' width='558' height='160' fill='none' stroke='" + INK + "' stroke-width='1'/>" + '"'
cpc, wpc = chip(0, 188, 'DERIVED FROM DoS COUNTS', 'der'); cpn, _ = chip(wpc + 8, 188, 'NOT A DoS-PUBLISHED GOVERNORATE RATE', 'lim')
PANEL = f'''VAR sel = [SelGov]
VAR r = SELECTEDVALUE(DimGov[Rate], BLANK())
VAR u = SELECTEDVALUE(DimGov[Unemployed], BLANK())
VAR sh = SELECTEDVALUE(DimGov[Share], BLANK())
VAR note = SELECTEDVALUE(DimGov[Note1], "")
VAR note2 = SELECTEDVALUE(DimGov[Note2], "")
VAR hdg = IF(sel = "", "NATIONWIDE  ·  JORDANIANS 15+", "SELECTED  ·  " & UPPER(sel))
VAR big = IF(sel = "", FORMAT({NAT_R}, "0.0"), FORMAT(r, "0.0")) & "{PCT}"
VAR l1 = IF(sel = "", "derived 2025 annual rate", IF(r > {NAT_R}, "above the national derived rate of ", "below the national derived rate of ") & FORMAT({NAT_R}, "0.0") & "{PCT}")
VAR l2 = IF(sel = "", FORMAT({NAT_U}, "#,0") & " unemployed Jordanians", FORMAT(u, "#,0") & " unemployed Jordanians (" & FORMAT(sh * 100, "0") & "{PCT} of all)")
VAR l3 = IF(sel = "", "Select a governorate on the map or in the ledger. Select it again to clear.", note)
RETURN {svg(560, 200, ' & '.join([
    FRAME, cpc, cpn,
    TD(16, 30, 'hdg', 11.5, CLAY, 'Segoe UI Semibold', 700),
    TD(16, 80, 'big', 40, CLAY, 'Georgia', 700), TD(160, 64, 'l1', 13, INK, 'Segoe UI Semibold', 600), TD(160, 86, 'l2', 13, MUTE),
    TD(16, 110, 'l3', 12, MUTE), TD(16, 130, 'note2', 12, MUTE),
    T(16, 150, 'DoS publishes no sampling error; small governorates can swing year to year.', 11.5, MUTE)]))}'''
M('Panel SVG', PANEL, cat='ImageUrl', folder='3 Places')


# =========================================================== TMDL writers
def coltype(t, c):
    if c in INT.get(t, []): return 'int64', '0', 'Int64.Type'
    if c in DBL.get(t, []): return 'double', '0.0', 'type number'
    return 'string', None, 'type text'
def table_tmdl(t):
    cols = next(csv.reader(open(os.path.join(DATA, t + '.csv'), encoding='utf8')))
    out = [f'table {t}', f'\tlineageTag: {tag("t:" + t)}', '']; mc = []
    for c in cols:
        dt, fmt, mt = coltype(t, c); mc.append((c, mt))
        out += [f'\tcolumn {c}', f'\t\tdataType: {dt}'] + ([f'\t\tformatString: {fmt}'] if fmt else []) + [f'\t\tlineageTag: {tag("c:" + t + c)}', '\t\tsummarizeBy: none', f'\t\tsourceColumn: {c}', '']
    types = ', '.join('{"%s", %s}' % (c, m) for c, m in mc)
    if t == 'Lens':
        out = [l if l != '		summarizeBy: none' else l for l in out]
        i = out.index('	column Lens'); out.insert(i + 4, '		sortByColumn: LensOrder')
    out += [f'\tpartition {t} = m', '\t\tmode: import', '\t\tsource =', '\t\t\t\tlet',
            f'\t\t\t\t  Source = Csv.Document(File.Contents(DataFolder & "{t}.csv"), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),',
            '\t\t\t\t  Promoted = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),', f'\t\t\t\t  Typed = Table.TransformColumnTypes(Promoted, {{{types}}}, "en-US")',
            '\t\t\t\tin', '\t\t\t\t  Typed', '', '\tannotation PBI_ResultType = Table', '']
    return '\n'.join(out)
def meas_block(m):
    n = m['name']; q = f"'{n}'" if ' ' in n else n
    lines = [f'\tmeasure {q} ='] + ['\t\t\t' + b for b in m['expr'].split('\n')]
    if m.get('fmt'): lines.append(f"\t\tformatString: {m['fmt']}")
    if m.get('cat'): lines.append(f"\t\tdataCategory: {m['cat']}")
    if m.get('folder'): lines.append(f"\t\tdisplayFolder: {m['folder']}")
    lines += [f'\t\tlineageTag: {tag("m:" + n)}', '']
    return '\n'.join(lines)
def main():
    d = os.path.join(SM, 'definition')
    if os.path.isdir(d): shutil.rmtree(d)
    os.makedirs(d + '/tables')
    w = lambda p, t: open(os.path.join(SM, p), 'w', encoding='utf-8', newline='\n').write(t)
    for t in TABLES: w(f'definition/tables/{t}.tmdl', table_tmdl(t))
    mt = ['table _Measures', f'\tlineageTag: {tag("t:_Measures")}', ''] + [meas_block(m) for m in MEAS] + ['\tcolumn Placeholder', f'\t\tlineageTag: {tag("c:ph")}', '\t\tisNameInferred', '\t\tsourceColumn: [Placeholder]', '', '\tpartition _Measures = calculated', '\t\tmode: import', '\t\tsource = ROW("Placeholder", 1)', '']
    w('definition/tables/_Measures.tmdl', '\n'.join(mt))
    names = TABLES + ['_Measures']
    w('definition/model.tmdl', 'model JordanUnemployment\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-US\n\tdataAccessOptions\n\t\tlegacyRedirects\n\t\treturnErrorValuesAsNull\n\n' + f'annotation PBI_QueryOrder = {json.dumps(names + ["DataFolder"])}\n\n' + ''.join(f'ref table {n}\n' for n in names))
    w('definition/database.tmdl', 'database 6b3c5f10-6a8e-4b0b-9a42-5b7e1f6c2a55\n\tcompatibilityLevel: 1606\n\tcompatibilityMode: powerBI\n\tlanguage: 1033\n')
    folder = DATA.replace('/', '\\') + '\\'
    w('definition/expressions.tmdl', f'/// Folder holding the curated CSVs. Change this one value if the project is moved.\nexpression DataFolder = "{folder}" meta [IsParameterQuery=true, Type="Text", IsParameterQueryRequired=true]\n\tlineageTag: {tag("e:df")}\n\n\tannotation PBI_ResultType = Text\n')
    open(os.path.join(SM, 'definition.pbism'), 'w').write('{\n  "version": "4.2",\n  "settings": {}\n}')
    open(os.path.join(SM, '.platform'), 'w').write(json.dumps({"$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json", "metadata": {"type": "SemanticModel", "displayName": "JordanUnemployment"}, "config": {"version": "2.0", "logicalId": "7f1c9a62-3b4d-4e8a-8c55-2a9d0e6b1f55"}}, indent=2))
    print('model written', len(MEAS), 'measures')
if __name__ == '__main__': main()
