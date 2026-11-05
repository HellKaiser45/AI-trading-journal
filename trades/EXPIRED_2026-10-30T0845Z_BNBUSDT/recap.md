# Recap — EXPIRED_2026-10-30T0845Z_BNBUSDT
**TL;DR** Clean analysis and the journal's best stop-widening logic, but the entry sat on the least likely branch of its own scenario set → no fill 0.75% away.

`BNBUSDT 1h · SHORT LIMIT 716 · TP 694 (−3.07%) / SL 734 (+2.51%) · RR 1.22 · 30T09:01Z→31T02:00Z · P(fill) 0.56 · P(TP|fill) 0.80 · p_BE 0.45`

## Plan / predicted
Sell the lower third of the 715–722 supply that had rejected three times (719.94/720.00/722.08) after the 744.90→680.00 liquidation hour; TP inside the 692–698 cluster; SL 1.0% (≈1.2× hourly ATR) above the 726.84 rebound high. Forecast: afternoon push into 715–718, then fade to 693.5.

## Why (chart input)
137,383 BNB sold in the 29 Oct hour during the Binance security incident (statement 30T02:23Z, withdrawals guided to resume within 48h); the bounce to 722.08 was rejected three times with volume decayed to 14–31k BNB/h (no absorption). Research raised the downside-continuation weight from 0.02 to 0.22.

## What happened
Window high 710.62 — 0.75% short of the limit, so 715–722 was never retested; price drifted to 693.4 (0.6 through the TP) and exited 706.47. The chosen scenario was `base_chop 690–722` at 0.42 with "pop then fade" only 0.09.

## Right / wrong
Right: direction, target level, stop that was never in play, and the 17h expiry capped for headline risk. Wrong: the order was written at the top of a band the modal path did not reach — incoherent with the scenario work.

## Right trade
Counterfactual, same candles: market short at the 704.98 open reaches 694 = +1.56%; shorting the 710.62 print into 693.4 paid +2.43%.

## Lesson
1. Put the entry inside the modal path's *dense* band (here 690–712), not at the edge of the plausible range: 716 vs 712 is 0.6% of price and the difference between a trade and none.
2. Derive P(fill) from measured touch frequency — three rejections did not imply a return.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`