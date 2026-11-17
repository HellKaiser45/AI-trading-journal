# Recap — EXPIRED_2026-11-13T1531Z_BNBUSDT
**TL;DR** EXPIRED, never filled · The limit sat 0.42% above a high that printed 4.9h after placement, then the trade the thesis predicted paid 10% to anyone already short — an entry that required a bounce cost the whole edge.

`BNBUSDT 1h · SHORT LIMIT 642 · TP 588 (−8.41%) / SL 686 (+6.85%) · RR 1.23 · 13T15:31Z→15T15:31Z · P(fill) 0.640 · P(TP|fill) 0.30 · p_BE 0.448`

## Plan / predicted
Sell the retest of 642 into a market in a measured downtrend, TP at 588 on the way to the 566 handle, SL 686 above the structure. Forecast: a bounce into 642 within ~13h (median fill time from 110 historical analogues), then continuation lower to the target by Sunday.

## Why (chart input)
1h decline from 724 to 632 with a sharp final leg; the thesis was that a dead-cat bounce to 642 would offer a better short than selling the low. Research at the time: no dated catalyst inside the 13-15 Nov window (no US macro prints, no Binance announcement dated for the weekend), and the measured probability of a bounce to 642 within 47h was 0.640.

## What happened
Window high **639.29 at 2026-11-13T20:20Z** — 4.9 hours after placement and **0.42% short of the limit**. Never filled. From there the market fell to **566.00 at 15T01:45Z**, and TP 588 printed at **14T16:15Z**, 24.7h after placement. Expiry close 590.88.

## Right / wrong
Right: the directional read was emphatically correct — the market fell 11.6% from the placement price and 588 traded less than a day later. Wrong: the **entry**. Requiring a +1.8% bounce to sell meant the order needed the one thing the declining market never gave; a market entry at 631.35 would have paid +6.41% and a short at the placement open reached +10.35% at the low.

## Right trade
Counterfactual, same candles: SHORT MARKET at 631.35 (placement-time open) → 566.00 = **+10.35%**. The trade was right and the ticket captured none of it.

## Lesson
1. When a base rate says P(bounce to the limit) = 0.64 and the market is in a one-way decline, the 36% no-fill branch carries the *entire* edge: here it cost 10.35 points of a trade that was correctly called.
2. Measure the cost of the filter, not just the fill rate. Fill 0.64 × (+6.41% market result) still beat fill-capture of 0% here; the limit needs its own measured edge, not just a plausible entry price.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`