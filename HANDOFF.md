# karankapoor.net — project handoff (2026-09-04)

Read this first in any new session. The repo is the single source of truth;
nothing lives only in an old conversation.

## What this is
Karan Kapoor's personal site, rebuilt from Squarespace as a hand-written static
site on GitHub Pages. Repo: https://github.com/onlypoemsmag/karankapoor-net
(public, Pages from `main` branch root). Local checkout: `~/Claude/karankapoor-net`.

## Design system (approved through many mock rounds — do not re-litigate)
- Identity: cadmium yellow #FDDA0D, pure black, white. Fraunces (display, opsz 144
  for big sizes), Literata (text). Self-hosted woff2 in assets/fonts. Tokens in
  assets/css/site.css.
- Dark mode ("the Night Edition"): via prefers-color-scheme — near-black #0b0a08
  page, warm-white text, yellow display headings; yellow bands become black with
  hairline borders.
- Interactions (measured off onlypoems.com and ported from Karan's own
  Projects/Webflow/onlypoems-poets/op-poets.js): Lenis smooth scroll
  (lerp .075, wheelMultiplier .9, vendored in assets/js), zoom hovers (never
  lifts/shadows), draw-on underlines for nav, marker-highlight hover on poem rows,
  black-pill/yellow-text buttons that invert + scale(1.055) on hover, icon footer
  with envelope whose flap opens on hover, OP/SP logos as CSS masks
  (assets/img/*-logo.png, colored via currentColor).
- Photographs lightbox: opens growing out of the clicked tile, page blurs behind,
  card tilts with the pointer (rotateX 13.6 / rotateY 16, perspective 1600),
  click flips it (rAF-eased 620ms, direction from which half you push, gloss
  sweep) to reveal the paired poem. Everything dies under prefers-reduced-motion.
- Content fidelity is absolute: wording from archive/content.md unless Karan
  approved a change (current bio + book description in tools/build_pages.py are
  the approved 2026-09-04 versions). Titles italic per style: journals/books
  italic, presses roman.

## Build
- `python3 tools/gen_images.py` regenerates responsive images from archive/
  (WebP 2000/1200/700 + JPEG fallback). Pillow required.
- `python3 tools/build_pages.py` regenerates index.html, poems/, photographs/,
  404.html, home/ (redirect), sitemap.xml, robots.txt. ALL page edits happen in
  this script, not in the emitted HTML.
- Poem texts for the photo card backs: drop plain-text files in content/poems/
  named by slug (see content/poems/README.md), rebuild, push. Dickinson's
  marble-veil.txt is the working example (public domain). Karan holds permissions
  for the rest and pastes them himself; Claude must not paste in-copyright texts.
- PAIRINGS.md = full photo→poem pairing table + verified source links.

## Deployment / domain state (as of 2026-09-04)
- gh CLI authenticated as `onlypoemsmag` (keyring). Pages custom domain:
  www.karankapoor.net; CNAME file in repo.
- Squarespace DNS (account poetkarankapoor@gmail.com — email 2FA on every login
  AND on DNS edits; codes go to that inbox, Karan relays them): DONE —
  4× A @ → 185.199.108/109/110/111.153, 4× AAAA @ → 2606:50c0:8000-8003::153,
  CNAME www → onlypoemsmag.github.io,
  TXT _github-pages-challenge-onlypoemsmag → 9eef2820b3d0fba55797d724d8b6de.
  Squarespace-defaults preset was replaced; "Squarespace Domain Connect" preset
  left in place (harmless).
- Domain verified in GitHub user settings (takeover protection) ✓.
- Registration: keep! Renews Jun 16 2027, ~$20/yr, auto-renew ON.

## Remaining / next steps
1. DONE (2026-09-04): HTTPS cert issued, https_enforced=true. Full go-live
   checklist passed: https on www + apex (apex 301→www), http→https 301,
   /poems/, /photographs/, /home redirect, photos, OG image, sitemap all 200.
   ⇒ It is now SAFE for Karan to cancel the Squarespace WEBSITE plan — but
   NEVER the domain registration (keep auto-renew ON; cancelling the site plan
   must not release the domain — confirm the domain stays active afterwards).
2. DONE — see 1.
3. Karan pastes cleared poem texts into content/poems/ (links in PAIRINGS.md);
   verify a few of my from-memory attributions (Chang's Hopper study, Smith's
   "When the Burning Begins", Hayes's "New York Poem", Shahid's "After You",
   Lee's "The Sandalwood").
4. Optional /thirst/ page (spec said ask first — never built).
5. Consider transferring the repo from onlypoemsmag to a personal GitHub account
   (Pages + domain move with it).
6. Old review artifacts (claude.ai/code/artifact/...) are superseded by the live
   site; mocks/ and archive/ stay in the repo forever per ground rules.
