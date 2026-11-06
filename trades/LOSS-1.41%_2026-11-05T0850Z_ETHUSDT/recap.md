# Recap — LOSS-1.41%_2026-11-05T0850Z_ETHUSDT
**TL;DR** LOSS · bought the floor of a 16-hour balance for a 1.5% pop; the balance broke 3h20m after the fill and the TP never printed again.

`ETHUSDT 1h · LONG LIMIT 2408 · TP 2444 (+1.49%) / SL 2374 (−1.41%) · RR 1.06 · 05T09:08Z→06T08:00Z · fill 05T12:30Z · stop 05T14:35Z`

## Plan / predicted
Buy the 2408 floor of the 2405.23-2446.28 balance with a stop under it and take the 1.5% rotation to 2444. The balance had been tested three times at the floor (2405.23 / 2405.59 / 2407.66) and three times at the top.

## Why (chart input)
The 2026-11-04T16:00Z hour printed the whole 24h range (2310.00-2450.00, 6.06%) on 2.3x volume; the following 16 hours held a 1.7% band with a 23.6-point mean hourly range. A post-impulse balance, with the floor the natural long level.

## What happened
Filled 2026-11-05T12:30Z at the floor. MFE +0.12% (2411.00) — the floor never even held a full hour — and the stop at 2374 came at 14:35Z, 2h05m later. The TP never printed: the post-stop maximum was 2382.18 (−1.07% versus the entry) and the window fell to 2205.11 (−8.43%), closing at 2227.00.

## Right / wrong
Right: the balance was measured correctly and both edges were real. Wrong: a 1.5% target inside a 1.7% balance is not a rotation, it is the other edge — while the stop sat only 1.41% below the floor, i.e. roughly half the balance's own height, with the balance already 16 hours old.

## Right trade
Counterfactual from these candles: the break of the 2405 floor was the trade. A SHORT on the 2026-11-05T13:00Z rejection of 2408-2410 into 2205 paid about +8.4% over the following 19 hours.

## Lesson
1. When the target is inside the range and the stop is also inside the range, the ticket is a coin flip on which edge is tested first; require the stop beyond the balance's opposite extreme or a target beyond it.
2. This is the sixth journal loss where a 1.0-1.5% stop was hit inside normal noise while the favourable side never printed; the pattern (LOSS-1.01% ASTER 10-23, LOSS-1.08% BTC 11-04, LOSS-1.45% SOL 11-04) now dominates the record.

Evidence: `review.md` `trade.toml` `outcome_candles.csv` `decision_tree.dot`