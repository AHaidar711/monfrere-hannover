#!/usr/bin/env python3
"""Baut die statische Seite von monfrere-hannover.de.

Aufruf (im Repo-Hauptordner):  python3 werkzeug/build.py

Liest daten/betrieb.json + daten/karte.json und schreibt
index.html, speisekarte.html, impressum.html, datenschutz.html und 404.html.
Keine Abhängigkeiten außer Python 3.
"""
import json
import html
import os
import re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = json.load(open(os.path.join(ROOT, "daten/betrieb.json"), encoding="utf-8"))
K = json.load(open(os.path.join(ROOT, "daten/karte.json"), encoding="utf-8"))
VERSION = date.today().strftime("%Y%m%d")


def e(s):
    return html.escape(str(s), quote=True)


def preis(p):
    if not p:
        return ""
    plus = p.startswith("+")
    zahl = p.lstrip("+").replace(".", ",")
    return ("+ " if plus else "") + zahl + " €"


def slug(s):
    s = s.lower().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss").replace("è", "e")
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")


TEL = B["telefon"]
TEL_LINK = "tel:+49" + re.sub(r"\D", "", TEL)[1:]
ADRESSE = f'{B["strasse"]}, {B["plz"]} {B["ort"]}'
MAPS = "https://www.google.com/maps/search/?api=1&query=" + "Mon+Fr%C3%A8re+Nikolaistra%C3%9Fe+32+30159+Hannover"
APPLE = f'https://maps.apple.com/?q=Mon%20Fr%C3%A8re&address=Nikolaistra%C3%9Fe%2032,%2030159%20Hannover&ll={B["geo"][0]},{B["geo"][1]}'

ICON = {
    "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6.5a2.5 2.5 0 0 1 0 5z"/></svg>',
    "insta": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.3 5.5a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM21.9 7.1c-.1-1.6-.4-3-1.6-4.2S17.7 1.3 16.1 1.2C14.4 1.1 9.6 1.1 7.9 1.2 6.3 1.3 4.9 1.6 3.7 2.8S2.1 5.5 2 7.1C1.9 8.8 1.9 15.2 2 16.9c.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.7.1 6.5.1 8.2 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.1-1.7.1-8.1.1-9.8zm-2.2 11.7a3.3 3.3 0 0 1-1.9 1.9c-1.3.5-4.4.4-5.8.4s-4.5.1-5.8-.4a3.3 3.3 0 0 1-1.9-1.9c-.5-1.3-.4-4.4-.4-5.8s-.1-4.5.4-5.8a3.3 3.3 0 0 1 1.9-1.9C7.5 4.8 10.6 4.9 12 4.9s4.5-.1 5.8.4a3.3 3.3 0 0 1 1.9 1.9c.5 1.3.4 4.4.4 5.8s.1 4.5-.4 5.8z"/></svg>',
    "tiktok": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M16.6 2h-3.4v13.4a2.9 2.9 0 1 1-2.9-2.9c.3 0 .6 0 .9.1V9.1a6.4 6.4 0 1 0 5.4 6.3V8.6a8 8 0 0 0 4.7 1.5V6.7a4.7 4.7 0 0 1-4.7-4.7z"/></svg>',
    "uhr": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm0 18a8 8 0 1 1 0-16 8 8 0 0 1 0 16zm.5-13H11v6l5.2 3.2.8-1.3-4.5-2.7z"/></svg>',
}

NAV = [
    ("speisekarte.html", "Speisekarte"),
    ("speisekarte.html#shisha", "Shisha"),
    ("index.html#zeiten", "Öffnungszeiten"),
    ("index.html#anfahrt", "Anfahrt"),
]


def layout(*, datei, titel, beschreibung, inhalt, extra_head="", body_klasse=""):
    canonical = B["domain"] + ("" if datei == "index.html" else datei)
    aktuell = ' aria-current="page"'
    nav = "".join(
        f'<a href="{href}"{aktuell if href == datei else ""}>{e(t)}</a>' for href, t in NAV
    )
    return f"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(titel)}</title>
<meta name="description" content="{e(beschreibung)}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#0b0b0b">
<meta property="og:type" content="website">
<meta property="og:locale" content="de_DE">
<meta property="og:site_name" content="Mon Frère Hannover">
<meta property="og:title" content="{e(titel)}">
<meta property="og:description" content="{e(beschreibung)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{B["domain"]}assets/img/og-bild.jpg">
<link rel="icon" type="image/png" sizes="32x32" href="assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
<link rel="preload" href="assets/fonts/CormorantGaramond-500.woff" as="font" type="font/woff" crossorigin>
<link rel="stylesheet" href="assets/css/stil.css?v={VERSION}">
{extra_head}</head>
<body class="{body_klasse}">
<a class="skip" href="#inhalt">Zum Inhalt springen</a>
<header class="kopf">
  <div class="kopf__innen">
    <a class="kopf__logo" href="index.html" aria-label="Mon Frère – Startseite">
      <img src="assets/img/logo-mf.png" alt="" width="40" height="30">
      <span>Mon Frère</span>
    </a>
    <nav class="kopf__nav" aria-label="Hauptnavigation">{nav}</nav>
    <a class="knopf knopf--klein" href="{TEL_LINK}">{ICON["tel"]}<span>Anrufen</span></a>
  </div>
</header>
<main id="inhalt">
{inhalt}
</main>
<footer class="fuss">
  <div class="fuss__innen">
    <div class="fuss__marke">
      <img src="assets/img/logo-mf.png" alt="Mon Frère" width="64" height="48">
      <p>Shisha · Sushi · Cocktails<br>{e(ADRESSE)}</p>
    </div>
    <div class="fuss__spalte">
      <h2>Kontakt</h2>
      <p><a href="{TEL_LINK}">{e(TEL)}</a><br>
      <a href="{B["instagram_url"]}" rel="noopener" target="_blank">Instagram @{e(B["instagram"])}</a><br>
      <a href="{B["tiktok_url"]}" rel="noopener" target="_blank">TikTok @{e(B["tiktok"])}</a></p>
    </div>
    <div class="fuss__spalte">
      <h2>Lieferung</h2>
      <p>Sushi aus unserer Küche nach Hause:<br><a href="{B["lieferung_url"]}" rel="noopener" target="_blank">{e(B["lieferung_name"])} · {e(B["lieferung_anzeige"])}</a></p>
    </div>
  </div>
  <div class="fuss__unten">
    <span>© {date.today().year} Mon Frère Hannover</span>
    <span><a href="impressum.html">Impressum</a> · <a href="datenschutz.html">Datenschutz</a></span>
  </div>
</footer>
</body>
</html>
"""


# ---------- Öffnungszeiten ----------

def zeiten_tabelle():
    zeilen = "".join(
        f'<tr><th scope="row">{e(z["tage"])}</th><td>{e(z["von"])} – {e(z["bis"])} Uhr</td></tr>' for z in B["zeiten"]
    )
    return f'<table class="zeiten">{zeilen}</table>'


def json_ld():
    tage = {"Mo": "Monday", "Di": "Tuesday", "Mi": "Wednesday", "Do": "Thursday", "Fr": "Friday", "Sa": "Saturday", "So": "Sunday"}
    spec = []
    for z in B["zeiten_maschinell"]:
        spec.append({
            "@type": "OpeningHoursSpecification",
            "dayOfWeek": [tage[t] for t in z["tage"]],
            "opens": z["von"],
            "closes": z["bis"],
        })
    daten = {
        "@context": "https://schema.org",
        "@type": "BarOrPub",
        "name": "Mon Frère",
        "description": B["kurz"],
        "url": B["domain"],
        "telephone": "+49" + re.sub(r"\D", "", TEL)[1:],
        "image": B["domain"] + "assets/img/og-bild.jpg",
        "logo": B["domain"] + "assets/img/icon-512.png",
        "priceRange": "€€",
        "servesCuisine": ["Sushi", "Asiatisch", "Cocktails"],
        "hasMenu": B["domain"] + "speisekarte.html",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": B["strasse"],
            "postalCode": B["plz"],
            "addressLocality": B["ort"],
            "addressCountry": "DE",
        },
        "geo": {"@type": "GeoCoordinates", "latitude": B["geo"][0], "longitude": B["geo"][1]},
        "openingHoursSpecification": spec,
        "sameAs": [B["instagram_url"], B["tiktok_url"]],
    }
    return '<script type="application/ld+json">' + json.dumps(daten, ensure_ascii=False) + "</script>\n"


OFFEN_JS = """<script>
(function(){
  // Öffnungszeiten in Minuten ab Mitternacht, Schließzeit nach Mitternacht = +1440
  var plan = %s; // Index 0 = Sonntag
  var el = document.getElementById('jetzt');
  if (!el) return;
  function berlin(){
    var p = new Intl.DateTimeFormat('de-DE',{timeZone:'Europe/Berlin',weekday:'short',hour:'2-digit',minute:'2-digit',hour12:false}).formatToParts(new Date());
    var o = {}; p.forEach(function(x){o[x.type]=x.value;});
    var tage = {'So':0,'Mo':1,'Di':2,'Mi':3,'Do':4,'Fr':5,'Sa':6};
    return {tag: tage[o.weekday.replace('.','')], min: (parseInt(o.hour,10)%%24)*60+parseInt(o.minute,10)};
  }
  function uhr(m){ m = m %% 1440; return String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%%60).padStart(2,'0'); }
  try {
    var n = berlin(), heute = plan[n.tag], gestern = plan[(n.tag+6)%%7];
    var text, offen = false;
    if (gestern && n.min < gestern[1]-1440) { offen = true; text = 'Jetzt geöffnet · bis ' + uhr(gestern[1]) + ' Uhr'; }
    else if (heute && n.min >= heute[0]) { offen = true; text = 'Jetzt geöffnet · bis ' + uhr(heute[1]) + ' Uhr'; }
    else if (heute) { text = 'Heute ab ' + uhr(heute[0]) + ' Uhr geöffnet'; }
    if (text) { el.textContent = text; el.classList.add(offen ? 'ist-offen' : 'ist-zu'); el.hidden = false; }
  } catch(err) {}
})();
</script>
"""


def plan_js():
    plan = [None] * 7
    idx = {"So": 0, "Mo": 1, "Di": 2, "Mi": 3, "Do": 4, "Fr": 5, "Sa": 6}
    for z in B["zeiten_maschinell"]:
        h1, m1 = map(int, z["von"].split(":"))
        h2, m2 = map(int, z["bis"].split(":"))
        auf = h1 * 60 + m1
        zu = h2 * 60 + m2
        if zu <= auf:
            zu += 1440
        for t in z["tage"]:
            plan[idx[t]] = [auf, zu]
    return OFFEN_JS % json.dumps(plan)


# ---------- Startseite ----------

def startseite():
    karten = ""
    for k in B["bereiche"]:
        karten += f"""
      <a class="bereich" href="{k["link"]}">
        <img src="assets/img/{k["bild"]}.webp" alt="{e(k["alt"])}" loading="lazy" width="800" height="600">
        <div class="bereich__text">
          <h3>{e(k["titel"])}</h3>
          <p>{e(k["text"])}</p>
          <span class="pfeil">{e(k["cta"])} →</span>
        </div>
      </a>"""
    inhalt = f"""
<section class="held">
  <div class="held__bild" aria-hidden="true"></div>
  <div class="held__innen">
    <img class="held__logo" src="assets/img/logo-mf.png" alt="" width="180" height="137">
    <h1>Mon Frère</h1>
    <p class="held__zeile">Shisha · Sushi · Cocktails</p>
    <p class="held__ort">{e(B["strasse"])} · {e(B["ort"])}-Mitte</p>
    <p class="status" id="jetzt" hidden></p>
    <div class="held__knoepfe">
      <a class="knopf" href="speisekarte.html">Speisekarte ansehen</a>
      <a class="knopf knopf--rand" href="{TEL_LINK}">{ICON["tel"]}<span>Tisch reservieren</span></a>
    </div>
  </div>
</section>

<section class="abschnitt willkommen">
  <div class="eng">
    <p class="dachzeile">Willkommen</p>
    <h2>Dein Abend in der Nikolaistraße</h2>
    {"".join(f"<p>{e(a)}</p>" for a in B["willkommen"])}
  </div>
</section>

<section class="abschnitt" aria-labelledby="angebot">
  <div class="breit">
    <h2 id="angebot" class="sr-only">Unser Angebot</h2>
    <div class="bereiche">{karten}
    </div>
  </div>
</section>

<section class="happy">
  <div class="happy__innen">
    <p class="dachzeile">Happy Hour · täglich 12–17 Uhr</p>
    <p class="happy__preis">Alle Shisha-Sorten <strong>8,90 €</strong></p>
  </div>
</section>

<section class="abschnitt" id="zeiten">
  <div class="zwei">
    <div>
      <p class="dachzeile">{ICON["uhr"]} Öffnungszeiten</p>
      <h2>Täglich ab 12 Uhr</h2>
      {zeiten_tabelle()}
      <p class="klein">{e(B["zeiten_hinweis"])}</p>
    </div>
    <div id="anfahrt">
      <p class="dachzeile">{ICON["pin"]} Anfahrt</p>
      <h2>So findest du uns</h2>
      <address>
        <strong>Mon Frère</strong><br>
        {e(B["strasse"])}<br>
        {e(B["plz"])} {e(B["ort"])}
      </address>
      <p>{e(B["anfahrt"])}</p>
      <div class="knopfreihe">
        <a class="knopf knopf--rand" href="{MAPS}" rel="noopener" target="_blank">Google Maps</a>
        <a class="knopf knopf--rand" href="{APPLE}" rel="noopener" target="_blank">Apple Karten</a>
      </div>
    </div>
  </div>
</section>

<section class="abschnitt kontakt" id="kontakt">
  <div class="eng mitte">
    <p class="dachzeile">Kontakt & Reservierung</p>
    <h2>Ruf uns an oder schreib uns</h2>
    <p>Für Tischreservierungen, Geburtstage und größere Gruppen erreichst du uns telefonisch während der Öffnungszeiten.</p>
    <div class="knopfreihe knopfreihe--mitte">
      <a class="knopf" href="{TEL_LINK}">{ICON["tel"]}<span>{e(TEL)}</span></a>
      <a class="knopf knopf--rand" href="{B["instagram_url"]}" rel="noopener" target="_blank">{ICON["insta"]}<span>@{e(B["instagram"])}</span></a>
      <a class="knopf knopf--rand" href="{B["tiktok_url"]}" rel="noopener" target="_blank">{ICON["tiktok"]}<span>TikTok</span></a>
    </div>
    <p class="lieferung">Lust auf Sushi zu Hause? Unsere Küche liefert als <a href="{B["lieferung_url"]}" rel="noopener" target="_blank">{e(B["lieferung_name"])}</a> – bestellen auf <a href="{B["lieferung_url"]}" rel="noopener" target="_blank">{e(B["lieferung_anzeige"])}</a>.</p>
  </div>
</section>
"""
    return layout(
        datei="index.html",
        titel="Mon Frère Hannover – Shisha, Sushi & Cocktails in der Nikolaistraße",
        beschreibung=B["kurz"],
        inhalt=inhalt,
        extra_head=json_ld(),
        body_klasse="start",
    ).replace("</body>", plan_js() + "</body>")


# ---------- Speisekarte ----------

def zusatz(a):
    return f'<sup class="z" title="Zusatzstoffe/Allergene: {e(a["z"])}">{e(a["z"])}</sup>' if a.get("z") else ""


def artikel_liste(artikel, groessen=None):
    if not artikel:
        return ""
    zeilen = []
    for a in artikel:
        nr = f'<span class="nr">{a["nr"]}</span>' if a.get("nr") else ""
        txt = f'<span class="txt">{e(a["text"])}</span>' if a.get("text") else ""
        preise = a.get("preis", [])
        if groessen and len(groessen) > 1:
            p = "".join(f'<span class="p">{preis(x) or "–"}</span>' for x in preise)
        else:
            p = "".join(f'<span class="p">{preis(x)}</span>' for x in preise)
        such = e((a["name"] + " " + a.get("text", "")).lower())
        zeilen.append(
            f'<li class="art{" art--nr" if a.get("nr") else ""}" data-such="{such}">{nr}'
            f'<span class="name">{e(a["name"])}{zusatz(a)}{txt}</span>'
            f'<span class="preise">{p}</span></li>'
        )
    return '<ul class="arts">' + "".join(zeilen) + "</ul>"


def kategorie(k):
    gr = k.get("groessen")
    kopf_gr = ""
    if gr:
        kopf_gr = '<span class="groessen">' + "".join(f"<span>{e(g)}</span>" for g in gr) + "</span>"
    hinweis = f'<p class="hinweis">{e(k["hinweis"])}{" · " + preis(k["preis"]) if k.get("preis") else ""}</p>' if k.get("hinweis") else ""
    if k.get("liste"):
        such = e(" ".join(a["name"].lower() for a in k["artikel"]))
        chips = "".join(
            f'<li data-such="{e(a["name"].lower())}">{e(a["name"])}{zusatz(a)}{" <em>" + e(a["text"]) + "</em>" if a.get("text") else ""}</li>'
            for a in k["artikel"]
        )
        koerper = f'<ul class="chips" data-such="{such}">{chips}</ul>'
    else:
        koerper = artikel_liste(k.get("artikel"), gr)
    unter = ""
    for u in k.get("unter", []):
        unter += f'<h4>{e(u["titel"])}</h4>' + artikel_liste(u["artikel"])
    fuss = f'<p class="hinweis">{e(k["fuss"])}</p>' if k.get("fuss") else ""
    return (
        f'<div class="kat" id="{slug(k["titel"])}"><div class="kat__kopf"><h3>{e(k["titel"])}</h3>{kopf_gr}</div>'
        f"{hinweis}{koerper}{unter}{fuss}</div>"
    )


def speisekarte():
    tabs = "".join(f'<a href="#{g["id"]}">{e(g["titel"])}</a>' for g in K["gruppen"])
    gruppen = ""
    for g in K["gruppen"]:
        intro = f'<p class="gruppe__intro">{e(g["intro"])}</p>' if g.get("intro") else ""
        kats = "".join(kategorie(k) for k in g["kategorien"])
        gruppen += f"""
<section class="gruppe" id="{g["id"]}">
  <div class="gruppe__kopf" style="--bild:url('assets/img/{g["bild"]}.webp')">
    <h2>{e(g["titel"])}</h2>
  </div>
  <div class="breit">{intro}
    <div class="kats">{kats}</div>
  </div>
</section>"""
    zs = "".join(f"<li><b>{e(c)}</b> {e(t)}</li>" for c, t in K["zusatzstoffe"])
    al = "".join(f"<li><b>{e(c)}</b> {e(t)}</li>" for c, t in K["allergene"])
    inhalt = f"""
<section class="karte-kopf">
  <div class="breit">
    <p class="dachzeile">Mon Frère · Hannover</p>
    <h1>Speisekarte</h1>
    <p>Sushi, Bowls und warme Küche, Shisha, Cocktails und Drinks. Alle Preise in Euro inkl. MwSt. Stand: {e(K["stand"])}.</p>
    <label class="suche"><span class="sr-only">Karte durchsuchen</span>
      <input id="suche" type="search" placeholder="Suchen, z. B. Lachs, Mojito, Minze …" autocomplete="off">
    </label>
  </div>
</section>
<nav class="tabs" aria-label="Bereiche der Speisekarte"><div class="tabs__innen">{tabs}</div></nav>
{gruppen}
<p class="leer" id="leer" hidden>Nichts gefunden. Frag gern unser Team!</p>
<section class="abschnitt legende">
  <div class="breit">
    <h2>Zusatzstoffe & Allergene</h2>
    <div class="zwei">
      <div><h3>Zusatzstoffe</h3><ul>{zs}</ul></div>
      <div><h3>Allergene</h3><ul>{al}</ul></div>
    </div>
    <p class="klein">Bei Fragen zu Allergenen und Zutaten wende dich bitte an unser Personal. Änderungen und Irrtümer vorbehalten.</p>
  </div>
</section>
"""
    such_js = """<script>
(function(){
  var f = document.getElementById('suche'); if (!f) return;
  var leer = document.getElementById('leer');
  f.addEventListener('input', function(){
    var q = f.value.trim().toLowerCase(), treffer = 0;
    document.querySelectorAll('.gruppe').forEach(function(g){
      var gz = 0;
      g.querySelectorAll('.kat').forEach(function(k){
        var kz = 0;
        k.querySelectorAll('[data-such]').forEach(function(el){
          if (el.classList.contains('chips')) return;
          var ok = !q || el.getAttribute('data-such').indexOf(q) > -1;
          el.hidden = !ok; if (ok) kz++;
        });
        var kt = k.querySelector('h3').textContent.toLowerCase();
        if (q && kt.indexOf(q) > -1) { k.querySelectorAll('[data-such]').forEach(function(el){ el.hidden = false; }); kz++; }
        k.hidden = kz === 0; gz += kz;
      });
      g.hidden = gz === 0; treffer += gz;
    });
    leer.hidden = treffer > 0;
  });
})();
</script>
"""
    return layout(
        datei="speisekarte.html",
        titel="Speisekarte – Mon Frère Hannover",
        beschreibung="Speisekarte von Mon Frère Hannover: Sushi, Bowls, Curry, Penne, Desserts, Shisha-Sorten, Cocktails, Wein, Spirituosen und Softdrinks mit Preisen.",
        inhalt=inhalt,
        body_klasse="karte",
    ).replace("</body>", such_js + "</body>")


# ---------- Rechtliches ----------

def impressum():
    r = B["recht"]
    inhalt = f"""
<section class="abschnitt text">
  <div class="eng">
    <h1>Impressum</h1>
    <h2>Angaben gemäß § 5 DDG</h2>
    <p>{e(r["inhaber"])}<br>Mon Frère<br>{e(B["strasse"])}<br>{e(B["plz"])} {e(B["ort"])}</p>
    <h2>Kontakt</h2>
    <p>Telefon: <a href="{TEL_LINK}">{e(TEL)}</a><br>E-Mail: <a href="mailto:{e(r["email"])}">{e(r["email"])}</a></p>
    {f'<h2>Umsatzsteuer-ID</h2><p>Umsatzsteuer-Identifikationsnummer gemäß § 27 a UStG: {e(r["ust_id"])}</p>' if r.get("ust_id") else ""}
    <h2>Verantwortlich für den Inhalt</h2>
    <p>{e(r["inhaber"])}, Anschrift wie oben</p>
    <h2>Verbraucherstreitbeilegung</h2>
    <p>Wir sind nicht bereit und nicht verpflichtet, an Streitbeilegungsverfahren vor einer Verbraucherschlichtungsstelle teilzunehmen.</p>
    <h2>Bildnachweise</h2>
    <p>Fotos: Mon Frère sowie lizenzierte Bilder von Adobe Stock, Pexels und Unsplash.</p>
  </div>
</section>
"""
    return layout(datei="impressum.html", titel="Impressum – Mon Frère Hannover", beschreibung="Impressum von Mon Frère Hannover.", inhalt=inhalt)


def datenschutz():
    r = B["recht"]
    inhalt = f"""
<section class="abschnitt text">
  <div class="eng">
    <h1>Datenschutzerklärung</h1>
    <h2>1. Verantwortlicher</h2>
    <p>{e(r["inhaber"])}, Mon Frère, {e(ADRESSE)}<br>Telefon: {e(TEL)} · E-Mail: <a href="mailto:{e(r["email"])}">{e(r["email"])}</a></p>

    <h2>2. Grundsatz</h2>
    <p>Diese Website ist eine reine Informationsseite. Wir setzen keine Cookies, keine Analyse- oder Tracking-Werkzeuge und keine Kontaktformulare ein. Schriftarten und Bilder werden von unserem eigenen Webspace geladen, nicht von Dritten.</p>

    <h2>3. Hosting und Server-Logfiles</h2>
    <p>Die Website wird über GitHub Pages bereitgestellt, einen Dienst der GitHub Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA. Beim Aufruf der Seiten verarbeitet GitHub technisch notwendige Daten, insbesondere die IP-Adresse, Datum und Uhrzeit des Abrufs, die aufgerufene Seite und Informationen zum Browser. Diese Daten werden benötigt, um die Website auszuliefern und ihre Sicherheit zu gewährleisten (Art. 6 Abs. 1 lit. f DSGVO). Dabei kann eine Übermittlung in die USA stattfinden. GitHub ist unter dem EU-US Data Privacy Framework zertifiziert. Weitere Informationen: <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement" rel="noopener" target="_blank">Datenschutzerklärung von GitHub</a>.</p>

    <h2>4. Externe Links</h2>
    <p>Unsere Seite enthält Links zu Instagram, TikTok, Google Maps, Apple Karten und unserem Lieferdienst {e(B["lieferung_name"])}. Erst wenn du einen dieser Links anklickst, wird eine Verbindung zum jeweiligen Anbieter hergestellt; dort gelten dessen Datenschutzbestimmungen.</p>

    <h2>5. Kontakt per Telefon oder E-Mail</h2>
    <p>Wenn du uns anrufst oder schreibst, verarbeiten wir deine Angaben, um deine Anfrage zu beantworten, etwa eine Tischreservierung (Art. 6 Abs. 1 lit. b und f DSGVO). Die Daten werden gelöscht, sobald sie dafür nicht mehr benötigt werden.</p>

    <h2>6. Deine Rechte</h2>
    <p>Du hast das Recht auf Auskunft, Berichtigung, Löschung, Einschränkung der Verarbeitung, Datenübertragbarkeit und Widerspruch (Art. 15–21 DSGVO). Wende dich dazu an die oben genannten Kontaktdaten. Außerdem kannst du dich bei einer Datenschutz-Aufsichtsbehörde beschweren, zum Beispiel bei: {e(r["aufsicht"])}.</p>

    <p class="klein">Stand: {e(r["stand"])}</p>
  </div>
</section>
"""
    return layout(datei="datenschutz.html", titel="Datenschutz – Mon Frère Hannover", beschreibung="Datenschutzerklärung von Mon Frère Hannover.", inhalt=inhalt)


def nicht_gefunden():
    inhalt = """
<section class="abschnitt text">
  <div class="eng mitte">
    <h1>Seite nicht gefunden</h1>
    <p>Diese Seite gibt es nicht (mehr).</p>
    <div class="knopfreihe knopfreihe--mitte">
      <a class="knopf" href="/">Zur Startseite</a>
      <a class="knopf knopf--rand" href="/speisekarte.html">Speisekarte</a>
    </div>
  </div>
</section>
"""
    # 404 wird von GitHub Pages unter beliebigen Pfaden ausgeliefert → absolute Pfade
    s = layout(datei="404.html", titel="Seite nicht gefunden – Mon Frère Hannover", beschreibung="Seite nicht gefunden.", inhalt=inhalt)
    return re.sub(r'(href|src)="(?!https?:|tel:|mailto:|/|#)', r'\1="/', s)


def main():
    seiten = {
        "index.html": startseite(),
        "speisekarte.html": speisekarte(),
        "impressum.html": impressum(),
        "datenschutz.html": datenschutz(),
        "404.html": nicht_gefunden(),
    }
    for name, inhalt in seiten.items():
        with open(os.path.join(ROOT, name), "w", encoding="utf-8") as f:
            f.write(inhalt)
        print("geschrieben:", name, len(inhalt) // 1024, "KB")


if __name__ == "__main__":
    main()
