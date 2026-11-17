# Recap — REJECTED_2026-11-17T1407Z_XRPUSDT
**TL;DR** REJECTED · Superseded stub: a stray trade-folder creation at 14:07Z was never used. The substantive record for this XRPUSDT chart is REJECTED_2026-11-17T1505Z_XRPUSDT.

`XRPUSDT 1h · NO TRADE · 17T14:07Z · duplicate of 17T15:05Z · no measurement performed in this folder`

## Plan / predicted
Nothing. `new_trade.py XRPUSDT` created this folder at 14:07Z and the run was restarted; the analysis was redone from scratch at 15:05Z with a declared state definition, correct next-bar-open entry, and era splits.

## Why (chart input)
Same image as the 15:05Z folder: 1.2100 → 0.8977 then a bounce to 0.9771.

## What happened
No position and no measurement. The folder held only template files until this recap was added.

## Right / wrong
Right: discarding an unfinished draft instead of retro-fitting a story to it. Wrong: the folder should have been rejected in the same run that abandoned it, at 15:05Z, rather than left as an IDEA until noticed now — `stats.py --check` was exiting non-zero the whole time and that exit code is what surfaced it.

## Right trade
None. See REJECTED_2026-11-17T1505Z_XRPUSDT for the four candidates that were priced and why each failed.

## Lesson
1. If a run is restarted, close the abandoned folder in the same run. A stray IDEA blocks `stats.py --check` and hides the next folder's real status behind it.
2. A duplicate folder is not free: it doubles the review surface while adding zero evidence.

Evidence: `graphpoints.csv` `chart_prediction.svg` `chart.svg`