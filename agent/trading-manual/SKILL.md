---
name:trading-manual
description:trading manual guidelines to follow whenever the user gives a chart or a trading related request
---

## Pipeline order

The journal runs in one fixed order. Do not reorder it, and do not skip a stage because
it looks unnecessary.

1. Chart analysis, vision only, as described below.
2. Searches: news, on-chain/protocol data, derivatives positioning, macro catalysts, and recent prices.
3. Learning pass over settled recaps and active book exposure.
4. Decision: JEV conclave over trend alignment, execution mode (Near-Market `LIMIT`, `MARKET`, or `STOP_MARKET`), coherent structural `TP` and `SL`, Checkmate structure, expiry, and go or reject.
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

  Then do a thorough chart analysis to find the dominant multi-day trend, key supports, resistances, VWAP/consolidation shelves, and chart patterns. 
  Then draw the chart_prediction.svg with those findings.

## 2. Searches
Define and approve what to search, why, and how (parallel, sequential, or mixed) using our decision engine JEV (`jev_decide` / `jev_screen` / `jev_verify`).
Unless the timeframe is ultra-short scalping with zero external dependency, gather multi-source evidence across:
1. **Exchange Kline & VWAP Structure**: Multi-timeframe candles (`15m`, `1h`, `4h`), session/multi-day VWAPs (`12h`, `24h`, `48h`, `72h`, `7d`), ATR envelope, and official cash-session close benchmarks (for stock/ETF/commodity perps).
2. **Derivatives Positioning & Liquidation Flow**: Funding rates, **coin-denominated Open Interest** (never rely on USD-denominated OI alone, which falls mechanically when price drops), and recent long vs short liquidation skew.
3. **On-Chain / Fundamental / Corporate-Action Catalysts**: Protocol TVL/volume/fees (`DefiLlama` for DeFi tokens), regulatory or earnings catalysts, stock splits or futures contract roll dates, and scheduled tier-1 macro prints (FOMC, CPI, Core PCE).

Screen external web text with `jev_screen` and verify factual claims with `jev_verify` before logging them in `research_log.txt`.

## 3. Learning pass & Active Book Audit
This is a mandatory two-part step.

### 3A. Settled Trades Review & The 5 Empirical Guardrails
Review settled `recap.md` files and enforce the journal's five empirical laws (without hardcoding rigid percentage templates—always scale to the specific instrument's live volatility and structure):
1. **Trend-Alignment & Near-Market Execution Rule (Defeating Adverse Selection)**:
   - Historical journal data proves that passive `LIMIT` orders placed far from spot suffer severe adverse selection (`100%` fill rate on losing trades vs high missed-fill rate on winning trades), whereas **trend-aligned entries taken at or very close to current market price** (`Near-Market LIMIT` on the immediate bid/ask edge to avoid thin-book slippage, or `MARKET`) capture `~100%` of winning trend moves.
   - **Never catch falling knives**: Counter-trend passive `LONG LIMIT` bids placed into a one-way macro downtrend suffer `100%` adverse fill and low win rate. Only trade counter-trend reversals if coin-denominated OI, volume climax, and a defended multi-session floor confirm leverage has already flushed.
2. **Structural Envelope Stop Rule (Never Inside Noise)**:
   - Place `SL` strictly **outside** the full multi-session overshoot and wick envelope (above the relevant multi-day VWAP and prior session high block for shorts; below the defended multi-session low for longs).
   - Even when entering via `MARKET` or a `Near-Market LIMIT` close to spot, **keep `SL` behind the real structural invalidation level**—never shift `SL` into mid-air noise just because entry is closer to spot.
   - If current market price is over-extended in mid-air so that the real structural `SL` is too far away for a coherent Reward-to-Risk relative to `TP`, **do not force a mid-air trade and do not leave a far-away passive limit order**: either call **`NO_TRADE`** or use a momentum-confirming **`STOP_MARKET`** breakout trigger.
3. **Interior High-Traffic Target Rule**:
   - Anchor `TP` at a high-traffic interior magnet (`12h/24h/72h VWAP`, Volume Point of Control, interior multi-touch shelf, or official cash-session settlement gap for equity/commodity perps), never at an unreached outer wick extreme that has already rejected price multiple times.
4. **Sequence & Falsification Gate (`t_extreme < t_fill`, Market Control, Horizon Stability)**:
   - Verify that the target excursion has not already printed and reversed prior to entry.
   - When backtesting or simulating a setup on historical klines, verify that the edge holds under a near-market/market entry control (not just a limit-discount illusion), remains stable across `24h/48h/72h` horizons, and is not driven by a single outlier ticker.
5. **Corporate Action, Split & Macro-Print Veto**:
   - Never place or hold orders across an impending or fresh (`< 72h`) stock split or futures contract roll where historical klines mix pre- and post-adjustment prices, and never carry a tight stop into an imminent tier-1 macro release.

### 3B. Active Book & Correlation Audit
Inspect active `PENDING` and `OPEN` folders in `trades/` (and run `python3 scripts/stats.py`) before finalizing any new setup:
- **Cap Correlated Same-Direction Exposure**: Never stack 3 or 4 same-direction trades in the same correlation group (e.g., 4 crypto shorts at once). A single macro squeeze will fill and wipe out all correlated tickets simultaneously.
- **Avoid the "Double-Limit" Adverse-Selection Trap**: Never pair a passive `LONG LIMIT` below spot with a passive `SHORT LIMIT` above spot as a "hedge"—in trending markets, only the losing limit fills while the winning limit sits unfilled.

## 4. Decision & Checkmate Conclave (JEV)
Based on all four sources of information:
- chart geometry and dominant trend read
- multi-track research & falsification checks
- settled trade intelligence (the 5 empirical guardrails)
- active book exposure (`PENDING` and `OPEN` trades)

Refine `chart_prediction.svg` and use JEV (`jev_decide`, `jev_classify`, `jev_rerank`, `jev_verify`) to select the optimal execution structure from the **four proven Aster Pro UI setups**:

1. **Setup A — High-Conviction Near-Market Trend Trade (`LIMIT` near spot or `MARKET`, with `TP` & `SL`)**:
   - **When to use**: The chart has a clear dominant trend + VWAP slope, current spot is already near the structural inflection shelf (so a coherent structural `SL` outside the overshoot envelope and an interior magnet `TP` offer strong Reward-to-Risk right from current price), and the active book is not already stacked in that direction.
   - **How to execute**: Place a **Near-Market `LIMIT`** (quoted just off current spot on the bid/ask edge to prevent thin-book slippage while guaranteeing fill participation) or a **`MARKET`** order, with explicit structural `TP` and `SL`.

2. **Setup B — Single-Chart Fade + Tight Breakout Flip (`LIMIT` + `STOP_MARKET` Pair)**:
   - **When to use**: Price is testing a major structural resistance or support shelf where a rejection offers high R:R, but a breakout squeeze through the shelf is a genuine threat.
   - **How to execute**:
     - **Leg 1 (`LIMIT` with `TP/SL`)**: Fade the structural shelf with a tight invalidation `SL` placed just outside the shelf and an interior `TP` (`R:R >= 2:1`).
     - **Leg 2 (Opposite-Side `STOP_MARKET` with `TP/SL`)**: Place a `STOP_MARKET` order in the opposite direction triggered at Leg 1's exact `SL` price, with a tight `SL` back inside the shelf and a wide breakout `TP` (`R:R >= 2.5:1`).
     - **Payoff across states**: If the shelf holds, Leg 1 wins and Leg 2 never triggers (`$0`). If price blasts straight through the shelf on a squeeze, Leg 1 takes a small stop and Leg 2 immediately triggers into the breakout momentum to recover the stop and net a profit.

3. **Setup C — Compressed-Coil Breakout Straddle (`LONG STOP_MARKET` + `SHORT STOP_MARKET` Pair)**:
   - **When to use**: Price is tightly compressed inside a multi-session consolidation coil where directional bias is 50/50 (e.g., post-squeeze consolidation with falling coin-denominated OI), and clean air exists beyond both boundaries.
   - **How to execute**: Place a `LONG STOP_MARKET` just above the coil ceiling and a `SHORT STOP_MARKET` just below the coil floor, each with an asymmetric expansion `TP` and `SL` inside the coil. If price chops inside the range, neither triggers; whichever side breaks out only fills when momentum confirms.

4. **Setup D — Cross-Asset or Relative-Strength Dispersion Pair (Market Scans & Portfolio Balancing)**:
   - **When to use**: When scanning the market for multiple opportunities or when adding a trade while the active book already carries directional exposure.
   - **How to execute**: Pair a trend-aligned `SHORT` on a structurally weak, catalyst-impaired asset (e.g., guidance-cut or regulatory-probed equity/crypto at resistance) with a trend-aligned `LONG` on an uncorrelated asset class (e.g., physical commodity with supply-side tailwinds, or an institutional IPO floor / relative-strength leader).

### Aster Pro Web UI Execution Rule (`asterdex.com/en/trade/pro/futures/<SYMBOL>`)
The user executes manually on the Aster Pro Web UI order panel (`Market` | `Limit` | `Stop Limit ▾ -> Stop Market`).
- In the Aster Pro UI, **`Market`**, **`Limit`**, and **`Stop Market`** each have a one-click **`☑ TP/SL`** checkbox (`Take Profit` + `Stop Loss`).
- **`Trailing Stop`** is a separate order tab (`Callback rate` + `Activation price` + `Reduce-Only`) without a `TP/SL` checkbox and **cannot** be combined into a single `Stop Market` order click.
- Therefore, **always specify explicit `--tp` and `--sl` on every `LIMIT`, `MARKET`, `STOP`, or `STOP_MARKET` ticket** (do not combine `STOP_MARKET` with `--trail` in `finalize.py`).

## 5. Finalize
Write the trade(s) with `finalize.py` (creating a separate folder via `new_trade.py` for each leg of a paired setup and linking them with `--group` and `--role`).

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
tp       = 62000.0               # required for 1-click Aster Pro UI orders
sl       = 58500.0               # required
trail    = 1.5                   # optional legacy/post-fill TRAILING_STOP_MARKET callback rate in %

[schedule]
place_at  = 2026-10-19T09:00:00Z
expire_at = 2026-10-20T21:00:00Z

[checkmate]                      # optional checkmate combination metadata
group    = "BTC-FADE-FLIP"
role     = "FADE_LIMIT"
```

`--price` is required for `LIMIT`, `STOP`, and `STOP_MARKET`, and forbidden for `MARKET`
(though `--ref-price` may be passed to `finalize.py` on `MARKET` orders to print percentage
distances to `TP` and `SL` in the brief output without storing `entry.price` in `trade.toml`).
At least one of `--tp` or `--trail` is required alongside `--sl`, and `STOP`/`STOP_MARKET`
entries must not use `--trail` (since Aster Pro UI does not support combining a Stop Market
entry with a Trailing Stop in a single order). Datetimes look like `2026-10-19T09:00:00Z`.

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
scripts/finalize.py FOLDER (--reject REASON | --side S --type T [--price P] [--ref-price R] [--tp X] --sl Y [--trail R] --expire-at T [--place-at T] [--group G] [--role R])
scripts/resolve_expired.py [--root ROOT] (--list | FOLDER [--now T] [--dry-run])
scripts/set_status.py [--root ROOT] FOLDER NEW_STATUS [--force]
scripts/stats.py [--check] [ROOT]
```

- `finalize.py` takes the decision as parameters, checks the numbers are coherent (TP
  and SL on the right sides of each other and of the entry, valid datetimes, expiry
  after placement, Aster Pro UI order compatibility), writes `trade.toml`, renames the
  folder, prints a BRIEF block. It reads no other file.
- `resolve_expired.py` decides the outcome deterministically from `outcome_candles.csv`:
  it refuses candles that do not cover the whole window or have holes longer than 4
  steps; prefer 1m or 5m candles.

Do not reimplement, wrap, or bypass any of these. Do not pass them flags this manual
does not describe.

## Out of scope

- Live execution, order routing, broker connections, position management.
- Dollar capital allocation across accounts (directional correlation and state coverage across active `PENDING`/`OPEN` journal folders is evaluated during Stage 3B & Stage 4).
- Tax, accounting and reporting formats.
