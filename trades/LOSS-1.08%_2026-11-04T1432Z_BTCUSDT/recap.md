# Recap — LOSS-1.08%_2026-11-04T1432Z_BTCUSDT
**TL;DR** LOSS · the limit filled 25h after placement inside the roll-over from the 81188 impulse high, and the favourable extreme had already printed the previous day.

`BTCUSDT 1h · LONG LIMIT 78900 · TP 79850 (+1.20%) / SL 78050 (−1.08%) · RR 1.12 · 04T14:50Z→06T06:00Z · fill 05T14:40Z · stop 05T14:55Z`

## Plan / predicted
Buy the pullback into 78900 for a 1.2% bounce to 79850, stopping 1.08% below. The thesis assumed the impulse off 04T15:15Z would hold its break and that 78900 was a defended shelf.

## Why (chart input)
Price had run to 81188 (+2.90% over the fill) on 2026-11-04T15:15Z, then spent 23 hours drifting down. 78900 was chosen from the prior consolidation, 2.8% under that high.

## What happened
Filled 2026-11-05T14:40Z on the way down, not on a tested hold; MFE +0.25% (79097.50); stopped at 78050 fifteen minutes later. Price never returned: the post-stop maximum was 78591.80, the window low 75158 (−4.74% from entry), and the TP was still 1.7% above the best print after the stop. The whole 39h window ended at 75629.

## Right / wrong
Right: bounded, pre-committed risk and a fill exactly at the level. Wrong: the favourable extreme (81188) was 23 hours older than the fill — the same sequence-gate defect as ZECUSDT 2026-10-19 — and a limit sitting 2.8% under a freshly printed impulse high was always going to be filled by the unwind, not by a retest. The 1.08% stop was also tighter than the 5-minute noise of that unwind.

## Right trade
Counterfactual from these candles: a SHORT at the 2026-11-05T12:30Z roll-over (78900 area) into the 75158 low paid about +4.7% in 17 hours — the mirror of this ticket.

## Lesson
1. Check the age of the favourable extreme: if the impulse high predates the fill by more than a few hours, P(TP|fill) collapses (here the TP never printed in the 15h that followed the stop).
2. A stop of 1.08% (about the 5-minute range of a BTC unwind) is inside the leg; either widen it past the swing or do not take the pullback trade.

Evidence: `review.md` `trade.toml` `outcome_candles.csv` `decision_tree.dot`