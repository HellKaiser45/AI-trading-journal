# Recap — EXPIRED-0.54%_2026-10-31T0901Z_XMRUSDT
**TL;DR** Clean levels and a stop that was never tested, but the fade filled 9.7h after the drop had already completed → −0.54%.

`XMRUSDT 1h · SHORT LIMIT 601.5 · TP 589 (+2.08%) / SL 615.5 (−2.33%) · RR 0.89 · 31T09:24Z→01T05:00Z · P(fill) 0.70 · P(TP|fill) 0.79 · p_BE 0.528`

## Plan / predicted
Sell the lower half of the 600–604 ask band capping 18 hourly bars inside a 588.23–604.38 compression; TP at the top of the 588.20–590.20 bid shelf (not the 574.08 extreme), SL above the whole 604–615 block. Forecast: push to 601.6, then fade to 589.

## Why (chart input)
Falling highs 604.2→602.1→600.0→601.8 with rising lows, inside an 8-day 564.24–660.73 range left by the 29 Oct spike to 651.13 and flush to 574.08. Research: Binance hot-wallet incident bid (OI +4.9%), 63.9% of accounts long, haven bid expected to decay on withdrawal resumption.

## What happened
Window low 589.27 at 10:40Z — 9.7h **before** the 20:20Z fill. Post-fill MFE +0.71% only (low ~597.2), high 611.11 at 01T02:35Z (MAE −1.60%), exit 604.75.

## Right / wrong
Right: SL 615.5 finished 4.4 points clear of the 611.11 high, and 589 was a real shelf (tagged to 589.27). Wrong: the order sold a level whose leg had already completed, and RR 0.89 needed the 0.79 conditional to be right (realised TP-first = 0).

## Right trade
Counterfactual, same candles: long 589.27→611.11 (+3.71%, 10:40Z→01T02:35Z) was the window's pay.

## Lesson
1. Before finalising a fade, record the time of the favourable extreme already printed; when it precedes the fill, the conditional must be repriced far below the touch probability.
2. A TP that needs the whole box consumed is not a fade — and a 2.08% target inside a 2.7% box may simply not pay.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg` `outcome_candles.csv`