# raven-steele-website

The Raven Steele website.

Plain HTML and CSS, no framework and no build step. Every page is a file you can
open in a browser.

Right now this repository holds a holding page only — enough for GitHub Pages to
have something to publish. The real site is being built.

## Before you push a change to the CSS or the JavaScript

Run this first:

    python stamp.py

It puts the file's own version number into every page's `<link>` and
`<script>`. Without it, phones and browsers keep serving the old stylesheet and
your change appears not to have worked.
