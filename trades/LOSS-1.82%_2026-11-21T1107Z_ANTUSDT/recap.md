# Recap — LOSS-1.82%_2026-11-21T1107Z_ANTUSDT
**TL;DR** LOSS-1.82% · Tight −1.82% stop at 89.55 sat 14 cents above Friday's 89.41 triple top after ANT had already defended its $83.00 IPO floor.

`ANTUSDT 15m · SHORT LIMIT 87.95 · TP 86.00 (+2.22%) / SL 89.55 (−1.82%) · RR 1.22 · 2026-11-21T11:07Z→2026-11-23T11:07Z · P(fill) 0.83 · P(TP|fill) 0.87`

## Plan / predicted
Fade the 87.95-88.06 intraday bounce high (`SHORT LIMIT 87.95` from 87.27 spot) targeting a pullback to the 86.00 morning demand zone (`+2.22%`) with SL at 89.55 (`-1.82%`).

## Why (chart input)
On the 15m chart, ANT had fallen from its 111.50 IPO-day spike to 83.22 and appeared capped near 88.00-89.40 over the prior 18 hours.

## What happened
Filled at 87.95 on 2026-11-21T11:30Z, gravitated immediately toward Friday's official $88.91 Nasdaq cash close, and swept SL 89.55 at 2026-11-21T13:35Z before trending up to 93.94 on Nov 23.

## Right / wrong
Reading the 15m chart as a continuation downtrend missed the dominant structural event: on Friday Nov 20, ANT had defended its exact `$83.00` Nasdaq IPO price (`83.05` cash low, `83.22` perp low) and closed cash trading at `$88.91`. Shorting at `87.95` (below Friday's `$88.91` cash close) with SL `89.55` placed just `0.15%` above Friday night's `89.41` triple top invited an immediate weekend cash-close magnet sweep.

## Right trade
Going `LONG` after the `$83.00` IPO floor defense—or triggering `LONG STOP_MARKET` at 89.55 (`TP 93.50`, `SL 87.50`) as price reclaimed Friday's `$88.91` cash close—would have captured `+4.41%`.

## Lesson
1. On equity/IPO perps, never short below the official Friday cash-session settlement (`$88.91`) after an institutional IPO floor (`$83.00`) has just been defended.
2. Never place a short stop (`89.55`) within `0.15%` of an obvious multi-touch liquidity pool (`89.27-89.41`); either pair with a `LONG STOP_MARKET` breakout flip at `89.55` or stand aside.
Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`
