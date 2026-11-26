# Recap — EXPIRED_2026-11-22T1100Z_UNIUSDT
**TL;DR** EXPIRED · Downside SHORT STOP_MARKET @ 4.55 never triggered (window low 4.6300) as UNIUSDT broke upward to 5.3040, costing 0.00% while the paired LONG won +5.01%.

`UNIUSDT 1h · SHORT STOP_MARKET 4.55 · TP 4.30 (+5.49%) / SL 4.75 (−4.40%) · RR 1.25 · 2026-11-22T11:00Z→2026-11-24T11:00Z · P(fill) 0.42 · P(TP|fill) 0.58`

## Plan / predicted
Downside bracket leg of the `UNIUSDT` coil (`4.556–4.784`): trigger short only on a breakdown below the `4.556` 22h consolidation floor (`SHORT STOP_MARKET @ 4.55`), targeting `4.30` (`+5.49%`) with `SL` at `4.75` (`-4.40%`).

## Why (chart input)
With `UNIUSDT` at `4.720` after a weekend short-covering bounce where coin-denominated OI fell `-2.75%`, a rollover below `4.556` would have signaled squeeze exhaustion toward `4.25–4.30`.

## What happened
Price never broke the `4.556` coil floor: the 48h window low was `4.6300` at `23T02:40Z` (`1.76%` above the `4.55` trigger). Buyers broke upward through `4.79` at `23T03:20Z` and rallied to `5.3040` (`23T14:25Z`), banking `+5.01%` on the paired `LONG STOP_MARKET @ 4.79` while this downside `STOP_MARKET` expired untouched at `0.00%`.

## Right / wrong
Right: using a `SHORT STOP_MARKET` trigger below support (`4.55`) instead of a passive `SHORT LIMIT` above spot (`4.75–4.80`) defeated adverse selection—when `UNIUSDT` surged to `5.3040`, a passive `SHORT LIMIT` would have stopped out, whereas the `SHORT STOP_MARKET` stayed unfilled (`0.00%` loss).

## Right trade
Keeping the downside leg as a `STOP_MARKET @ 4.55` while the upside `LONG STOP_MARKET @ 4.79` captured `+5.01%` was optimal for an upside breakout.

## Lesson
1. Expressing a bearish breakdown case via `SHORT STOP_MARKET` below support (`4.55`) rather than a passive `SHORT LIMIT` above spot prevents adverse fill during an upside breakout (`5.3040` peak, `0.00%` loss).
2. A two-way `STOP_MARKET` bracket resolves cleanly when the coil holds above the opposite trigger boundary (`low 4.6300 > 4.55`).
Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`
