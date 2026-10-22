# Deterministic detectors: narrow scope and falsification

The catalog **does not** imply 383 implemented detectors. The package provides demonstrative standard-library algorithms only for a few patterns:

| Detector | Exact implemented condition | Limitations |
|---|---|---|
| `inside_day` | high[t] < high[t-1] and low[t] > low[t-1] | Strict inequality; bar frequency not inferred |
| `outside_day` | high[t] > high[t-1] and low[t] < low[t-1] | No predicted direction |
| `nr4` / `nr7` | range[t] strictly below all previous 3 / 6 ranges | Equal ranges excluded; no next-bar breakout assumption |
| `full_gap_up/down` | low[t] > high[t-1] / high[t] < low[t-1] | Not an overnight close-to-open change; adjust for splits/dividends |
| `double_bottom/top` | local extrema confirmed with right=2 bars; two similar lows/highs within 3.5% and 4–70-bar separation; neckline height >3%; closes beyond neckline after 2nd pivot confirmed | Heuristic, not faithful implementation of all Bulkowski rules; overlapping candidates can repeat; no prior trend filter |

All conditions use data available through the stated signal bar; right=2 for pivots creates identification lag. The event date is the **confirmation** date, never the pivot's historical date. No classifier accuracy, generalization, signal profitability or false positive rates are claimed.

## CSV

`date,open,high,low,close,volume` sorted strictly in ISO-style ascending strings. Volume optional; strict positive price; high/low envelope required; NaNs and duplicate dates rejected. Corporate actions and instrument-specific calendars must be processed upstream.

```bash
python skills/pattern-atlas/scripts/scan_ohlcv.py examples/demo_ohlcv.csv
python skills/pattern-atlas/scripts/scan_ohlcv.py examples/demo_ohlcv.csv --no-double
```

## Before adding any detector

1. Pick precisely one pattern and obtain its **primary definition** with allowed deviations, market/timeframe and confirmation.
2. Write positive and near-miss *synthetic* unit tests before tuning. Track overlaps and multiple hits.
3. Pivot algorithms cannot use future right-hand bars when claiming an entry timestamp. Separate setup discovery from executable confirmation.
4. Backtest using walk-forward/holdout, adjusted prices where appropriate, delistings, volume filters, fees, slippage, stop feasibility, and a benchmark. Limit multiple-comparison fishing.
5. Report precision/recall only with manually labeled ground truth, and investment performance only with verified fills.
