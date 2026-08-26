# Design research — round 2 (2026-08-25, overnight)

## The verdict on round 1
Rejected as "too AI": cream paper + centered serif + generic elegance. The tell of an
AI-designed site is a tasteful-but-anonymous surface — nothing that could only belong
to this one person. The fix is to build from Karan's existing identity, not from
"elegant poet site" priors.

## The Karan Kapoor identity (measured from the live site)
- **Cadmium yellow `#FDDA0D`** — used as full-bleed page-width fields (`data-section-theme="bright"`)
- **Pure black `#000000`** and **white `#FFFFFF`**
- Buttons on the old site: black pills with yellow text
- Footer: bright-inverse (black field, yellow text)
- Secondary (old site only, probably droppable): pale blue `hsl(208,100%,97%)` behind two blurbs; dark blue links `hsl(220,100%,30%)`
- ONLY POEMS (must NOT resemble): pastel pink/purple/blue, playful illustration,
  swash didone display, electric blue UI. Black/yellow is maximally distant from it.

## Sites studied (screenshots taken where possible)
- **kavehakbar.com** — the whole homepage is his name. Ultra-minimalism as confidence.
- **danezsmithpoet.com** — full-bleed portrait, giant name overlaid, books as nav items.
- **oceanvuong.com** — book-cover hero + plain nav; commerce-forward.
- **aworkinglibrary.com** (Mandy Brown) — slab-serif ledger; label column + content column
  separated by hairlines. Bookish but structured; nothing centered.
- **thedriftmag.com** — homepage is a single riddling paragraph where every link is
  an underlined word. Text as interface. Cream + red.
- **frankchimero.com** — typographic index, dates as texture, zero imagery.
- **craigmod.com** — single column, book covers as anchors, conversational microcopy.
- **robinrendle.com** — file-browser conceit (sidebar of folders); the site as artifact.

## What the good ones share
1. One idea, committed to totally (a name, a paragraph, a ledger, a cover).
2. The design could belong to no one else — it grows out of the person's own material.
3. Type does everything; color is identity, not decoration.
4. Never a centered hero + sections + cards. Structure is asymmetric or full-bleed.

## Directions built this round (all on the #FDDA0D / #000 / #FFF identity)
- **D — The Cover** (`mock-d-cover.html`): opens as a full-bleed cadmium-yellow book
  cover, name set enormous in Fraunces Black. Scroll: white bio, black THIRST section
  (the old footer's bright-inverse promoted to a chapter), blurbs, black/yellow footer.
- **E — The Index** (`mock-e-index.html`): white ledger. IBM Plex Mono catalog labels
  in a left rail, Newsreader text right, hairline rows. Yellow only as highlighter:
  link hover wash, the one button, selection.
- **F — The Letter** (`mock-f-letter.html`): the homepage is prose — bio and THIRST
  as flowing large Literata paragraphs, links underlined in-text, the announcement
  line permanently marked in yellow highlighter. The Drift's move, made personal.
- **G — The Night Edition** (`mock-g-night.html`): black page, white text, yellow
  display type in Instrument Serif. The old site's footer expanded into a whole site.
  Photographs would sing on this ground.

## Directions considered and not built (available on request)
- Akbar-style radical minimum: yellow page, name, three links, nothing else.
- Danez-style photo-led: full-bleed photograph hero (his photos are strong enough).
- Rendle-style conceit: site as manuscript/typescript (mono, marginalia).
- Broadsheet: newspaper grid, poems list as front-page columns.

## Palette accessibility notes
- Black on #FDDA0D: ~14.7:1 (AAA). Yellow on black: ~14.7:1 (AAA).
- Yellow on white: fails — yellow is never used as text on white, only as a field,
  a highlight behind black text, or an underline/rule.
