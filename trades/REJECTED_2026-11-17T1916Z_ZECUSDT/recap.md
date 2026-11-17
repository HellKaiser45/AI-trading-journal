# Recap — REJECTED_2026-11-17T1916Z_ZECUSDT
**TL;DR** REJECTED · A +13.6% rebound after a −19.1% flush looks tradeable but fails the mirror test: the opposite side of the same bars scores better.

`ZECUSDT 15m · NO TRADE · live 923.78 · 17T19:16Z · flush −19.1% · rebound +13.6% · JEV none 0.99`

## Plan / predicted
No ticket. Four candidates went to JEV, each 72h: LONG LIMIT 900.00 / TP 962.00 / SL 860.00, LONG MARKET 923.78 / TP 962.00 / SL 890.00, SHORT LIMIT 950.00 / TP 900.00 / SL 985.00, SHORT MARKET 923.78 / TP 880.00 / SL 950.00.

## Why (chart input)
1005.00 (13 Nov) → 813.00 (15 Nov), a −19.1% capitulation, then +13.6% to 962.00 on 17 Nov and a −4.0% pullback to 923.78. A deep-flush recovery that either continues or fails.

## What happened
No position. The state was already measured here at 1329Z on ZEC 4h, 12 symbols, 141 fills: LONG +0.820% per fill, but SHORT on identical bars +1.991 and bars 1–3 earlier +2.235, against a −0.092 unconditional baseline. LONG was ahead on 4 of 12 symbols.

## Right / wrong
Right: the structure is real, the flush is not noise, and 813.00 held. Wrong: reading direction into the recovery. The drawdown gate flips sign between −10% (+0.164) and −15% (−0.193), and the only setup here with a demonstrated direction — flush ≥20% in 12 bars, plus 8–15% bounce, plus volume z ≥ 2 — does not fire: the decline took ~120 bars and no volume series exists.

**Declared:** no candle files were available, so no new backtest was computed; every statistic is quoted from committed folders and an error there propagates uncaught. The replica is hourly, not 15m.

## Right trade
Counterfactual: no candidate is positive on both requirements. The honest one is the flush-plus-volume long behind the UNI and XMR tickets — absent on this bar.

## Lesson
1. Run the mirror test before the story. Where the opposite side of the same bars pays more, it is volatility, not direction.
2. This folder sat two days as an IDEA stub that made `stats.py --check` exit 1. Fill or reject in the run that creates it.

Evidence: `research_log.txt` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg`