# Recap — LOSS-0.55%_2026-11-03T0858Z_XRPUSDT
**TL;DR** Textbook ticket whose 0.55% stop was set by break-even algebra, not volatility: stopped in 65 minutes, target reached 14h45m later.

`XRPUSDT 1h · SHORT LIMIT 1.2625 · TP 1.2440 (−1.47%) / SL 1.2695 (+0.55%) · RR 2.64 · 03T09:12Z→05T09:00Z · P(fill) 0.57 · P(TP|fill) 0.63 · p_BE 0.2745`

## Plan / predicted
Fade the five-touch ceiling 1.2596/1.2613/1.2615/1.2633/1.2642 inside the 1.2333–1.2642 four-day range (90.9% of closes in 1.2440–1.2560); TP at the edge of the dense 1.2440–1.2560 band, SL 0.42% (0.65× ATR) above 1.2642. Forecast: 1.2468 trough, 1.2605 peak, 1.2512 at expiry.

## Why (chart input)
Contraction after the 2 Nov 18:00Z sweep to 1.2355 that was defended (Jev 0.82). Research: funding neutral +0.0100%/8h for 17 settlements, OI rebuilt to 101–103% of pre-event, liquidations at the 26th percentile, no scheduled catalyst.

## What happened
Filled 11:10Z on the ceiling retest exactly as designed, stopped at 1.2695 at 12:15Z — 65 minutes later. Price then rallied to 1.3414 (+6.3% from entry) and the 1.2440 target printed at 04T03:00Z, 14h45m after the stop. Window span 8.0%.

## Right / wrong
Right: entry mechanics (a genuine wick, not a fall-through), the target level was reached, and the three-branch EV plus sensitivity table are reproducible. Wrong: risk sized from p_BE, not from the volatility the thesis had to survive; the invalidation was "range breaks up" (1.8–6.2% away), not 0.55%.

## Right trade
Counterfactual, same candles: no honest short existed at this geometry — a stop beyond the 1.2721 fib (RR 1.84, p_TP needed 0.36) or a range-edge stop (1.2333, 2.3%, RR 0.64, p_BE 0.61 ≈ fail, i.e. reject). The window paid the long 1.242→1.3414 (+8.0%).

## Lesson
1. Size the stop from the volatility the thesis must survive, then check RR — never the reverse; a tight stop makes any candidate look positive-EV.
2. A range ceiling is not an invalidation; if the true invalidation is too far for the target, the setup is not expressible.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`