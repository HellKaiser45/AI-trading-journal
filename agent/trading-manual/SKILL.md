---
name:trading-manual
description:trading manual guidelines to follow whenever the user gives a chart or a trading related request
---

## Pipeline order

The journal runs in one fixed order. Do not reorder it, and do not skip a stage because
it looks unnecessary.

1. Chart analysis, vision only, as described above.
2. Searches: news, context and, if the decision needs it, recent prices.
3. Learning pass over the settled recaps you already have.
4. Decision: direction, entry, TP, SL, expiry, and go or reject.
5. Finalize: record the trade with `finalize.py`.
6. Settle expired trades and write recaps with `resolve_expired.py`.

## Before pipeline
Before starting the pipeline start a new trade folder with `new_trade.py`

## 1. Chart Analysis
The user provided a chart as image, you ①extract the points into graphpoints.csv. 
as precisely as you can, ②you remake the exact graph provided by the user it could be candles 
or lines . 

- Read charts with your own vision on the image. Nothing else is an acceptable
  instrument. See "Reading a chart with your eyes". 
  No script and no OCR reads the chart. Do not sample pixels, do not calibrate the axes,
do not trace the candles in code, and do not fit your read against exchange data.
- Never invent a number. Every price, percentage and level you write down is either
  read off the image or read off a source you fetched in stage 2.

  Then do a thorough chart analysis to find potential supports,resistances, or chart patterns. 
  Then draw the chart_prediction.svg with those findings.

## 2. Searches
This is an optional step. In fact , if we search, what to search , and why should be defined 
and approved or decided by our decision engine JEV.
Even how we search , parallel, sequential, a mix of the 2, and after every round of search 
we determine if we command more searches or not. 
Because sometimes searches are purely a waste of time and tokens if the timeframe is small
and we are confident on prediction based on the graph.

## 3. Learning pass
This is mandatory step.
If in the journal you have already finished trades you must review them.
Those trade were also made by you by this exact system. 
You can read charts , charts_predictions as well as the recap for those trades.
This is very important because you must learn from your past trades to enhance the
precision and odds to provide a win for the user. 

## 4. Finalize
Based on all the previous step, you gathered 3 sources of information:
- graph with chart analysis
- resarches
- past trade knowledge
  
You define trade based on those, you correct and refine the chart_prediction.svg at 
this step.
You run all the possibles scenarios you have against JEV with the necessary unbiaised, neutral context.
The goal is to find the most profitable and probable outcome for a trade, by evaluating everything.
You also must confirm your answer by using jev with different angles provided in context to see if the 
outcome changes .
This is a conclave so iterate until you find the best candidate possible. 

## 5. Finalize
write the trade with `finalize.py`

## 6. Settle
Check among the open trades if some are over (expiry). 
If it is the case you must research the klines for that period (between entry and expiry)
Then you must resolve the trade by also finding out what happened and why and make a recap.md.
then you can use `resolve_expired.py` to finish this process. 

## Decision rules - JEV
if you have a skill related to jev or typesafeai - READ IT.
EVERY single decision you make explicit or implicit must be done by JEV.
the only decision you don't make using jev is deciding whether you use jev or not. YOU DO!
JEV doesn't know anything so you must provide it the necessary context for it to decide.
Presenting the option no_trade to jev against the other option will always be the highest score 
so don't do that. 
Or consider that the user don't want to lose a good opportunity. 

## Folder contents

One folder per trade, named by the grammar below. Each folder holds these files:

| File | What it is |
| --- | --- |
| `chart.svg` | SVG replica of each chart image, original series in blue. |
| `graphpoints.csv` | `timestamp,close_price`, UTC. Rows up to the folder time are extracted from the chart image; rows after it are the forecast, up to `expire_at`. |
| `chart_prediction.svg` | The chart completed with the forecast: history blue, prediction orange/magenta from a "now" line, entry yellow, TP green, SL red, support bands light green, resistance bands light red, invalidation dashed grey, expiry dotted. |
| `research_log.txt` | Dated findings that bear on the forecast, with links; what could not be found. |
| `decision_tree.dot` | Free-form reasoning record (Graphviz); no script reads it. |
| `trade.toml` | Written by `finalize.py`; absent in IDEA and REJECTED. |
| `outcome_candles.csv` | Candles for settlement (`time,open,high,low,close`, UTC). |
| `review.md` | Written by `resolve_expired.py` at a terminal status: outcome, fill, exit, window. |
| `recap.md` | Written by the agent on every terminal folder. |

Every folder must contain `graphpoints.csv`, `chart.svg`, `chart_prediction.svg`,
`research_log.txt` and `decision_tree.dot` (`chart.svg` and the numbered variants for
each image supplied). This holds for REJECTED folders too: a documented non-trade is as
reusable as a settled one. `trade.toml`, `outcome_candles.csv` and `review.md` appear
only when the journal scripts write them, and `recap.md` is added by you on every
terminal folder. Do not add any other file.

Numbered variants exist for additional images: `chart2.svg`, `graphpoints2.csv`,
`chart_prediction2.svg`.

`research_log.txt` is append-only. Never rewrite an earlier line; add a new one with a
timestamp.

`research-logs/` run folders from research tools are git-ignored and must not be relied
on. Terminal folders are frozen. Never touch folders that have not expired.

## recap.md convention

Budget: at most 2,200 characters, aim 1,500 (~330 words). Line 2 is always
`**TL;DR**` (<= 180 characters): the status plus the single reusable verdict. No tables.
The fixed sections, exactly these headings in this order:

```markdown
# Recap — <folder name>
**TL;DR** <status> · <one reusable verdict>

`SYMBOL timeframe · SIDE TYPE entry · TP x (+a%) / SL y (−b%) · RR r · placed→expired · P(fill) f · P(TP|fill) c`

## Plan / predicted    the ticket, and the forecast path it assumed
## Why (chart input)   the measured structure that motivated it, one or two sentences
## What happened       measured from outcome_candles.csv: fill context, MFE, MAE, when each level printed
## Right / wrong       which part of the reasoning the path confirmed or refuted
## Right trade         counterfactual from the same candles: the trade those candles actually paid
## Lesson              max two numbered, testable rules with the numbers that support them
Evidence: `review.md` `trade.toml` `decision_tree.dot` `outcome_candles.csv`
```

It is written by the agent, never by a script, and never in a PENDING/OPEN/IDEA folder.
Write it in the same run that settles the trade, immediately after `resolve_expired.py`
renames the folder. Ground every number in the folder's own files. Separate decision
quality from outcome. Any "would have" statement is a labelled counterfactual, never a
trade result. A rejected idea gets one too.

## Naming grammar

Every trade folder uses `STATUS_YYYY-MM-DDTHHMMZ_SYMBOL`:

```
PENDING_2026-10-19T0900Z_BTCUSDT
WIN+5.32%_2026-10-19T0900Z_BTCUSDT
EXPIRED-1.20%_2026-10-19T0900Z_BTCUSDT
```

- status is uppercase; the date-time is UTC, is the first evaluation moment and never
  changes across renames
- no colons, brackets or spaces; percentages have two decimals and an explicit sign for
  `WIN`, `LOSS`, `EXPIRED±`
- a colliding rename gets `-2`, `-3`, ...

Renaming happens only through `set_status.py`, which is what keeps the folder name and
`trade.toml` in agreement.

## Statuses and state machine

| Status | Meaning |
| --- | --- |
| `IDEA` | exists only while a run is in progress |
| `REJECTED` | decided not to trade; no `trade.toml` |
| `PENDING` | order placed, not filled (LIMIT only) |
| `OPEN` | position live (MARKET goes straight here) |
| `WIN+X.XX%` | TP hit |
| `LOSS-X.XX%` | SL hit |
| `EXPIRED` | pending order never filled by `expire_at`; carries no % |
| `EXPIRED+X.XX%` / `EXPIRED-X.XX%` | position still open at `expire_at`, closed at the expiry price (`+0.00%` at breakeven) |

The state machine:

```
IDEA    -> REJECTED
IDEA    -> PENDING -> EXPIRED
PENDING -> OPEN    -> WIN+x% | LOSS-x% | EXPIRED±x%
IDEA    -> OPEN            (MARKET fills at placement)
```

`set_status.py` rejects other transitions unless `--force`. IDEA to PENDING needs
`entry.type = LIMIT`, IDEA to OPEN needs MARKET, and REJECTED folders must not contain
`trade.toml`. Terminal folders (WIN*, LOSS*, EXPIRED*, REJECTED) are frozen: only
`review.md` and `recap.md` may be added.

## trade.toml

`trade.toml` is written only by `finalize.py`, never by hand.

```toml
symbol   = "BTCUSDT"
side     = "LONG"                # LONG | SHORT

[entry]
type     = "LIMIT"               # MARKET | LIMIT
price    = 60000.0               # LIMIT only

[exit]
tp       = 62000.0               # optional
sl       = 58500.0               # optional

[schedule]
place_at  = 2026-10-19T09:00:00Z
expire_at = 2026-10-20T21:00:00Z
```

`--price` is required for LIMIT and forbidden for MARKET. Datetimes look like
`2026-10-19T09:00:00Z`. Do not add keys.

## Fill model

Settlement is deterministic. `resolve_expired.py` applies one fill model to
`outcome_candles.csv`.

- Candles cover `place_at` to `expire_at`; the candle straddling `place_at` is skipped.
- LIMIT fills at the limit price on the first candle that touches it (low <= price for
  LONG, high >= price for SHORT). Never touched: PENDING becomes EXPIRED. MARKET fills
  at the open of the first candle.
- After the fill, TP and SL fill at their level on touch. A candle touching both is a
  LOSS. In the candle where a LIMIT fills, only SL counts.
- Neither touched: `EXPIRED±x.xx%` at the close of the last candle before `expire_at`.
- A filled PENDING folder is renamed twice (PENDING to OPEN, then to the result).

The model is all-or-nothing: no fees, no funding, no slippage, no partial fills.

## Metrics

- Per-trade %: LONG `(exit - entry) / entry * 100`; SHORT `(entry - exit) / entry * 100`.
- Aggregate: arithmetic sum of all terminal %, no compounding.
- Win rate = WIN / (WIN + LOSS); `EXPIRED±%` counted separately; REJECTED excluded.
- `stats.py --check` exits non-zero if an IDEA folder remains or a PENDING/OPEN folder
  has no `trade.toml`.

Read the metrics sceptically. A headline win rate on a handful of trades means very
little, and the learning pass should say so rather than draw a conclusion.


## Scripts

All scripts are stdlib-only Python 3.8+. Run them from the repository root.

```
scripts/new_trade.py [--root ROOT] SYMBOL
scripts/finalize.py FOLDER (--reject REASON | --side S --type T [--price P] --tp X --sl Y --expire-at T [--place-at T])
scripts/resolve_expired.py [--root ROOT] (--list | FOLDER [--now T] [--dry-run])
scripts/set_status.py [--root ROOT] FOLDER NEW_STATUS [--force]
scripts/stats.py [--check] [ROOT]
```

- `finalize.py` takes the decision as parameters, checks the numbers are coherent (TP
  and SL on the right sides of each other and of the entry, valid datetimes, expiry
  after placement), writes `trade.toml`, renames the folder, prints a BRIEF block. It
  reads no other file.
- `resolve_expired.py` decides the outcome deterministically from `outcome_candles.csv`:
  it refuses candles that do not cover the whole window or have holes longer than 4
  steps; prefer 1m or 5m candles.

Do not reimplement, wrap, or bypass any of these. Do not pass them flags this manual
does not describe.

## Out of scope

- Live execution, order routing, broker connections, position management.
- Portfolio sizing across trades, correlation between open trades, capital allocation.
- Tax, accounting and reporting formats.
- Editing or improving the scripts. If a script is wrong, record the problem in
  `research_log.txt` and stop.
