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
LABELS = {"tool": "Tools", "prompt": "Prompts", "meme": "Meme Bots", "toolbox": "Toolboxes"}
ORDER = ["tool", "prompt", "meme", "toolbox"]


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
    prods.sort(key=lambda p: (ORDER.index(p["tag"]), p["name"]))

    chips = ['        <button class="chip" data-filter="all" aria-pressed="true">All</button>']
    chips += ['        <button class="chip" data-filter="%s" aria-pressed="false">%s</button>'
              % (t, LABELS[t]) for t in present]

    s = io.open("shop.html", encoding="utf-8").read()

    s = re.sub(r'(<div class="filters" data-target="products">).*?(</div>)',
               lambda m: m.group(1) + "\n" + "\n".join(chips) + "\n        " + m.group(2),
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
