---
name: trading-journal
description: Operate the AI-trading-journal repository. Use whenever you create, finalize, settle or review a trade folder (IDEA, PENDING, OPEN, REJECTED, WIN, LOSS, EXPIRED), run new_trade.py, finalize.py, resolve_expired.py, set_status.py or stats.py, or need the folder naming, allowed files, trade.toml schema, state machine, fill model or metrics of the journal.
---

# trading-journal

A git-tracked, mock trading journal. One folder per trade idea under `trades/`. Nothing is ever sent to an exchange. Every trade risks one identical stake that is never recorded, so every result is a percentage: no leverage, no fees, funding, slippage or partial fills.

The repo is the single source of truth: folder names encode the current status, `trade.toml` encodes intent, the other files encode evidence. All scripts are stdlib-only Python (>= 3.8), run from the repo root, and `ROOT` defaults to `trades/`.

## Hard rules

- Create trade folders only with `new_trade.py`; change status or rename only through `finalize.py`, `resolve_expired.py` or `set_status.py`. Never create, rename or edit them by hand.
- Never write `trade.toml` by hand and never edit any script.
- IDEA is never an end state: a new trade ends as PENDING, OPEN or REJECTED, produced only by `finalize.py`.
- Only MARKET and LIMIT entries exist. A LIMIT fills when price comes TO the level (pullback or retest). Breakout entries cannot be expressed: use MARKET after confirmation, or reject.
- Terminal folders (`WIN*`, `LOSS*`, `EXPIRED*`, `REJECTED`) are frozen: only `review.md` (written by `resolve_expired.py`) and `recap.md` (written by the agent, see "recap.md convention") may be added.
- Never touch folders that have not expired. Never reconstruct candles from memory: real market data only.
- A settled folder must never be left without `recap.md`, and no decision may be taken before the learning pass of workflow step 3. Both are blocking, not advisory.
- If a script fails, fix the cause (inconsistent levels, incomplete candle data). Never work around it.
- Scoped files only (see "Folder contents"). Run helper code inline or from `/tmp`; never save scripts, dumps, caches or run folders in the repo.

## Workflow

The run has a fixed order: **1. chart analysis → 2. searches → 3. learning from past trades → 4. decision.**
The chart comes first and is read independently; research only answers questions the decision engine marks
material; the journal's settled history is read third, so that its lessons are applied to the *execution*
of an already-formed forecast rather than to the forecast itself; only then are candidates priced and decided.
Step 3 is also where past *setup images* are compared with the current chart: `recap.md` says what happened,
while the comparable folder's `chart.svg` / `chart_prediction.svg` show whether that structure is today's.

```sh
# 0. Create an IDEA folder (bookkeeping only; no side or entry yet)
python3 scripts/new_trade.py BTCUSDT

# 1. CHART ANALYSIS - extract graphpoints.csv + chart.svg, measure the structure,
#    build the scenarios and the independent forecast (chart_prediction.svg).

# 2. SEARCHES - only the questions the decision engine marks material, scaled to the horizon.

# 3. LEARNING FROM PAST TRADES - python3 scripts/stats.py for the aggregates, then:
#    a. skim the title + **TL;DR** line of every trades/*/recap.md (one cheap line each);
#    b. open the full body of the COMPARABLE setups (same symbol, same structure, same defect)
#       and their chart.svg / chart_prediction.svg, next to this run's chart image;
#    c. record the applicable lessons with their source folder names in decision_tree.dot.
#    (Settled folders are read through recap.md; open review.md, trade.toml, decision_tree.dot or
#     outcome_candles.csv only to verify a claim or to study a close comparable.)

# 4. DECISION - evaluate LONG and SHORT candidates independently, then exactly one of:
python3 scripts/finalize.py IDEA_2026-10-19T0900Z_BTCUSDT --side LONG --type LIMIT --price 60000 --tp 62000 --sl 58500 --expire-at 2026-10-20T21:00:00Z
python3 scripts/finalize.py IDEA_2026-10-19T0900Z_BTCUSDT --reject 'reason'

# 5. Check consistency (must exit 0)
python3 scripts/stats.py --check

# 6. Settle every PENDING/OPEN folder whose expire_at has passed
python3 scripts/resolve_expired.py --list
#    fetch real candles for the folder's place_at..expire_at, save them as
#    <folder>/outcome_candles.csv (header time,open,high,low,close; UTC), then:
python3 scripts/resolve_expired.py PENDING_2026-10-19T0900Z_BTCUSDT

# 7. RECAP - BLOCKING: write recap.md in every folder just settled (see "recap.md convention").
#    No commit and no report while a folder this run settled has no recap.md. Target <= 2,200
#    characters with a one-line **TL;DR**, so the whole history stays readable before every decision.

# 8. Summary
python3 scripts/stats.py
```

Step 6's settlement only produces `review.md` (what happened). Step 7 produces `recap.md` (why it happened,
which trade the path actually paid, and what to change next time). A run that settles a trade but writes no recap
breaks the next run's learning pass and is an unfinished run.

Script reference:

- `scripts/new_trade.py [--root ROOT] SYMBOL`
- `scripts/finalize.py FOLDER (--reject REASON | --side S --type T [--price P] --tp X --sl Y --expire-at T [--place-at T])`
- `scripts/resolve_expired.py [--root ROOT] (--list | FOLDER [--now T] [--dry-run])`
- `scripts/set_status.py [--root ROOT] FOLDER NEW_STATUS [--force]` (manual transitions; `--note` is accepted and ignored)
- `scripts/stats.py [--check] [ROOT]`

`finalize.py` only takes your parameters, checks that the numbers are coherent (TP and SL on the right sides of each other and of the entry, valid datetimes, expiry after placement), writes `trade.toml`, renames the folder and prints the BRIEF block. It reads no other file. `--price` is required for LIMIT and forbidden for MARKET. Datetimes look like `2026-10-19T09:00:00Z`.

`resolve_expired.py` decides the outcome deterministically from `outcome_candles.csv`: do not compute the result yourself and do not use a probability tool for it. It refuses candles that do not cover the whole window or have holes longer than 4 steps. Prefer 1m or 5m candles. If no real candle data can be found for a folder, leave it alone and say so.

## Folder contents

A trade folder may contain exactly these files:

| File | Purpose |
|---|---|
| `chart.svg` (`chart2.svg`, ...) | SVG replica of each chart image, original series in blue |
| `graphpoints.csv` (`graphpoints2.csv`, ...) | `timestamp,close price`, UTC. Rows up to the folder time are extracted from the chart image; rows after it are the forecast, up to `expire_at` |
| `chart_prediction.svg` (`chart_prediction2.svg`, ...) | the chart completed with the forecast: history blue, prediction orange/magenta from a "now" line, entry yellow, TP green, SL red, support bands light green, resistance bands light red, invalidation dashed grey, expiry dotted |
| `research_log.txt` | dated findings that bear on the forecast, with links; what could not be found |
| `decision_tree.dot` | free-form reasoning record (Graphviz); no script reads it |
| `trade.toml` | written by `finalize.py`; absent in IDEA and REJECTED |
| `outcome_candles.csv` | candles for settlement (`time,open,high,low,close`, UTC) |
| `review.md` | written by `resolve_expired.py` at a terminal status: outcome, fill, exit, window |
| `recap.md` | written by the agent on every terminal folder (≤ 2,200 characters, `**TL;DR**` on line 2): why the trade was taken, the plan, what the market did, what worked and failed, the right trade, and the lessons — the input of the next run's learning pass |

`research-logs/` run folders from research tools are git-ignored and must not be relied on.

## recap.md convention

`recap.md` is the fourth stage of the loop: chart analysis → searches → learning from past trades → decision.
`review.md` says *what* happened; `recap.md` says *why*, and what to change. One file per terminal folder,
named exactly `recap.md`, written by the agent (never by a script, never in a PENDING/OPEN/IDEA folder).

**When to write it**

- In the same run that settles the trade, immediately after `resolve_expired.py <folder>` renames the folder.
- Retrospectively, for any older terminal folder that still lacks one; this is the only writing allowed inside
  a frozen folder apart from `review.md`.
- A rejected idea gets one too, recording why no trade was placed — a documented non-trade is as reusable as a
  settled one.
- A run may not commit and may not report while a folder it settled still has no `recap.md`.

**Size budget — this is what keeps the journal readable**

The next run must read the accumulated history before deciding, so brevity is a hard requirement.

- **≤ 2,200 characters per file** (aim 1,500, ~330 words). The first 18 settled folders total ~35 KB at this
  budget; at 4–5 KB each the same history was 86 KB and could not be read in full.
- **Line 2 is always `**TL;DR**`** (≤ 180 characters): the status plus the single reusable verdict.
- The learning pass reads title + TL;DR of *every* terminal folder first, and opens a full body only for
  comparable setups. So: no tables, no field-by-field restatement of `trade.toml`, no prose about which files
  exist — the closing `Evidence:` line is the only file talk. Numbers inline, named levels and times.

**Rules**

- Ground every number in the folder's own files: `trade.toml` (levels, schedule), `review.md` and
  `outcome_candles.csv` (fill, exit, timing, path), `decision_tree.dot` (the reasoning and the recorded
  probabilities), `graphpoints.csv` (what was forecast). Recompute excursions from `outcome_candles.csv` with a
  script; never quote a path from memory.
- Answer three questions in order: why the trade was taken (the chart input), what was predicted, and what the
  market actually did. Only then judge it.
- Separate decision quality from outcome. A win is not proof of good reasoning and a loss is not proof of bad
  reasoning; say which part of the process the outcome actually tested.
- Any "would have" statement must be labelled as a counterfactual, computed from the recorded candles, and must
  never be presented as a trade result.
- Keep sample-size honesty: n is small, setups are mixed. State a lesson as a hypothesis with the observations
  that support it and the observations that would refute it — not as a law.
- Name the specific levels, times and percentages. "The stop was too tight" is useless; "stop 0.55% (0.65x ATR)
  while the window realised an 8.0% span; TP touched 14h45m after the stop" is reusable.

**Sections** (fixed headings, so the learning pass can read them by section):

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

`recap.md` is a record, not a scoreboard: it must be able to say "the reasoning was good and the trade still
lost" as easily as the reverse.

## Naming grammar

`STATUS_YYYY-MM-DDTHHMMZ_SYMBOL`, e.g. `PENDING_2026-10-19T0900Z_BTCUSDT`, `WIN+5.32%_2026-10-19T0900Z_BTCUSDT`, `EXPIRED-1.20%_2026-10-19T0900Z_BTCUSDT`.

- status is uppercase; the date-time is UTC, is the first evaluation moment and never changes across renames
- no colons, brackets or spaces; percentages have two decimals and an explicit sign for `WIN`, `LOSS`, `EXPIRED±`
- a colliding rename gets `-2`, `-3`, ...

## Statuses and state machine

| Status | Meaning |
|---|---|
| `IDEA` | exists only while a run is in progress |
| `REJECTED` | decided not to trade; no `trade.toml` |
| `PENDING` | order placed, not filled (LIMIT only) |
| `OPEN` | position live (MARKET goes straight here) |
| `WIN+X.XX%` | TP hit |
| `LOSS-X.XX%` | SL hit |
| `EXPIRED` | pending order never filled by `expire_at`; carries no % |
| `EXPIRED+X.XX%` / `EXPIRED-X.XX%` | position still open at `expire_at`, closed at the expiry price (`+0.00%` at breakeven) |

```
IDEA    -> REJECTED
IDEA    -> PENDING -> EXPIRED
PENDING -> OPEN    -> WIN+x% | LOSS-x% | EXPIRED±x%
IDEA    -> OPEN            (MARKET fills at placement)
```

`set_status.py` rejects other transitions unless `--force`. IDEA to PENDING needs `entry.type = LIMIT`, IDEA to OPEN needs MARKET, and REJECTED folders must not contain `trade.toml`.

## trade.toml

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

## Fill model (used by `resolve_expired.py`)

- Candles cover `place_at` to `expire_at`; the candle straddling `place_at` is skipped.
- LIMIT fills at the limit price on the first candle that touches it (low <= price for LONG, high >= price for SHORT). Never touched: PENDING becomes EXPIRED. MARKET fills at the open of the first candle.
- After the fill, TP and SL fill at their level on touch. A candle touching both is a LOSS. In the candle where a LIMIT fills, only SL counts.
- Neither touched: `EXPIRED±x.xx%` at the close of the last candle before `expire_at`.
- A filled PENDING folder is renamed twice (PENDING to OPEN, then to the result).

## Metrics (`stats.py`)

- Per-trade %: LONG `(exit - entry) / entry * 100`; SHORT `(entry - exit) / entry * 100`.
- Aggregate: arithmetic sum of all terminal %, no compounding.
- Win rate = WIN / (WIN + LOSS); `EXPIRED±%` counted separately; REJECTED excluded.

## Out of scope

Breakout (STOP) entries, trailing stops, compounding, fees and funding.
