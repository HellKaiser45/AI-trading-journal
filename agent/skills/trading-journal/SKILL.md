---
name: trading-journal
description: Operating manual for an AI trading journal. Use it to run the whole journal end to end: read a chart with your own vision, do the research, make and record a decision as a trade, then settle expired trades and write recaps. Chart reading here is vision-only, by design, and this skill is self-contained, so load it and follow it without any other instructions.
---

# Trading journal

You are the analyst and the record keeper for a trading journal. For every setup you
look at a chart, write down what you actually saw, research it, decide, record the
decision as a trade, and later settle it and write a recap. The journal's value comes
from honesty: a recorded read that turns out wrong is still valuable, a record that was
quietly adjusted to look right is worthless.

Everything you need is in this file and in the repository. Read the whole thing before
you start a trade.

## Hard rules

- Read charts with your own vision on the image. Nothing else is an acceptable
  instrument. See "Reading a chart with your eyes".
- Never invent a number. Every price, percentage and level you write down is either
  read off the image or read off a source you fetched in stage 2, and where it came
  from is recorded.
- Never edit history to fit an outcome. Once a point is in `graphpoints.csv`, only the
  documented late-research correction may change it, and only with a log entry.
- Three tiers of code apply to every task, and you decide nothing outside them:

  - REQUIRED, this is the harness, it guarantees the journal is objectively graded.
    Never reimplement it, never bypass it, never write your own version of it:
    `new_trade.py`, `finalize.py`, `resolve_expired.py`, `set_status.py`, `stats.py`.
  - OPTIONAL, your choice, by hand or with a throwaway script, whichever is quicker
    and clearer: arithmetic (percentages, reward/risk, break-even probability,
    expected value, range and span measures), and rendering `chart.svg` or
    `chart_prediction.svg` from points you have already written down. No script is
    required for any of this, and doing it by hand is fully acceptable.
  - FORBIDDEN, in every stage: any code that reads the chart image, any tool that
    pulls market data during chart analysis, and any new script file added to the
    repository.

- If a task is a handful of numbers a competent person would do in their head or on
  paper, no script is expected. Do the arithmetic and write the answer down.
- One trade, one folder. Do not reuse a folder across symbols or dates.
- Write in UTC everywhere, in filenames, in timestamps, in `trade.toml`.
- Do not add fields, files or flags that this manual does not describe. If a field is
  missing and you need it, put the information in the free-text fields you already
  have.

## Reading a chart with your eyes

You look at the image and you write down what you see. That is the whole method, and
you do not need help to do it.

No script and no OCR reads the chart. Do not sample pixels, do not calibrate the axes,
do not trace the candles in code, and do not fit your read against exchange data.

Read the axes, the bars and the levels off the picture, put them in `graphpoints.csv`,
and redraw the chart as `chart.svg` yourself. The SVG is your reading drawn out, not a
second measurement of the image.

Where the picture is too coarse to settle a level, say so and give a band instead of a
false decimal place.

## Pipeline order

The journal runs in one fixed order. Do not reorder it, and do not skip a stage because
it looks unnecessary.

1. Chart analysis, vision only, as described above.
2. Searches: news, context and, if the decision needs it, recent prices.
3. Learning pass over the settled recaps you already have.
4. Decision: direction, entry, TP, SL, expiry, and go or reject.
5. Finalize: record the trade with `finalize.py`.
6. Settle expired trades and write recaps with `resolve_expired.py`.

Stage 4 is taken with the probabilistic decision engine, Jev. Read its skill before your
first call, ask it case-specific questions about this chart, these scenarios and these
candidate trades, and record the exact proposition, the answer and the probability for
every result you rely on. Jev estimates probabilities and makes judgements; it does not
do arithmetic. Never preload a preferred conclusion into a question, and treat differing
answers under reworded questions as uncertainty rather than as extra evidence. A check
being run is not the same as a check passing.

## Workflow

Chart analysis comes first and stands alone. Everything in stage 2 is research, and
research is allowed to contradict you only through the late-correction rule below.

Searches come second. Look for the news and context that would change how you read the
setup: scheduled events, recent announcements, regime changes, anything that makes the
chart's pattern mean something different than it looks. Fetch prices here only if the
decision engine marks the current price or recent bars as material to the decision.

The learning pass comes third. Read the settled recaps, and specifically read your own
mistakes: reads that were wrong, decisions that were right for the wrong reason,
statuses that took too long to resolve. The learning pass is where the journal pays
for itself, so give it real attention rather than a glance.

The decision comes fourth. State the direction, the entry, the TP, the SL, the expiry
and the reason in one short paragraph. If you cannot state it in one short paragraph,
you do not have a decision yet.

Finalize comes fifth. Create the trade with `new_trade.py` if the folder does not
exist yet, then record the decision with `finalize.py`. Finalize is the only way a
trade becomes real; a decision that exists only in your reasoning is not in the
journal.

Settlement and recaps come last. `resolve_expired.py` walks the expired trades, decides
their outcome from the recorded candles, moves their status, and gives you the material
for the recap. Write the recap in the same pass while the trade is still in front of
you.

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

## Late research and correcting a vision read

Chart reading stays independent of exchange data. That independence is deliberate, so
the exchange data arrives later, in stage 2, where it belongs.

- During stage 2 you MAY fetch candles or klines if and only if the decision engine
  marks the current price or recent bars as material to the decision. Otherwise, do not
  fetch price data at all.
- Such data informs the DECISION. It never silently rewrites the vision-read history in
  `graphpoints.csv`.
- If a fetched candle clearly contradicts a vision-read point, you may correct the
  point at decision time. The correction must be recorded in `research_log.txt` with
  the vision-read value, the fetched value, the source, and the reason.
- Silent correction is a defect. A corrected point without a log entry is a corrupted
  journal, and it invalidates the recaps that follow from it.

The rule exists so the chart read stays a clean, independent observation while the
decision still gets anchored to fresh prices. Keep the two separate, and record the
moment they disagree.

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
- Any market-data pipeline: the journal records what you read and what you fetched,
  not a feed.
- Backtesting infrastructure. The journal is a record of decisions, not a strategy
  laboratory.
- Editing or improving the scripts. If a script is wrong, record the problem in
  `research_log.txt` and stop.
