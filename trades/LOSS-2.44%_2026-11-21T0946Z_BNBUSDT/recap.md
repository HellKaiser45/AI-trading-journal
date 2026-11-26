# Recap — LOSS-2.44%_2026-11-21T0946Z_BNBUSDT
**TL;DR** LOSS-2.44% · Passive SHORT LIMIT at 532.00 stepped in front of an accelerating Saturday post-capitulation V-bounce with SL 545.00 below the 48h VWAP.

`BNBUSDT 1h · SHORT LIMIT 532.00 · TP 517.80 (+2.67%) / SL 545.00 (−2.44%) · RR 1.09 · 2026-11-21T09:46Z→2026-11-23T09:46Z · P(fill) 0.58 · P(TP|fill) 0.64`

## Plan / predicted
Fade the Saturday morning rebound at the 24h VWAP (`SHORT LIMIT 532.00` from 526.16 spot) targeting a pullback to the 12h VWAP at 517.80 (`+2.67%`) with SL at 545.00 (`-2.44%`).

## Why (chart input)
BNB had broken below its 572-595 multi-day shelf to 503.60 and was rebounding toward its 24h VWAP (`532.69`) inside a broad HTF downtrend.

## What happened
Price dipped only to 522.88 at 10:10Z (unfilled), then squeezed through 532.00 at 2026-11-21T11:30Z (`LTF` post-liquidation short squeeze), never pulled back below 531.50, and hit SL 545.00 at 13:35Z on its way to 563.57 on Nov 23.

## Right / wrong
While the HTF trend was down, `04:00-07:00Z` had just completed a `$2.4B` long-liquidation flush (`503.60` low) that flipped funding negative and ignited a `$400M+` weekend short-covering wave. Stepping in front of an expanding `LTF` V-bounce with a passive `SHORT LIMIT`—and placing SL (`545.00`) *below* the `48h VWAP (546.99)`—guaranteed an early stop-out.

## Right trade
Using a `SHORT STOP_MARKET` below the `LTF` higher-low pivot (`522.00`) would have stayed 100% unfilled (`0.00%` loss) as the squeeze continued, or pairing the fade with a `LONG STOP_MARKET` flip at 545.00 (`TP 562.00`) would have captured `+3.12%`.

## Lesson
1. When `LTF` is actively expanding upward after a major liquidation climax, never step in front of it with a passive `SHORT LIMIT`; use a `SHORT STOP_MARKET` below the `LTF` pivot so you only enter if the bounce actually breaks down (`Lever #3`).
2. Never place a short stop (`545.00`) below the `48h-72h VWAP` (`546.99`).
Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`
