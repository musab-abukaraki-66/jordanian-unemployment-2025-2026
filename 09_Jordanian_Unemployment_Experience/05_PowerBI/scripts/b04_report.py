"""Generates pbip/JordanUnemployment.Report (PBIR). Never hand-edit generated files. Kill own Desktop instance first.
Pages: p01Number, p02People, p03Places. Canvas 1440x900. Static chrome = art/bg_p*.png; every number = SVG measures from the model."""
import os, sys, json, shutil
import pbir_lib as L
from pbir_lib import *

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
PB = os.path.join(ROOT, 'pbip'); REP = os.path.join(PB, 'JordanUnemployment.Report')
PAPER, INK, MUTE, CLAY = '#F1ECE2', '#1C1B19', '#5A4F44', '#B5472E'
L.DS.update(canvas=PAPER, ink=INK, mute=MUTE, faint='#8C8577', petrol=CLAY, slate='#3E4C52', amber=CLAY, white='#FFFFFF', hair='#CFC6B3',
            font='Segoe UI', font_sb='Segoe UI Semibold', font_lt='Segoe UI Light')
CAL = json.load(open(os.path.join(ROOT, 'scripts', 'calib.json'))) if os.path.exists(os.path.join(ROOT, 'scripts', 'calib.json')) else {}
PADW, PADH = 60, 36
INSET = (5, 10, 29, 30)
IMGDX, IMGDY = 5, 2   # image offset inside a table cell (measured in Desktop at 100% zoom)   # visual padding around a table-image cell (header row + cell padding), so no scrollbars appear

def fcol(e, p): return field_col(e, p)
def agg(e, p, fn=0):
    return {"field": {"Aggregation": {"Expression": {"Column": {"Expression": {"SourceRef": {"Entity": e}}, "Property": p}}, "Function": fn}}, "queryRef": f"Sum({e}.{p})", "nativeQueryRef": f"Sum of {p}"}

def card_image(name, x, y, z, measure, iw, ih, bg=PAPER):
    q = {"queryState": {"Values": {"projections": [field_meas(measure)]}}}
    hid = {"fontColor": COL(bg), "fontSize": N(1), "backColor": COL(bg)}
    obj = {"stylePreset": [{"properties": {"name": S("None")}}],
           "grid": [{"properties": {"rowPadding": N(0), "gridHorizontal": B(False), "gridVertical": B(False), "outlineWeight": N(0), "imageHeight": N(ih), "imageWidth": N(iw)}}],
           "columnHeaders": [{"properties": hid}], "values": [{"properties": {"fontSize": N(1), "fontColor": COL(bg), "backColor": COL(bg)}}]}
    vco = container(); vco['visualTooltip'] = [{"properties": {"show": B(False)}}]
    t = visual(name, x - IMGDX, y - IMGDY, iw + PADW, ih + PADH, z, "tableEx", obj, query=q, vco=vco)
    sh = L.solid('shield_' + name, x - IMGDX, y - IMGDY, iw + PADW, ih + PADH, z + 1, '#000000', tr=100)
    return [t, sh]

def hotspots(name, cat, xcol, ycol, x, y, iw, ih, z, color, size, tip=False):
    """Native scatter used as transparent-ish click targets over an image. cal = (dx, dy, l, t, r, b): image offset and plot-area insets."""
    l, t, r, b = INSET   # scatter plot-area insets measured in Desktop at 100% zoom (hidden axes still reserve space)
    dx, dy = CAL.get(name, (0, 0))
    vx, vy, vw, vh = x + IMGDX - l + dx, y + IMGDY - t + dy, iw + l + r, ih + t + b
    q = {"queryState": {"Category": {"projections": [dict(fcol(*cat), active=True)]}, "X": {"projections": [agg(cat[0], xcol)]}, "Y": {"projections": [agg(cat[0], ycol)]}}}
    obj = {"legend": [{"properties": {"show": B(False)}}],
           "categoryAxis": [{"properties": {"show": B(False), "start": N(0), "end": N(iw), "showAxisTitle": B(False), "gridlineShow": B(False)}}],
           "valueAxis": [{"properties": {"show": B(False), "start": N(0), "end": N(ih), "showAxisTitle": B(False), "gridlineShow": B(False)}}],
           "bubbles": [{"properties": {"bubbleSize": lit(f"{size}L"), "preventOverflow": B(False)}}],
           "plotArea": [{"properties": {"transparency": N(100)}}], "dataPoint": [{"properties": {"fill": {"solid": {"color": S(color)}}}}]}
    vco = container(); vco['visualTooltip'] = [{"properties": {"show": B(False)}}]
    return visual(name, vx, vy, vw, vh, z, "scatterChart", obj, query=q, vco=vco)

def lens_slicer(name, x, y, w, h, z):
    q = {"queryState": {"Values": {"projections": [dict(fcol('Lens', 'Lens'), active=True)]}}}
    o = {"data": [{"properties": {"mode": S("Basic")}}],
         "selection": [{"properties": {"singleSelect": B(True), "selectAllCheckboxEnabled": B(False), "strictSingleSelect": B(True)}}],
         "header": [{"properties": {"show": B(False)}}],
         "items": [{"properties": {"fontFamily": S('Segoe UI Semibold'), "fontSize": N(13), "fontColor": COL(INK), "background": COL(PAPER)}}],
         "general": [{"properties": {"orientation": lit("1D"), "filter": {"filter": {"Version": 2, "From": [{"Name": "d", "Entity": "Lens", "Type": 0}],
                      "Where": [{"Condition": {"In": {"Expressions": [{"Column": {"Expression": {"SourceRef": {"Source": "d"}}, "Property": "Lens"}}], "Values": [[{"Literal": {"Value": "'Sex'"}}]]}}}]}}}}]}
    return visual(name, x, y, w, h, z, "slicer", o, query=q, vco=container())

def nav(name, x, y, w, h, z, target, tip):
    obj = {"icon": [{"properties": {"shapeType": S("blank")}, "selector": {"id": "default"}}],
           "outline": [{"properties": {"show": B(False)}}, {"properties": {"show": B(False)}, "selector": {"id": "default"}}],
           "fill": [{"properties": {"show": B(True)}}, {"properties": {"fillColor": COL('#FFFFFF'), "transparency": N(100)}, "selector": {"id": "default"}},
                    {"properties": {"fillColor": COL(CLAY), "transparency": N(88)}, "selector": {"id": "hover"}}],
           "text": [{"properties": {"show": B(False)}}]}
    vco = container(); vco["visualLink"] = [{"properties": {"show": B(True), "type": S("PageNavigation"), "navigationSection": S(target), "tooltip": S(tip)}}]
    return visual(name, x, y, w, h, z, "actionButton", obj, vco=vco)

def chapter_nav(z0):
    return [nav('navNumber', 48, 22, 150, 30, z0, 'p01Number', 'Chapter 1: The number'), nav('navPeople', 208, 22, 150, 30, z0 + 1, 'p02People', 'Chapter 2: The people'),
            nav('navPlaces', 368, 22, 150, 30, z0 + 2, 'p03Places', 'Chapter 3: The places')]
def next_btn(z, target, tip): return nav('nextBtn', 1160, 852, 232, 34, z, target, tip)

def page1():
    v = chapter_nav(60)
    v += card_image('hero', 48, 276, 10, 'Hero SVG', 700, 130) + card_image('chart', 48, 462, 12, 'Chart SVG', 900, 344)
    v += [hotspots('hotQuarter', ('Quarter', 'Label'), 'HotX', 'HotY', 48, 462, 900, 344, 40, INK, 1)]
    v += card_image('ruler', 953, 124, 20, 'Ruler SVG', 432, 460) + card_image('people', 953, 650, 22, 'People SVG', 432, 156) + [next_btn(63, 'p02People', 'Next: who are they?')]
    write_page(REP, 'p01Number', 'The number', v, 'bg_p1.png', w=1440, h=900)
def page2():
    v = chapter_nav(60)
    v += [lens_slicer('lens', 100, 296, 420, 34, 30)] + card_image('dots', 48, 376, 10, 'Dots SVG', 640, 340) + card_image('rates', 760, 376, 12, 'Rate SVG', 600, 310) + [next_btn(63, 'p03Places', 'Next: where are they?')]
    write_page(REP, 'p02People', 'The people', v, 'bg_p2.png', w=1440, h=900)
def page3():
    v = chapter_nav(60)
    v += card_image('map', 48, 296, 10, 'Map SVG', 700, 500) + [hotspots('hotMap', ('DimGov', 'Name'), 'CX', 'HotMapY', 48, 296, 700, 500, 40, INK, 1)]
    v += card_image('ledger', 812, 156, 12, 'Ledger SVG', 560, 412) + [hotspots('hotRows', ('DimGov', 'Name'), 'HotRowX', 'HotRowY', 812, 156, 560, 412, 41, INK, 1)]
    v += card_image('panel', 812, 606, 14, 'Panel SVG', 560, 200) + [next_btn(63, 'p01Number', 'Back to the number')]
    write_page(REP, 'p03Places', 'The places', v, 'bg_p3.png', w=1440, h=900,
               interactions=[{"source": "hotMap", "target": "hotRows", "type": "NoFilter"}, {"source": "hotRows", "target": "hotMap", "type": "NoFilter"}])

def skeleton(pages):
    os.makedirs(REP, exist_ok=True)
    write_json(os.path.join(PB, 'JordanUnemployment.pbip'), {"version": "1.0", "artifacts": [{"report": {"path": "JordanUnemployment.Report"}}], "settings": {"enableAutoRecovery": True}})
    write_json(os.path.join(REP, 'definition.pbir'), {"version": "4.0", "datasetReference": {"byPath": {"path": "../JordanUnemployment.SemanticModel"}}})
    write_json(os.path.join(REP, '.platform'), {"$schema": "https://developer.microsoft.com/json-schemas/fabric/gitIntegration/platformProperties/2.0.0/schema.json", "metadata": {"type": "Report", "displayName": "Jordanian Unemployment 2025-2026"}, "config": {"version": "2.0", "logicalId": "2b8d4e71-90c3-4f1a-b7d6-5e0a3c9f8d55"}})
    write_json(os.path.join(REP, 'definition', 'version.json'), {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/versionMetadata/1.0.0/schema.json", "version": "2.0.0"})
    rj = json.load(open(os.path.join(ROOT, 'scripts', 'report_template.json')))
    rj['themeCollection']['customTheme']['name'] = 'JordanUnemployment.json'
    resdir = os.path.join(REP, 'StaticResources', 'RegisteredResources'); os.makedirs(resdir, exist_ok=True)
    for f in ('bg_p1.png', 'bg_p2.png', 'bg_p3.png'): shutil.copy(os.path.join(ROOT, 'art', f), os.path.join(resdir, f))
    for p in rj['resourcePackages']:
        if p['name'] == 'RegisteredResources':
            p['items'] = [{"name": "JordanUnemployment.json", "path": "JordanUnemployment.json", "type": "CustomTheme"}] + [{"name": n, "path": n, "type": "Image"} for n in ('bg_p1.png', 'bg_p2.png', 'bg_p3.png')]
    write_json(os.path.join(REP, 'definition', 'report.json'), rj)
    write_json(os.path.join(resdir, 'JordanUnemployment.json'), {"name": "Jordanian Unemployment", "dataColors": ["#1C1B19", "#B5472E", "#3E4C52", "#D8C8A8", "#6E2417", "#8C8577"], "foreground": "#1C1B19", "background": "#F1ECE2", "tableAccent": "#B5472E",
              "textClasses": {"callout": {"fontFace": "Georgia", "fontSize": 28, "color": "#1C1B19"}, "title": {"fontFace": "Segoe UI Semibold", "fontSize": 12, "color": "#1C1B19"}, "header": {"fontFace": "Segoe UI Semibold", "fontSize": 10, "color": "#1C1B19"}, "label": {"fontFace": "Segoe UI", "fontSize": 9, "color": "#5A4F44"}}})
    write_json(os.path.join(REP, 'definition', 'pages', 'pages.json'), {"$schema": "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/pagesMetadata/1.1.0/schema.json", "pageOrder": pages, "activePageName": pages[0]})

if __name__ == '__main__':
    pd_ = os.path.join(REP, 'definition', 'pages')
    if os.path.isdir(pd_): shutil.rmtree(pd_)
    pages = ['p01Number', 'p02People', 'p03Places']
    skeleton(pages); page1(); page2(); page3()
    print('report written', pages)
