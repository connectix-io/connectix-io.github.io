# connectix-io.github.io

The Connectix marketing site: plain HTML and CSS, no build step. Meant for
GitHub Pages under the `connectix-io` organisation.

## Files

| Path | What |
|---|---|
| `index.html` | What Connectix is, the three jobs, how it works, where it runs |
| `product.html` | The softphone, the bot on calls, events and screen pops, the chat, reports |
| `about.html` | Who makes it, what we hold to, what we do not claim |
| `contact.html` | The email address and the downloads |
| `assets/css/site.css` | The one stylesheet |
| `assets/js/site.js` | The mobile navigation toggle; nothing else needs JavaScript |
| `assets/images/connectix-mark.svg` | The logo mark (copied from the app) |
| `assets/images/logos/` | The logo band on the front page |
| `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` | The mark as icons; the raster ones come from `scripts/make-favicon.py` |
| `robots.txt`, `.nojekyll` | Crawlers allowed; Pages serves the files as they are |

The header and the footer are the same block of HTML in each page. Change
them in all four. All copy is in the HTML, none is generated.

## Publishing

1. Create the repository `connectix-io/connectix-io.github.io` and push this
   tree to its `main` branch.
2. In the repository's Settings, Pages: source **Deploy from a branch**,
   branch `main`, folder `/ (root)`.
3. The site is served at `https://connectix-io.github.io/` a minute later.

### A custom domain

<!-- CNAME: when the domain is decided, add a file named `CNAME` at the root
     containing only the bare domain (for example `www.example.com`), point the
     domain's DNS at GitHub Pages, and set the domain in Settings, Pages.
     The file is deliberately absent until then. -->

No `CNAME` file is in the tree yet; see the comment in this file's source.

## Before publishing

- Replace `CONTACT_EMAIL` in `contact.html` (one line, the `mailto:` link and
  its text) with the real address.
- Run `scripts/check-links.sh`: it tests that every local `href` and `src`
  resolves to a file.
- To regenerate the raster icons from the mark's geometry:
  `python3 scripts/make-favicon.py`.
