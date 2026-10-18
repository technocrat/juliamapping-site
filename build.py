"""Build the static pages. Run: python3 build.py (reads figures.json)."""
import html, json, re
from collections import OrderedDict

AMAZON = "https://www.amazon.com/dp/B0GF22VCHV"
YT = "https://www.youtube.com/@JuliaMapping"
DISCLAIMER = "Independent guide. Not affiliated with the Julia project."


def page(title, desc, body, path=""):
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="stylesheet" href="style.css">
<link rel="icon" href="img/mark.png">
</head><body>
<header class="top"><div class="wrap">
<a class="brand" href="index.html"><img src="img/mark.png" alt="">Julia Mapping</a>
<nav aria-label="Main"><a href="gallery.html">Figure gallery</a><a href="{AMAZON}">Buy the book</a><a href="{YT}">YouTube</a></nav>
</div></header>
{body}
<footer><div class="wrap">
<div>{DISCLAIMER}<br>&copy; Wm Playfair Press</div>
<div>Julia Mapping: A Practical Guide &middot; ISBN 979-8242492240</div>
</div></footer>
</body></html>"""


def index():
    body = f"""<main>
<div class="wrap hero">
<div>
<h1>Julia Mapping</h1>
<p class="sub">A practical guide to maps from data you already have, for people who are good at their own work and new to programming.</p>
<p><a class="btn" href="{AMAZON}">Get the book on Amazon</a><a class="btn alt" href="gallery.html">See the figures</a></p>
</div>
<img src="img/cover.webp" alt="Cover of Julia Mapping: A Practical Guide, an orange county map of the United States on a dark background" width="788" height="1008">
</div>
<section class="band"><div class="wrap">
<h2>Who it's for</h2>
<div class="cols">
<div><h3>You have data with places in it</h3><p>State, county or regional figures sitting in a spreadsheet, and a map you want that the tools you know make hard.</p></div>
<div><h3>You're not a programmer</h3><p>You need enough to make your maps, not to become a programmer. The book takes you from installation to a finished map with a minimum of heartache and confusion.</p></div>
<div><h3>You want a clear, honest map</h3><p>Thematic maps, bivariate and flow maps, cartograms and more, with restrained color and the reasons behind each choice.</p></div>
</div>
</div></section>
<div class="wrap">
<h2>Reading on a Kindle?</h2>
<p class="intro">Maps are hard to read on a small e-ink screen. The <a href="gallery.html">figure gallery</a> shows every figure from the book at full size, with its caption, so you can zoom in on a phone, tablet or monitor.</p>
<h2>Watch</h2>
<p>Short videos on mapping problems and how to solve them are on the <a href="{YT}">JuliaMapping channel</a>.</p>
</div>
</main>"""
    return page("Julia Mapping: A Practical Guide", "A practical guide to making maps with Julia, for people with geographically distributed data and no programming background.", body)


def gallery(figs):
    chapters = OrderedDict()
    for f in figs:
        chapters.setdefault(f["chapter"], []).append(f)
    toc = "".join(f'<li><a href="#{slug(c)}">{html.escape(c)}</a></li>' for c in chapters)
    secs = []
    for c, items in chapters.items():
        cells = []
        for f in items:
            cap = html.escape(f["caption"])
            cells.append(f"""<li><figure><a href="img/full/{f['slug']}.webp"><img src="img/thumb/{f['slug']}.webp" alt="{cap}" loading="lazy" width="640" height="{round(640*f['h']/f['w'])}"></a>
<figcaption>{cap}<a href="img/full/{f['slug']}.webp">Open full size</a></figcaption></figure></li>""")
        secs.append(f'<section class="chapter" id="{slug(c)}"><h2>{html.escape(c)}</h2><ul class="grid">{"".join(cells)}</ul></section>')
    body = f"""<main class="wrap">
<h1>Figure gallery</h1>
<p class="intro">Every figure from <em>Julia Mapping: A Practical Guide</em>, sized for screens, grouped by chapter. Tap a figure for the full-size image and zoom as needed. Figures are shown in book order within each chapter.</p>
<h2>Chapters</h2><ul class="toc">{toc}</ul>
{''.join(secs)}
</main>"""
    return page("Figure gallery | Julia Mapping", "Full-size figures from Julia Mapping: A Practical Guide, for readers who find the maps hard to see on a Kindle.", body)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


if __name__ == "__main__":
    figs = json.load(open("figures.json"))
    open("index.html", "w").write(index())
    open("gallery.html", "w").write(gallery(figs))
    print("built", len(figs), "figures")
