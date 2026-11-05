# Recap — LOSS-0.72%_2026-10-29T1149Z_BTCUSDT
**TL;DR** Correct direction, target and expiry — but the 0.72% stop was placed into a scheduled release the folder itself named as the main risk, and the thesis then delivered +4.7% of MFE.

`BTCUSDT 1h · SHORT LIMIT 80300 · TP 79250 (−1.31%) / SL 80880 (+0.72%) · RR 1.81 · 29T12:17Z→30T08:00Z · P(TP|fill) 0.74 · p_BE 0.3558`

## Plan / predicted
Sell the 263/317 BTC resting asks at 80250/80300 after the 81320→80019 crash and ride monthly max-pain (79000, 34.4% of OI expiring 30T08:00Z) to the 79000/79150/79200 bid block; SL 580 pts (≈1.15× ATR) behind the 80550–80850 congestion. Forecast: retest of the wall at 13–14Z, then drift to 79210–79240.

## Why (chart input)
Post-crash double bottom 79710/79764/79830/79852, printed rebound caps 80345/80374, ask wall at 80300. Research: funding never negative through the crash, OI +1.4%/24h while price −1.4% (longs re-loaded), long liquidation clusters $44–52M per $50 band at 78450–78800.

## What happened
Filled 13:15Z — 45 minutes **after** the 12:30Z PCE — and stopped at 80880 at 14:35Z on the post-release squeeze. The market then collapsed to 76500 and the 79250 target printed at 20:40Z, 6h after the stop. Post-entry high 81971 = +1.8% beyond entry vs a 0.72% stop.

## Right / wrong
Right: destination, TP above the liquidation clusters, event-aligned expiry, and the stop widening from prior inside-structure failures. Wrong: the identified risk ("PCE two-sided spike is the main risk to the fill-then-stop sequence") was written down and not paid for.

## Right trade
Counterfactual, same candles: post-release short from the 16:05Z high 81971 into 76500 = +6.67%; market short at the 80153 open = +1.13%.

## Lesson
1. A dated event inside the hold sizes the stop (needed ~2.1% here vs 0.72% used and a 1.31% target) — and if RR then fails, that is the answer: reject, or place after the release.
2. Sequence check 0: was the event before or after the fill? This order was a post-event entry carrying a pre-event stop.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`