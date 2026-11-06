# Recap — REJECTED_2026-11-06T0958Z_ZECUSDT
**TL;DR** REJECTED · mid-range 1278 in a 1212-1351 box at 2.29% hourly ATR; each ticket cleared break-even on judgment alone, not on this instrument's path base rates.

`ZECUSDT 1h · no order · SHORT 1312/1275/1362 p_BE 0.575 · SHORT 1305/1275/1352 p_BE 0.610 · LONG 1258/1305/1222 p_BE 0.434`

## Plan / predicted
No position. Forecast (contested; rows 240-287): dip to ~1259, probe 1300-1310 into the 1330-1334 shelf, rejection, fade to 1265-1280, end ~1275.

## Why (chart input)
Price sat at 51% of a 1212-1351 range after the 09:00Z bar spiked to 1298.11 and closed 1283.08. The 1330-1334 band had rejected three times in 30h while lows rose 1212.83 → 1221.48 → 1248.13 in 16h: a compressing box, not a trend. ATR(14) 29.4 = 2.29%: the 1305 entry was 0.92 ATR above spot with a 1.57-ATR stop; the 1258 long needed a 0.68-ATR pullback and a 1.25-ATR stop.

## What happened
No order, so no path to score. The call rested on whole-ticket economics: conditional hit rates (0.66-0.71 short, 0.50 long) put all three 0.07-0.11 above break-even, but re-sampling this instrument's 239 bars gave conditional TP 0.44-0.55 vs p_BE 0.434-0.610; the agreeing subsample had n=7. P(positive EV) 0.25-0.27, P(placing beats none) 0.49, P(a full stake is justified) 0.07, P(reject more defensible) 0.90.

## Right / wrong
Untested. The process refused an edge visible in one of two evidence sources only, and refused to shrink a strong level thesis (1330 shelf, trapped longs) into a mid-range entry 25-34 points below it.

## Right trade
Not computable: a rejection has no fill, MFE or MAE. The supported expression was 1330-1334 with the stop above 1352 — 0.41-0.55 fill odds, one no-fill precedent.

## Lesson
1. At ATR 2.3%/h a limit needing 1.6-2.7% cannot have a stop beyond the overshoot envelope and a reachable target; check that first — every geometry here sat within ±0.11 of break-even.
2. Put the thesis's own level into the entry: the 2026-10-28 ZEC short at 1332 and today's 1305 both sold below the shelf that motivated them. Express the shelf or skip it.

Evidence: `decision_tree.dot` `research_log.txt` `graphpoints.csv` `chart_prediction.svg`