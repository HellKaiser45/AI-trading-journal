# Recap — LOSS-1.01%_2026-10-23T1024Z_ASTERUSDT
**TL;DR** Right side, right support, wrong stop: a 0.5-ATR buffer below a wick was swept, and the target tagged six hours later.

`ASTERUSDT 1h · LONG LIMIT 0.695 · TP 0.706 (+1.58%) / SL 0.688 (−1.01%) · RR 1.57 · 23T10:40Z→25T10:00Z · P(fill) 0.45–0.52 · claimed P(TP|fill) 0.83–0.90 · p_BE 0.439`

## Plan / predicted
Buy the top of the rising-lows support zone (0.6741/0.6780/0.6920) after a five-candle V-bounce, target 0.706 resistance, stop at the 0.6900 wick low + 0.5 ATR. Direction votes were split (0.48/0.39, 0.49/0.35, 0.61/0.25) and correctly not used as votes. Forecast: tag 0.7115, fill 0.6948, rebound 0.7060.

## Why (chart input)
10-day range 0.6741–0.7271, −4.0% leg (0.7225→0.6935) on 22–23 Oct. Level probabilities: P(≥0.7140) 0.52, P(≤0.6940) 0.52 — a genuine two-sided coin flip traded on conditional expectancy.

## What happened
Filled 22:30Z, dipped to 0.685 (stop hit 24T14:15Z, MAE −1.44%), then rallied to 0.715 and tagged the 0.706 target at 24T20:15Z, six hours after the stop.

## Right / wrong
Right: side and support read (0.685 held, target exceeded by 1.3%), honest candidate comparison. Wrong: the claimed conditional (0.83–0.90) exceeded the unconditional P(touch 0.706) ≈ 0.45 — impossible when the condition is a subset of the path; and the stop was an ATR buffer inside the rotation, not a measured invalidation (the 0.674–0.680 triple floor).

## Right trade
Counterfactual, same candles: the same long with the stop under the 0.6740 triple floor survives the 0.685 sweep and reaches 0.706 = +1.58% at RR ≈ 0.9 — the honest price of this setup.

## Lesson
1. Cap every P(TP first | fill) at the measured unconditional touch probability, then re-run p_BE.
2. A buffer is not a structure; a coin-flip chart can only be traded with a stop the coin flip cannot reach.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`