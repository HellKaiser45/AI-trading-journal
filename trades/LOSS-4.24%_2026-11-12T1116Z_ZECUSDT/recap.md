# Recap — LOSS-4.24%_2026-11-12T1116Z_ZECUSDT
**TL;DR** LOSS · Stop was right-sized but wrongly placed; my earlier "SL 914 survives" claim was FALSE — 914 printed 1h after 925.

`ZECUSDT 1h · LONG LIMIT 966 · TP 1015 (+5.07%) / SL 925 (−4.24%) · RR 1.20 · 12T11:16Z→13T23:16Z · P(fill) 0.72 · P(TP|fill) 0.50`

## Plan / predicted
Buy the 966 retest after a −31.5% five-day flush (1388.00→951.21), stop 2.8% under the capitulation low, TP at the 11-11 16:00 high ~1015.76. Thesis: forced deleveraging, not fundamentals, so the 951–1024 coil gets reclaimed.

## Why (chart input)
A 21-day −31.5% decline ending in a 951.21 low, then two sessions coiling 951–1024. Entry 966 was mid-coil; SL 925 sat below the measured overshoot envelope (ATR14h 1.84%, stop = 1.5 ATR) — the one parameter both prior wins shared.

## What happened
Filled 12T11:50Z on a 965.06 wick, 34 min after placement. MFE **+2.28%** (987.98 at 12T14:35Z); the whole-window high 994.75 printed *before* the fill. Then a second leg: 925 touched 13T03:20Z from an open of 946.86 — a **1.9% gap through the stop**. MAE **−8.89%** (880.10 at 13T05:00Z). Expiry close 936.62.

## Right / wrong
Right: the cause was forced deleveraging, and 951.21 held on closes — 880.10 was a wick. Wrong: 966 was the coil's middle, not a floor. **Correction:** I claimed the round-5 SL 914 would have survived. It printed 13T04:20Z, one hour after 925; the trade loses at 914 too, larger (−5.39%). I asserted a counterfactual without running it.

## Right trade
Counterfactual, same candles: the window paid SHORT, 966→880.10 (+8.89%), and 966→936.62 (+3.04%) at expiry. Best long was the aftermath: 880.10→991.97 (+12.71%).

## Lesson
1. A limit mid-coil is a coin flip, not a fade. P(TP|fill) recorded 0.50, realised 0. Entry needed to be at the coil edge (≤951–955) to keep the stop under structure.
2. Price gap risk, not just touch risk: the 925 stop gapped to 946.86, adding ~1.9% beyond the model (−4.24% → ~−6%). Stops within 1.5 ATR of a fresh capitulation low carry this.

Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`