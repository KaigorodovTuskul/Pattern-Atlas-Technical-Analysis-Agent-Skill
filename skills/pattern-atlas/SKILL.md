---
name: pattern-atlas
description: Research, identify, critically validate, explain and illustrate chart patterns, short OHLC bar formations, gaps, Elliott/harmonic patterns and event setups. Use with price charts or OHLCV data for evidence-grounded technical analysis, source-aware chart-pattern lookup, falsification, risk levels and alternative hypotheses. Includes an offline catalog, original schematic examples and limited deterministic scanners; never invent performance statistics or claim all patterns are programmatically detected.
license: MIT
metadata:
  version: "1.0.0"
  category: financial-analysis
---

# Pattern Atlas — Describe. Verify. Falsify.

**Use catalog names as discovery pointers, not as evidence of a profitable signal.** Do not turn visual resemblance into a probability without an appropriate dataset. Work in the user's language; keep original English names for unambiguous lookup.

## Activate for
- User asks to name a pattern on chart/screenshot, find historical analogues, explain setups or compare competing technical-analysis interpretations.
- User supplies OHLCV data and wants formal candidate detection, a reproducible screener, charts or pattern annotations.
- User asks about Thomas Bulkowski / ThePatternSite chart, short, volume, event, harmonic or Elliott-wave patterns.

Do not invoke for unrelated fundamental analysis or portfolio questions unless technical patterns are relevant.

## Source-of-truth routing

1. **Find entry (not all 383)** by name/phrase: `python skills/pattern-atlas/scripts/search_catalog.py "ascending triangle" --limit 5`; use `--id` or `--json` for a single record. For class index use [INDEX](references/INDEX.md) or `--families`.
2. Open ONLY the appropriate [family reference](references/REFERENCE_MAP.md), then inspect matching `data/catalog.json` record for the original synthesis, variant notes, `confidence`, verified link, schematic path.
3. For exact author-specific ratio, thresholds, sample size or published win rate, consult original verified detail page when available. Otherwise explicitly state that **individual source verification is missing**, use family-level explanation and abstain from precise claims.
4. For historical performance: **never invent Bulkowski numbers**; require identified study period, source revision, market regime, upside/downside breakout, instrument universe, entry/exit assumptions, costs and failure definition. See [EVIDENCE](references/EVIDENCE.md).
5. For plotted image, inspect the user's actual chart before asserting geometry. If only a name is supplied, use an **original synthetic SVG diagram** for teaching; it is *not* a market sample and is *not* a site image.

## Visual pattern analysis — falsification first

- **Inputs**: instrument, exchange, adjusted/raw series, timezone, interval, last completed bar, available volume, known corporate actions. Do not invent missing observations.
- **Candidate**: classify family and variant. Mark swing pivots, touches, support/resistance lines, trend leading into pattern and relevant volume conditions, using bars available *at the alleged decision time*.
- **Status**: `unconfirmed` (shape only), `confirmed` (explicit closing-breakout rule met), `invalidated` (defined violation) or `indeterminate` (insufficient data or ambiguous geometry). Treat an intrabar break differently from a close.
- **Alternatives**: at least one plausible competing labeling or a no-pattern null; note why it could fit.
- **Risk**: explain invalidation level, potential stop location, liquidity, slippage, transaction costs and position sizing; geometric target is a **scenario**, never a forecast.
- **Evidence**: provide source URL, name and confidence of catalog record; differentiate source research from original synthesis. Do not claim detector verification merely because an SVG exists.

If computer vision on a screenshot lacks exact OHLC, give an interpretation with uncertainty and do not calculate fabricated percentages.

## OHLCV workflow

Use the dependency-free demo screener ONLY for implemented cases:

```bash
python skills/pattern-atlas/scripts/scan_ohlcv.py skills/pattern-atlas/assets/data/demo_ohlcv.csv --output results.json
```

For installed projects, resolve the script and demo file relative to the **installed skill directory** (the path shown above is for a source checkout). Supply your own OHLCV CSV for real analysis.

Supports strict `inside_day`, `outside_day`, `nr4`, `nr7`, true non-overlapping `full_gap_up/down`, and a conservative heuristic for **confirmed** `double_bottom/top`. Its rules are in [DETECTION](references/DETECTION.md). No 383-pattern general detector is bundled. For other patterns, propose formal criteria first, build and backtest if requested, with full acknowledgment of look-ahead bias.

## Output contract (analysis requests)

```text
Instrument / interval / last closed bar / data adjustments
Candidate pattern (catalog name + family) — status / confidence / evidence
Concrete landmarks: pivots, boundaries, breakout level, volume context
Confirmation and invalidation rules; alternative interpretations
Conditional scenarios and risk; NEVER a guaranteed target
Source link(s) and limits (image vs OHLC, verified vs family-level)
```

For comparisons, produce a short table including trigger, weaknesses and context. For scanners, emit timestamped JSON and a minimal visualization if useful.

## Reference map

- [Family selector](references/REFERENCE_MAP.md) → 38 family Markdown modules loaded on demand.
- [Identification guide](references/IDENTIFICATION.md) → chart annotation and competing explanations.
- [Detection protocol](references/DETECTION.md) → precise tested Python subset and extension methodology.
- [Evaluation / provenance](references/EVIDENCE.md) → claims and statistical hygiene.
- [Full index](references/INDEX.md) → alphabetical names and provenance states.
- [Source audit](../../docs/SOURCE_AUDIT.md) → hard limitations of this release.

## Non-negotiable boundaries

Do not reproduce, claim ownership of or bulk-download proprietary diagrams/page text from ThePatternSite. Cite Thomas Bulkowski's site as taxonomy inspiration, with no endorsement. Illustrative SVGs here are independently generated, not re-creations of specific historical charts. **Never imply that the entire source site was verified page by page**, that a pattern is a profitable edge, or that a model has a fully implemented detector unless true.
