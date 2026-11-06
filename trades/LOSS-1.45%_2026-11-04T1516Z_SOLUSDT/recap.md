# Recap — LOSS-1.45%_2026-11-04T1516Z_SOLUSDT
**TL;DR** LOSS · filled four minutes after placement at the top of a +4.8% vertical impulse, i.e. the fill itself was the signal that the move was over.

`SOLUSDT 1h · LONG LIMIT 96.4 · TP 99 (+2.70%) / SL 95 (−1.45%) · RR 1.86 · 04T15:20Z→06T06:00Z · fill 04T15:25Z · stop 04T19:00Z`

## Plan / predicted
Buy the first pullback to 96.40, the level SOL had capped under for five days and reclaimed that afternoon, and ride a continuation to 99.00 with a 1.45% stop. P(TP|fill) was recorded at 0.63-0.66.

## Why (chart input)
A synchronised impulse started ~04T14:29Z (BTC +4.4%, ETH +6.3%, XRP +4.8%, SOL +4.8%): SOL 92.85 → 98.14 in three 15m bars on 6-18x normal volume, closing 97.57 just under its own high. 96.00 had been hard resistance for five days and was reclaimed intraday.

## What happened
Filled 2026-11-04T15:25Z, four minutes after placement, 0.2% under the 97.51 impulse high. MFE only +0.94% (97.31) in the next three hours, then the stop at 95.00 at 19:00Z — 3h35m after the fill. The TP never printed in the remaining 35 hours: the post-stop best was 97.08, and the window ground to 88.24 (−8.46% from entry), closing at 89.34.

## Right / wrong
Right: the level research was sound (96.00 was a five-day ceiling) and the risk was pre-committed. Wrong: buying the first pullback of a one-bar vertical move means the fill is only available because the impulse has stalled. A 1.45% stop sat inside a market whose following 24h range was 9.4%.

## Right trade
Counterfactual from these candles: nothing on the long side worked after 15:25Z; the paid trade was a SHORT of the failed 97.31 retest into 88.24, about +9.3% over the remaining window.

## Lesson
1. When a limit fills within minutes of placement at the extreme of an impulse, treat the fill as adverse selection: prefer MARKET after a hold, or a limit deeper than one ATR below the high, never 0.2%.
2. Stops sized at 1.1-1.5% while the instrument's 24h range is 9% are inside normal noise; this is the fourth journal loss with that shape (ASTER 2026-10-23, XRP 2026-11-03, BTC 2026-11-04).

Evidence: `review.md` `trade.toml` `outcome_candles.csv` `decision_tree.dot`