# Recap — EXPIRED+4.01%_2026-11-15T0924Z_UNIUSDT
**TL;DR** EXPIRED +4.01% · Thesis right, stop never tested: price ran +8.07% in favour and missed TP by 2.42% — the loss was the target, not the direction.

`UNIUSDT 1h · LONG LIMIT 5.0467 · TP 5.586 (+10.69%) / SL 4.2376 (−16.03%) · RR 0.67 · 15T09:49Z→18T09:50Z · P(fill) 0.82 · P(TP|fill) 0.35`

## Plan / predicted
Buy the capitulation flush: 7d −28.97%, close in the 20–40% band of the 48h range, volume z=+2.49. On 134 bars forward 72h was +8.15% against +1.74% for a random hour of the same days. Limit 0.5 ATR, TP 4 ATR, stop 6 ATR — wide on purpose, since tight stops are this journal's killer.

## Why (chart input)
UNI −29.6% against BTC −14.7% and ETH −19.5%: beta, not a UNI shock, with no discrete catalyst. The premise was that the flush was exhausted at the 4.619 low.

## What happened
Filled 16T12:30Z at 5.0467, ~26h after placement. MFE **+8.07%** (5.4540 at 17T13:05Z). MAE just **−0.27%**, on the fill candle itself. TP 5.586 was **2.42% short** of the high; the SL sat **18.77%** under the lowest low and never came close. Expiry close 5.2440 → **+4.01%** booked with neither level printed.

## Right / wrong
Right: the condition — the matched control forecast +8.37% EV, the fill came, the direction held, and the adverse excursion was 0.27% against a −4.23% median expectation. Right: the wide stop; the day-clustered case for 6 ATR held. Wrong: the target, since a TP 4 ATR away asked +10.69% in 72h from a signal whose measured median forward return is +8.97%.

## Right trade
Counterfactual, same candles: the entry could not reach a 4-ATR TP here; a TP at the measured median (≈5.50) printed 17T13:05Z and banked ~+9%. The direction earned 8.07 points and the ticket captured 4.01.

## Lesson
1. Size the TP from the measured forward distribution, not an ATR multiple: P(TP|fill) was 0.35 while MFE median was +13.69%, so a target past the median turns a good signal into an expiry.
2. Do not book EXPIRED± as a partial win: this was +4.01% of a +8.07% excursion — a direction win and a geometry loss, which is what RR 0.67 buys.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`