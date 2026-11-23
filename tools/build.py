"""index.html (TR) ve en.html (EN) dosyalarını content.py'den üretir.
Çalıştırma: python3 tools/build.py  (depo kökünden)"""
import html, json, pathlib, re
from content import *

ROOT = pathlib.Path(__file__).resolve().parent.parent
ZW = re.compile("[\u200b\u200c\u200d\u2060\ufeff]")
JURY_FILE = pathlib.Path(__file__).resolve().parent / "jury.json"

def T(v, i):
    if isinstance(v, tuple):
        v = v[i]
    return html.escape(ZW.sub("", v), quote=False).replace("'", "\u2019")

ICONS = {
    "home": '<path d="M4 11.5 12 5l8 6.5V19a1 1 0 0 1-1 1h-4.5v-5h-5v5H5a1 1 0 0 1-1-1z"/>',
    "user": '<circle cx="12" cy="8.5" r="3.5"/><path d="M5 19.5c1.2-3.3 4-5 7-5s5.8 1.7 7 5"/>',
    "grid": '<rect x="4.5" y="4.5" width="6" height="6" rx="1.5"/><rect x="13.5" y="4.5" width="6" height="6" rx="1.5"/><rect x="4.5" y="13.5" width="6" height="6" rx="1.5"/><rect x="13.5" y="13.5" width="6" height="6" rx="1.5"/>',
    "tool": '<path d="M14.5 5.5a4 4 0 0 0-5 5L4.8 15.2a1.8 1.8 0 0 0 2.5 2.5l4.7-4.7a4 4 0 0 0 5-5l-2.4 2.4-2.3-.5-.5-2.3z"/>',
    "jury": '<path d="M12 4.5v15M7 19.5h10M5 8.5h14M5 8.5l-2.5 5a2.5 2.5 0 0 0 5 0zM19 8.5l-2.5 5a2.5 2.5 0 0 0 5 0z"/>',
    "mail": '<rect x="3.5" y="6" width="17" height="12" rx="2"/><path d="m4.5 7.5 7.5 5.5 7.5-5.5"/>',
    "gh": '<path d="M9 19c-4 1.3-4-2-5.5-2.5M14.5 21v-3.2a2.8 2.8 0 0 0-.8-2.2c2.6-.3 5.3-1.3 5.3-5.8a4.5 4.5 0 0 0-1.2-3.1 4.2 4.2 0 0 0-.1-3.1s-1-.3-3.2 1.2a11 11 0 0 0-5.8 0C6.5 3.3 5.5 3.6 5.5 3.6a4.2 4.2 0 0 0-.1 3.1 4.5 4.5 0 0 0-1.2 3.1c0 4.5 2.7 5.5 5.3 5.8a2.8 2.8 0 0 0-.8 2.2V21"/>',
    "in": '<rect x="4" y="4" width="16" height="16" rx="2.5"/><path d="M8.5 10.5v5M8.5 8v.01M12 15.5v-5M12 13c0-1.5 1-2.5 2.2-2.5s2.3.8 2.3 2.5v2.5"/>',
    "arrow": '<path d="M7 17 17 7M9 7h8v8"/>',
    "lock": '<rect x="5.5" y="10.5" width="13" height="9" rx="2"/><path d="M8.5 10.5V8a3.5 3.5 0 0 1 7 0v2.5"/>',
    "side": '<rect x="3.5" y="5" width="17" height="14" rx="2.5"/><path d="M9.5 5v14"/>',
}
def ic(name, cls="ic"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{ICONS[name]}</svg>'

LOGO = '<svg class="logo" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><rect width="64" height="64" rx="14"/><g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="5.5"><path class="k1" d="M15 15v34M15 35 29 15M21.5 27 29 49"/><path class="k2" d="M35 15v34M35 35 49 15M41.5 27 49 49"/></g></svg>'

def fmt(x, i):
    s = f"{x:.1f}"
    return s.replace(".", ",") if i == 0 else s

def by_name(n):
    for p in PROJ["items"]:
        nm = p["name"] if isinstance(p["name"], str) else p["name"][0]
        if nm == n:
            return p
    raise KeyError(n)

def bk(label, cls=""):
    return f'<span class="bk{cls}" aria-hidden="true">[</span>{label}<span class="bk{cls}" aria-hidden="true">]</span>'

def mem_svg(g):
    # MemPalace kutucuğu: notlar vektöre çevrilir, ChromaDB'de durur, ajanlar MCP ile geri çağırır
    M = V3["mem"]
    t = lambda k: g(M[k])
    notes = "".join(f'<rect x="{70 + k * 14}" y="{62 + k * 14}" width="120" height="78" rx="4" class="mm-note"/>' for k in range(3))
    lines = "".join(f'<line x1="{98 + 28}" y1="{108 + 28 + k * 12}" x2="{98 + 28 + (70 - k * 18)}" y2="{108 + 28 + k * 12}" class="mm-txt"/>' for k in range(3))
    agents = "".join(f'<g class="mm-agent"><circle cx="1030" cy="{58 + k * 52}" r="17"/><path d="M1022 {58 + k * 52} h16 M1030 {50 + k * 52} v16" /></g>' for k in range(3))
    return (f'<svg class="mem" viewBox="0 0 1200 230" role="img" aria-label="{t("cap")}" focusable="false">'
            f''
            f'<g class="mm-paths"><path id="mm-a" d="M222 120 C300 120 320 120 392 120"/><path id="mm-b" d="M548 120 C590 120 600 120 640 120"/>'
            f'<path id="mm-c" d="M780 106 C860 80 900 60 1008 58"/><path id="mm-d" d="M780 120 C880 112 920 110 1008 110"/><path id="mm-e" d="M780 134 C860 150 900 162 1008 162"/></g>'
            f'{notes}{lines}<text x="150" y="196" class="mm-l">{t("notes")}</text>'
            f'<rect x="392" y="98" width="156" height="44" rx="4" class="mm-chip"/><text x="470" y="126" class="mm-c">{t("embed")}</text>'
            f'<g class="mm-db"><ellipse cx="710" cy="74" rx="70" ry="16"/><path d="M640 74 v92 a70 16 0 0 0 140 0 v-92"/><path d="M640 104 a70 16 0 0 0 140 0 M640 134 a70 16 0 0 0 140 0" class="mm-ring"/></g>'
            f'<text x="710" y="210" class="mm-l">{t("store")}</text><text x="710" y="226" class="mm-s">{t("hnsw")}</text>'
            f'{agents}<text x="1030" y="210" class="mm-l">{t("agents")}</text><text x="895" y="196" class="mm-s">{t("mcp")}</text>'
            + "".join(f'<circle r="3.2" class="mm-dot"><animateMotion dur="{d}s" begin="{bg}s" repeatCount="indefinite"><mpath href="#{p}"/></animateMotion></circle>'
                      for p, d, bg in (("mm-a", 2.4, 0), ("mm-a", 2.4, 1.2), ("mm-b", 1.4, .6), ("mm-c", 2.8, .2), ("mm-d", 2.8, 1.1), ("mm-e", 2.8, 1.9)))
            + '</svg>')

def net_svg():
    # Altbilgideki kelime ağı: her kelimeden ortadaki ada ince çizgi
    words = V3["net"]
    cx, cy = 600, 330
    out_l, out_t = "", ""
    import math
    n = len(words)
    for k, w in enumerate(words):
        a = math.pi * (0.06 + 0.88 * k / (n - 1))
        r = 250 + (k % 3) * 70
        x = cx - math.cos(a) * r * 1.55
        y = cy - math.sin(a) * r * 0.78
        y = max(24, y)
        size = (13, 11, 15)[k % 3]
        out_l += f'<line x1="{x:.0f}" y1="{y + 4:.0f}" x2="{cx}" y2="{cy - 40}"/>'
        out_t += f'<text x="{x:.0f}" y="{y:.0f}" font-size="{size}" text-anchor="middle">{html.escape(w)}</text>'
    return f'<svg class="net" viewBox="0 0 1200 340" preserveAspectRatio="xMidYMax meet" aria-hidden="true" focusable="false"><g class="net-l">{out_l}</g><g class="net-t">{out_t}</g></svg>'

def jury_html(i, g):
    J = json.loads(JURY_FILE.read_text(encoding="utf-8"))
    slides, rows = [], ""
    for key, nm in (("deepseek", "DeepSeek"), ("gemini", "Gemini")):
        d = J["final"][key]
        for ck, cl in JURY["cats"]:
            c = d["scores"][ck]
            slides.append((nm, g(cl), float(c["score"]), c["reason_tr"] if i == 0 else c["reason_en"]))
        cells = "".join(f'<td>{fmt(float(d["scores"][ck]["score"]), i)}</td>' for ck, _ in JURY["cats"])
        rows += (f'<tr><th scope="row">{nm}<span class="jt-m">{html.escape(d["model"])}</span></th>{cells}'
                 f'<td class="jt-o">{fmt(float(d["overall"]), i)}</td><td class="jt-b">{fmt(float(J["baseline"][key]["overall"]), i)}</td></tr>')
    n = len(slides)
    sl = ""
    for k, (nm, cat, v, why) in enumerate(slides):
        sl += (f'<figure class="q{" on" if k == 0 else ""}" data-k="{k}" role="group" aria-roledescription="{("alıntı", "quote")[i]}" aria-label="{k + 1} / {n}">'
               f'<blockquote><p>{g(why)}</p></blockquote>'
               f'<figcaption><span class="q-who">{nm}</span><span class="q-cat">{cat} <span class="num">{fmt(v, i)}</span> / 10</span></figcaption></figure>')
    if J.get("version") == "v2":
        note = ("Alıntılar önceki sürümün son jüri turundan. Bu sürümün turu bitince yenilenecek.", "Quotes come from the previous version's last jury round. They are replaced once this version is judged.")[i]
    else:
        note = (f"Alıntılar bu sürümün son jüri turundan ({J['rounds']}. tur, {J.get('date', '')}). Sağdaki sütun önceki sürümün genel puanı.",
                f"Quotes come from this version's last jury round (round {J['rounds']}, {J.get('date', '')}). The last column is the previous version's overall score.")[i]
    head = "".join(f'<th scope="col">{g(cl)}</th>' for _, cl in JURY["cats"])
    return (f'<div class="qbox rv"><div class="q-top"><span class="q-mark" aria-hidden="true">“</span>'
            f'<p class="q-count" aria-live="polite"><span class="q-line" aria-hidden="true"></span><span class="num q-now">001</span> / <span class="num">{n:03d}</span></p></div>'
            f'<div class="q-stage">{sl}</div>'
            f'<div class="q-ctl"><button type="button" class="q-btn" data-d="-1" aria-label="{g(V3["prev"])}"><span aria-hidden="true">←</span></button>'
            f'<button type="button" class="q-btn" data-d="1" aria-label="{g(V3["next"])}"><span aria-hidden="true">→</span></button></div></div>'
            f'<div class="jt-wrap rv"><div class="jt-scroll" tabindex="0" role="region" aria-label="{g(JURY["h"])}"><table class="jt"><caption class="sr">{g(JURY["h"])}</caption><thead><tr><th scope="col">{("Jüri", "Judge")[i]}</th>{head}'
            f'<th scope="col">{g(JURY["overall"])}</th><th scope="col">{g(JURY["before"])}</th></tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="small muted">{g(JURY["p"])} {html.escape(note)}</p></div>')

def page(i):
    lang = ("tr", "en")[i]
    other = ("en.html", "index.html")[i]
    url = BASE if i == 0 else BASE + "en.html"
    g = lambda v: T(v, i)
    items = PROJ["items"]
    gname = dict(PROJ["groups"])
    E = CONTACT["email"]

    nav = "".join(f'<li><a class="nl" href="#{k}" data-sec="{k}">{bk(g(v))}</a></li>' for k, v in V3["nav"])

    # İşler
    work_names = [n for n, _ in V3["work"]]
    cards = ""
    for k, (nm, t) in enumerate(V3["work"]):
        p = by_name(nm)
        meta = f'{g(p["name"])} · {g(p["s"])}'
        if nm == "V.A.U.L.T. // B.R.E.A.C.H.":
            im = '<img src="img/vault-panel-1500.webp" srcset="img/vault-panel-750.webp 750w, img/vault-panel-1500.webp 1500w" sizes="(max-width: 760px) 90vw, 76vw" width="1500" height="755" alt="' + g(("V.A.U.L.T. paneli: solda görev kartları, ortada nokta küresi, altta komut satırı", "The V.A.U.L.T. panel: task cards on the left, a dot sphere in the middle, a prompt at the bottom")) + '" loading="lazy" decoding="async">'
            kind = "wide"
        elif nm == "Kuti Dock":
            im = ('<div class="desk" aria-hidden="true"></div><img class="menu" src="img/kuti-menu-3080.webp" width="3080" height="52" alt="" loading="lazy" decoding="async"><img class="dock" src="img/kuti-dock-2000.webp" width="2000" height="66" alt="'
                  + g(("Kuti Dock alt çubuğu: uygulama simgeleri, kullanım kartı, işlemci ve bellek göstergeleri, disk ve saat", "The Kuti Dock bar: app icons, a usage card, CPU and RAM gauges, disk and clock")) + '" loading="lazy" decoding="async">')
            kind = "dockc"
        elif nm == "Nota Kulağı":
            im = ('<div class="phone"><img src="img/nota-kulagi-390.webp" width="390" height="780" alt="'
                  + g(("Nota Kulağı açılış ekranı: nota tuşları simgesi ve Başlamak için dokunun düğmesi", "Nota Kulağı start screen: a note keys icon and a Tap to start button")) + '" loading="lazy" decoding="async"></div>')
            kind = "phonec"
        else:
            m = p["img"]
            ss = f' srcset="{m["srcset"]}" sizes="(max-width: 760px) 90vw, 44vw"' if m.get("srcset") else ""
            im = f'<img src="{m["src"]}"{ss} width="{m["w"]}" height="{m["h"]}" alt="{g(m["alt"])}" loading="lazy" decoding="async">'
            kind = ""
        if p.get("url"):
            title = f'<a class="wk-link" href="{p["url"]}" rel="noopener">{g(t)}<span class="wk-arr" aria-hidden="true">↗</span></a>'
            tag = g(PROJ["gh"] if p["kind"] == "gh" else PROJ["site"])
        else:
            title = g(t)
            tag = g(PROJ["priv"])
        extra = ""
        if p.get("why"): extra += f'<p class="wk-x"><span>{g(PROJ["why"])}</span>{g(p["why"])}</p>'
        if p.get("how"): extra += f'<p class="wk-x"><span>{g(PROJ["how"])}</span>{g(p["how"])}</p>'
        cards += (f'<li class="wk rv {kind}"><article><div class="wk-stage"><span class="glow" aria-hidden="true"></span><span class="scan" aria-hidden="true"></span>{im}</div>'
                  f'<div class="wk-cap"><h3 class="wk-t">{title}</h3><p class="wk-m"><span>{meta}</span><span class="wk-tag">{tag}</span></p></div>'
                  f'<p class="wk-d">{g(p["d"])}</p>{extra}</article></li>')

    # Deneyler (bento)
    tiles = ""
    spans = ["t4"] + ["t1"] * 8
    for k, (nm, big, d) in enumerate(V3["lab"]):
        p = by_name(nm)
        vis = ""
        if nm.startswith("MemPalace"):
            vis = mem_svg(g)
        if big:
            vis = f'<p class="t-big" aria-hidden="true">{big}</p>'
        link = (f'<a class="t-link" href="{p["url"]}" rel="noopener">{g(p["name"])}<span class="sr"> ({g(PROJ["gh"])})</span></a>'
                if p.get("url") else f'<span>{g(p["name"])}</span>')
        tiles += (f'<li class="tile rv {spans[k]}"><div class="t-vis">{vis}</div><div class="t-txt"><h3 class="t-n">{link}</h3>'
                  f'<p class="t-d">{g(d)}</p><p class="t-s">{g(gname[p["g"]])} · {g(p["s"])}</p></div>'
                  f'{"<span class=\"t-arr\" aria-hidden=\"true\">↗</span>" if p.get("url") else ""}</li>')

    # Tüm projeler tablosu
    rest = [p for p in items if (p["name"] if isinstance(p["name"], str) else p["name"][0]) not in work_names]
    trs = ""
    for p in rest:
        if p.get("url"):
            lk = f'<a class="pt-go" href="{p["url"]}" rel="noopener"><span class="sr">{g(p["name"])}: {g(PROJ["gh"] if p["kind"] == "gh" else PROJ["site"])}</span><span aria-hidden="true">↗</span></a>'
        elif p.get("priv"):
            lk = f'<span class="pt-q">{g(PROJ["priv"])}</span>'
        else:
            lk = f'<span class="pt-q">{g(PROJ["nolink"])}</span>'
        trs += (f'<tr data-n="{g(p["name"])}" data-c="{g(gname[p["g"]])}" data-s="{g(p["s"])}"><th scope="row"><span class="pt-n">{g(p["name"])}</span>'
                f'<span class="pt-c">{g(gname[p["g"]])}</span></th><td class="pt-d">{g(p["d"])}</td><td class="pt-s">{g(p["s"])}</td><td class="pt-l">{lk}</td></tr>')

    # Hakkımda
    about_p = "".join(f"<p>{g(p)}</p>" for p in ABOUT["p"])
    facts = "".join(f'<tr><th scope="row">{g(a)}</th><td class="num">{g(b)}</td></tr>' for a, b in ABOUT["rows"])
    jobs = "".join(
        f'<li class="xp rv"><p class="xp-w num"><time>{j["from"]}</time> <span aria-hidden="true">·</span> <time>{j["to"]}</time></p>'
        f'<div class="xp-r"><h4>{g(j["role"])}</h4><p>{g(j["org"])}</p></div><p class="xp-s">{g(j["sum"])}</p></li>'
        for j in EXP["jobs"])
    interns = "".join(f'<li class="xp rv"><p class="xp-w num"><time>{y}</time></p><div class="xp-r"><h4>{g(r)}</h4><p>{g(o)}</p></div><p class="xp-s">{g(d)}</p></li>'
                      for y, r, o, d in EXP["interns"])
    groups = "".join(f'<div class="sk rv"><h4>{g(h)}</h4><ul>{"".join(f"<li>{g(x)}</li>" for x in xs)}</ul></div>' for h, xs in SKILLS["groups"])
    certs = "".join(f'<li><span class="kv-k">{g(n)}</span><span class="kv-v">{g(d)}</span></li>' for n, d in SKILLS["certs"])
    langs = "".join(f'<li><span class="kv-k">{g(a)}</span><span class="kv-v">{g(b)}</span></li>' for a, b in SKILLS["langs"])

    tools = "".join(f'<li class="tl">{html.escape(t)}</li>' for t in V3["tools"])

    ld = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Kutay Kılıç", "url": BASE,
                     "image": BASE + "profile.jpg", "jobTitle": HERO["role"][i].split(",")[0],
                     "sameAs": [CONTACT["linkedin"], CONTACT["github"]],
                     "alumniOf": "İstanbul Aydın Üniversitesi", "description": META["desc"][i]}, ensure_ascii=False)
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{g(META["title"])}</title>
<meta name="description" content="{html.escape(META["desc"][i])}">
<meta name="author" content="Kutay Kılıç">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0a0b0d">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="tr" href="{BASE}">
<link rel="alternate" hreflang="en" href="{BASE}en.html">
<link rel="alternate" hreflang="x-default" href="{BASE}">
<meta property="og:type" content="profile">
<meta property="og:title" content="{html.escape(META["title"][i])}">
<meta property="og:description" content="{html.escape(META["desc"][i])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(META["title"][i])}">
<meta property="og:locale" content="{("tr_TR", "en_GB")[i]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{html.escape(META["title"][i])}">
<meta name="twitter:description" content="{html.escape(META["desc"][i])}">
<meta name="twitter:image" content="{BASE}og.png">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="apple-touch-icon.png">
<link rel="preload" href="fonts/newsreader-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="fonts/newsreader-latin-ext-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{ld}</script>
<script>document.documentElement.classList.add('js');if(!matchMedia('(prefers-reduced-motion: reduce)').matches)document.documentElement.classList.add('mo')</script>
</head>
<body>
<a class="skip" href="#main">{g(META["skip"])}</a>
<div class="grid-lines" aria-hidden="true"></div>
<header class="nav">
  <a class="brand" href="#top">{LOGO}<span>Kutay Kılıç</span></a>
  <nav aria-label="{g(META["menu"])}"><ul class="nav-l">{nav}<li><a class="nl" href="{other}" hreflang="{("en", "tr")[i]}" lang="{("en", "tr")[i]}">{bk(("EN", "TR")[i])}<span class="sr"> {g(META["langlabel"])}</span></a></li></ul></nav>
</header>
<p class="corner c-l"><span class="gold-dot" aria-hidden="true"></span>© 2026</p>
<p class="corner c-r"><a href="{CONTACT["linkedin"]}" rel="noopener" aria-label="LinkedIn">{ic("in")}</a><a href="{CONTACT["github"]}" rel="noopener" aria-label="GitHub">{ic("gh")}</a></p>
<main id="main">
  <section id="top" class="hero" aria-labelledby="hero-h">
    <canvas class="silk" aria-hidden="true"></canvas>
    <figure class="hero-por"><img src="img/portre-800.jpg" srcset="img/portre-480.jpg 480w, img/portre-800.jpg 800w" sizes="(max-width: 960px) 60vw, 34vw" width="800" height="800" alt="{g(V3["portrait"])}" fetchpriority="high" decoding="async"></figure>
    <div class="hero-in">
      <h1 id="hero-h"><span class="h1-l"><span>{g(V3["h1_a"])}</span></span> <span class="h1-l"><span>{g(V3["h1_b"])}</span></span></h1>
      <p class="bio">{g(V3["bio"])}</p>
      <div class="cta">
        <a class="talk" href="mailto:{E}" data-ask><span class="talk-a" aria-hidden="true">↳</span>{g(V3["talk"])}</a>
        <a class="chip" href="#work">{bk(g(V3["see"]))}</a>
      </div>
    </div>
    <dl class="hero-meta">
      <div><dt>{g(HERO["f2_t"])}</dt><dd class="num">{len(items)}</dd></div>
      <div><dt>{g(HERO["f_pub"])}</dt><dd class="num">{sum(1 for p in items if p.get("kind") == "gh")}</dd></div>
      <div><dt>{g(HERO["f1_t"])}</dt><dd>{g(HERO["f1"])}</dd></div>
    </dl>
  </section>

  <section id="work" class="sec" aria-labelledby="work-h">
    <div class="sh rv"><h2 id="work-h"><span class="sh-n" aria-hidden="true">01</span>{g(V3["work_h"])}</h2><p>{g(V3["work_p"])}</p></div>
    <ul class="works">{cards}</ul>
  </section>

  <section id="lab" class="sec" aria-labelledby="lab-h">
    <div class="sh rv"><h2 id="lab-h"><span class="sh-n" aria-hidden="true">02</span>{g(V3["lab_h"])}</h2><p>{g(V3["lab_p"])}</p><p class="sh-act"><a class="chip" href="#all">{bk(g(V3["all"]))}</a></p></div>
    <ul class="bento">{tiles}</ul>
  </section>

  <section id="all" class="sec" aria-labelledby="all-h">
    <div class="sh rv"><h2 id="all-h"><span class="sh-n" aria-hidden="true">03</span>{g(V3["table_h"])} <span class="num cnt">{len(rest)}</span></h2><p>{g(V3["table_p"])}</p></div>
    <div class="pt-wrap rv"><table class="pt"><thead><tr><th scope="col">{g(V3["col_p"])}</th><th scope="col">{g(V3["col_d"])}</th><th scope="col" class="pt-s">{g(V3["col_s"])}</th><th scope="col"><span class="sr">{("Bağlantı", "Link")[i]}</span><span aria-hidden="true">↗</span></th></tr></thead><tbody>{trs}</tbody></table></div>
    <div class="peek" aria-hidden="true"><p class="peek-c"></p><p class="peek-n"></p><p class="peek-s"></p></div>
  </section>

  <section id="about" class="sec" aria-labelledby="about-h">
    <div class="sh rv"><h2 id="about-h"><span class="sh-n" aria-hidden="true">04</span>{g(V3["about_h"])}</h2><p>{g(ABOUT["h"])}</p></div>
    <div class="about">
      <figure class="por rv"><img src="img/portre-480.jpg" width="480" height="480" alt="{g(HERO["alt"])}" loading="lazy" decoding="async"></figure>
      <div class="about-t rv">{about_p}</div>
      <table class="facts rv"><caption>{g(ABOUT["table_cap"])}</caption><tbody>{facts}</tbody></table>
    </div>
    <h3 class="sub rv">{g(V3["exp_h"])}</h3>
    <ol class="xps">{jobs}</ol>
    <h3 class="sub rv">{g(EXP["intern_h"])}</h3>
    <ol class="xps">{interns}</ol>
    <div class="skbox rv"><h3 class="sub">{g(SKILLS["h"])}</h3><div class="sks">{groups}</div></div>
    <div class="cl">
      <div class="rv cl-c"><h3 class="sub">{g(SKILLS["cert_h"])}</h3><p class="small muted">{g(SKILLS["cert_p"])}</p><ul class="kv">{certs}</ul></div>
      <div class="rv cl-l"><h3 class="sub">{g(SKILLS["lang_h"])}</h3><ul class="kv">{langs}</ul></div>
    </div>
  </section>

  <section id="tools" class="sec sec-tight" aria-labelledby="tools-h">
    <h2 id="tools-h" class="lbl rv">{g(V3["tools_h"])}</h2>
    <div class="mq rv"><ul class="mq-t">{tools}</ul><ul class="mq-t" aria-hidden="true">{tools}</ul></div>
  </section>

  <section id="jury" class="sec sec-tight" aria-labelledby="jury-h">
    <h2 id="jury-h" class="lbl rv">{g(V3["jury_h"])}</h2>
    {jury_html(i, g)}
  </section>
</main>
<footer id="contact" class="foot" aria-labelledby="contact-h">
  <div class="foot-in">
    <h2 id="contact-h" class="rv">{g(V3["contact_h"])}</h2>
    <p class="muted rv">{g(V3["contact_p"])}</p>
    <p class="rv"><a class="mail" href="mailto:{E}" data-ask>{E}</a></p>
    <ul class="foot-links rv">
      <li><a class="chip" href="{CONTACT["linkedin"]}" rel="noopener">{bk("LinkedIn")}</a></li>
      <li><a class="chip" href="{CONTACT["github"]}" rel="noopener">{bk("GitHub")}</a></li>
      <li><a class="chip" href="#top">{bk(g(CONTACT["top"]))}</a></li>
    </ul>
  </div>
  <div class="netw">{net_svg()}<p class="net-c" aria-hidden="true"><span>{g(V3["net_c"])}</span><em>{g(V3["net_s"])}</em></p></div>
  <p class="foot-m small">© 2026 Kutay Kılıç</p>
</footer>
<div class="ask" role="dialog" aria-modal="false" aria-labelledby="ask-q" hidden>
  <p id="ask-q">{g(V3["ask"]["q"])}</p>
  <p class="ask-a num">{E}</p>
  <div class="ask-b"><a class="chip ask-open" href="mailto:{E}">{bk(g(V3["ask"]["open"]))}</a><button type="button" class="chip ask-copy" data-done="{g(V3["ask"]["copied"])}">{bk(g(V3["ask"]["copy"]))}</button><button type="button" class="chip ask-x">{bk(g(V3["ask"]["close"]))}</button></div>
</div>
<script src="script.js" defer></script>
</body>
</html>
"""

for i, name in enumerate(("index.html", "en.html")):
    out = page(i)
    assert not ZW.search(out)
    assert "\u2014" not in out and "\u2013" not in out, "uzun tire var"
    (ROOT / name).write_text(out, encoding="utf-8")
    print("wrote", name)
