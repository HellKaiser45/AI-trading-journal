# Recap — REJECTED_2026-11-19T1241Z_ASTERUSDT
**TL;DR** Rejected · every Aster state that beat a matched control failed on absolute EV or had one thin symbol carrying it.

`ASTERUSDT 1h · SHORT (no ticket) · never placed · P(fill) n/a · P(TP|fill) n/a`

## Plan / predicted
No ticket. Intent: sweep the venue, not one chart, and trade only if a pre-specified state
cleared four tests fixed in advance. Candidate in `chart_prediction.svg`, audit only.

## Why (chart input)
No image supplied, so structure came from Aster klines: ASTER fell from 0.6013 (17 Nov) to
0.5210, then 24h in 0.5152–0.5334. Eight states were defined before any expectancy.

## What happened
No fill; the measurement is the event. 78 perps pulled, 57 excluded for dead bars. Each
state was scored against three random same-symbol same-day bars with identical geometry,
then deduplicated over 120 bars: `failed_bounce` fell from 1300 raw signals to 36 episodes.

`failed_bounce` +1.48% but control p=0.487, CI [−1.32,+4.08]; `overbought_reject` +3.15 at
p=0.041 fell to −0.50% without BTWUSDT; `failed_breakdown` p=0.000 had 8/21 positive symbols
and −0.27% without LITUSDT; `range_fade`, the shape of this journal's only two wins, beat
its control by +0.66 yet was −0.08% absolutely in both halves.

## Right / wrong
Right: refusing on absolute EV, not relative edge — a random bar returns +0.17% at 72h
(mirror SHORT) with a negative median, so any short state earns a positive mean for free.
Right: catching that the ATR array was a fraction of price multiplied as currency, faking
0.0%-win clusters on 13 symbols. Wrong: I had a +3.37% first-half result and hunted the
geometry that survived the split; it killed it.

## Right trade
Counterfactual: ASTER's own two `failed_bounce` episodes returned +2.44% and +7.62%. n=2 is
not evidence.

## Lesson
1. A positive edge versus a matched control is not an edge: `range_fade` beat its control by
   +0.66% while losing 0.08% per ticket. Require positive absolute EV first.
2. Test drop-one-symbol before believing a p-value: BTW removed `overbought_reject`
   (+2.08% → −0.50%), LIT removed `failed_breakdown` (−0.14% → −0.27%).

Evidence: `research_log.txt`