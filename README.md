# trading-journal

A personal, git-tracked journal of futures trade ideas. Each idea is one folder. The journal is manual: `trade.toml` documents intent, nothing is ever submitted to an exchange.

Backtest-only semantics: every trade risks one identical stake; the amount is deliberately never recorded — that is why everything is a percentage. No leverage, no fees, funding, slippage or partial fills.

The repository is the single source of truth:

- folder names encode the **current status**
- `trade.toml` encodes **intent**
- `graphpoints.csv`, `chart.svg`, `chart_prediction.svg`, research notes and reviews encode **evidence**

## Quick start

All scripts are stdlib-only Python (>= 3.8) and run from the repository root.

```sh
# 1. Create an IDEA folder (no side or entry yet)
python3 scripts/new_trade.py BTCUSDT

# 2. Chart, research, forecast and Jev decisions (reasoning recorded in decision_tree.dot), then exactly one of:
python3 scripts/finalize.py IDEA_2026-10-19T0900Z_BTCUSDT --side LONG --type LIMIT --price 60000 --tp 62000 --sl 58500 --expire-at 2026-10-20T21:00:00Z
python3 scripts/finalize.py IDEA_2026-10-19T0900Z_BTCUSDT --reject 'setup_holds 0.54'

# 3. Settle PENDING/OPEN folders whose expire_at has passed
python3 scripts/resolve_expired.py --list
#    save candles as <folder>/outcome_candles.csv (time,open,high,low,close), then:
python3 scripts/resolve_expired.py PENDING_2026-10-19T0900Z_BTCUSDT

# 4. Manual transitions still work
python3 scripts/set_status.py PENDING_2026-10-19T0900Z_BTCUSDT OPEN --note 'limit filled'

# 5. Summarise, and check the journal is consistent
python3 scripts/stats.py
python3 scripts/stats.py --check
```

- `scripts/new_trade.py [--root ROOT] SYMBOL`
- `scripts/finalize.py FOLDER (--reject REASON | --side S --type T [--price P] --tp X --sl Y --expire-at T)`
- `scripts/resolve_expired.py [--root ROOT] (--list | FOLDER [--now T] [--dry-run])`
- `scripts/set_status.py [--root ROOT] FOLDER NEW_STATUS [--note TEXT] [--force]`
- `scripts/stats.py [--check] [ROOT]`

`ROOT` defaults to `trades/`, next to `scripts/`.

## Naming grammar

Pattern: `STATUS_YYYY-MM-DDTHHMMZ_SYMBOL`

Examples:

- `IDEA_2026-10-19T0900Z_BTCUSDT`
- `PENDING_2026-10-19T0900Z_BTCUSDT`
- `WIN+5.32%_2026-10-19T0900Z_BTCUSDT`
- `EXPIRED-1.20%_2026-10-19T0900Z_BTCUSDT`

Rules:

- status is uppercase
- date-time is UTC, and is the **first evaluation moment**; it never changes across renames
- no colons, brackets or spaces in names
- `%` values always have two decimals and an explicit sign for `WIN`, `LOSS` and `EXPIRED±` statuses
- if a rename would collide with an existing folder, append `-2`, `-3`, ...

## Statuses & state machine

Exact status tokens:

| Status | Meaning |
|---|---|
| `IDEA` | exists only while a run is in progress. A run always ends in PENDING, OPEN or REJECTED, via finalize.py |
| `REJECTED` | after research, decided NOT to trade (reason is given to finalize.py and printed in its brief); no `trade.toml` |
| `PENDING` | order placed, not filled (LIMIT entries only) |
| `OPEN` | position live (MARKET entries go straight here) |
| `WIN+X.XX%` | TP hit |
| `LOSS-X.XX%` | SL hit |
| `EXPIRED` | pending order never filled by `expire_at` (never carries a %) |
| `EXPIRED+X.XX%` / `EXPIRED-X.XX%` | position still open at `expire_at`, resolved at the expiry price; `+0.00%` at exact breakeven (never bare `EXPIRED` for a filled position) |

Transitions:

```
IDEA    -> REJECTED
IDEA    -> PENDING -> EXPIRED
PENDING -> OPEN    -> WIN+x% | LOSS-x% | EXPIRED±x%
IDEA    -> OPEN            (MARKET entries fill at placement)
```

Terminal statuses (`WIN*`, `LOSS*`, `EXPIRED*`, `REJECTED`) freeze the folder: no edits to plan files. Post-trade notes go in `review.md`.

`set_status.py` rejects out-of-machine transitions unless `--force` is given. IDEA to PENDING requires `entry.type = LIMIT`, IDEA to OPEN requires MARKET, and REJECTED folders must not contain `trade.toml`.

## Folder contents

| File | Purpose |
|---|---|
| `trade.toml` | intent; written by finalize.py, never by hand; absent while `IDEA` and in `REJECTED` |
| `graphpoints.csv` | chart points, `timestamp,close price`: rows up to the folder time are extracted from the chart image(s), rows after it are the forecast up to `expire_at` |
| `chart.svg` | SVG replica of the chart (original series in blue) |
| `chart_prediction.svg` | the chart completed with the forecast: history blue, prediction orange, entry yellow, TP green, SL red, expiry marked |
| `research_log.txt` | thesis, data checked (news / prices / other assets / forums / tokenomics), links |
| `decision_tree.dot` | thought process (Graphviz), free-form record of the reasoning; not read by any script |
| `outcome_candles.csv` | market candles for the settlement check (header `time,open,high,low,close`; UTC) |
| `review.md` | written when the trade reaches a terminal status; resolve_expired.py writes it |

## trade.toml schema

```toml
# trade.toml — one per trade folder
symbol   = "BTCUSDT"
side     = "LONG"                # LONG | SHORT

[entry]
type     = "LIMIT"               # MARKET | LIMIT
price    = 60000.0               # LIMIT only; MARKET fills at the CSV's last close

[exit]
tp       = 62000.0               # optional — omit to ride to expiry
sl       = 58500.0               # optional — expiry closes it

[schedule]
place_at  = 2026-10-19T09:00:00Z
expire_at = 2026-10-20T21:00:00Z
```

Field rules:

- `side` ∈ {`LONG`, `SHORT`}
- `entry.type` ∈ {`MARKET`, `LIMIT`}
- `price` is required iff `type = LIMIT`; the line is removed entirely for MARKET
- `tp` and `sl` are optional; omit the key when unused (no `tp` = ride to expiry; no `sl` = exit on tp or expiry)
- datetimes are unquoted TOML offset datetimes with the `Z` suffix

## Decisions and forecast

The AI makes the decision (Jev, the probability engine, is its decision tool) and passes it to finalize.py as parameters. No script reads `decision_tree.dot`, `graphpoints.csv` or `chart_prediction.svg`: they are the evidence and the reasoning record, kept for review. finalize.py only checks that the numbers are coherent (TP and SL on the right sides of each other and of the entry, datetimes valid, expiry after placement) and then writes `trade.toml` and renames the folder.

Every folder, rejected ones included, carries the forecast: `graphpoints.csv` rows after the folder's date-time are the predicted path (up to `expire_at`), and `chart_prediction.svg` draws it on the chart.

## Fill model

Assumptions: all-or-nothing; no fees, funding, slippage or partial fills; one identical stake per trade (amount unrecorded); nothing is submitted anywhere.

- **Entry LIMIT:** fills AT the limit price when price touches it (candle low <= price for LONG; candle high >= price for SHORT).
- **Entry MARKET:** fills at the open of the first candle at or after `place_at`.
- **Exit TP / SL:** fill at the level on touch (same touch semantics as LIMIT entry).
- **Exit at expiry:** the price at `expire_at`, read off the chart at review time; recorded once as the % in the folder name.
- **Determinism rule:** if a single candle's range touches BOTH tp and sl, resolve pessimistically as SL.

## Settlement

`resolve_expired.py` settles every PENDING or OPEN folder whose `expire_at` has passed:

- A folder is settled when it is PENDING or OPEN and `expire_at` has passed. The candles cover `place_at` to `expire_at` (any timeframe, finer is better); the candle that straddles `place_at` is skipped.
- LIMIT fills at the limit price on the first candle that touches it (low <= price for LONG, high >= price for SHORT). Never touched: PENDING becomes EXPIRED. MARKET fills at the open of the first candle.
- After the fill, TP and SL fill at their level on touch. A candle that touches both is a LOSS. In the candle where a LIMIT fills, only SL counts: the order of events inside one candle is unknown, so a TP touch there is ignored.
- If neither is touched, the result is `EXPIRED+x.xx%` or `EXPIRED-x.xx%` at the close of the last candle before `expire_at`.
- A filled PENDING folder is renamed twice (PENDING to OPEN, then OPEN to the result); git history shows the path.

The search agents only fetch the candles (`outcome_candles.csv`); the script decides the outcome with the fill model above, so the result is deterministic and Jev is not involved. Use `--now 2026-10-25T00:00:00Z` to test against an old folder and `--dry-run` to preview the new name. The script refuses to resolve when the candles do not cover the whole window or have holes longer than 4 steps, because a partial series would wrongly give EXPIRED. Prefer 1m or 5m candles: coarse candles produce more candles that touch both TP and SL, and those count as a LOSS.

## Metrics

- Per-trade %: price move on 1 unit. LONG `(exit - entry) / entry * 100`; SHORT `(entry - exit) / entry * 100`. No leverage anywhere.
- Aggregate: **arithmetic sum** of all terminal % (`WIN*`, `LOSS*`, `EXPIRED±*`). No compounding, no reinvestment. The sum reads as "% of one stake".
- Win rate = WIN count / (WIN + LOSS). `EXPIRED±%` is counted separately. `REJECTED` is excluded from all metrics.

## Conventions

- UTC everywhere (folder names, `trade.toml`, `graphpoints.csv`).
- The date-time in a folder name is frozen at first evaluation and never changes.
- Terminal folders are frozen; post-trade notes go in `review.md`.
- Follow-up ideas are new folders; mention the target folder in `research_log.txt`.
- Percentages always have two decimals.

## Deliberately out of scope

- Breakout entries. A `LIMIT` entry gets you in when price comes *down* to your level (LONG pullback: candle low <= price). A breakout entry — get in when price pushes *up* through your level — is the opposite touch direction, and `MARKET` or `LIMIT` cannot express it; it would need a `STOP` entry type. Out of scope until you trade breakouts. If that day comes: one enum value in `trade.toml` and `new_trade.py`, one line in the fill model — nothing else in the repo changes.
- Trailing stops.
- Compounding and reinvestment.
- Fees and funding.
