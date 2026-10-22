# Analytical protocol: from geometry to falsifiable hypothesis

## Observation versus inference

For each chart, record the last completed date/time, symbol, timeframe, exchange, OHLC adjustment policy, timestamp timezone, missing bars and volume availability. Treat screenshot-only analysis as **visual and approximate**. Never fabricate OHLC values.

Name an entry from the index; open the corresponding family methodology, identify 2–3 essential geometric landmarks and plausible competing interpretations, and label the current status `unconfirmed`, `confirmed`, `invalidated` or `indeterminate`. A source name alone does not establish predictability.

## Minimal annotated report

| Field | Question |
|---|---|
| Instrument and interval | What series was actually observed? |
| Label / alternative | Which taxonomy entries could fit; what null model? |
| Formation window | What bars were available at discovery time? |
| Extremum confirmation | How many right-hand bars were needed to know the pivot existed? |
| Boundaries and trigger | What exact price/close must be exceeded? |
| Invalidity | What future observation would disprove the setup? |
| Context | Prior trend, volume, volatility, earnings, liquidity and data quality? |
| Outcome metric | What constitutes a success or failure, and over what horizon? |
| Uncertainty | What is measured, assumed, not verified or unknowable from screenshot? |

## Causal validation checklist

- Time-split training/evaluation and out-of-sample holdout, no future bar access at the time of signal.
- Use completed-pivot confirmation timestamps, not retrospective midpoint extrema without lag.
- Distinguish candidate labels from actionable triggers.
- Avoid fitting dozens of thresholds to the test set; disclose how many patterns were screened (multiple testing).
- Control for delisted instruments, survivorship, cash dividends/splits and large overnight gaps.
- Add fees, spreads, slippage, delayed execution and position limits.
- Report sample size, base rate, confidence intervals, false-positive frequency, regime instability and a simple baseline.
- Reconcile contradictory pattern interpretations instead of declaring all bullish.

For available code rules see [DETECTION](../skills/pattern-atlas/references/DETECTION.md), and for provenance see [SOURCE_AUDIT](SOURCE_AUDIT.md).
