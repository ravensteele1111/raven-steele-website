"""
Write sitemap.xml: every page on the site, for search engines.

    python build-sitemap.py

Run it after adding or removing a page. It reads the folder rather than a
list, so a new page cannot be forgotten.

Until 15 November 2026 the whole site told search engines to stay away, on
purpose, because there was no point being found at a temporary address. The
day the domain arrived that came off, and this went on.

Pages are weighted by what they are for. The home page leads, then the four
the whole site is built around, then the events, then the legal pages, which
exist to be correct rather than to be found.
"""

import io
import os
import re
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = "https://ravensteele.com/"

# Pages nobody should be sent to from a search result.
SKIP = {"404.html", "share-test.html"}

WEIGHT = {
    "index.html": "1.0",
    "story.html": "0.9",
    "music.html": "0.9",
    "events.html": "0.9",
    "shop.html": "0.8",
    "be-like-raven.html": "0.8",
    "privacy.html": "0.2",
    "terms.html": "0.2",
    "cookies.html": "0.2",
}


def weight(name):
    if name in WEIGHT:
        return WEIGHT[name]
    return "0.7" if name.startswith("event-") else "0.5"


def main():
    pages = sorted(f for f in os.listdir(HERE)
                   if f.endswith(".html") and f not in SKIP
                   and not f.startswith("_"))

    # The date each page last really changed, not the date this was run.
    rows = []
    for name in pages:
        when = time.strftime("%Y-%m-%d",
                             time.gmtime(os.path.getmtime(os.path.join(HERE, name))))
        where = SITE if name == "index.html" else SITE + name
        rows.append("  <url>\n"
                    "    <loc>%s</loc>\n"
                    "    <lastmod>%s</lastmod>\n"
                    "    <priority>%s</priority>\n"
                    "  </url>" % (where, when, weight(name)))

    xml = ('<?xml version="1.0" encoding="UTF-8"?>\n'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
           + "\n".join(rows) + "\n</urlset>\n")
    io.open(os.path.join(HERE, "sitemap.xml"), "w", encoding="utf-8",
            newline="").write(xml)
    print("sitemap.xml: %d pages" % len(pages))


if __name__ == "__main__":
    main()
