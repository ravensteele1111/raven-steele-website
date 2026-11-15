"""
Build backstage.html from backstage.json.

    python build-backstage.py
    python stamp.py

The members-only page: where the Backstage Pass actually leads. Everything
the public site does not show.

NOT SECRET, UNLISTED

There is no password, by the customer's choice. It is simply not advertised:
not in the menu, not in the sitemap, and carrying a noindex tag so search
engines leave it alone. Anybody with the address can open it.

That is worth saying out loud rather than letting it be discovered later: a
Backstage Pass that costs an email address is a soft lock, and a soft lock is
a courtesy, not a wall. It is the right trade for a fan site, where the cost
of annoying a member is higher than the cost of somebody sharing a link. But
nothing behind it should ever be anything that must not get out.

HOW SOMEBODY GETS HERE

They join the Rebels, then press confirm in Kit's email. Kit currently sends
them to the home page; it gets pointed here once this is live, and the
address goes in the welcome email too.

ADDING TO IT

Add a block to backstage.json. "ready": false shows it as coming soon, which
is honest while the folders are still arriving, and is better than a link
that goes nowhere. Set it true and give it a "href" once a set is up.
"""

import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def tile(item, kind="event"):
    ready = item.get("ready")
    name = esc(item["name"])
    note = esc(item.get("note", ""))
    count = item.get("count")
    if count:
        note = note + (". " if note else "") + "%d photographs" % count

    if ready and item.get("href"):
        return ('        <a class="vault" href="%s">\n'
                '          <span class="vault-name">%s</span>\n'
                '          <span class="vault-note">%s</span>\n'
                '          <span class="vault-go">Open</span>\n'
                '        </a>' % (esc(item["href"]), name, note))

    return ('        <div class="vault" data-soon="true">\n'
            '          <span class="vault-name">%s</span>\n'
            '          <span class="vault-note">%s</span>\n'
            '          <span class="vault-go">Coming soon</span>\n'
            '        </div>' % (name, note))


def main():
    data = json.load(io.open(os.path.join(HERE, "backstage.json"), encoding="utf-8"))
    events = "\n".join(tile(e) for e in data["events"])
    extras = "\n".join(tile(e) for e in data["extras"])
    ready = sum(1 for e in data["events"] + data["extras"] if e.get("ready"))

    page = io.open(os.path.join(HERE, "_backstage-template.html"), encoding="utf-8").read()
    page = (page.replace("%%EVENTS%%", events)
                .replace("%%EXTRAS%%", extras)
                .replace("%%COUNT%%", str(len(data["events"]))))
    io.open(os.path.join(HERE, "backstage.html"), "w", encoding="utf-8").write(page)

    print("backstage.html: %d events, %d extras, %d of them ready"
          % (len(data["events"]), len(data["extras"]), ready))
    if not ready:
        print("   nothing is live behind it yet, so every tile says coming soon.")
        print("   That is deliberate: a tile that says soon is honest, a tile that")
        print("   links nowhere is a broken promise to somebody who just joined.")


if __name__ == "__main__":
    main()
