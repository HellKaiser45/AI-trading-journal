# Recap — EXPIRED_2026-11-01T1010Z_ASTERUSDT
**TL;DR** Best-built analysis of week two, decided by 0.0017 of price: the box ceiling was tagged nine times and then never retested → no fill.

`ASTERUSDT 1h · SHORT LIMIT 0.7050 · TP 0.6986 (−0.91%) / SL 0.7122 (+1.02%) · RR 0.89 · 01T10:20Z→02T22:00Z · P(fill) 0.64 · P(TP|fill) 0.68 · p_BE 0.529`

## Plan / predicted
Sell the 0.7045–0.7057 band that capped 8 of the last 17 hourly bars into the 0.6972–0.6988 shelf; SL 0.0022 above the 0.7100 recovery high (the WIN+1.26% ASTER stop shape). Forecast: drift to 0.6974, rebound to 0.7050 at 22:00–23:00Z.

## Why (chart input)
After the 29 Oct spike to 0.7321 and crash to 0.6589, ASTER recovered 7.8% to 0.7100 and spent 17h in a 0.6972–0.7057 box with volume contracting 510k→110–160k. Research: funding 0.0216%/4h (12 consecutive positives, longs paying), 62.3% accounts long, top traders 82.1% long, bid wall 0.6986, ask walls 0.7040/0.7100.

## What happened
Window high 0.7033 — 0.0017 short of the limit. Everything else happened: the box broke down, the low printed 0.687 (four times through the TP), exit 0.6959, i.e. 1.29% under the entry level.

## Right / wrong
Right: read of the box and its ceiling, TP inside the shelf, SL beyond the measured extreme, honest cost caveat. Wrong: entry at the *inner* edge (0.7050) of a measured band whose far edge (0.7057) had been tagged nine times — 0.10% of extra reward cost the entire trade.

## Right trade
Counterfactual, same candles: recomputed far-edge entry 0.7057 with TP 0.6986/SL 0.7122 keeps RR 1.09 (vs 0.89) at a price the market had tagged repeatedly; the pay in the window was shorting the 0.7033 print into 0.687 = +2.32%.

## Lesson
1. Fill-robustness beats 0.1% of reward: quote the far edge of a band, then check RR still exceeds break-even.
2. A near-miss is not an almost-win — under the model an unfilled order pays 0 and is scored 0; fix the entry rule.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`