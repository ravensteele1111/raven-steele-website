"""
Build the shop from products.json.

    python build-shop.py
    python stamp.py

Rules this follows, from the customer:
  - No prices anywhere. The price lives on the product page, so it can change
    without anybody touching this website. Cards say "See the price".
  - A product with no working address does not go on the site at all.
  - Pictures are optional. A product without one gets a labelled placeholder.
"""
import io, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
BEST_SHELL = """        <a class="best" href="%s" target="_blank" rel="noopener">
          <p class="eyebrow">Best seller</p>
          <img src="assets/products/%s.webp" alt="%s"
               width="600" height="600">
          <p class="name">%s</p>
          <span class="price">See the price</span>
        </a>"""

LABELS = {"tool": "Tools", "prompt": "Prompts", "meme": "Meme Bots", "toolbox": "Toolboxes"}
# Prompts lead. Raven asked for the shop to open with her skin and prompt
# packs, because that is what sells, and the chips follow the same order
# so the first one after All is the one she wants pressed.
ORDER = ["prompt", "tool", "meme", "toolbox"]

# And inside the prompts, her own order rather than the alphabet: the best
# seller, then skin, then hair, then body. Anything not named here keeps
# its place behind them.
LEADS = ["Ultra Realistic Skin Prompt Pack",
         "Ultra Realistic Skin Conditions Pack",
         "The Skin Vault",
         "The Complete Skin Add-On Pack",
         "The Hair Vault",
         "The Hair Vault Prompt Pack",
         "The Hair Style Vault",
         "The Complete Hair Add-On Pack",
         "The Occasion Hair Prompt Pack",
         "The Body Blueprint Prompt Pack",
         "Body Blueprint Add-On Pack",
         "The Body Vault",
         "Body Vault Prompt Pack",
         "The Colour Lab",
         "The Complete SEEN Collection"]


def card(p, indent="          "):
    if p.get("img"):
        pic = ('<img src="assets/products/%s.webp" alt="%s" width="600" height="600" loading="lazy">'
               % (p["img"], p["name"]))
    else:
        pic = '<span class="ph ph-square"><span>Product</span></span>'
    line = ('\n%s  <span class="line">%s</span>' % (indent, p["line"])) if p.get("line") else ""
    return ('%(i)s<a class="product" data-tag="%(tag)s" href="%(url)s" target="_blank" rel="noopener">\n'
            '%(i)s  %(pic)s\n'
            '%(i)s  <span class="name" style="display:block">%(name)s</span>%(line)s\n'
            '%(i)s  <span class="price">See the price</span>\n'
            '%(i)s</a>') % {"i": indent, "tag": p["tag"], "url": p["base"] + p["id"],
                            "pic": pic, "name": p["name"], "line": line}


def main():
    os.chdir(HERE)
    data = json.load(io.open("products.json", encoding="utf-8"))
    prods = [p for p in data["products"] if not p.get("hide")]

    present = [t for t in ORDER if any(p["tag"] == t for p in prods)]
    def place(p):
        lead = LEADS.index(p["name"]) if p["name"] in LEADS else len(LEADS)
        return (ORDER.index(p["tag"]), lead, p["name"])

    prods.sort(key=place)

    chips = ['        <button class="chip" data-filter="all" aria-pressed="true">All</button>']
    chips += ['        <button class="chip" data-filter="%s" aria-pressed="false">%s</button>'
              % (t, LABELS[t]) for t in present]

    s = io.open("shop.html", encoding="utf-8").read()

    s = re.sub(r'(<div class="filters" data-target="products">).*?(</div>)',
               lambda m: m.group(1) + "\n" + "\n".join(chips) + "\n        " + m.group(2),
               s, count=1, flags=re.S)

    # The best seller block, from the product carrying "best": true. It used
    # to be typed into the page by hand, which meant every change left the
    # comment above it describing a product that was no longer there.
    best = next((p for p in prods if p.get("best")), None)
    if best:
        block = (BEST_SHELL
                 % (best["base"] + best["id"], best["img"], best["name"], best["name"]))
        s = re.sub(r"        <!-- BEST -->.*?<!-- /BEST -->",
                   lambda m: "        <!-- BEST -->\n" + block + "\n        <!-- /BEST -->",
                   s, count=1, flags=re.S)

    a = s.index('<div class="grid-2" id="products">')
    b = s.index('<p class="empty" data-hidden="true">')
    s = (s[:a] + '<div class="grid-2" id="products">\n'
         + "\n".join(card(p) for p in prods) + "\n\n          " + s[b:])

    io.open("shop.html", "w", encoding="utf-8").write(s)
    counts = {t: sum(1 for p in prods if p["tag"] == t) for t in present}
    print("%d products: %s" % (len(prods), ", ".join("%s %d" % (LABELS[t], counts[t]) for t in present)))
    print("with a picture: %d" % sum(1 for p in prods if p.get("img")))


if __name__ == "__main__":
    main()
