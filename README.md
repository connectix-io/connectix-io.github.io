# connectix-io.github.io

The Connectix site: plain HTML and CSS, no build step. Served by GitHub
Pages from the `main` branch, root folder.

The design follows voipappz.com (header, hero, section rhythm, cards, footer),
written as one stylesheet without Bootstrap or jQuery. The copy of the front
page, the about page and the contact promo is voipappz.com's (branch `rotem`
of va-voipappz.com) with the product named Connectix; the product page is
Connectix's own.

## Files

| Path | What |
|---|---|
| `index.html` | The one page: what Connectix does, downloads for every platform (links to the latest GitHub Release), contact |
| `product.html`, `about.html`, `contact.html` | Redirects to the matching section of `index.html`, so old links still work |
| `assets/css/site.css` | The one stylesheet |
| `assets/js/site.js` | The mobile navigation toggle; nothing else needs JavaScript (the FAQ uses `<details>`) |
| `assets/images/connectix-mark.svg` | The logo mark (copied from the app) |
| `assets/images/connectix-logo.svg`, `connectix-logo-white.svg` | The mark plus the word "Connectix" in Rubik; the word is SVG text, not paths. The pages inline this markup so the web font applies |
| `assets/images/logos/` | The customer logos, as on voipappz.com |
| `favicon.svg`, `favicon.ico`, `apple-touch-icon.png` | The mark as icons; the raster ones come from `scripts/make-favicon.py` |
| `robots.txt`, `.nojekyll` | Crawlers allowed; Pages serves the files as they are |

The header and the footer are the same block of HTML in each page. Change
them in all four. All copy is in the HTML, none is generated.

## Publishing

Pages is set to **Deploy from a branch**, `main`, `/ (root)`. A push to
`main` publishes within about a minute at `https://connectix-io.github.io/`.

### A custom domain

<!-- CNAME: when the domain is decided, add a file named `CNAME` at the root
     containing only the bare domain (for example `www.example.com`), point the
     domain's DNS at GitHub Pages, and set the domain in Settings, Pages.
     The file is deliberately absent until then. -->

No `CNAME` file is in the tree yet; see the comment in this file's source.

## Before publishing a change

- `CONTACT_EMAIL` in `contact.html` (one line, the `mailto:` link and its
  text) is a placeholder until the real address is set.
- Run `scripts/check-links.sh`: it tests that every local `href` and `src`
  resolves to a file.
- To regenerate the raster icons from the mark's geometry:
  `python3 scripts/make-favicon.py`.
