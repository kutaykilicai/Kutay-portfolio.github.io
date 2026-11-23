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

def jury_html(i, g):
    if not JURY_FILE.exists():
        w = (40, 30, 20, 10)
        cards = ""
        for nm, sub, model in ((JURY["ds"], JURY["ds_sub"], "deepseek-v4.1-flash-abliterated"), (JURY["gm"], JURY["gm_sub"], "gemini-3.1-pro-preview")):
            cats = "".join(f'<li class="jr"><div class="jr-top"><span class="jr-k">{g(cl)}</span><span class="jr-v">%{w[k]}</span></div></li>' for k, (ck, cl) in enumerate(JURY["cats"]))
            cards += (f'<article class="judge rv"><header class="judge-head"><div><h3>{g(nm)}</h3><p class="muted small">{g(sub)}</p>'
                      f'<p class="small model">{model}</p></div></header><ul class="jrs">{cats}</ul></article>')
        return f'<div class="judges">{cards}</div>'
    J = json.loads(JURY_FILE.read_text(encoding="utf-8"))
    out = ""
    for key, nm, sub in (("deepseek", JURY["ds"], JURY["ds_sub"]), ("gemini", JURY["gm"], JURY["gm_sub"])):
        d = J["final"][key]
        rows = ""
        for ck, cl in JURY["cats"]:
            c = d["scores"][ck]
            v = float(c["score"])
            reason = c["reason_tr"] if i == 0 else c["reason_en"]
            rows += (f'<li class="jr"><div class="jr-top"><span class="jr-k">{g(cl)}</span><span class="jr-v">{fmt(v, i)}</span></div>'
                     f'<span class="meter" aria-hidden="true"><span style="--v:{v/10:.3f}"></span></span>'
                     f'<p class="jr-why">{g(reason)}</p></li>')
        b = J["baseline"][key]["overall"]
        out += (f'<article class="judge rv"><header class="judge-head"><div><h3>{g(nm)}</h3><p class="muted small">{g(sub)}</p>'
                f'<p class="small model">{html.escape(d["model"])}</p></div>'
                f'<p class="judge-score"><span class="big">{fmt(d["overall"], i)}</span><span class="small muted">{g(JURY["overall"])}</span></p></header>'
                f'<ul class="jrs">{rows}</ul>'
                f'<p class="judge-foot small muted">{g(JURY["before"])}: {fmt(b, i)} · {J["rounds"]} {g(JURY["rounds"])}</p></article>')
    return f'<div class="judges">{out}</div>'

def page(i):
    lang = ("tr", "en")[i]
    other = ("en.html", "index.html")[i]
    url = BASE if i == 0 else BASE + "en.html"
    g = lambda v: T(v, i)
    items = PROJ["items"]
    n_all = len(items)
    n_pub = sum(1 for p in items if p.get("kind") == "gh")

    side = "".join(f'<li><a href="#{k}" data-sec="{k}">{ic(icon)}<span>{g(v)}</span></a></li>' for k, v, icon in NAV)
    sec_names = {k: g(v) for k, v, _ in NAV}

    rows = "".join(f'<tr><th scope="row">{g(a)}</th><td>{g(b)}</td></tr>' for a, b in ABOUT["rows"])
    about_p = "".join(f"<p>{g(p)}</p>" for p in ABOUT["p"])
    jobs = "".join(
        f'<li class="job"><p class="job-when"><time>{j["from"]}</time> <span aria-hidden="true">·</span> <time>{j["to"]}</time></p>'
        f'<div><h4>{g(j["role"])}</h4><p class="job-org">{g(j["org"])}</p><p class="job-sum">{g(j["sum"])}</p></div></li>'
        for j in EXP["jobs"])
    interns = "".join(f'<li class="job"><p class="job-when"><time>{y}</time></p><div><h4>{g(r)}</h4><p class="job-org">{g(o)}</p></div></li>'
                      for y, r, o, d in EXP["interns"])

    gname = dict(PROJ["groups"])
    counts = {k: sum(1 for p in items if p["g"] == k) for k, _ in PROJ["groups"]}
    chips = f'<button type="button" class="chip" aria-pressed="true" data-f="all">{g(PROJ["all"])}<span class="cnt">{n_all}</span></button>'
    chips += "".join(f'<button type="button" class="chip" aria-pressed="false" data-f="{k}">{g(v)}<span class="cnt">{counts[k]}</span></button>' for k, v in PROJ["groups"])

    def link(p):
        if p.get("url"):
            label = g(PROJ["gh"] if p["kind"] == "gh" else PROJ["site"])
            return f'<a class="go" href="{p["url"]}" rel="noopener"><span>{label}</span>{ic("arrow", "ic go-ic")}<span class="sr">: {g(p["name"])}</span></a>'
        if p.get("priv"):
            return f'<span class="tag">{ic("lock", "ic tag-ic")}{g(PROJ["priv"])}</span>'
        return f'<span class="tag tag-quiet">{g(PROJ["nolink"])}</span>'

    feat = ""
    for p in [x for x in items if x.get("feat")]:
        im = p["img"]
        ss = f' srcset="{im["srcset"]}" sizes="(max-width: 900px) 92vw, 640px"' if im.get("srcset") else ""
        why = f'<p class="why"><span>{g(PROJ["why"])}</span> {g(p["why"])}</p>' if p.get("why") else ""
        if p.get("how"): why += f'<p class="why"><span>{g(PROJ["how"])}</span> {g(p["how"])}</p>'
        feat += (f'<li class="card rv" data-g="{p["g"]}"><figure class="shot {im.get("cls", "")}">'
                 f'<div class="win-bar" aria-hidden="true"><span class="win-t">{g(p["name"])}</span><span class="win-btns"><i class="w-min"></i><i class="w-max"></i><i class="w-x"></i></span></div>'
                 f'<div class="win-body"><img src="{im["src"]}"{ss} width="{im["w"]}" height="{im["h"]}" alt="{g(im["alt"])}" loading="lazy" decoding="async"></div></figure>'
                 f'<div class="card-body"><p class="cat">{g(gname[p["g"]])}</p><h3>{g(p["name"])}</h3>{why}<p class="d">{g(p["d"])}</p>'
                 f'<div class="card-foot"><p class="stack">{g(p["s"])}</p>{link(p)}</div></div></li>')
    rest = ""
    for p in [x for x in items if not x.get("feat")]:
        rest += (f'<li class="row rv" data-g="{p["g"]}"><div class="row-main"><h3>{g(p["name"])}</h3><p class="cat">{g(gname[p["g"]])}</p></div>'
                 f'<p class="d">{g(p["d"])}</p><div class="row-side"><p class="stack">{g(p["s"])}</p>{link(p)}</div></li>')

    groups = "".join(f'<div class="sk rv"><h3>{g(h)}</h3><ul>{"".join(f"<li>{g(x)}</li>" for x in xs)}</ul></div>' for h, xs in SKILLS["groups"])
    certs = "".join(f'<li><span>{g(n)}</span><span class="muted">{g(d)}</span></li>' for n, d in SKILLS["certs"])
    langs = "".join(f'<tr><th scope="row">{g(a)}</th><td>{g(b)}</td></tr>' for a, b in SKILLS["langs"])

    ld = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Kutay Kılıç", "url": BASE,
                     "image": BASE + "profile.jpg", "jobTitle": HERO["role"][i].split(",")[0],
                     "sameAs": [CONTACT["linkedin"], CONTACT["github"]],
                     "alumniOf": "İstanbul Aydın Üniversitesi", "description": META["desc"][i]}, ensure_ascii=False)
    E = CONTACT["email"]
    secjson = html.escape(json.dumps(sec_names, ensure_ascii=False))
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{g(META["title"])}</title>
<meta name="description" content="{html.escape(META["desc"][i])}">
<meta name="author" content="Kutay Kılıç">
<meta name="color-scheme" content="dark">
<meta name="theme-color" content="#0b0b0c">
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
<link rel="preload" as="image" href="img/portre-800.jpg" imagesrcset="img/portre-480.jpg 480w, img/portre-800.jpg 800w" imagesizes="(max-width: 960px) 100vw, 58vw" fetchpriority="high">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{ld}</script>
<script>document.documentElement.classList.add('js')</script>
</head>
<body>
<a class="skip" href="#main">{g(META["skip"])}</a>
<header class="toolbar">
  <button class="side-btn" type="button" aria-expanded="false" aria-controls="side">{ic("side")}<span class="sr">{g(META["menu"])}</span></button>
  <a class="brand" href="#top">{LOGO}<span>Kutay Kılıç</span></a>
  <p class="here" aria-hidden="true"><span class="here-t" data-sec-names="{secjson}">{sec_names["top"]}</span></p>
  <div class="tb-end">
    <a class="lang" href="{other}" hreflang="{("en", "tr")[i]}" lang="{("en", "tr")[i]}">{("EN", "TR")[i]}<span class="sr"> {g(META["langlabel"])}</span></a>
    <a class="tb-mail" href="mailto:{E}">{ic("mail")}<span>{g(sec_names["contact"])}</span></a>
  </div>
</header>
<div class="shell">
<nav id="side" class="side" aria-label="{g(META["menu"])}">
  <ul class="side-list">{side}</ul>
  <div class="side-foot">
    <a href="{CONTACT["github"]}" rel="noopener">{ic("gh")}<span>GitHub</span></a>
    <a href="{CONTACT["linkedin"]}" rel="noopener">{ic("in")}<span>LinkedIn</span></a>
  </div>
</nav>
<div class="scrim" hidden></div>
<main id="main">
  <section id="top" class="hero" aria-labelledby="hero-h">
    <svg class="hero-mark" viewBox="0 0 64 64" aria-hidden="true" focusable="false"><g fill="none" stroke-linecap="round" stroke-linejoin="round" stroke-width="1.1"><path d="M15 15v34M15 35 29 15M21.5 27 29 49"/><path d="M35 15v34M35 35 49 15M41.5 27 49 49"/></g></svg>
    <div class="hero-text">
      <p class="eyebrow hi" style="--d:0">{g(HERO["role"])}</p>
      <h1 id="hero-h" class="hi" style="--d:1">Kutay Kılıç</h1>
      <p class="lede hi" style="--d:2">{g(HERO["lede_a"])}<em class="hl">{g(HERO["mark"])}</em>{g(HERO["lede_b"])}</p>
      <div class="actions hi" style="--d:3">
        <a class="btn" href="#projects">{g(HERO["cta"])} <svg class="btn-arrow" width="14" height="14" viewBox="0 0 16 16" aria-hidden="true"><path d="M8 3v10M4 9l4 4 4-4" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
        <a class="btn-2" href="mailto:{E}">{g(HERO["mail"])}</a>
      </div>
    </div>
    <figure class="hero-photo hi" style="--d:1">
      <img src="img/portre-800.jpg" srcset="img/portre-480.jpg 480w, img/portre-800.jpg 800w" sizes="(max-width: 960px) 100vw, 58vw" width="800" height="800" alt="{g(HERO["alt"])}" fetchpriority="high" decoding="async">
    </figure>
    <dl class="facts-strip hi" style="--d:4">
      <div><dt>{g(HERO["f1_t"])}</dt><dd>{g(HERO["f1"])}</dd></div>
      <div><dt>{g(HERO["f2_t"])}</dt><dd>{n_all} {g(HERO["f_proj"])}, {n_pub} {g(HERO["f_pub"])}</dd></div>
      <div><dt>{g(HERO["f3_t"])}</dt><dd>{g(HERO["f3"])}</dd></div>
    </dl>
  </section>

  <section id="about" class="sec" aria-labelledby="about-h">
    <h2 id="about-h" class="rv">{g(ABOUT["h"])}</h2>
    <div class="about-grid">
      <div class="about-text rv">{about_p}</div>
      <table class="facts rv"><caption>{g(ABOUT["table_cap"])}</caption><tbody>{rows}</tbody></table>
    </div>
    <div class="exp rv">
      <h3>{g(EXP["h"])}</h3>
      <ol class="jobs">{jobs}</ol>
      <h3 class="interns-h">{g(EXP["intern_h"])}</h3>
      <ol class="jobs jobs-small">{interns}</ol>
    </div>
  </section>

  <section id="projects" class="sec" aria-labelledby="proj-h">
    <div class="sec-head rv">
      <h2 id="proj-h">{g(PROJ["h"])}</h2>
      <p class="muted">{g(PROJ["p"])}</p>
    </div>
    <div class="filter rv" role="group" aria-label="{g(PROJ["filter"])}"><span class="pill" aria-hidden="true"></span>{chips}</div>
    <p class="sr" aria-live="polite" id="f-status"></p>
    <ul class="cards">{feat}</ul>
    <h3 class="more-h rv">{g(PROJ["more_h"])}</h3>
    <ul class="rows">{rest}</ul>
  </section>

  <section id="skills" class="sec" aria-labelledby="skills-h">
    <h2 id="skills-h" class="rv">{g(SKILLS["h"])}</h2>
    <div class="skills">{groups}</div>
    <div class="certs-langs">
      <div class="panel rv">
        <h3>{g(SKILLS["cert_h"])}</h3>
        <p class="muted small">{g(SKILLS["cert_p"])}</p>
        <ul class="certs">{certs}</ul>
      </div>
      <div class="panel rv">
        <h3>{g(SKILLS["lang_h"])}</h3>
        <table class="facts"><tbody>{langs}</tbody></table>
      </div>
    </div>
  </section>

  <section id="jury" class="sec" aria-labelledby="jury-h">
    <div class="sec-head rv">
      <h2 id="jury-h">{g(JURY["h"])}</h2>
      <p class="muted">{g(JURY["p"])}</p>
    </div>
    {jury_html(i, g)}
  </section>
</main>
</div>
<footer id="contact" class="foot" aria-labelledby="contact-h">
  <div class="foot-in">
    <h2 id="contact-h" class="rv">{g(CONTACT["h"])}</h2>
    <p class="muted rv">{g(CONTACT["p"])}</p>
    <a class="mail rv" href="mailto:{E}">{E}</a>
    <ul class="foot-links rv">
      <li><a href="{CONTACT["linkedin"]}" rel="noopener">{ic("in")}linkedin.com/in/kutay-kilicc</a></li>
      <li><a href="{CONTACT["github"]}" rel="noopener">{ic("gh")}github.com/kutaykilicai</a></li>
    </ul>
    <div class="foot-base">
      <p>© 2026 Kutay Kılıç. {g(CONTACT["foot"])}</p>
      <a href="#top">{g(CONTACT["top"])}</a>
    </div>
  </div>
</footer>
<p class="statusbar"><span>{n_all} {g(HERO["f_proj"])}</span><span>{n_pub} {g(HERO["f_pub"])}</span><span>{g(PROJ["status"])}</span><span class="sb-here" aria-hidden="true"></span></p>
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
