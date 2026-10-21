# monfrere-hannover.de

Statische Infoseite für **Mon Frère** (Shisha · Sushi · Cocktails), Nikolaistraße 32, 30159 Hannover.
Gehostet über GitHub Pages, Domain bei IONOS.

## Inhalte ändern

| Was | Wo |
|---|---|
| Speisekarte, Preise, Shisha-Sorten | `daten/karte.json` |
| Öffnungszeiten, Telefon, Texte, Social Links, Impressum-Daten | `daten/betrieb.json` |
| Aussehen | `assets/css/stil.css` |
| Seitenaufbau | `werkzeug/build.py` |

Danach neu bauen und hochladen:

```sh
python3 werkzeug/build.py
git add -A && git commit -m "Karte aktualisiert" && git push
```

GitHub Pages veröffentlicht `main` automatisch (1–2 Minuten).
Die erzeugten HTML-Dateien (`index.html`, `speisekarte.html`, …) nie direkt bearbeiten, sie werden beim Bauen überschrieben.

Lokal ansehen: `python3 -m http.server 8080` → http://localhost:8080

## Quellen

- Speisekarte: Restaurantkarte „Speisekarte FINAL (Doppelseiten).pdf“ (Stand Oktober 2026, Nr. 10–81)
- Fotos: Bilder aus der Speisekarte (Adobe Stock, Pexels, Unsplash) + eigenes Foto Crunchy Roll
- Logo: `logodc.png` aus dem Speisekarten-Paket
- Schriften: Cormorant Garamond + Poppins (SIL Open Font License, siehe `assets/fonts/`)

## DNS bei IONOS

| Typ | Host | Wert |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA | @ | 2606:50c0:8000::153 |
| AAAA | @ | 2606:50c0:8001::153 |
| AAAA | @ | 2606:50c0:8002::153 |
| AAAA | @ | 2606:50c0:8003::153 |
| CNAME | www | ahaidar711.github.io |

Vorhandene A/AAAA-Einträge von IONOS für `@` und `www` vorher löschen.
