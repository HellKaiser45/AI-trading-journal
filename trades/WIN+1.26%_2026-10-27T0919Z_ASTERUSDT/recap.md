# Recap — WIN+1.26%_2026-10-27T0919Z_ASTERUSDT
**TL;DR** The journal's reference template: level that was repeatedly tagged, stop beyond the whole measured overshoot envelope, target at a high-traffic level, entry ~0.5% from spot.

`ASTERUSDT 1h · SHORT LIMIT 0.7150 · TP 0.7060 (−1.26%) / SL 0.7200 (+0.70%) · RR 1.80 · 27T10:45Z→28T22:30Z · P(fill) 0.64 · P(TP|fill) 0.765 · P(SL) 0.13 · p_BE 0.357`

## Plan / predicted
Fade the 0.7140–0.7152 band (4 of the last 48 hourly highs, 6–7 tags in 72h) into 0.7060 (27 of the last 48 hourly lows, not the range extreme); stop 0.0022 above the single 0.71784 spike. Forecast: probe 0.7150 by 27T17–18Z, fade through 0.7060 on 28T02–03Z, end 0.7104.

## Why (chart input)
8-day range 0.68507–0.72714 with higher lows (0.68507→0.69749→0.70270) and lower highs in the last 24h; Jev: rotation rather than trend 0.86, downside break more likely than upside 0.94. Research agenda (Jev's): ASTER events in the window — none confirmed.

## What happened
Filled 28T03:50Z, 17.1h after placement. MAE only −0.53% (window high 0.7188, 0.17% under the stop), MFE +1.82%; TP hit 28T12:30Z, 8.7h after the fill; exit 0.7089.

## Right / wrong
Right: all three design choices were deliberate carry-overs from prior losses — stop beyond the measured overshoot envelope (7 bars reaching 0.7140 never exceeded 0.7195), target inside the range at a high-tag level, entry within ~0.5% of spot with measured P(fill). Wrong: nothing material; the entry took 17.1h to fill and a 0.7155 limit would only have had ~0.50 fill probability.

## Right trade
Essentially the trade taken: the window's best short was 0.7188→0.702 = +2.34%, the ticket banked 1.26% of 1.26% targeted.

## Lesson
1. The working shape is repeatable: repeatedly touched level + stop beyond the entire measured overshoot envelope + TP at a high-tag level + entry near spot (both journal wins show MAE ≈ 0.53%).
2. Measure the overshoot envelope as a base rate before choosing any stop; the stop's survival is worth more than RR cosmetics.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`