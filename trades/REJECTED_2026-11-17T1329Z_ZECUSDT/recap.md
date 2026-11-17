# Recap — REJECTED_2026-11-17T1329Z_ZECUSDT
**TL;DR** REJECTED · A state that beats the unconditional baseline is not a trade: the short mirror and the bars 4-12h earlier both paid more than the long did.

`ZECUSDT 4h · LONG LIMIT 921.90 (candidate, never placed) · TP 1014.09 (+10%) / SL 848.15 (−8%) · RR 1.25 · 17T13:29Z→22T13:29Z · P(fill) 0.94 · P(TP|fill) 0.56`

## Plan / predicted
Buy the reclaim: −32.0% under the 20-bar high, +18.7% off the 800.67 low, back above SMA20 while still under SMA50. Limit 3% below the close, TP inside the 975–1015 supply shelf, stop 2.32× ATR under the 800.67 wick.

## Why (chart input)
A −44.1% decline from the 2026-09-26 high of 1699.00, then a 900–960 box built over four sessions, higher lows from 846.10 to 951.89. Textbook reclaim of a base.

## What happened
Signal fired at 0.117% of 144,000 scanned 4h bars. Audited over 12 symbols and 5.5 years: 141 fills, EV **+0.820%** per fill, median +0.593%, TP 51 / SL 54 / EXP 36. ZEC alone looked far better — 16 fills at +2.753%.

## Right / wrong
Right: the state is real. It beats the unconditional baseline (−0.092%, n=98,685) and clusters by day (78 days, 59% positive, CI95 [+0.72, +3.87]). Wrong: that is volatility, not direction. The **short mirror paid +1.991%** on the same bars; a bar **4–12h earlier paid +2.235%**; long beat short on only **4 of 12** symbols; and ZEC's own unconditional 120h drift is +1.46%, so most of the headline was beta.

## Right trade
Counterfactual on the same bars: the short mirror, not the long. And on ZEC's deepest drawdowns (dd ≤ −35%) the short paid +5.500% against the long's +1.000%.

## Lesson
1. Before trusting a state, price its mirror. A long that loses to its own short on the same bars carries no direction — here the gap was negative in 13 of 15 threshold combinations.
2. Price the neighbouring bars too. If entering 4–12h earlier pays more, the edge belongs to the episode, not to the signal.

Evidence: `research_log.txt` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg`