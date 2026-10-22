# Contributing

Issues and PRs correcting individual pattern definitions and expanding *verified* coverage are welcome. Please identify the **specific original source page**, the dated snapshot/reference, and a separately worded formulation with reproducible OHLC criteria. Never add copyrighted diagrams, wholesale page transcriptions, proprietary tables or copied screenshots.

## Development loop

```bash
python scripts/build_catalog.py
python scripts/render_diagrams.py
python scripts/build_docs.py
python scripts/validate.py
python -m unittest discover -s tests -v
```

Source-of-truth edits: `scripts/build_catalog.py` and `skills/pattern-atlas/data/index_names.txt`. Generated content: `skills/pattern-atlas/data/catalog.json`, `families.json`, `references/<family>.md`, `patterns/*.md`, `assets/charts/*.svg`, `gallery.html`. Keep builds deterministic. Improve source verification **without silently overwriting the meaning of confidence statuses**.

Definition submissions must include positive and negative examples, breakout/invalidation rules, data adjustments, and a no-look-ahead definition. Computational scanner extensions need tests and documented limitations.
