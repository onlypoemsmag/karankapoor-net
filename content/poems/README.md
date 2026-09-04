# Poem texts for the photograph cards

Drop one plain-text file per photograph here, named by the photograph's slug
(see assets/photos/manifest.json), e.g. `caged.txt`, `beloved.txt`.

- The file's contents are the poem exactly as it should appear: one line per line,
  blank lines for stanza breaks. No title or attribution inside the file — the
  card already shows the poem title and poet from the pairing table.
- After adding files, run `python3 tools/build_pages.py` and push.

Karan holds the permissions for these texts; only put up poems that are cleared.
