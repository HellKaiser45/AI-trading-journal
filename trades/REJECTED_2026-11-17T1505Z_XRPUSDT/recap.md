# Recap — REJECTED_2026-11-17T1505Z_XRPUSDT
**TL;DR** REJECTED · "Bounce to the top of the range after a decline" is a volatility state, not a direction: SHORT loses in the current era, LONG in the previous one.

`XRPUSDT 1h · NO TRADE · spot 0.9771 · 17T15:05Z · pos 0.976 of 20-bar range · dd 8d −12.37% · SHORT E3 −0.193% · LONG E3 +0.453% but E2 −0.470%`

## Plan / predicted
Considered SHORT LIMIT 0.9793 (20-bar high), TP 2 ATR below, SL 3 ATR above, 24h, betting the bounce fails. Also tested LONG there, LONG market, SHORT with a 1-ATR target. No position.

## Why (chart input)
1.2100 → 0.8977 (−25.8%) in seven sessions, then +8.8% to 0.9771 — position 0.976 of the 20-bar range, still −12.37% under the 8-day high. Relief rally into a downtrend.

## What happened
No position. Pooled 14 symbols, 1h, n=1922 at the −15% gate: SHORT at the range high is negative in E3 2024-26 at all five geometries (−0.154 to −0.314); LONG is positive there (+0.257 to +0.453) and negative in E2.

## Right / wrong
Right: the drawdown is real. Wrong: the gate flips sign between −10% (+0.164) and −15% (−0.193), live at −12.37% inside the flip. SHORT excess over a matched control is +0.027 there; LONG excess is −0.044, ahead on 7 of 14 symbols. The one state with a real direction — flush ≥20% plus 8–15% bounce plus volume z ≥ 2, CI [+0.50, +22.10] — does not fire: 4h drawdown −0.07%, z −0.65.

**Violation, disclosed:** after `finalize.py` renamed this folder at 16:09Z I regenerated the SVGs and `graphpoints.csv` at 16:13Z to fix a layout defect. Terminal folders are frozen. Numbers unchanged, rule broken.

## Right trade
Counterfactual: no candidate is positive on both requirements. The honest one is the flush-plus-volume setup behind the UNI and XMR tickets — absent here.

## Lesson
1. A gate that flips sign inside the live reading is a noise band. −10% paid +0.164, −15% paid −0.193, live −12.37%. Require monotonicity first.
2. Shallow gates made SHORT look positive and deep gates made LONG look positive, on the same bars. When both sides win on an arbitrary cut, there is no direction.

Evidence: `research_log.txt` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg`