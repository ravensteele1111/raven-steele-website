"""
Build reviews.html from reviews.json.

    python build-reviews.py
    python build-sitemap.py
    python stamp.py

Forty three reviews came from the Revenue Revolution Skool. Five are held
back: two mention money made and three mention something personal, and
Raven's side asked for those to be checked before they go on a public site.
They stay in reviews.json with "hold": true so nothing is lost, and this
refuses to put them on the page.

Same rule as the two Rebel wins, which have been sitting unpublished for
weeks. A real person's words on a public website wait for that person.

The names are shortened to a first name and a last initial, because the Skool
is members only and this website is not. Raven can open that up whenever she
likes; it is one line here.

The page reuses what is already on the site: the same chip bar as the Music
page, which also brings the "show all" fold with it, so forty three reviews
do not arrive as a wall. No new JavaScript.
"""

import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

SITE = "https://ravensteele.com/"

THEMES = [("all", "All"),
          ("community", "Raven and the community"),
          ("wins", "Wins"),
          ("courses", "Courses and tools"),
          ("creative", "Creative wins")]

# A results-vary line sits with the Wins, because several of them name an
# outcome even where they are not flagged.
CAVEAT = ("What any one Rebel gets out of it is their own. These are their "
          "words, not a promise.")


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def card(r, shown):
    """One review.

    data-featured is what the All chip looks for when the list is folded up.
    Leaving it off shipped a page where every single review was hidden and a
    "Read all 20" button sat above nothing. The build said 20 on the page and
    it was telling the truth about the file and nothing about the screen.
    """
    return ('        <figure class="review" data-tag="%s"%s data-hidden="%s">\n'
            '          <blockquote>%s</blockquote>\n'
            '          <p class="said">%s</p>\n'
            '          <figcaption><span class="who">%s</span>'
            '<span class="when">%s</span></figcaption>\n'
            '        </figure>'
            % (r["theme"], ' data-featured="true"' if shown else "",
               "false" if shown else "true",
               esc(r["quote"]), esc(r["words"]),
               esc(r["display"]), esc(r["when"])))


def main():
    data = json.load(io.open(os.path.join(HERE, "reviews.json"), encoding="utf-8"))
    everyone = data["reviews"]
    held = [r for r in everyone if r.get("hold")]
    live = [r for r in everyone if not r.get("hold")]

    # The opening set is a spread across the themes rather than the first six
    # in order, so nobody opens the page and sees six reviews about one thing.
    taken, opening = {}, []
    for r in live:
        if taken.get(r["theme"], 0) < 2:
            taken[r["theme"]] = taken.get(r["theme"], 0) + 1
            opening.append(id(r))

    chips = "\n".join(
        '        <button class="chip" data-filter="%s" aria-pressed="%s">%s</button>'
        % (slug, "true" if slug == "all" else "false", esc(name))
        for slug, name in THEMES)

    cards = "\n".join(card(r, id(r) in opening) for r in live)

    page = io.open(os.path.join(HERE, "_reviews-template.html"), encoding="utf-8").read()
    page = (page.replace("%%CHIPS%%", chips)
                .replace("%%CARDS%%", cards)
                .replace("%%COUNT%%", str(len(live)))
                .replace("%%CAVEAT%%", CAVEAT))
    io.open(os.path.join(HERE, "reviews.html"), "w", encoding="utf-8").write(page)

    print("reviews.html: %d on the page, %d held back" % (len(live), len(held)))
    for r in held:
        print("   held: %-22s %s" % (r["display"], r.get("why", "")))
    print("opening set: %d, spread across the themes" % len(opening))


if __name__ == "__main__":
    main()
