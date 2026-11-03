"""Plantilla de carrusel Goodfellas (estilo v2: oscuro, mucha foto, poco texto).
Uso: python3 carrusel.py spec.json outdir
spec = {
  "auto": "BMW M4 G82", "titulo": ["Alerón", "ducktail"], "sub": "MHC · carbono pre-preg",
  "slides": [
    {"tipo":"portada","img":"path","pos":"50% 50%"},
    {"tipo":"doble","imgs":["a","b"],"fondo":["foto","blanco"],"cap":"texto","cap_pos":"medio|arriba"},
    {"tipo":"full","img":"path","fondo":"foto|blanco","cap":"texto"},
    {"tipo":"cierre","img":"path"}
  ]}
"""
import base64, asyncio, pathlib, json, sys, mimetypes
from playwright.async_api import async_playwright

LOBO = pathlib.Path(__file__).with_name('lobo.svg').read_text()
RED = '#e3262e'

def uri(p):
    p = pathlib.Path(p); m = mimetypes.guess_type(p.name)[0] or 'image/jpeg'
    return f'data:{m};base64,' + base64.b64encode(p.read_bytes()).decode()

CSS = """*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1350px;overflow:hidden;background:#0c0c0c;font-family:'Inter',sans-serif;color:#fff;position:relative}
.it{font-style:italic;font-weight:900;letter-spacing:-.02em}
.sp{letter-spacing:.3em;text-transform:uppercase;font-weight:700}
.wolf svg{width:100%;height:100%}
.ph{position:absolute;left:0;right:0;overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover}
.cap{position:absolute;left:56px;display:flex;align-items:center;gap:16px;padding:12px 22px 12px 0}
.cap .bar{width:8px;height:44px;background:#e3262e}
.cap span{font-size:30px;font-weight:600}
"""

def logo(size=70, color='#fff'):
    return f'''<div style="display:flex;align-items:center;gap:16px;color:{color}">
      <div class="wolf" style="width:{size}px;height:{size*1.13:.0f}px">{LOBO}</div>
      <div><div class="it" style="font-size:{size*0.52:.0f}px;line-height:1">GOODFELLAS</div>
      <div class="sp" style="font-size:{size*0.17:.0f}px;margin-top:6px">Performance Division</div></div></div>'''

def dots(i, n):
    return '<div style="position:absolute;top:66px;right:56px;display:flex;gap:8px">' + ''.join(
        f'<div style="width:{36 if k==i else 12}px;height:6px;background:{RED if k==i else "rgba(128,128,128,.6)"}"></div>' for k in range(1, n+1)) + '</div>'

def cap(text, top, dark_text=False, kicker=''):
    col = '#111' if dark_text else '#fff'
    bg = 'rgba(255,255,255,.9)' if dark_text else 'rgba(10,10,10,.72)'
    k = f'<div class="sp" style="font-size:16px;color:{RED};margin-bottom:8px">{kicker}</div>' if kicker else ''
    return f'''<div style="position:absolute;left:0;top:{top}px;display:flex;align-items:stretch;background:{bg};padding:20px 34px 20px 0;backdrop-filter:blur(6px)">
      <div style="width:10px;background:{RED};margin-right:30px"></div>
      <div style="padding-left:16px">{k}<div class="it" style="font-size:38px;line-height:1.05;color:{col}">{text}</div></div></div>'''

def photo(src, top, h, fondo='foto', pos='50% 50%'):
    if fondo == 'negro':
        return f'<div class="ph" style="top:{top}px;height:{h}px;background:#000"><img src="{uri(src)}" style="object-fit:contain;padding:30px"></div>'
    if fondo == 'blanco':
        return f'<div class="ph" style="top:{top}px;height:{h}px;background:#fff"><img src="{uri(src)}" style="object-fit:contain;padding:40px"></div>'
    return f'<div class="ph" style="top:{top}px;height:{h}px"><img src="{uri(src)}" style="object-position:{pos}"></div>'

def slide(spec, i):
    s = spec['slides'][i-1]; n = len(spec['slides']); t = s['tipo']
    if t == 'portada':
        b = f'''{photo(s['img'],0,960,'foto',s.get('pos','50% 50%'))}
        <div style="position:absolute;top:0;left:0;right:0;height:240px;background:linear-gradient(#000c,#0000)"></div>
        <div style="position:absolute;top:700px;left:0;right:0;height:270px;background:linear-gradient(#0c0c0c00,#0c0c0c)"></div>
        <div style="position:absolute;top:52px;left:56px">{logo()}</div>
        <div style="position:absolute;left:56px;right:56px;top:900px">
          <div class="sp" style="font-size:22px;color:{RED}">{spec['auto']}</div>
          <div class="it" style="font-size:100px;line-height:.95;margin-top:18px;text-transform:uppercase">{'<br>'.join(spec['titulo'])}</div>
          <div class="it" style="font-size:44px;color:#9a9a9a;margin-top:14px">{spec['sub']}</div></div>'''
    elif t == 'doble':
        f = s.get('fondo', ['foto', 'foto'])
        b = photo(s['imgs'][0], 0, 672, f[0], s.get('pos', ['50% 50%']*2)[0]) + photo(s['imgs'][1], 678, 672, f[1], s.get('pos', ['50% 50%']*2)[1])
        if s.get('cap'):
            top = 40 if s.get('cap_pos') == 'arriba' else 588
            darkt = f[0] == 'blanco' if top == 40 or top == 588 else False
            b += cap(s['cap'], 40 if top == 40 else 560, darkt, s.get('kicker',''))
    elif t == 'beneficios':
        items = ''.join(f'''<div style="display:flex;gap:28px;align-items:flex-start;padding:30px 0;border-top:1px solid rgba(255,255,255,.18)">
          <div class="it" style="font-size:58px;line-height:1;color:{RED};width:210px;flex-shrink:0;white-space:nowrap">{x.get('dato','')}</div>
          <div><div class="it" style="font-size:42px;line-height:1.05">{x['titulo']}</div>
          <div style="font-size:28px;line-height:1.4;color:#c9c9c9;margin-top:10px">{x['texto']}</div></div></div>''' for x in s['items'])
        b = f'''<div class="ph" style="top:0;height:1350px"><img src="{uri(s['img'])}" style="object-position:{s.get('pos','50% 50%')};filter:brightness(.25) grayscale(.3)"></div>
        <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,12,12,.3),rgba(12,12,12,.9))"></div>
        <div style="position:absolute;left:70px;right:70px;top:200px">
          <div class="sp" style="font-size:20px;color:{RED}">{s.get('kicker','Beneficios')}</div>
          <div class="it" style="font-size:76px;line-height:.95;margin:22px 0 40px;text-transform:uppercase">{s.get('titulo','¿Qué ganás?')}</div>{items}</div>'''
    elif t == 'full':
        b = photo(s['img'], 0, 1350, s.get('fondo', 'foto'), s.get('pos', '50% 50%'))
        if s.get('cap'): b += cap(s['cap'], 1150, s.get('fondo') == 'blanco', s.get('kicker',''))
    else:
        chat = '<svg viewBox="0 0 24 24" width="46" height="46"><path fill="#fff" d="M12 2.5C6.8 2.5 2.6 6.4 2.6 11.2c0 2.6 1.2 4.9 3.2 6.5L5 21.5l4-2.1c.9.3 1.9.4 3 .4 5.2 0 9.4-3.9 9.4-8.6S17.2 2.5 12 2.5z"/><circle cx="8" cy="11.2" r="1.3" fill="#1fae55"/><circle cx="12" cy="11.2" r="1.3" fill="#1fae55"/><circle cx="16" cy="11.2" r="1.3" fill="#1fae55"/></svg>'
        dm = '<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#fff" stroke-width="2" stroke-linejoin="round"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4 20-7z"/></svg>'
        tel = spec.get('whatsapp', '11 5135-9817')
        b = f'''<div class="ph" style="top:0;height:1350px"><img src="{uri(s['img'])}" style="object-position:{s.get('pos','50% 50%')};filter:brightness(.28) grayscale(.4)"></div>
        <div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(12,12,12,.2),rgba(12,12,12,.85) 70%)"></div>
        <div style="position:absolute;top:52px;left:56px">{logo()}</div>
        <div style="position:absolute;left:70px;right:70px;top:330px">
          <div class="sp" style="font-size:22px;color:{RED}">Goodfellas Performance Division</div>
          <div class="it" style="font-size:94px;line-height:.95;margin-top:26px;text-transform:uppercase">Cotizá tus<br>piezas y<br>repuestos</div>
          <div style="font-size:38px;color:#cfcfcf;margin-top:30px;font-weight:500">con nosotros. Te asesoramos y lo conseguimos para tu auto.</div>
          <div style="margin-top:70px;display:flex;flex-direction:column;gap:22px">
            <div style="display:flex;align-items:center;gap:26px;background:#1fae55;padding:26px 34px;border-radius:14px">
              {chat}<div><div class="sp" style="font-size:17px;opacity:.85">WhatsApp</div><div class="it" style="font-size:54px;line-height:1;margin-top:6px">{tel}</div></div></div>
            <div style="display:flex;align-items:center;gap:26px;border:2px solid rgba(255,255,255,.5);padding:24px 34px;border-radius:14px">
              {dm}<div class="it" style="font-size:40px">Mandanos un DM</div></div>
          </div></div>'''
    if t not in ('portada', 'cierre'):
        top_fondo = (s.get('fondo', ['foto'])[0] if isinstance(s.get('fondo'), list) else s.get('fondo', 'foto')) if t != 'beneficios' else 'foto'
        if top_fondo == 'blanco':
            b += f'<div style="position:absolute;top:52px;left:56px">{logo(color="#111")}</div>'
        else:
            b += f'<div style="position:absolute;top:0;left:0;right:0;height:220px;background:linear-gradient(rgba(0,0,0,.75),rgba(0,0,0,0))"></div><div style="position:absolute;top:52px;left:56px">{logo()}</div>'
    return f'<html><head><style>{CSS}</style></head><body>{b}{dots(i, n)}</body></html>'

async def main(spec, out):
    out = pathlib.Path(out); out.mkdir(parents=True, exist_ok=True)
    async with async_playwright() as p:
        br = await p.chromium.launch(); pg = await br.new_page(viewport={'width':1080,'height':1350})
        for i in range(1, len(spec['slides'])+1):
            await pg.set_content(slide(spec, i)); await pg.wait_for_timeout(200)
            await pg.screenshot(path=str(out/f'{i:02d}.jpg'), type='jpeg', quality=92)
        await br.close()

if __name__ == '__main__':
    asyncio.run(main(json.load(open(sys.argv[1])), sys.argv[2]))
