# Recap — LOSS-1.50%_2026-10-23T1147Z_ZECUSDT
**TL;DR** The canonical adverse-selection case: the limit was filled by the very sellers the thesis was betting against, and the stop came 5 minutes later.

`ZECUSDT 1h · LONG LIMIT 1203 · TP 1242 (+3.24%) / SL 1185 (−1.50%) · RR 2.17 · 23T12:45Z→24T06:00Z · P(fill) 0.44–0.61 · pooled P(TP|fill) 0.57 · p_BE 0.316`

## Plan / predicted
Buy the 1203 retest of 1187.5–1245 box support after a −13.2% flush and an 11:00Z sweep to 1198.62 that V-reversed; TP the tested 1235–1245 ask wall. Stop 18 points = 0.85× the 1h ATR of 22.22. Forecast: wall fade, dip to 1203 ~15:00Z, rotation to 1242 ~23:00Z.

## Why (chart input)
21 hours of 1187.5–1245 balance after the flush from 1368.4. Research: the 11:00Z sweep was an idiosyncratic stop-run ($88K of 4h liquidations), PMI priced small, ZEC median 3h range on PMI days 3.7% (Jev 0.81) — i.e. both box edges reachable.

## What happened
Filled 22:30Z inside a fresh down-leg, not on a retest-and-hold; stopped at 1185 five minutes later (22:35Z). MFE +1.18%. The window high 1258.13 had printed **before** the fill; price then fell to 1158.22 and exited 1167.2.

## Right / wrong
Right: box framing (both edges were indeed reachable), bounded risk, and a short candidate rejected on a stated reason. Wrong: a support level reached during a fast one-way bar is filled by continuation flow — the fill itself was information that the box was breaking; a 0.85-ATR stop under a level being sold was inside the leg's reach.

## Right trade
Counterfactual, same candles: the short — selling the 14:00Z high 1258.13 into 1158.22 = +7.94%; the long was buying the second half of a rotation that had already turned.

## Lesson
1. Check the fill's context: a wide one-way candle that fills a limit is adverse selection, not a bargain — require the bounce to print (higher limit or MARKET after confirmation).
2. Stops under 1× ATR inside an actively sold level sit inside the leg; structure plus ≥1× ATR is the floor, not a target.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`