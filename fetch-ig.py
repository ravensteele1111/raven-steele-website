"""
Pull the cover frame off an Instagram reel or post.

    python fetch-ig.py mirror-video https://www.instagram.com/therealravenai/reel/DcLxBl8JQ7z/

The first argument is the name to save it under, the second is the address.
The picture lands in assets/ig/<name>.jpg, resized to 360 wide.

WHAT THIS CAN AND CANNOT DO

  Reels and posts    yes. Instagram still answers /p/<code>/media/?size=l with
                     the real cover frame, no login needed.
  Highlights         no. A highlight is a collection, not a post, so it has no
                     code to ask for, and the page behind it is a login wall.
                     Highlight covers have to come from the person who owns the
                     account: open the highlight, Edit highlight, and the cover
                     image can be saved from there.

The addresses Instagram hands back are signed and expire within days, so the
picture is downloaded and kept, never linked to directly.
"""

import os
import re
import sys
import urllib.request

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

HERE = os.path.dirname(os.path.abspath(__file__))


def shortcode(url):
    m = re.search(r"/(?:p|reel|reels|tv)/([A-Za-z0-9_-]+)", url)
    return m.group(1) if m else None


def fetch(name, url, width=360):
    code = shortcode(url)
    if not code:
        print("not a post or reel address, skipped:", url)
        print("  (a highlight cannot be fetched - see the notes at the top of this file)")
        return False

    src = "https://www.instagram.com/p/%s/media/?size=l" % code
    try:
        data = urllib.request.urlopen(
            urllib.request.Request(src, headers={"User-Agent": UA}), timeout=30).read()
    except Exception as e:
        print("failed:", name, e)
        return False

    if len(data) < 5000:
        print("came back too small to be a picture:", name)
        return False

    os.makedirs(os.path.join(HERE, "assets", "ig"), exist_ok=True)
    dest = os.path.join(HERE, "assets", "ig", name + ".jpg")
    open(dest, "wb").write(data)

    try:
        from PIL import Image
        im = Image.open(dest).convert("RGB")
        if im.width > width:
            im = im.resize((width, int(width * im.height / im.width)), Image.LANCZOS)
        im.save(dest, quality=80, optimize=True)
        print("saved assets/ig/%s.jpg  %dx%d" % (name, im.width, im.height))
    except ImportError:
        print("saved assets/ig/%s.jpg (not resized)" % name)
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3 or len(sys.argv) % 2 == 0:
        print(__doc__)
        sys.exit(1)
    args = sys.argv[1:]
    for i in range(0, len(args), 2):
        fetch(args[i], args[i + 1])
