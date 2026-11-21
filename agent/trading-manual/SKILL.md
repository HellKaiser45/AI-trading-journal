---
name:trading-manual
description:trading manual guidelines to follow whenever the user gives a chart or a trading related request
---

## Pipeline order

The journal runs in one fixed order. Do not reorder it, and do not skip a stage because
it looks unnecessary.

1. Chart analysis, vision only, as described above.
2. Searches: news, context and, if the decision needs it, recent prices.
3. Learning pass over settled recaps and active book exposure.
4. Decision: Checkmate conclave across states of nature, order type (`MARKET`, `LIMIT`, `STOP`, `STOP_MARKET`), direction, entry, exits (`tp`, `sl`, `trail`), expiry, and go or reject.
5. Finalize: record the trade(s) with `finalize.py`.
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
- do not use commands to crop or else to read the image , it is loaded in your context anyway.
- Just rewrite it from memory

  Then do a thorough chart analysis to find potential supports,resistances, or chart patterns. 
  Then draw the chart_prediction.svg with those findings.

## 2. Searches
This is an optional step. In fact , if we search, what to search , and why should be defined 
and approved or decided by our decision engine JEV.
Even how we search , parallel, sequential, a mix of the 2, and after every round of search 
we determine if we command more searches or not. 
Because sometimes searches are purely a waste of time and tokens if the timeframe is small
and we are confident on prediction based on the graph.

## 3. Learning pass & Active Book Audit
This is a mandatory two-part step.

### 3A. Settled Trades Review
If in the journal you have already finished trades you must review them.
Those trades were also made by you by this exact system.
You can read charts, `chart_prediction.svg`, and `recap.md` for those trades to internalize structural lessons:
- **Adverse Selection & Sequence**: Notice why passive orders missed fills when the directional thesis was right, why passive orders filled into momentum when the thesis was wrong, and whether the favorable excursion had already printed before fill.
- **Invalidation vs Noise**: Notice where stops sat inside normal volatility versus outside the genuine structural invalidation envelope, and where targets sat at high-traffic interior zones versus unreached outer extremes.
- **No Rigid Templates**: Never hardcode fixed distances or mechanical rules from past trades; adapt dynamically to each asset's live volatility and regime.

### 3B. Active Book & Directional Balance Audit
Inspect active `PENDING` and `OPEN` folders in `trades/` (or run `stats.py`) to measure current `LONG` versus `SHORT` exposure, asset-class concentration, and entry clustering before adding new trades.
- **No One-Way Directional Stacking**: Never leave the book—or any set of proposed trades—leaning all in one direction (such as all shorts or all longs). If existing active trades lean one way, new setups must restore two-way balance.

## 4. Two-Way Checkmate Conclave (JEV)
Based on all the previous steps, you gathered 4 sources of information:
- graph with chart analysis
- researches
- past trade knowledge
- active book exposure (`PENDING` and `OPEN` trades)

You refine `chart_prediction.svg` and evaluate candidate setups across both directions (`PUMP` / upside breakout vs `DUMP` / downside breakdown). **You must never assume your primary directional guess is right.** Every trade proposal must be structured so that if the market moves violently in the opposite direction, an opposing leg or trigger captures that move:

1. **Single-Chart Two-Way Checkmate (Always Pair Opposite Sides)**:
   When the user gives a single chart (unless it is specifically offsetting an existing opposite-side position in the active book), construct a **two-leg paired setup** (`LONG` + `SHORT`, recorded as two linked folders sharing a `--group` ID) or an asymmetric structure that covers both a pump and a dump:
   - **Fade + Breakout Flip (`LIMIT` + `STOP_MARKET`)**: Pair a structural fade (`e.g., SHORT LIMIT` at resistance or `LONG LIMIT` at support) with an opposite-direction breakout trigger (`e.g., LONG STOP_MARKET` at/near the short's invalidation level, or `SHORT STOP_MARKET` at/near the long's invalidation level) using an asymmetric target or `TRAILING_STOP_MARKET` (`--trail`). If the fade works, the breakout trigger never fills; if the market squeezes through the level, the `STOP_MARKET` leg triggers into the breakout momentum and offsets or exceeds the stopped-out fade.
   - **Two-Way Breakout Straddle (`LONG STOP_MARKET` + `SHORT STOP_MARKET`)**: When price is coiled inside an inflection range, bracket the structure with both a `LONG STOP_MARKET` above resistance and a `SHORT STOP_MARKET` below support (using trailing stops or asymmetric targets) so whichever way the market explodes, the winning breakout leg pays more than the opposite leg risks.
   - **Sequential Catch-and-Flip (`SHORT` + Deep `LONG`)**: Pair an upper-shelf `SHORT` with a deep washout-floor `LONG` placed beyond the short's target so a full dump-and-rebound pays on both legs while a one-way dump is caught at the floor.

2. **Multi-Asset Dispersion Checkmate (Market Scans & Portfolio Baskets)**:
   When proposing multiple trades across the market, **enforce strict directional balance (`LONG` paired with `SHORT`)**:
   - Pair shorts on structurally weak or catalyst-impaired instruments with longs on structurally strong relative-strength leaders or uncorrelated assets (across crypto, shares/semis, and commodities).
   - Never output a one-way list of same-direction trades. If the market pumps, your `LONG` legs and `LONG STOP_MARKET` breakout triggers must profit; if the market dumps, your `SHORT` legs and `SHORT STOP_MARKET` breakdown triggers must profit.

3. **Full Execution Toolkit on Aster DEX**:
   - `MARKET`: immediate participation when waiting for a pullback risks missing the move entirely.
   - `LIMIT`: passive entry at a structural inflection level.
   - `STOP` / `STOP_MARKET`: conditional trigger entry on a breakout or reversal confirmation (`LONG` triggers when price breaks up through `price`; `SHORT` triggers when price breaks down through `price`). Never fills unless price moves in that direction.
   - `TRAILING_STOP_MARKET` (`--trail` callback rate, with or without `--tp` and `--sl`): dynamic trailing exit that lets the winning side of a Checkmate pair ride an extended pump or dump without capping upside prematurely.

Run all candidate order types and paired Checkmate combinations against JEV with unbiased, neutral context from multiple angles. Verify in JEV that the proposed combination survives both a sudden market pump and a sudden market dump before finalizing.

## 5. Finalize
Write the trade(s) with `finalize.py` (creating a separate folder via `new_trade.py` for each leg of a two-way Checkmate pair and linking them with `--group` and `--role`).

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

## Output
The user does not want explanations, commentary, narratives, or tables.
Output ONLY the clean trade block(s) — nothing else.

## IMPORTANT
- Do not create files that are not specified by the framework into the repo.

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
| `PENDING` | order placed, not filled (`LIMIT`, `STOP`, `STOP_MARKET`) |
| `OPEN` | position live (`MARKET` goes straight here) |
| `WIN+X.XX%` | TP or profitable trailing stop hit |
| `LOSS-X.XX%` | SL or negative trailing stop hit |
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
`entry.type` in (`LIMIT`, `STOP`, `STOP_MARKET`), IDEA to OPEN needs `MARKET`, and REJECTED
folders must not contain `trade.toml`. Terminal folders (WIN*, LOSS*, EXPIRED*, REJECTED)
are frozen: only `review.md` and `recap.md` may be added.

## trade.toml

`trade.toml` is written only by `finalize.py`, never by hand.

```toml
symbol   = "BTCUSDT"
side     = "LONG"                # LONG | SHORT

[entry]
type     = "LIMIT"               # MARKET | LIMIT | STOP | STOP_MARKET
price    = 60000.0               # required for LIMIT / STOP / STOP_MARKET; omitted for MARKET

[exit]
tp       = 62000.0               # optional if trail is set
sl       = 58500.0               # required
trail    = 1.5                   # optional TRAILING_STOP_MARKET callback rate in %

[schedule]
place_at  = 2026-10-19T09:00:00Z
expire_at = 2026-10-20T21:00:00Z

[checkmate]                      # optional checkmate combination metadata
group    = "BTC-SOL-PAIR"
role     = "PRIMARY"
```

`--price` is required for `LIMIT`, `STOP`, and `STOP_MARKET`, and forbidden for `MARKET`.
At least one of `--tp` or `--trail` is required alongside `--sl`. Datetimes look like
`2026-10-19T09:00:00Z`.

## Fill model

Settlement is deterministic. `resolve_expired.py` applies one fill model to
`outcome_candles.csv`.

- Candles cover `place_at` to `expire_at`; the candle straddling `place_at` is skipped.
- `LIMIT` fills at the limit price on the first candle that touches it (`low <= price` for
  `LONG`, `high >= price` for `SHORT`).
- `STOP` and `STOP_MARKET` trigger and fill at the stop price on the first candle that
  reaches it in the breakout direction (`high >= price` for `LONG`, `low <= price` for `SHORT`).
- Never touched: `PENDING` becomes `EXPIRED`. `MARKET` fills at the open of the first candle.
- After the fill, `TP` and `SL` fill at their level on touch (and if `trail` is set, a
  trailing stop tracks the favorable extreme after fill and triggers on a `trail%` pullback).
  A candle touching both `SL` and `TP` is a `LOSS`. In the candle where a pending order fills,
  only `SL` counts.
- Neither touched: `EXPIRED±x.xx%` at the close of the last candle before `expire_at`.
- A filled `PENDING` folder is renamed twice (`PENDING` to `OPEN`, then to the result).

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
scripts/finalize.py FOLDER (--reject REASON | --side S --type T [--price P] [--tp X] --sl Y [--trail R] --expire-at T [--place-at T] [--group G] [--role R])
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
- Dollar capital allocation across accounts (directional correlation and state coverage across active `PENDING`/`OPEN` journal folders is evaluated during Stage 3B & Stage 4).
- Tax, accounting and reporting formats.
