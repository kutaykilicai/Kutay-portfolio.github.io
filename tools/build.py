"""index.html (TR) ve en.html (EN) dosyalarını content.py'den üretir.
Çalıştırma: python3 tools/build.py  (depo kökünden)"""
import html, json, pathlib, re
from content import *

ROOT = pathlib.Path(__file__).resolve().parent.parent
ZW = re.compile("[\u200b\u200c\u200d\u2060\ufeff]")

def T(v, i):
    """Metni seçili dile çevir, HTML'e kaçır, düz kesme işaretini tipografik yap."""
    if isinstance(v, tuple):
        v = v[i]
    return html.escape(ZW.sub("", v), quote=False).replace("'", "\u2019")

TICK = '<svg class="tick" viewBox="0 0 28 24" aria-hidden="true" focusable="false"><path d="M3 13.2c2.4 1.7 4.4 3.8 6.2 6.6C13 12.6 17.6 7.2 25 3.4"/></svg>'

def page(i):
    lang = ("tr", "en")[i]
    me = ("index.html", "en.html")[i]
    other = ("en.html", "index.html")[i]
    url = BASE if i == 0 else BASE + "en.html"
    g = lambda v: T(v, i)
    nav = "".join(f'<li><a href="#{k}">{g(v)}</a></li>' for k, v in NAV)

    rows = "".join(f'<tr><th scope="row">{g(a)}</th><td>{g(b)}</td></tr>' for a, b in ABOUT["rows"])
    about_p = "".join(f"<p>{g(p)}</p>" for p in ABOUT["p"])

    jobs = ""
    for j in EXP["jobs"]:
        items = "".join(f"<li>{g(x)}</li>" for x in j["items"])
        jobs += (f'<li class="job"><p class="job-when"><time>{j["from"]}</time><span class="sr"> </span><time>{j["to"]}</time></p>'
                 f'<div class="job-head"><h3>{g(j["role"])}</h3><p class="job-org">{g(j["org"])}</p></div>'
                 f'<div class="job-body"><p>{g(j["sum"])}</p><ul>{items}</ul></div></li>')
    interns = "".join(f'<li class="job job-small"><p class="job-when"><time>{y}</time></p><div class="job-head"><h4>{g(r)}</h4><p class="job-org">{g(o)}</p></div><div class="job-body"><p>{g(d)}</p></div></li>'
                      for y, r, o, d in EXP["interns"])

    projs = ""
    for p in PROJ["items"]:
        name = g(p["name"])
        if p["url"]:
            go = g(PROJ["gh"] if p["kind"] == "gh" else PROJ["site"])
            title = f'<a class="proj-link" href="{p["url"]}" rel="noopener">{name}<span class="sr">, {go}</span></a>'
            tail = f'<span class="proj-go" aria-hidden="true">{go}<svg viewBox="0 0 16 16" focusable="false"><path d="M4 12 12 4M6 4h6v6"/></svg></span>'
            cls, tick = "proj is-public", TICK
        else:
            title, tail, cls, tick = name, "", "proj", ""
        fig = ""
        if p.get("img"):
            im = p["img"]
            ss = f' srcset="{im["srcset"]}" sizes="(max-width: 760px) 90vw, 720px"' if im.get("srcset") else ""
            fig = f'<figure class="proj-fig {im["cls"]}"><img src="{im["src"]}"{ss} width="{im["w"]}" height="{im["h"]}" alt="{g(im["alt"])}" loading="lazy" decoding="async"></figure>'
            cls += " has-fig"
        projs += (f'<li class="{cls}"><span class="proj-mark">{tick}</span><h3 class="proj-name">{title}</h3>'
                  f'<p class="proj-cat">{g(p["cat"])}</p><p class="proj-d">{g(p["d"])}</p><p class="proj-s">{g(p["s"])}</p>{tail}{fig}</li>')

    groups = "".join(f'<div class="sk"><h3>{g(h)}</h3><ul>{"".join(f"<li>{g(x)}</li>" for x in xs)}</ul></div>' for h, xs in SKILLS["groups"])
    certs = "".join(f"<li><span>{g(n)}</span><span class=\"muted\">{g(d)}</span></li>" for n, d in SKILLS["certs"])
    langs = "".join(f"<tr><th scope=\"row\">{g(a)}</th><td>{g(b)}</td></tr>" for a, b in SKILLS["langs"])

    ld = json.dumps({"@context": "https://schema.org", "@type": "Person", "name": "Kutay Kılıç", "url": BASE,
                     "image": BASE + "profile.jpg", "sameAs": [CONTACT["linkedin"], CONTACT["github"]],
                     "alumniOf": "İstanbul Aydın Üniversitesi", "description": META["desc"][i]}, ensure_ascii=False)
    E = CONTACT["email"]
    return f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{g(META["title"])}</title>
<meta name="description" content="{html.escape(META["desc"][i])}">
<meta name="author" content="Kutay Kılıç">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="tr" href="{BASE}">
<link rel="alternate" hreflang="en" href="{BASE}en.html">
<meta property="og:type" content="profile">
<meta property="og:title" content="{html.escape(META["title"][i])}">
<meta property="og:description" content="{html.escape(META["desc"][i])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{("tr_TR", "en_GB")[i]}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4f2ec">
<link rel="icon" href="favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="profile.jpg">
<link rel="stylesheet" href="style.css">
<script type="application/ld+json">{ld}</script>
<script>document.documentElement.classList.add('js')</script>
</head>
<body id="top">
<a class="skip" href="#main">{g(META["skip"])}</a>
<header class="bar">
  <div class="wrap bar-in">
    <a class="brand" href="#top">{TICK}Kutay Kılıç</a>
    <nav aria-label="{g(META["menu"])}">
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="nav-list">{g(META["menu"])}</button>
      <ul id="nav-list" class="nav-list">{nav}</ul>
    </nav>
    <a class="lang" href="{other}" hreflang="{("en", "tr")[i]}" lang="{("en", "tr")[i]}" >{("EN", "TR")[i]}<span class="sr"> {g(META["langlabel"])}</span></a>
  </div>
</header>
<main id="main">
  <section class="hero wrap" aria-labelledby="hero-h">
    <div class="hero-text">
      <h1 id="hero-h">{TICK.replace('class="tick"', 'class="tick tick-name"')}Kutay Kılıç</h1>
      <p class="lede">{g(HERO["lede_a"])}<mark class="hl">{g(HERO["mark"])}</mark>{g(HERO["lede_b"])}</p>
      <div class="actions">
        <a class="btn" href="#projects">{g(HERO["cta"])}</a>
        <a class="link" href="mailto:{E}">{g(HERO["mail"])}</a>
      </div>
      <p class="hero-role">{g(HERO["role"])}</p>
    </div>
    <figure class="hero-photo">
      <img src="profile.jpg" width="800" height="800" alt="{g(HERO["alt"])}" fetchpriority="high" decoding="async">
    </figure>
  </section>

  <section id="about" class="sec wrap about" aria-labelledby="about-h">
    <h2 id="about-h">{g(ABOUT["h"])}</h2>
    <div class="about-text">{about_p}</div>
    <table class="facts"><caption>{g(ABOUT["table_cap"])}</caption><tbody>{rows}</tbody></table>
  </section>

  <section id="experience" class="sec band" aria-labelledby="exp-h">
    <div class="wrap">
      <h2 id="exp-h">{g(EXP["h"])}</h2>
      <ol class="jobs">{jobs}</ol>
      <h3 class="interns-h">{g(EXP["intern_h"])}</h3>
      <ol class="jobs jobs-small">{interns}</ol>
    </div>
  </section>

  <section id="projects" class="sec wrap" aria-labelledby="proj-h">
    <div class="sec-head">
      <h2 id="proj-h">{g(PROJ["h"])}</h2>
      <p class="legend">{TICK}<span>{g(PROJ["legend"])}</span></p>
    </div>
    <ul class="projs">{projs}</ul>
  </section>

  <section id="skills" class="sec wrap" aria-labelledby="skills-h">
    <h2 id="skills-h">{g(SKILLS["h"])}</h2>
    <div class="skills">{groups}</div>
    <div class="certs-langs">
      <div>
        <h3>{g(SKILLS["cert_h"])}</h3>
        <p class="muted">{g(SKILLS["cert_p"])}</p>
        <ul class="certs">{certs}</ul>
      </div>
      <div>
        <h3>{g(SKILLS["lang_h"])}</h3>
        <table class="facts"><tbody>{langs}</tbody></table>
      </div>
    </div>
  </section>
</main>
<footer id="contact" class="foot" aria-labelledby="contact-h">
  <div class="wrap">
    <h2 id="contact-h">{g(CONTACT["h"])}</h2>
    <p class="foot-p">{g(CONTACT["p"])}</p>
    <a class="mail" href="mailto:{E}">{E}</a>
    <ul class="foot-links">
      <li><a href="{CONTACT["linkedin"]}" rel="noopener">linkedin.com/in/kutay-kilicc</a></li>
      <li><a href="{CONTACT["github"]}" rel="noopener">github.com/kutaykilicai</a></li>
    </ul>
    <div class="foot-base">
      <p>© 2026 Kutay Kılıç. {g(CONTACT["foot"])}</p>
      <a href="#top">{g(CONTACT["top"])}</a>
    </div>
  </div>
</footer>
<script src="script.js" defer></script>
</body>
</html>
"""

for i, name in enumerate(("index.html", "en.html")):
    out = page(i)
    assert not ZW.search(out)
    (ROOT / name).write_text(out, encoding="utf-8")
    print("wrote", name)
