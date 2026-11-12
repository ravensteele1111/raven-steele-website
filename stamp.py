"""
Stamp the stylesheet and script links with a version, so a changed file is
never served from an old cache.

The problem it solves: GitHub Pages tells browsers they may keep site.css for
ten minutes, and phones in practice keep it a great deal longer. So you push a
fix, you look at the site on your phone, and nothing has changed — because the
phone never asked for the new file.

The fix is to change the ADDRESS whenever the file changes:

    assets/css/site.css?v=8f3a1c20

The browser has never seen that address before, so it has to fetch it. The
version is the first eight characters of the file's own hash, so it changes
exactly when the file does and not a moment sooner.

Run this after any change to the CSS or the JavaScript, before committing:

    python stamp.py
"""

import glob
import hashlib
import io
import os
import re

ASSETS = {
    "assets/css/site.css": re.compile(r'(href=")(assets/css/site\.css)(\?v=[0-9a-f]+)?(")'),
    "assets/js/site.js": re.compile(r'(src=")(assets/js/site\.js)(\?v=[0-9a-f]+)?(")'),
}


def short_hash(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()[:8]


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    os.chdir(here)

    versions = {}
    for asset in ASSETS:
        if not os.path.exists(asset):
            print("missing, skipped:", asset)
            continue
        versions[asset] = short_hash(asset)

    changed = 0
    for page in sorted(glob.glob("*.html")):
        text = io.open(page, encoding="utf-8").read()
        before = text

        for asset, pattern in ASSETS.items():
            if asset not in versions:
                continue
            stamp = "?v=" + versions[asset]
            text = pattern.sub(lambda m: m.group(1) + m.group(2) + stamp + m.group(4), text)

        if text != before:
            io.open(page, "w", encoding="utf-8").write(text)
            changed += 1
            print("stamped:", page)

    for asset, version in versions.items():
        print("%-22s v=%s" % (asset, version))
    print("%d page(s) updated" % changed)


if __name__ == "__main__":
    main()
