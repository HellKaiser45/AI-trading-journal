# Recap — LOSS-1.26%_2026-11-20T1007Z_XRPUSDT
**TL;DR** LOSS-1.26% · Counter-trend LONG LIMIT at 0.9500 suffered classic sequence & falling-knife adverse selection after the 0.9678 high printed pre-fill.

`XRPUSDT 4h · LONG LIMIT 0.9500 · TP 0.9685 (+1.95%) / SL 0.9380 (−1.26%) · RR 1.54 · 2026-11-20T10:07Z→2026-11-22T10:07Z · P(fill) 0.72 · P(TP|fill) 0.56`

## Plan / predicted
Bid the 0.9480-0.9520 5-day support shelf (`LONG LIMIT 0.9500` from 0.9599 spot) targeting a mean-reversion bounce to the 0.9685 72h VWAP (`+1.95%`) with SL at 0.9380 (`-1.26%`).

## Why (chart input)
XRP appeared to be defending a 5-day horizontal base at 0.945-0.952 after its drop from 1.32 to 0.912, with three prior reactions off 0.948.

## What happened
Before the limit order filled, XRP peaked at 0.9678 at 2026-11-20T10:40Z (`0.07%` below our 0.9685 TP target) and rolled over. It filled 0.9500 on the way down at 12:00Z (`t_extreme < t_fill`), saw virtually zero bounce, and hit SL 0.9380 85 minutes later at 13:25Z before flushing to 0.8594 on Nov 21.

## Right / wrong
Bidding a counter-trend horizontal floor in a macro 4H downtrend (`HTF_ret = -36%`) with a tight `-1.26%` stop violated both the Sequence Gate (`t_extreme < t_fill`) and the Falling-Knife Filter (`Lever #1`).

## Right trade
Flipping the fragile 0.9480-0.9500 support shelf into a breakdown `SHORT STOP_MARKET` at 0.9450 (`TP 0.9100`, `SL 0.9680`) would have captured `+3.70%` on the flush to 0.8594.

## Lesson
1. Never leave a counter-trend `LONG LIMIT` resting at a multi-touch floor in an HTF downtrend after the bounce target (`0.9678`) has already been tagged and rejected (`t_extreme < t_fill`).
2. Repeatedly tested support floors in HTF downtrends are breakdown triggers (`SHORT STOP_MARKET`), not passive buy zones.
Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`
