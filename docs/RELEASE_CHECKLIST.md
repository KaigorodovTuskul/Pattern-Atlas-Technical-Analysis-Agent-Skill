# GitHub release checklist

- [x] Canonical Skill metadata and progressive-reference folder under `skills/pattern-atlas/`.
- [x] Curated 426 source-name index rows, 383 normalized entries, explicit 43 repeated names.
- [x] 38 family references; 383 standalone entry guides; 334 programmatic static SVG examples.
- [x] Fixed, limited OHLCV scanner with sample CSV (inside skill and root examples).
- [x] Discovery CLI, offline gallery, cross-reference validation, local installer.
- [x] 15 offline unittests and GitHub Actions CI configuration.
- [x] Disclosed source-content limits, IP/attribution, status of unverified author-specific definitions.
- [x] English README plus a complete Russian translation with a language switcher.
- [x] Published at <https://github.com/KaigorodovTuskul/Pattern-Atlas-Technical-Analysis-Agent-Skill> with `stable` as the default branch.
- [ ] Independently inspect each of the 383 upstream detail pages — **not completed**; this is not required for operating the research skill, but is required before asserting definition-completeness.
- [ ] Independently test each pattern as a profitable signal — **not done**; do not claim detection completeness or trading edge.

## Publishing

The project is published at <https://github.com/KaigorodovTuskul/Pattern-Atlas-Technical-Analysis-Agent-Skill> with `stable` as the default branch. To publish an update from a checkout:

```bash
git add .
git commit -m "chore: update Pattern Atlas"
git push origin stable
```

Do not run `git init` again in an existing checkout. Keep the repository root layout unchanged.
