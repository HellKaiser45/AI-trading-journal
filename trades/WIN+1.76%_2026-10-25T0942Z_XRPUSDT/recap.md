# Recap — WIN+1.76%_2026-10-25T0942Z_XRPUSDT
**TL;DR** A process win, not a lucky one: the stop was moved out of structure three times and the market never came within 1.0% of it.

`XRPUSDT 1h · SHORT LIMIT 1.3040 · TP 1.2810 (−1.76%) / SL 1.3245 (+1.57%) · RR 1.12 · 25T10:03Z→26T21:00Z · P(fill) 0.71 · P(TP|fill) 0.69 · p_BE 0.4712`

## Plan / predicted
Sell the retest of the chop highs after a 42% bounce; entry at the measured 1.3024/1.3042/1.3026 highs just under the 4h SMA20 1.3043, TP at the top of the Oct 23–24 shelf above the daily SMA200 1.2788, SL above the Oct 23 high 1.3238. Forecast: drift to 1.3040 into 14:00Z, decline to ~1.2810 by 26T04:00Z.

## Why (chart input)
−10.3% (1.3985→1.2544) then a +4.8% bounce to 1.3149/1.3154 (42% of the drop) and six hours of 1.2886–1.3136 chop. Research: funding +0.010%/8h, OI −4.0% in 47h, 75.3% of accounts long, 1h taker ratio 0.9314, and a base-rate study (67.8% vs a 51.3% control) that explicitly gave no directional edge and was not used as evidence.

## What happened
Filled 16:55Z after 6.9h on a normal retest. MAE only −0.53% (high 1.3109, 1.0% under the stop), MFE +2.35%; TP hit 26T02:40Z, 9.8h after the fill; exit 1.2899.

## Right / wrong
Right: the stop was moved 1.3170 (rejected, too near the 1.3150 session high) → 1.3235 (rejected, inside the Oct 23 high 1.3238) → 1.3245; the market never tested it. Wrong: nothing material — but RR 1.12 is thin, so the trade needed its conditional to be right (p_BE 0.47 vs 0.69 estimated).

## Right trade
Essentially the trade taken: the window's best short was 1.3109→1.2733 = +2.87% vs 1.76% banked.

## Lesson
1. Stop beyond measured structure beats RR aesthetics: this folder is the deliberate fix of LOSS-1.30%_2026-10-19T1533Z_XRPUSDT, where a 1.30% stop was squeezed out.
2. Use same-symbol history on *parameters*, not on side — and a contested chart is tradeable when entry, stop and target are each measured.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`