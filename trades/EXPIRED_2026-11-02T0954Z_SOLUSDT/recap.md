# Recap — EXPIRED_2026-11-02T0954Z_SOLUSDT
**TL;DR** The scenario set contained a path that paid the target without the entry — and that is the path that happened → no fill, target 5.4% lower.

`SOLUSDT 1h · SHORT LIMIT 96.00 · TP 94.30 (−1.77%) / SL 97.20 (+1.25%) · RR 1.42 · 02T10:12Z→04T10:00Z · P(fill) 0.68 · P(TP|fill) 0.55 · p_BE 0.414`

## Plan / predicted
Sell a retest of the 95.90–96.44 supply shelf (17 of the last 54 hourly highs, nothing above 96.44 in 31h) into the 93.18–96.44 box floor; SL 0.11 above the 54h extreme 97.09. Forecast: probe 96.05 at 21:00Z, then 94.30 → 93.30 → 94.70.

## Why (chart input)
−15.4% flush (109.20→92.34 on 30 Oct 00:23Z) in the market-wide cascade around the Binance hot-wallet disclosure; descending highs 98.59→97.09→96.04→95.95. Both directions were costed; the long at 93.25–93.40 was rejected because its stop sat inside the 92.34–93.18 sweep zone.

## What happened
Window high 94.96 — 1.08% short of the limit — then a breakdown to 89.86 (well through the TP) and an exit at 93.12.

## Right / wrong
Right: box-vs-break framing, TP inside the deliverable range, honest rejection of the long, and an explicit reason for LIMIT over MARKET. Wrong: the folder recorded that a downside break delivers the target without ever touching the entry (P(close<93.18) = 0.38) and yet priced P(fill) 0.68; its own learning node already warned of a 4th no-fill in 17 orders.

## Right trade
Counterfactual, same candles: market short at the 94.14 open reached 94.30 = +0.23%; shorting the 94.96 high into 89.86 paid +5.37%.

## Lesson
1. When a scenario pays the target without touching the entry, price it as its own branch (or move the entry onto the modal path).
2. Base-rate the fill from measured retest frequency; an order whose fill needs the retest the flush destroyed is a bet on the losing branch.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`