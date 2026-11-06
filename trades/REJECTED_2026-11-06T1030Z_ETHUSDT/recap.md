# Recap — REJECTED_2026-11-06T1030Z_ETHUSDT
**TL;DR** REJECTED · mid-coil 2242 in a 3.59% coil after −9.96%; every ticket sat within ±0.01 of break-even on this instrument's own paths, with a >2%-class release 2h45m later.

`ETHUSDT 1h · no order · SHORT 2247/TP 2206/SL 2291 p_BE 0.518 · LONG 2228/TP 2286/SL 2200-2168 p_BE 0.326-0.510 · decided 06T10:45Z`

## Plan / predicted
No position. Forecast (contested, 36 rows to 11-07T22:00Z): hold 2225-2246 into the 13:30Z release, dip to 2207-2213 testing 2205.67 without breaking, bounce 2228, fade, end ~2226 — the "neither edge" branch, with the 0.34-vs-0.26 downside tilt.

## Why (chart input)
A +10.1% impulse to 2449.70 (11-04T15:00Z) then −9.96% to 2205.67 (11-05T23:00Z), then 19 hours inside 2205.67-2286.09: descending highs 2286.09→2246.23, rising lows 2205.67→2213.30, last 6 bars 1.47%, ATR 1.09%/h. The 2240-2249 cap was touched in 11 of 19 bars; 2205.67 once. The envelope below runs to 2173.78.

## What happened
No order, so no fill, MFE or MAE. Jev: first touch down 0.34 / up 0.26 / neither 0.40; cap rejects 0.75; the short was the weaker side (0.80), own-path EV ≈ −0.35% per order; the long's was +0.16 to +0.29% against an SE near 0.6pp over ~5 independent windows, with 0.04 that the margin justified the stake and 0.31/0.22 that placing beat no order.

## Right / wrong
Untested. The process refused a ticket that existed only as a positive point estimate, and refused to buy the coil floor with a stop 0.23 ATR below it — the geometry of LOSS-1.41% (ETH, 24h earlier) and LOSS-1.01% ASTER.

## Right trade
Not computable. The structure-honest expressions (2246-2249 with a stop above 2286.09, or a 2168-buffered long) were both RR ≈ 1 into a modal "neither" outcome.

## Lesson
1. When both edges of a 3.6% coil land within ±0.01 of break-even, the geometry, not the side, is the problem: require a stop beyond the envelope and a target beyond the coil before pricing a ticket.
2. Check scheduled releases before pricing levels, not before choosing a side: 13:30Z was 2h45m out and inside every horizon (LOSS-0.72% BTC, 10-29).
Evidence: `decision_tree.dot` `research_log.txt` `graphpoints.csv` `chart_prediction.svg`