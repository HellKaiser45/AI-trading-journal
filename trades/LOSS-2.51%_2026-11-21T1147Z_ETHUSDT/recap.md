# Recap — LOSS-2.51%_2026-11-21T1147Z_ETHUSDT
**TL;DR** LOSS-2.51% · 4th correlated Saturday SHORT LIMIT at 1670.00 stepped in front of an accelerating LTF V-bounce (+7.6% off 1535.54) and hit SL 1712.00 in 60m.

`ETHUSDT 1h · SHORT LIMIT 1670.00 · TP 1615.00 (+3.29%) / SL 1712.00 (−2.51%) · RR 1.31 · 2026-11-21T11:47Z→2026-11-23T11:47Z · P(fill) 0.56 · P(TP|fill) 0.89`

## Plan / predicted
Fade the Saturday V-bounce at the 48h VWAP (`SHORT LIMIT 1670.00` from 1653.29 spot) targeting a pullback to the 12h VWAP at 1615.00 (`+3.29%`) with SL at 1712.00 (`-2.51%`, above the 1699.30 72h VWAP).

## Why (chart input)
ETH had broken its 1,732-1,843 6-day shelf to flush to 1,535.54 at 05:00Z and was rebounding sharply into the 1,670-1,675 48h VWAP zone.

## What happened
Filled at 1670.00 on 2026-11-21T12:35Z during the `$400M+` Saturday short-covering squeeze and blasted straight through SL 1712.00 60 minutes later at 13:35Z (simultaneously with BNB and ANT), subsequently rallying to 1751.65 on Nov 23.

## Right / wrong
At placement (`11:47Z`), `LTF` had already surged `+7.67%` off the `1535.54` 05:00Z capitulation low without a single 1h lower low. Adding a 4th correlated `SHORT LIMIT` into an accelerating `LTF` V-bounce turned one macro short-covering wave (`12:35-13:35Z`) into four simultaneous stop-outs.

## Right trade
Placing a `SHORT STOP_MARKET` below the `LTF` higher-low pivot (`1635.00`) would have never triggered (`0.00%` loss), while a `LONG STOP_MARKET` flip at 1712.00 (`TP 1750.00`) would have recovered `+2.22%`.

## Lesson
1. Enforce `Lever #3`: when `LTF` is actively ripping (`> +1.5%`) against `HTF` after a capitulation wick, never step in front of the bounce with a passive `SHORT LIMIT`; require a `SHORT STOP_MARKET` breakdown below the `LTF` pivot.
2. Enforce portfolio anti-correlation hygiene: never hold 4 unhedged same-direction tickets (`BNB`, `HYPE`, `ANT`, `ETH`) at the same time.
Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`
