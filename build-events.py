"""
Build the event pages from events.json.

One event page looks exactly like every other event page, so writing them by
hand would be forty chances to make a typo. Add an event to events.json and
run this:

    python build-events.py
    python stamp.py

It writes one event-<slug>.html per event, and rewrites the list of events on
events.html between the two EVENTS markers.

Real photos are used wherever assets/events/index.json has them, which
photos.py fills in from the shared Drive folders. Events with no photos yet
get labelled placeholders instead.
"""

import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))

PHOTOS = {}

# Where the site lives. Only used for the share pictures, which have to be
# full addresses. Change this line the day a real domain is pointed here.
SITE = "https://ravensteele1111.github.io/raven-steele-website/"

NAV = """  <nav class="site-nav" id="site-nav" data-open="false">
      <div class="wrap">
        <ul>
        <li><a href="index.html">Home</a></li>
        <li><a href="story.html">The Story</a></li>
        <li><a href="music.html">Music</a></li>
        <li><a href="events.html" aria-current="page">Events</a></li>
        <li><a href="be-like-raven.html">Be Like Raven</a></li>
        <li><a href="shop.html">Shop</a></li>
        </ul>
      </div>
    </nav>"""

FOOT = """<footer class="site-foot">
  <div class="wrap">
    <div class="socials">
      <a href="https://www.instagram.com/therealravenai" rel="noopener">Instagram</a>
      <a href="https://www.youtube.com/@Therealravenai" rel="noopener">YouTube</a>
    </div>
    <div class="legal">
      <a href="privacy.html">Privacy</a><a href="terms.html">Terms</a><a href="cookies.html">Cookies</a>
    </div>
    <p class="copyright">&copy; 2026 Raven Steele</p>
  </div>
</footer>

<div class="pinned">
  <div class="wrap">
    <p>Get the pics first.</p>
    <a class="btn btn-primary" href="index.html#rebels">Join</a>
  </div>
</div>

<div class="lightbox" id="lightbox" data-open="false" role="dialog" aria-modal="true" aria-label="Photos">
  <button class="close" aria-label="Close">&times;</button>
  <button class="lb-prev" aria-label="Previous photo"></button>
  <button class="lb-next" aria-label="Next photo"></button>
  <div class="lb-stage">
    <div class="ph"><span>Photo, full size</span></div>
    <p class="label"></p>
  </div>
</div>

</body>
</html>
"""

def photo_grid(slug, count):
    """Real photos where we have them, labelled placeholders where we do not."""
    names = PHOTOS.get(slug) or []
    if names:
        rows = []
        for i, n in enumerate(names, 1):
            rows.append(
                '        <button data-caption="Photo %d" data-big="assets/events/%s/%s.webp">'
                '<img src="assets/events/%s/%s-sm.webp" alt="" width="400" height="533" '
                'loading="lazy"></button>' % (i, slug, n, slug, n))
        return "\n".join(rows)

    rows = []
    for i in range(count):
        rows.append(
            '        <button data-caption="Photo %d">'
            '<span class="ph ph-square"><span>Photo</span></span></button>' % (i + 1))
    return "\n".join(rows)


# Mood filters were removed for good: the customer decided the photos will not
# be tagged goofy / sweet / action, so there is nothing for them to filter.


def cover_shot(ev):
    """The photo used for the cover and the hero. events.json can name one
    with "cover": N, counting from 1; otherwise it is the first."""
    shots = PHOTOS.get(ev["slug"]) or []
    if not shots:
        return None
    n = ev.get("cover", 1)
    if not isinstance(n, int) or n < 1 or n > len(shots):
        n = 1
    return shots[n - 1]


def share_card(slug, shot):
    """A JPEG of the event's cover, for the preview when a link is shared.

    It has to be a JPEG. The photos on the site are webp, which is smaller
    and better, but WhatsApp and the iPhone message preview will not draw a
    webp and simply show nothing instead. A share picture that nobody can
    see is the same as no share picture.

    Square, because the surfaces this lands in treat a square kindly and a
    tall photograph badly: a wide crop out of a portrait shot keeps about a
    quarter of its height, which is how people lose their heads.
    """
    out = os.path.join(HERE, "assets", "share", slug + ".jpg")
    src = os.path.join(HERE, "assets", "events", slug, shot + ".webp")
    if not os.path.exists(src):
        return None
    if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src):
        return "assets/share/%s.jpg" % slug

    try:
        from PIL import Image
    except ImportError:
        print("  no Pillow, share picture not made for", slug)
        return None

    im = Image.open(src).convert("RGB")
    side = min(im.width, im.height)
    left = (im.width - side) // 2
    # A third of the way down rather than the middle: in a standing shot the
    # faces are in the top half, and the middle crop cuts them off.
    top = int((im.height - side) * 0.33)
    im = im.crop((left, top, left + side, top + side))
    if side != 1200:
        im = im.resize((1200, 1200), Image.LANCZOS)

    os.makedirs(os.path.dirname(out), exist_ok=True)
    im.save(out, "JPEG", quality=82, optimize=True)
    print("  share picture:", os.path.basename(out))
    return "assets/share/%s.jpg" % slug


def share_tags(ev, shot):
    """What a phone shows when this event gets shared.

    An event already owns the right picture: its own cover. Pages that are
    not an event have nothing of their own yet and are waiting on a logo
    from the customer, which is why this only exists here.
    """
    lines = ['<meta property="og:type" content="article">',
             '<meta property="og:title" content="%s">' % ev["name"],
             '<meta property="og:description" content="%s. The night, and every photo from it.">'
             % ev["name"],
             '<meta property="og:url" content="%sevent-%s.html">' % (SITE, ev["slug"])]
    card = share_card(ev["slug"], shot) if shot else None
    if card:
        pic = SITE + card
        lines.append('<meta property="og:image" content="%s">' % pic)
        lines.append('<meta property="og:image:width" content="1200">')
        lines.append('<meta property="og:image:height" content="1200">')
        lines.append('<meta property="og:image:alt" content="%s">' % ev["name"])
        lines.append('<meta name="twitter:card" content="summary_large_image">')
        lines.append('<meta name="twitter:image" content="%s">' % pic)
    return "\n".join(lines)


def cover_for(ev):
    shot = cover_shot(ev)
    if shot:
        return ('<img src="assets/events/%s/%s-sm.webp" alt="" '
                'width="400" height="533" loading="lazy">' % (ev["slug"], shot))
    return '<span class="ph ph-wide"><span>Best photo from this event</span></span>'


def home_tiles(events, n=4):
    """The four event tiles on the home page, from the same data as the rest."""
    pick = [e for e in events if PHOTOS.get(e["slug"])][:n]
    if len(pick) < n:
        pick += [e for e in events if e not in pick][:n - len(pick)]
    out = []
    for ev in pick:
        shot = cover_shot(ev)
        if shot:
            pic = ('<img src="assets/events/%s/%s-sm.webp" alt="" width="400"'
                   ' height="533" loading="lazy">' % (ev["slug"], shot))
        else:
            pic = '<span class="ph ph-square"><span>Photo</span></span>'
        out.append(chr(10).join([
            '        <a class="tile" href="event-%s.html">' % ev["slug"],
            '          %s' % pic,
            '          <span class="name" style="display:block">%s</span>' % ev["name"],
            '        </a>']))
    return chr(10).join(out)


def page(ev, nxt):
    story = ev.get("story") or "[WHAT HAPPENED: two lines telling the story of the night.]"
    date = ev.get("date", "")
    sub = ev.get("subtitle")


    shot = cover_shot(ev)
    if shot:
        hero = ('      <img src="assets/events/%s/%s.webp" alt="%s" width="900" height="1200"'
                ' style="border-radius:.5rem; margin-bottom:1.25rem">'
                % (ev["slug"], shot, ev["name"]))
    else:
        hero = ('      <div class="ph ph-wide" style="margin-bottom:1.25rem">'
                '<span>Group shot, full width</span></div>')

    share = share_tags(ev, shot)

    return """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(name)s | Raven Steele</title>

<!-- GENERATED by build-events.py from events.json. Do not edit by hand:
     the next build will overwrite it. Change events.json instead. -->

<meta name="description" content="%(name)s. The night, and every photo from it.">
<meta name="theme-color" content="#000000">
<meta name="robots" content="noindex, nofollow">

<!-- The picture that shows when somebody shares this page. It has to be a
     full address: a phone sharing a link does not know where the page came
     from, so "assets/..." means nothing to it. SITE at the top of
     build-events.py is that address, and it changes the day a real domain
     is pointed at the site. -->
%(share)s
<link rel="stylesheet" href="assets/css/site.css">
<script src="assets/js/site.js" defer></script>
</head>
<body>

<header class="site-head">
  <div class="wrap">
    <a class="logo" href="index.html">Raven Steele</a>
    <button class="menu-btn" aria-expanded="false" aria-controls="site-nav" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
%(nav)s
</header>

<main>

  <section class="hero" style="padding-top:1.25rem">
    <div class="wrap">
      <a class="back" href="events.html">&larr; Back to all events</a>

%(hero)s

      %(datep)s
      <h2 style="margin-top:.3rem">%(name)s</h2>%(sub)s
      <p class="lede">%(story)s</p>
    </div>
  </section>

  <section>
    <div class="wrap">
      <div class="section-head">
        <p class="eyebrow">The night</p>
        <h2>Photos</h2>
      </div>

      <div class="photo-grid" id="photos">
%(photos)s
      </div>

      <p class="hint">Tap any photo to see it big and share it.</p>

      <!-- "#top" with nothing of that name on the page is the browser's own
           way of saying the top of the document. No script, and it works
           even if the page is still loading. Somebody who has scrolled past
           two dozen photographs should not have to swipe all the way back. -->
      <div class="entry">
        <a class="btn btn-ghost" href="#top">&uarr; Back to the top</a>
        <button class="btn btn-ghost" data-share>Share event</button>
        <a class="btn btn-primary" href="event-%(next)s.html">Next event</a>
      </div>
    </div>
  </section>

</main>

%(foot)s""" % {
        "name": ev["name"],
        "nav": NAV,
        "hero": hero,
        "datep": ('<p class="event-date">%s</p>' % date) if date else "",
        "sub": ('\n      <p class="lede" style="margin-top:.2rem"><em>%s</em></p>' % sub) if sub else "",
        "story": story,
        "photos": photo_grid(ev["slug"], ev.get("photos", 8)),
        "next": nxt,
        "share": share,
        "foot": FOOT,
    }


def card(ev):
    date = ev.get("date", "")
    count = len(PHOTOS.get(ev["slug"]) or []) or ev.get("photos", 8)
    meta = ("%s &middot; %s photos" % (date, count)) if date else ("%s photos" % count)
    return """        <a class="event-card" href="event-%(slug)s.html"
           data-tag="%(year)s"
           data-event="%(name)s"
           data-event="%(name)s">
          %(cover)s
          <span class="name" style="display:block">%(name)s</span>
          <span class="meta">%(meta)s</span>
        </a>""" % {
        "slug": ev["slug"],
        "year": ev["year"],
        "name": ev["name"],
        "cover": cover_for(ev),
        "meta": meta,
    }


def main():
    global PHOTOS
    os.chdir(HERE)

    index = os.path.join("assets", "events", "index.json")
    if os.path.exists(index):
        PHOTOS = json.load(io.open(index, encoding="utf-8"))

    data = json.load(io.open("events.json", encoding="utf-8"))
    events = data["events"]

    for i, ev in enumerate(events):
        nxt = events[(i + 1) % len(events)]["slug"]
        io.open("event-%s.html" % ev["slug"], "w", encoding="utf-8").write(page(ev, nxt))

    listing = "\n\n".join(card(ev) for ev in events)
    listing += '\n\n        <p class="empty" data-hidden="true">Nothing from that year yet.</p>'

    text = io.open("events.html", encoding="utf-8").read()
    if "EVENTS:START" not in text:
        print("!! EVENTS markers missing from events.html")
    else:
        text = re.sub(r"(<!-- EVENTS:START -->).*?(<!-- EVENTS:END -->)",
                      lambda m: m.group(1) + "\n" + listing + "\n        " + m.group(2),
                      text, flags=re.S)
        io.open("events.html", "w", encoding="utf-8").write(text)

    home = io.open("index.html", encoding="utf-8").read()
    if "HOMEEVENTS:START" in home:
        home = re.sub(r"(<!-- HOMEEVENTS:START -->).*?(<!-- HOMEEVENTS:END -->)",
                      lambda m: m.group(1) + chr(10) + home_tiles(events) + chr(10) + "        " + m.group(2),
                      home, flags=re.S)
        io.open("index.html", "w", encoding="utf-8").write(home)

    withphotos = sum(1 for e in events if PHOTOS.get(e["slug"]))
    print("%d events, %d with real photos" % (len(events), withphotos))


if __name__ == "__main__":
    main()
