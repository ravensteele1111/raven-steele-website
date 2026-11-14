"""
Build the music list on music.html from songs.json.

    python build-music.py
    python stamp.py

The songs used to be typed straight into the page, forty three of them. That
made adding a new release an editing job in two places at once, and it is how
seventeen songs once ended up pointing at the wrong videos without anybody
noticing. Now the page has the list in one place and the page is written from
it.

Two parts of music.html are rewritten, each between its own pair of markers:

    PLAYER   the big video at the top, which is always the newest release
    SONGS    the whole list underneath, plus the "show all" button

Nothing else on the page is touched, so the wording, the highlights and the
rest can still be edited by hand.

WHAT songs.json HOLDS

    newest   the video id shown in the player at the top
    mix      how many of each of Raven, Ethan and duets to show before a
             visitor presses "show all". Two of each makes six
    songs    every song, newest first, each with id, title and who it is by
             ("raven", "ethan" or "duet")

A song may also carry "featured": true to pin it into that opening six by
hand. If no song is pinned the mix is taken off the top of the list, which
means a new release appears in the opening six on its own.

After running this, run check_music.py. It asks YouTube what each video is
really called and fails loudly if anything has drifted.
"""

import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

WHO = {"raven": "Raven", "ethan": "Ethan", "duet": "Duet"}


def esc(s):
    """Safe inside an HTML attribute and safe as text."""
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def load():
    return json.load(io.open(os.path.join(HERE, "songs.json"), encoding="utf-8"))


def opening_six(data):
    """The ids shown before anybody presses "show all".

    Pinned songs win. Otherwise it is the first few of each kind, taken in
    list order, so the mix stays fresh as new songs go on the top.
    """
    pinned = [s["id"] for s in data["songs"] if s.get("featured")]
    if pinned:
        return set(pinned)

    want = data.get("mix", 2)
    taken, out = {}, []
    for s in data["songs"]:
        who = s["who"]
        if taken.get(who, 0) < want:
            taken[who] = taken.get(who, 0) + 1
            out.append(s["id"])
    return set(out)


def player_block(data):
    newest = None
    for s in data["songs"]:
        if s["id"] == data["newest"]:
            newest = s
            break
    if newest is None:
        raise SystemExit("songs.json: newest id %s is not in the list" % data["newest"])

    title = esc(newest["title"])
    return ('''      <div class="player">
        <button class="player-frame" id="player-frame"
                data-video="%s" data-title="%s"
                aria-label="Play %s">
          <img src="assets/thumbs/%s.jpg" alt="" width="640" height="360">
          <span class="play-big" aria-hidden="true"></span>
        </button>
        <p class="now-playing">Now playing &nbsp;<strong id="now-playing">%s</strong></p>
      </div>'''
            % (newest["id"], title, title, newest["id"], title))


def songs_block(data):
    six = opening_six(data)
    total = len(data["songs"])

    rows = []
    for s in data["songs"]:
        title = esc(s["title"])
        hidden = "false" if s["id"] in six else "true"
        rows.append(
            '        <a class="song" data-tag="%s"%s data-hidden="%s"\n'
            '           href="https://www.youtube.com/watch?v=%s"\n'
            '           data-video="%s" data-title="%s">\n'
            '          <img class="thumb" src="assets/thumbs/%s-sm.jpg" alt="" '
            'loading="lazy" width="160" height="90">\n'
            '          <span class="words"><span class="name">%s</span>'
            '<span class="tag">%s</span></span>\n'
            '          <span class="go">Play</span>\n'
            '        </a>'
            % (s["who"], ' data-featured="true"' if s["id"] in six else "",
               hidden, s["id"], s["id"], title, s["id"], title, WHO[s["who"]]))

    return ('''      <div class="filters" data-target="songs">
        <button class="chip" data-filter="all" aria-pressed="true">All</button>
        <button class="chip" data-filter="duet" aria-pressed="false">Duets</button>
        <button class="chip" data-filter="raven" aria-pressed="false">Raven</button>
        <button class="chip" data-filter="ethan" aria-pressed="false">Ethan</button>
      </div>

      <div class="stack" id="songs" data-collapse="6">
%s
        <p class="empty" data-hidden="true">Nothing in that one yet.</p>
      </div>

      <div class="cta-wide">
        <button class="btn btn-ghost" data-more="songs"
                data-more-label="Show all {n} songs"
                data-less-label="Show fewer">Show all %d songs</button>
      </div>'''
            % ("\n".join(rows), total))


def swap(page, name, block):
    start = "<!-- " + name + " -->"
    end = "<!-- /" + name + " -->"
    pattern = re.compile(re.escape(start) + ".*?" + re.escape(end), re.S)
    if not pattern.search(page):
        raise SystemExit("music.html has no %s markers" % name)
    return pattern.sub(lambda m: start + "\n" + block + "\n      " + end, page, count=1)


def main():
    data = load()
    path = os.path.join(HERE, "music.html")
    page = io.open(path, encoding="utf-8").read()

    page = swap(page, "PLAYER", player_block(data))
    page = swap(page, "SONGS", songs_block(data))

    # Default newline handling, so the file keeps the same line endings as
    # every other page here. build-events.py does the same.
    io.open(path, "w", encoding="utf-8").write(page)

    kinds = {}
    for s in data["songs"]:
        kinds[s["who"]] = kinds.get(s["who"], 0) + 1
    print("music.html written: %d songs (%s)"
          % (len(data["songs"]),
             ", ".join("%d %s" % (n, k) for k, n in sorted(kinds.items()))))
    print("opening six: %d shown before \"show all\"" % len(opening_six(data)))
    print("now run:  python stamp.py   and   python ../Tools/check_music.py")


if __name__ == "__main__":
    main()
