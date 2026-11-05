# Recap — LOSS-1.08%_2026-10-18T1703Z_ETHUSDT
**TL;DR** Sold the middle of a 60-point resistance block, which the market pushed straight through to 2478 before falling to the target.

`ETHUSDT 1h · SHORT LIMIT 2405 · TP 2352 (−2.20%) / SL 2431 (+1.08%) · RR 2.04 · 18T17:03Z→20T21:00Z · P(fill)/conditionals not recorded`

## Plan / predicted
Fade a dense "39-touch" 2400–2460 resistance block in a −17.43% downtrend; TP inside the 2340–2380 support band above the hard 2318 invalidation; SL 1.9× ATR above entry. Jev side SHORT 0.99/0.94/0.91, GO_LIMIT 0.93/0.89/0.87. Only five forecast points existed (ending 2365.65) — no path work to contradict the ticket.

## Why (chart input)
2807 → 2318 decline with a 2340–2380 support band; early-format research (4 agents): ETF −$320.1M week to 16 Oct, RSI 30–36, daily ATR 98.52.

## What happened
Filled 23:25Z after a 1.7% bounce from the 2365 placement price, then rallied to 2478 — the 2431 stop hit at 19T02:45Z, 3.3h after the fill. Only afterwards did price fall to 2329, through the 2352 target; exit 2449.07.

## Right / wrong
Right: destination (2329 vs TP 2352) and a real ATR multiple rather than a token buffer. Wrong: the entry sat inside the block, leaving 1.08% of stop before the block's own reach of 2478 — "dense resistance" was treated as a ceiling when in a 6.4%-wide window it was a passage.

## Right trade
Counterfactual, same candles: a far-edge fade at 2465–2470 with the stop above 2485 and the same 2352 target is +4.5% at RR ≈ 5 and survives the sweep; a market short at the 2365.29 open = +1.53%.

## Lesson
1. Fade the far edge of a wide block, not its middle; measure the block's realised reach (2478), not its touch count (39).
2. Early-folder gap to never repeat: no P(fill) and no adverse-branch probability — the branch that decided the trade was unpriced.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart.svg` `outcome_candles.csv`