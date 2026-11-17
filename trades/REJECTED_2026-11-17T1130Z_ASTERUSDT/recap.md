# Recap — REJECTED_2026-11-17T1130Z_ASTERUSDT
**TL;DR** REJECTED · A post-flush state plus a wide-stop bracket measures +1.9% EV, but long and short are a coin flip — test the market-entry control before believing any of it.

`ASTERUSDT 4h · NO TRADE · spot 0.5816 · 2026-11-17T11:30Z · state EV +1.897% over 103 events/25 months · paired LONG−SHORT 95% CI [-2.00,+4.28] · market entry 95% CI [-2.03,+2.95]`

## Plan / predicted
Two candidates built, neither taken. LONG LIMIT 0.5589, TP 0.6725 / SL 0.4452. SHORT LIMIT 0.6043, TP 0.4907 / SL 0.7180. Both RR 1.00, 72h, geometry 0.6 ATR limit / 3.0 ATR target / 3.0 ATR stop on ASTER's ATR14 of 6.51%.

## Why (chart input)
dd20 −17.73%, bounce off the 48h low +21.80%, volume z −0.36, ATR14 at the 95.9th percentile of ASTER's own 13 months. The 2026-11-15 20:00Z bar printed a 48% range (0.7124 / 0.4812) in four hours. Envelope is symmetric: p90 up +13.04% / down 13.18%.

## What happened
No position, no outcome. The signal was fixed before the geometry search and fires 103 times over 13 symbols and 25 months. It survives an ATR-matched control (95-100th band: +2.303% vs +0.143% for non-event bars) and is not a fill artifact: median fill 2 bars, 47% on the first bar, within-bar retrace only +0.391%, and an 18-bar forced hold still leaves +2.255%.

## Right / wrong
Right: the state is not redundant with volatility, and the fill is honest. Wrong: I built a directional ticket on a two-sided harvest. With the identical bracket LONG beats SHORT on 48 of 103 events; paired gap +1.219%, 95% CI [−1.997,+4.276]. Market entry returns +0.438% [−2.028,+2.948]. The limit premium (+1.459pp) is smaller than the mechanical entry discount (0.6 ATR = 3.91%), so the EV is geometry plus a discount, not a forecast.

## Right trade
Counterfactual, not a result: holding LONG 0.5589 and SHORT 0.6043 together would harvest both tails and pay the bracket twice. The journal cannot hold both sides, so one side is half the expectancy at full single-side variance. Nothing correct was available.

## Lesson
1. An EV that dies when you switch to market entry is an entry discount, not an edge. Run that control before writing any limit ticket.
2. Symmetric envelope plus LONG beating SHORT on ~50% of events means a volatility harvest, which cannot be expressed as one direction.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg`