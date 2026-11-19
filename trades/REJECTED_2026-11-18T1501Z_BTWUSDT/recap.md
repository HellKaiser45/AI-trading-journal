# Recap — REJECTED_2026-11-18T1501Z_BTWUSDT
**TL;DR** Rejected · a real edge exists on clean Aster crypto, but the only live signals failed out-of-sample or already sit in the journal.

`BTWUSDT 1h · LONG (no ticket) · never placed · P(fill) n/a · P(TP|fill) n/a`

## Plan / predicted
No ticket. Intent: sweep all 647 Aster perps, trade only what survives measurement on
Aster's own bars. The candidate in `chart_prediction.svg` is BTWUSDT LONG 0.481202 / TP
0.550141 / SL 0.426051 at tp2.5/sl2.0 ATR — for audit, never placed.

## Why (chart input)
No image supplied, so stage 1 was unavailable and JEV chose the cohort-split data path at
0.99. Structure came from Aster klines: BTW sat −49.7% under its 120h high after a 43.6%
bounce off the 48h low, ATR 5.6%/h.

## What happened
No fill, no outcome. The measurement is the event. The first sweep found nothing (crypto
oversold_reclaim +0.22%, CI [−0.78,+0.65]). Cause: dead bars — median 45.9% of stock-perp
bars are flat, 34.2% zero-volume, versus 25.2%/14.0% for crypto. On the 36 symbols with ≤5%
dead bars the same hypothesis returned +1.58% EV/ticket over 237 events, 18/25 positive, all
16 geometry cells positive.

## Right / wrong
Right: refusing BTW. Era-late EV negative at every geometry (−1.65% to −2.15%), top-5 bid
$424, already rejected as non-generic on Binance. Right: refusing LIT, already PENDING and
both-era positive only at tp2.5/sl2.5.
Wrong, caught by the holdout: I first wanted the highest-EV cell tp3.0/sl1.5 (+2.55%
in-sample). On the untouched second half it returned +0.36%.

## Right trade
Counterfactual, not a result: pre-specified tp2.5/sl2.0 held +1.69% on H1 and +1.32% on H2
(8/16 symbols), CI still crossing zero over 21 weeks. Correct action is none today plus a
standing watch on clean-eligible crypto.

## Lesson
1. Filter bars before testing signals. 138 of 174 symbols were disqualified by dead bars;
   including them turned +1.58% into +0.22% and buried the edge.
2. Fix geometry before seeing the evaluation window, or the holdout lies: +2.55% in-sample
   became +0.36% out-of-sample on the same data.
Evidence: `research_log.txt` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg`