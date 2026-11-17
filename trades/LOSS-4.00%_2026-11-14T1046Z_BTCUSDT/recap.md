# Recap — LOSS-4.00%_2026-11-14T1046Z_BTCUSDT
**TL;DR** LOSS −4.00% · A commanded ticket, not a signalled one: EV was +0.006% at placement and the stop was hit 7.8h later — the loss is the honest cost of an order written on instruction.

`BTCUSDT 1h · LONG LIMIT 66163.41 · TP 67486.68 (+2.00%) / SL 63516.87 (−4.00%) · RR 0.50 · 14T10:47Z→16T10:46Z · P(fill) 0.63 · P(TP|fill) 0.50`

## Plan / predicted
Buy a 1.7% dip to 66163.41 on the theory that the selloff was over-extended, TP a 2% bounce, SL 4% lower. This ticket was written **because the user ordered a trade**, after every measured candidate that evening had failed its falsification test. The RR 0.50 was set by choosing a 2%/4% box, not by measuring a hit rate first.

## Why (chart input)
No qualifying structure of its own. The underlying measurement was a 47,068-trade simulation across 12 symbols in which **0 of 12 were positive in both sample halves**; BTC was the least-bad at +0.006%, i.e. zero.

## What happened
Filled 14T14:20Z on the way down within a wide one-way leg. MFE after the fill was only **+0.32%** (66373.41); the market then fell to 63326.43, **−4.29%**, and the SL filled at 14T22:10Z, 7.8h after the fill. TP 67486.68 was never touched at any point in the window. Last close 64544.63.

## Right / wrong
Right: nothing in the market read. The one thing done correctly was declaring at placement that the expected value was zero rather than presenting it as an edge. Wrong: everything about the construction — the entry was filled by continuation flow inside the down-leg (the exact adverse-selection pattern named in LOSS-1.50%_2026-10-23T1147Z_ZECUSDT), the stop was 1.0x ATR inside an active leg, and RR 0.50 required a 67% hit rate against a measured 50%.

## Right trade
Counterfactual, same candles: the same window **shorted** at the placement open 67273.89 → 62006.00 = **+7.83%**. The candles paid the opposite side; the chosen side was the crowded one.

## Lesson
1. Geometry must follow a measured hit rate, never the reverse: writing TP 2% / SL 4% to make a ticket look plausible produced a construction needing 67% accuracy from a 50% signal.
2. An instruction to produce a trade is not evidence for one. Record the EV at placement — here +0.006% — so the outcome is scored against what was claimed, not against what happened to occur.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`