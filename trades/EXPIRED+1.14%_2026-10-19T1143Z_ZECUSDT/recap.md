# Recap — EXPIRED+1.14%_2026-10-19T1143Z_ZECUSDT
**TL;DR** Direction and levels right, but the down-leg printed 45m *before* the fill → +1.14% drift, no TP.

`ZECUSDT 15m · SHORT LIMIT 1151 · TP 1105 (+4.00%) / SL 1172 (−1.82%) · RR 2.19 · 19T12:26Z→20T12:00Z · P(fill) 0.65 · P(TP|fill) 0.61–0.66`

## Plan / predicted
Sell the retest of the broken 1158.77–1160.27 neckline into the 0.618 fib 1103.64; SL above neckline + 50d MA 1163.29 + 1170.65 high. Forecast: min 1104.3, end 1106.4.

## Why (chart input)
Lower highs 1174.09→1160.99→1153.30→1138.20 after a +12.7% V-reversal stalled, six-touch support 1120.32–1127.56, distribution shelf 1186/1175/1167. Research: ZEC 30d −25.7%, ZEC-BTC 48h corr 0.83.

## What happened
Low 1110.79 at 14:00Z, **45 min before** the 14:45Z fill. Post-fill MFE only +3.18% (high 1114.4), then 1171.81 at 22:15Z — 0.19 under the stop (MAE −1.81%); expiry close 1137.87.

## Right / wrong
Right: level map, direction, stop clearing the window high by 0.19 — but that clearance is luck, not skill. Wrong: the 4% target needed a second leg the market never mounted; the banked +1.14% was drift.

## Right trade
Counterfactual, same candles: long 1110.79→1171.81 (+5.49%, 14:00Z→22:15Z); a short initiated on the 22:15Z rejection ran +4.53% to 1120 by 01:15Z.

## Lesson
1. Sequence gate: if the favourable extreme predates the fill, reprice P(TP|fill) far below the unconditional touch probability (realised TP-first = 0).
2. Target the deliverable (1112–1115), not a fib sitting 0.5% past the printed low.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`