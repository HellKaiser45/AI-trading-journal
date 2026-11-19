# Recap — REJECTED_2026-11-18T0941Z_ZECUSDT
**TL;DR** REJECTED · A +21.5% recovery has no side: the winning direction flips between 24h and 48h, and LONG loses to a random entry on its own days.

`ZECUSDT 15m · NO TRADE · live 947.52 img / 949.06 spot · 18T09:41Z · −37.9% leg · +21.5% bounce · JEV none 0.99`

## Plan / predicted
No ticket. Five candidates went to JEV: LONG MKT 949.06, LONG LIM 935.00, SHORT LIM 973.87, SHORT MKT 949.06, LONG MKT wide 1045.76/873.

## Why (chart input)
1229.00 (10 Nov) → 813.00 (15 Nov) on the image, −37.9% on the candles, then +21.5% off the low with higher lows 846.62 → 873.00 → 907.53 → 916.25 → 944.13. Live sits −4.60% under the 120h high.

## What happened
No position. First-hand, 67,128 Binance 1h bars, current era, 53 independent episodes, day-clustered bootstrap: SHORT lim-1 tp12/sl8 72h **+0.70%** CI [−0.64, +2.24]; SHORT mkt tp8/sl8 **+0.45%** CI [−0.71, +1.74]; LONG mkt tp8/sl8 **−0.47%** CI [−1.72, +0.66]. All CIs cross zero.

## Right / wrong
Right: calling it a repaired recovery, not a flush: `jev_classify` gave `repaired_recovery_chop` 0.98, and the journal's one directional setup (flush ≥20% in 12 bars + volume z ≥ 2) cannot fire at −4.60%. Bounce thresholds were monotone (+0.41/+0.55/+0.53/+0.56/+0.61), so not a knife-edge fit. Wrong: nothing in the read is falsified; the refusal rests on measurement, not forecast.

**Deciding measurement:** the LONG−SHORT gap runs +0.69 (8h), +0.36 (24h), **−0.51 (48h)**, −0.81 (72h), −0.99 (96h). LONG wins intraday, SHORT wins from two days out — the expiry was silently picking the side.

**Declared:** read 1229/813/962/947.52 vs candles 1199.82/801.52/973.87/949.06 — 0.6–1.4% error, shape agrees.

## Right trade
Counterfactual: the SHORT cell (+0.70%) beat both its mirror and its same-day random control, but its CI crosses zero: a hypothesis, not a ticket.

## Lesson
1. Test the horizon before believing the side: a gap crossing zero between 24h and 48h means the expiry picks the direction.
2. A signal losing to a random-hour entry on its own days has no edge: +0.53% vs +1.23%.

Evidence: `research_log.txt` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg`