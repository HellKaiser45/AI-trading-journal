# Recap — REJECTED_2026-11-19T0946Z_ASTERUSDT
**TL;DR** REJECTED · Structure was real and the state fired, but the whole measured edge came from symbols far thinner than ASTER — 0 of 90 episodes exist at its liquidity tier.

`ASTERUSDT 1h · NO TRADE · live 0.5282 · failed-bounce state met · pooled SHORT +2.060% n=90 (microcap) · liquid-tier SHORT −1.273% · episodes at ASTER's tier 0 of 90`

## Plan / predicted
Two candidates built, neither taken. SHORT LIMIT 0.53563 (+1.0 ATR), TP 0.51303 / SL 0.55446, RR 0.83. LONG LIMIT 0.52077 (−1.0 ATR), TP 0.54274 / SL 0.50246, RR 1.07. Both 120h, no `trade.toml`.

## Why (chart input)
Crash 0.6729 → 0.4784 (−28.90%), bounce to 0.7124 (+48.91%) by 15 Nov 21:00Z, then −25.9% to 0.5282. ATR14 1.41%, p68. My eye read the low near 0.4812 and the bounce near 0.6050; the folder keeps the exchange values.

## What happened
No position, no outcome. The state was fixed before any geometry was tested: within 120 bars a decline ≥25%, a bounce ≥20% off that low, ≥10% given back with the bounce high ≥6 bars old. 107 episodes, 22 symbols. The live bar meets it, and the bounce is genuine — only 1.9% of panel bounces are intrabar.

## Right / wrong
Right: tested as pre-specified, and the bounce-artifact hypothesis was checked then discarded when it failed. Wrong: I nearly shipped the pooled +2.06%. It is a microcap effect — Spearman ρ(liquidity, outcome) −0.210, CI [−0.394, −0.021]; quintile EVs run +6.45% in the thinnest fifth to −1.96% in the second-thickest. ASTER is at the 93rd liquidity percentile with no episode at its tier; liquid-only SHORT −1.273%; three microcaps drive the whole result.

## Right trade
Counterfactual, not a result: the pooled cell pays +2.06% on the symbols it was measured on. On ASTER's tier it is −1.27%. Nothing correct was available.

## Lesson
1. State the liquidity tier of every episode before quoting an EV: an edge that inverts across liquidity quintiles describes microcaps, not structure.
2. Count the cells tested. 5 of 24 passing a two-half holdout is 21% against 25% chance — a holdout does not fix a grid search.

Evidence: `research_log.txt` `decision_tree.dot` `chart_prediction.svg` `graphpoints.csv`