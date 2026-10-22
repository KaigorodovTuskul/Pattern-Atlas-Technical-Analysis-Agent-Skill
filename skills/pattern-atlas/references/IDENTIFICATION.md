# Identification: operational protocol

## 1. Fix the observation boundary
- Timestamp of latest closed bar and exchange timezone.
- Frequency (daily/weekly/intraday); adjusted or raw series; volume quality.
- Context window: preceding trend, pivot scale, corporate actions and regime.

## 2. Label candidate and null alternative
- Select a **specific** catalog record, not merely “looks bullish”.
- Mark precise coordinates of extrema and touched boundaries, distinguish a wick touch from close.
- Compare with a nearby family (pennant versus triangle; rounded bottom versus cup; H&S versus broadening).
- Do not identify using candles printed after the claimed first recognition time.

## 3. State the testable logic
- Setup: what prior price action must exist.
- Geometry: minimum pivot/touch/period count, width, slope tolerances and near-equality measure.
- Confirmation: close through neckline, trendline or range, optionally with volume.
- Failure: re-entry, wrong-side breakout, invalidating swing level or expiry window.
- Target is separate from whether the setup was triggered; geometric targets may fail.

## 4. Quality grade
- High confidence **in geometry**: shape, swings and breakout levels directly observable.
- Moderate confidence: alternate geometries nearly as plausible.
- Low/indeterminate: no last-close data, synthetic chart only or missing source rules.
- NEVER convert these qualitative descriptions to made-up probabilities.

## 5. Practical report
Return candidate + alternate candidate + null, named points and levels, confirmed/unconfirmed state, invalidation level, context and why interpretation could fail.
