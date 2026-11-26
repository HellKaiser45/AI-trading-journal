# Recap — WIN+5.01%_2026-11-22T1100Z_UNIUSDT
**TL;DR** WIN+5.01% · LONG STOP_MARKET @ 4.79 triggered on the Nov 23 breakout above the 4.784 ceiling (MAE −1.46% vs −4.38% SL) and hit TP 5.03 in 10h50m.

`UNIUSDT 1h · LONG STOP_MARKET 4.79 · TP 5.03 (+5.01%) / SL 4.58 (−4.38%) · RR 1.14 · 2026-11-22T11:00Z→2026-11-24T11:00Z · P(fill) 0.56 · P(TP|fill) 0.64`

## Plan / predicted
Trigger long above the 22h coil ceiling (`4.784`) via `LONG STOP_MARKET @ 4.79`, targeting the interior Nov 15–19 breakdown shelf and D1 SMA-200 magnet at `5.03` (`+5.01%`) with `SL` at `4.58` (`-4.38%`) near the coil floor.

## Why (chart input)
After the Nov 21 washout to `4.186` and rebound to `4.784`, `UNIUSDT` coiled for 22h inside `4.556–4.784` (`spot 4.720`), backed by a `+14.4%` TVL rebound to `$3.218B` and `+35.85%` WoW Uniswap v4 volume growth.

## What happened
Price dipped inside the coil to `4.6300` at `23T02:40Z`, triggered `LONG STOP_MARKET @ 4.79` at `23T03:20Z`, saw a post-fill MAE of only `4.7200` (`-1.46%` at `13:50Z`, well above `SL 4.58`), and surged through `TP 5.03` (`+5.01%`) at `23T14:10Z` on the way to `5.3040` (`MFE +10.73%` at `14:25Z`).

## Right / wrong
Right: the `STOP_MARKET` trigger required buyers to prove follow-through above `4.784`, while the `-4.38%` `SL` (`4.58`) absorbed the `-1.46%` retest (`4.7200`). Interior `TP` scaling at `5.03` banked `+5.01%` before price retraced back to `4.7680` at expiry.

## Right trade
The executed trade (`LONG STOP_MARKET @ 4.79 -> TP 5.03`) captured `+5.01%` of the spike to `5.3040` and locked in profit before the round-trip to `4.7680`.

## Lesson
1. A `LONG STOP_MARKET` just outside a multi-session coil ceiling (`4.79` above `4.784`) with `SL` near the coil base (`4.58`) filters out range noise (`MAE -1.46%`) and enters only on confirmed momentum.
2. Scaling `TP` at the interior breakdown shelf (`5.03`) rather than holding to expiry (`4.7680`) converted a round-trip spike into a `+5.01%` `WIN`.
Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`
