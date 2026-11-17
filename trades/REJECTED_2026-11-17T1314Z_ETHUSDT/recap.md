# Recap — REJECTED_2026-11-17T1314Z_ETHUSDT
**TL;DR** REJECTED · The only state measuring positive on ETH 4h is contradicted by its own daily mirror, and it does not fire on the live bar anyway.

`ETHUSDT 4h · NO TRADE · spot 1820.58 · 2026-11-17T13:14Z · boxpos 54.0% vs 66% threshold · best SHORT EV +0.373% CI [-0.191,+1.023]`

## Plan / predicted
Considered a SHORT on strength — close in the top third of the 20-bar range, limit +0.5 ATR, TP 4.0 ATR / SL 2.0 ATR, 72h hold — and, as the chart's own read, a SHORT of the failed bounce off a higher low after a deep drawdown. Also tested the daily LONG mirror of the same idea.

## Why (chart input)
ETH fell 2796 → 1736 (−37.9%) over five weeks, bounced +9.1%, and stalled at 1820 in the lower half of a 9.13%-tall 72h box (1710.01-1866.21). The 72h envelope is symmetric (p90 +9.61% up / −10.53% down), so there was no excursion asymmetry to harvest either way.

## What happened
No position, so no outcome. The measurements: the chart's own read (dd + higher low + reclaim) gives SHORT +0.771% on the 13-symbol 4h panel but **−0.341% on ETH alone** and **+1.561% on the ETH daily series** — the sign flips between timeframes. The short-on-strength variant gives ETH EV +0.373%/ticket over 1227 fills with a positive era delta in 3 of 3 (+0.599/+0.103/+0.574) and beats its mirror by 0.842pp, but its month-block CI is **[−0.191,+1.023]** and the same idea on daily bars is **LONG, 11/12 symbols positive**.

## Right / wrong
Right: the state is not pure beta — it beats the unconditional control by +0.306pp on every era and the mirror side loses. Wrong: I went looking for a ticker and found a screen, not a signal. 336 configurations were tested and 72 passed a two-era filter, a 21.4% pass rate against ~25% expected under a pure null. The two timeframes of one instrument give opposite answers, and the live bar does not satisfy the state that produced the only positive number.

## Right trade
Counterfactual, not a result: SHORT limit 1841.23 (close +0.5 ATR) / TP 1693.59 / SL 1915.05, RR 2.00, would have been the ticket had the state been live and the daily mirror agreed. It is not placed, and the measured edge does not separate from zero.

## Lesson
1. **A state must agree with itself across timeframes.** 4h SHORT +0.373% versus 1d LONG +0.592% on the same instrument is a contradiction, not two edges — with no tiebreak, take neither.
2. **Check the bar, not just the condition.** The state was measured on 1227 historical fills and fails on the one bar available to trade. Require the measured state at placement, or the ticket is untested by construction.

Evidence: `research_log.txt` `decision_tree.dot` `graphpoints.csv` `chart.svg` `chart_prediction.svg`