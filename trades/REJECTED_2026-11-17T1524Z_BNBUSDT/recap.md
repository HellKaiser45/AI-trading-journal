# Recap — REJECTED_2026-11-17T1524Z_BNBUSDT
**TL;DR** REJECTED · A −18.2% decline into a 2.1%-wide chop produced no ticket: at −15.5% the drawdown gate is already past where the same measurement turns negative.

`BNBUSDT 1h · NO TRADE · live 592.80 · 17T15:24Z · −18.2% · JEV none 0.97`

## Plan / predicted
No ticket. Four 72h candidates went to JEV: LONG LIMIT 585.00 / TP 615.00 / SL 568.00, LONG MARKET 592.80 / TP 615.00 / SL 576.00, SHORT LIMIT 600.00 / TP 575.00 / SL 612.00, SHORT MARKET 592.80 / TP 570.00 / SL 606.00.

## Why (chart input)
702.00 (9 Nov) → 574.00 (15 Nov), −18.2%, then a recovery to 603.00 and three days of 588.00–600.50 chop. Live 592.80, −15.5% below the high. Either the 574.00 low holds or the 12–15 Nov leg resumes.

## What happened
No position. Repository measurements: LONG +0.820% per fill on the deep-drawdown-plus-chop state, but SHORT on identical bars +1.991 and bars 1–3 earlier +2.235 over 12 symbols and 141 fills. The gate flips sign between −10% (+0.164) and −15% (−0.193); BNB at −15.5% sits on the negative side.

## Right / wrong
Right: 574.00 held and the last three days are a real range. Wrong: inferring a side. The flush setup that carries a direction needs a ≥20% flush within 12 bars plus an 8–15% bounce — the 702→574 leg took six days and the bounce is +3.3%, failing both.

**Same-instrument:** the 13 Nov SHORT LIMIT 642.00 peaked at 639.29, missed by 0.42%, expired. A limit 8.3% above live does not fill here.

**Declared:** no candle files existed, so no new backtest was run; all statistics are second-hand and the replica is ~3-hourly, not 1h. This folder was already frozen — filled on explicit instruction, and recorded.

## Right trade
Counterfactual: no candidate is positive on both requirements. The honest one is the flush-plus-volume long behind the UNI and XMR tickets — not live here.

## Lesson
1. Check gate monotonicity before the chart story: at −15.5% the measurement that pays at −10% has already gone negative.
2. Distance from live price, not the thesis, binds a limit: the 642.00 short missed by 0.42% over 48h.

Evidence: `research_log.txt` `decision_tree.dot` `graphpoints.csv` `chart_prediction.svg`