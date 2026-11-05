# Recap — EXPIRED+1.73%_2026-10-26T0903Z_UNIUSDT
**TL;DR** Structural stop held by 0.19% and direction was right, but the target zone had already traded before the fill → +1.73% drift.

`UNIUSDT 1h · SHORT LIMIT 7.125 · TP 6.96 (−2.32%) / SL 7.225 (+1.40%) · RR 1.65 · 26T09:20Z→27T09:30Z · P(fill) 0.41 · P(TP|fill) 0.66 · p_BE 0.377`

## Plan / predicted
Sell the retest of the reclaimed-then-rejected 7.05–7.20 shelf; entry = 7.118 swing high + 0.786 fib 7.1296, SL behind 7.1854/7.1961, TP inside the 6.96–6.99 shelf. Forecast: 6.95 at expiry.

## Why (chart input)
V-recovery from 6.5201 topped 7.1182 just under the 0.786 fib and rolled back to 6.9964/6.9994 + 0.618 fib. Research: move was UNI-specific (+2.07% vs BTC +0.13%), spot-led short-covering, squeeze fuel 6.99–7.11 already consumed (Jev 0.83).

## What happened
Window low 6.932 at 13:25Z — **1h35m before** the 15:00Z fill. Post-fill low 6.9953 (MFE +1.82%), high 7.211 at 27T00:35Z (MAE −1.21%, stop 0.19% clear), expiry 7.002.

## Right / wrong
Right: the structural stop (7.225 vs the 7.211 print) and an honestly priced P(fill) = 0.41. Wrong: entry 1.68% above spot, and the 6.96 zone had already printed, so the ticket's payoff was empty at fill.

## Right trade
Counterfactual, same candles: long 6.932→7.211 (+4.02%, 13:25Z→27T00:35Z) was the window's pay.

## Lesson
1. Adverse selection is measurable: record the time of the favourable extreme already printed vs the fill assumption (here 1h35m earlier, TP-first realised 0 vs 0.66 estimated).
2. Distance-to-entry filters which trades you get — 1.68% above spot was enough to arrive after the move.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`