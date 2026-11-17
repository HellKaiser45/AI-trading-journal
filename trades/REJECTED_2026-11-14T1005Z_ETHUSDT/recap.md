# Recap — REJECTED_2026-11-14T1005Z_ETHUSDT
**TL;DR** REJECTED · A drawdown filter that moves LONG and SHORT equally is beta, not signal — run the unconditional control.

`ETHUSDT 1h · NO TRADE · spot 1909.06 · 2026-11-14T10:05Z · SHORT EV +0.279% in-sample vs −0.001% on 9y daily · P(bounce from 1878) 0.41`

## Plan / predicted
Considered SHORT at market 1909.06, TP 1851 / SL 1945, 48h expiry, on a −24.4% drawdown and five weeks of lower highs. Also tested the mirror LONG limit 1878 at the Aug base, TP 1929 / SL 1845.

## Why (chart input)
ETH fell 2806.76 → 1878.00, and 1862-1918 was the two-week Aug-2026 base that launched the rally. Spot sits 1.7% above that low, below a broken 2052-2116 shelf, lower highs at 2436-2450 → 2237-2253 → 2052-2116. Clean-looking continuation short.

## What happened
No position, so no outcome. On 60,000 independent 1h bars the SHORT at TP3.0/SL3.0 does win in drawdown: n=3238, EV +0.279%, WR 54.4% vs 50.0% needed, 5/5 symbols. But the **same trade unconditionally** gives +0.115%, and the mirror LONG is −0.281% conditional vs −0.115% unconditional — the filter shifts both sides ±0.165. On 9y daily the rule returns +0.394 / −0.360 / −0.053 / −0.001 across four eras; three negative or flat.

## Right / wrong
Right: the 1h result was real *inside that sample*. Wrong: I nearly sold it as an edge. It was beta — shorting a falling market in a falling year (BTC −37.4%, SOL −49.0%, XRP −54.5%). Geometry cannot rescue it either: no TP/SL pair is positive for both sides (TP1.5/SL3.0 → −0.016/−0.001; TP2.0/SL6.0 → −0.040/+0.033).

## Right trade
Counterfactual, not a result: SHORT 1909.06 / TP 1851 / SL 1945 = +0.279% on 1h, −0.001% on the 9y daily equivalent. Nothing durable. The correct action was none.

## Lesson
1. **Run the unconditional control.** A filter moving both sides equally is beta. Require conditional − unconditional > 0 *and* era stability.
2. **Exits do not create edge.** 15 TP/SL pairs over 60,000 independent bars all scored ~0.00 both ways.

Evidence: `research_log.txt` `decision_tree.dot` `graphpoints.csv` `chart.svg` `chart_prediction.svg`