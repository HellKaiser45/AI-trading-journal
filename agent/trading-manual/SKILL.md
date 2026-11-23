---
name:trading-manual
description:trading manual guidelines to follow whenever the user gives a chart or a trading related request
---

## Pipeline order

The journal runs in one fixed order. Do not reorder it, and do not skip a stage because
it looks unnecessary.

1. Chart analysis, vision only, as described below.
2. Searches: news, on-chain/protocol data, derivatives positioning, macro catalysts, and recent prices.
3. Learning pass over settled recaps, pre-trade chart geometry (`HTF`, `LTF`, `Pos`, `Range`), and active book exposure.
4. Decision: JEV conclave over trend alignment, execution mode (Near-Market `LIMIT`, `MARKET`, or `STOP_MARKET`), volatility-scaled structural `SL` and interior-scaled `TP`, Checkmate structure, expiry, and go or reject.
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

  Then do a thorough chart analysis to find:
  - the **Higher Timeframe (`HTF`, full visible multi-day chart) trend and slope**,
  - the **Lower Timeframe (`LTF`, final quarter of the chart) momentum and slope**,
  - the **Multi-Day Range Position (`Pos = (spot - low) / (high - low)`, from `0.00` at the chart floor to `1.00` at the chart ceiling)** and **total chart range span**,
  - key supports, resistances, VWAP/consolidation shelves, and chart patterns.
  Then draw the `chart_prediction.svg` with those findings.

## 2. Searches
Define and approve what to search, why, and how (parallel, sequential, or mixed) using our decision engine JEV (`jev_decide` / `jev_screen` / `jev_verify`).

### 2A. The 5-Class Information Hierarchy & Initiate-vs-Veto Rule
Separate every piece of research into five distinct classes:
1. **Class 1 — Positioning & Price Geometry (Continuous, Highest Signal-to-Noise)**: Multi-timeframe klines (`15m`, `1h`, `4h`), session/multi-day VWAPs (`12h`, `24h`, `48h`, `72h`, `7d`), ATR envelope, official cash-session close benchmarks (for stock/ETF/commodity perps), funding rates, **coin-denominated Open Interest** (never rely on USD-denominated OI alone, which falls mechanically when price drops), 24h long vs short liquidation skew, and implied volatility (`Deribit DVOL`).
2. **Class 2 — Scheduled Catalysts (Known Volatility Windows)**: Macroeconomic calendar prints (`US Core PCE`, `CPI`, `FOMC`, `NFP`, `PMI`, `EIA Crude Inventories`), earnings dates, stock splits, futures contract roll dates, and token unlocks.
3. **Class 3 — Unscheduled Catalysts & Real-Time Wires**: Breaking regulatory actions, executive/board changes, geopolitical strikes, exchange notices, and primary SEC filings (`SEC EDGAR`).
4. **Class 4 — Implied Crowd Probabilities**: Real-money prediction-market odds on discrete macro, geopolitical, and weekly price-bracket outcomes (`Polymarket`, `Kalshi`).
5. **Class 5 — Structural & On-Chain Thesis**: Protocol TVL, DEX volume, fee/burn revenue (`DefiLlama`), and long-horizon mechanism/protocol research (`ethresear.ch`).

**The Initiate-vs-Veto Rule**:
- **Initiating & Level-Anchoring (`Classes 1 & 2`)**: Entry timing, order type (`Near-Market LIMIT`, `MARKET`, or `STOP_MARKET`), and structural `TP`/`SL` placement must always be anchored in **Class 1** price/positioning geometry and **Class 2** scheduled catalyst windows.
- **Vetoing, Confirming & Sizing (`Classes 3, 4 & 5`)**: Headlines, crowd probabilities, and long-term thesis narratives must **never** be used to chase a counter-structural trade when Class 1 positioning contradicts them; use Classes 3–5 to **veto** dangerous setups (e.g., an unexpected CEO reinstatement or regulatory probe invalidating a thesis), **confirm** breakout triggers (`STOP_MARKET`), or **widen/select** the right Checkmate structure.

### 2B. Chrome Browser Research Playbook (Use Real Chrome for JS/Cloudflare-Gated Terminals)
Several high-value terminals (`Sharpe.ai`, `FinancialJuice`, `CryptoPanic`) block raw `curl` requests (`HTTP 403/429`) or serve empty client-rendered JS shells over raw HTTP, but render **100% free without login** inside the real Chrome browser tool. Use the Chrome browser with the following exact navigation and extraction rules alongside primary REST APIs (`fapi.asterdex.com`, `fapi.binance.com`, `api.llama.fi`, `efts.sec.gov`, `www.deribit.com/api/v2/public/get_volatility_index_data`, `api.elections.kalshi.com`):

1. **`Sharpe.ai` (Cross-Venue Derivatives, Liquidations, OI Delta & RWA Stock/Commodity Perps — Natively Tracks `Aster`)**:
   - *Why Chrome*: Raw HTTP gets `429` rate-limited; Chrome renders the full institutional terminal without login.
   - *Navigation quirk*: Sidebar links collapse; always navigate directly via URL (`goto <url>` + `wait 3500`):
     - `https://www.sharpe.ai/` — Cross-exchange funding rate matrix & APR carry table.
     - `https://www.sharpe.ai/market-brief` — Global Crypto + RWA Open Interest, **24h Liquidations split by Longs vs Shorts** (identifies whether the tape is a long flush or a short squeeze), Fear & Greed Index, stablecoin supply delta, and average RSI.
     - `https://www.sharpe.ai/open-interest` — Per-coin and per-exchange (`Aster`, `Binance`, `Bybit`, `Hyperliquid`, etc.) `1h`, `24h`, `7d`, and `30d` Open Interest changes.
     - `https://www.sharpe.ai/rwa-perps` — Cross-venue RWA Stock, Semiconductor, ETF, and Commodity perpetuals (`NVDA`, `SKHYNIX`, `MU`, `SOXL`, `ANT`, `SPCX`, `QQQ`, `XAU`, `CL`) funding, carry APR, and OI comparison across `Aster` and peer venues.
     - `https://www.sharpe.ai/positioning-risk` — Per-asset `0–10` **Short Pressure** and **Pump/Dump Risk** scores.

2. **`FinancialJuice` (Real-Time Macro Squawk Wire & Economic Calendar)**:
   - *URL*: `https://www.financialjuice.com/home` (`goto` + `wait 4000`).
   - *DOM extraction quirk*: The page loads asynchronously. In `document.body.innerText`:
     - **Characters `0–8,800`** contain the **Economic & Catalyst Calendar** (`Actual / Forecast / Previous` and exact UTC timestamps for `Core PCE`, `CPI`, `FOMC`, `GDP`, `PMI`, `EIA Crude`, holidays, and congressional testimonies).
     - **Characters `8,800+`** contain the **Live Real-Time Squawk Wire** (`document.body.innerText.slice(8000, 16000)`).
     - **Category Tab Filtering**: The feed tabs use `href="#"`, so switch tabs via JS `eval`:
       - **Market-Moving Red Headlines Only**: `document.querySelector('a[data-feedid="10"]').click()`
       - **Crypto Squawk Tab**: `document.querySelector('a[data-feedid="8"]').click()`

3. **`Polymarket` (Real-Money Crowd Probabilities on Macro, Geopolitics & Weekly Crypto Levels)**:
   - *Chrome URLs* (`goto` + `wait 3500`) or REST (`https://gamma-api.polymarket.com/events?limit=20&active=true&closed=false`):
     - `https://polymarket.com/economy` — Fed rate decision probabilities (bps hike/cut/hold), inflation/recession odds, and tariff/rate paths.
     - `https://polymarket.com/crypto` — Weekly and monthly BTC/ETH/SOL price-bracket touch probabilities (`↑` upper strike vs `↓` lower strike).
     - `https://polymarket.com/` — Trending cross-market and geopolitical resolution odds (e.g., Strait of Hormuz shipping normalization, corporate/CEO catalysts).

4. **`CryptoPanic` (Real-Time Crypto/Macro Aggregator & Per-Coin News Timeline)**:
   - *Why Chrome*: Public REST API returns `403` without a key and raw HTML is an empty shell; Chrome renders the full live wire and X/Twitter institutional feed (`@solidintel_x`, `@watcherguru`, `@reutersbiz`) without login.
   - *Navigation & Filter Rule*:
     - Global latest wire: `https://cryptopanic.com/` (`wait 3500`).
     - Per-coin dedicated timeline: `https://cryptopanic.com/news/<coin-slug>/` (e.g., `/news/zcash/`, `/news/uniswap/`, `/news/ethereum/`, `/news/solana/`).
     - **Never use `?filter=hot` or `?filter=rising`**, which surface stale viral posts from days or weeks ago instead of today's breaking news.

5. **`Hacker News` (Early Tech, AI & Semiconductor Catalysts)**:
   - *Chrome URL*: `https://news.ycombinator.com/` or Algolia REST API (`https://hn.algolia.com/api/v1/search_by_date?query=<TERM>&tags=story`).
   - *Use case*: Fastest early-warning signal for major tech, AI, semiconductor (`NVDA`, `AMD`, `MU`, `SKHYNIX`, `ANT`, `OPENAI`), cybersecurity, or regulatory stories; always cross-verify corporate headlines against primary IR/newsrooms or `SEC EDGAR` (`https://efts.sec.gov/LATEST/search-index?q=<TERM>`).

6. **`ethresear.ch` (Structural Ethereum & DeFi Mechanism Thesis)**:
   - *Chrome URL*: `https://ethresear.ch/` or JSON endpoint (`https://ethresear.ch/latest.json`).
   - *Use case*: Class 5 long-horizon protocol/AMM/L2 architecture context; never use as a short-term trade trigger.

Screen external web text with `jev_screen` and verify factual claims with `jev_verify` before logging them in `research_log.txt`.

## 3. Learning pass & Active Book Audit
This is a mandatory two-part step.

### 3A. Settled Trades Review & The 5 Empirical Gain Multipliers
Review settled `recap.md` files and enforce the journal's five backtest-proven gain multipliers (scaling all levels to the specific instrument's measured chart range and volatility structure):

1. **Pre-Trade Range-Position Filter & The Falling-Knife Breakdown Flip (`Lever #1`)**:
   - Compute the pre-trade geometry from `graphpoints.csv`: full-chart trend (`HTF`), final-quarter momentum (`LTF`), and range position (`Pos` in `[0.00, 1.00]`).
   - **Never buy the top of a multi-day range (`LONG` when `Pos > 0.80`)**: Historical journal backtests prove that buying minor dips in the top quintile of a multi-day chart range results in `0%` wins and immediate mean-reversion losses.
   - **Never catch a falling knife with a passive `LONG LIMIT`** when `HTF` and/or `LTF` are declining (`LTF < 0%` or `HTF` in a one-way downtrend), unless price has just completed a deep multi-day capitulation flush at the very bottom of the range (`Pos <= 0.05`) confirmed by coin-denominated OI washout, volume climax, and a wide multi-ATR envelope stop.
   - **Flip Fragile Floors Into Breakdown `SHORT STOP_MARKET` Triggers (and Fragile Ceilings Into Breakout `LONG STOP_MARKET` Triggers)**: When an asset in an `HTF` downtrend is pressing on a weak support shelf (or rolling over from an exhausted `LTF` spike at the top of the range), do **not** place a passive `LONG LIMIT` at the support shelf. Instead, place a **`SHORT STOP_MARKET`** trigger just below that fragile support floor so you capture the breakdown cascade when the floor gives way (and symmetrically, place a **`LONG STOP_MARKET`** above a fragile resistance ceiling in an `HTF` uptrend).

2. **Near-Market Execution on Aligned Trend Setups (`Lever #2 — Defeating Adverse Selection`)**:
   - Historical journal data proves that passive `LIMIT` orders placed far from spot (`> 0.8%–6.0%` away) miss `~44%` of winning trend moves while still filling `100%` of losing moves.
   - When `HTF` and `LTF` are aligned (or an `LTF` pullback has already stalled at the `HTF 48h–72h VWAP` shelf), quote your **`LIMIT` entry on the immediate bid/ask edge very close to spot** (or use `MARKET`) so you achieve `~100%` fill participation without paying thin-book taker slippage.

3. **Multi-Timeframe Conflict Resolution via `STOP_MARKET` Re-Alignment Triggers (`Lever #3 — HTF = Compass, LTF = Trigger`)**:
   - **Higher Timeframe (`4H / 1D`, `48h–72h VWAP` slope & structure)** sets the directional bias and the true invalidation envelope (`SL`). Never chase a Lower Timeframe counter-trend impulse against the Higher Timeframe trend.
   - **When `LTF` Is Actively Expanding Against `HTF` (Counter-Bounce in Progress)**: If `HTF` is bearish but the final quarter of the chart (`LTF`) is actively ripping upward (or `HTF` is bullish and `LTF` is actively dumping), **never step in front of the accelerating `LTF` wave with a passive or near-market `LIMIT` order**. Instead, place a **`STOP_MARKET`** trigger in the `HTF` direction just beyond the `LTF` higher-low/lower-high pivot (just below spot for a short, or just above spot for a long). If the `LTF` counter-move keeps running against the `HTF` trend, your `STOP_MARKET` **never fills (`$0` loss)**; it only triggers the moment the `LTF` counter-bounce breaks down and re-aligns with the `HTF` trend.

4. **Volatility-Scaled Structural Envelope Stop (`Lever #4 — Never Inside Noise`)**:
   - Place `SL` strictly **outside** the full multi-session overshoot and wick envelope (above the `48h–72h VWAP` and prior session high block for shorts; below the defended multi-session low for longs).
   - Size the stop distance proportionally to the instrument's measured multi-day chart range (`>= ~20%` of the visible 5-day chart range span) so normal intraday oscillations and macro prints cannot sweep it before the move develops.
   - Even when entering via `MARKET` or a `Near-Market LIMIT` close to spot, **keep `SL` behind the real structural invalidation shelf**—never shift `SL` into mid-air noise just because entry is closer to spot. If current spot is too far from the structural `SL` for a coherent Reward-to-Risk, use a **`STOP_MARKET`** trigger or call **`NO_TRADE`**.

5. **Interior Target Scaling (`0.70×–0.75×` of Outer Structure) & Full Multi-Session Horizon (`Lever #5`)**:
   - **Interior Target Scaling (`TP`)**: Never place `TP` on an outer wick extreme that has already rejected price. Scale `TP` inward to **`~70%–75%` of the distance to the outer structural extreme** (anchoring at a high-traffic interior magnet such as the `12h/24h/72h VWAP`, Volume Point of Control, or official cash-session close benchmark). Across historical journal trades, interior target scaling converts near-miss `EXPIRED+%` give-backs into full `WIN`s.
   - **Full Structural Hold Window & No Tight Trailing Choke**: Multi-day VWAP and trend continuation swings take `24h–48h` to complete. Give setups a full multi-session (`~48h`) expiry window and **do not attach tight early trailing stops (`1%–1.5%`)**, which historical backtests prove get shaken out by normal intraday noise long before `TP` is reached.
   - **Falsification & Corporate-Action Gates**: Verify sequence (`t_extreme < t_fill`), market-entry control, horizon stability (`24h/48h/72h`), and veto any ticker within `72h` of a stock split or futures contract roll.

### 3B. Active Book & Correlation Audit
Inspect active `PENDING` and `OPEN` folders in `trades/` (and run `python3 scripts/stats.py`) before finalizing any new setup:
- **Cap Correlated Same-Direction Exposure**: Never stack 3 or 4 same-direction trades in the same correlation group (e.g., 4 crypto shorts at once). A single macro squeeze will fill and wipe out all correlated tickets simultaneously.
- **Avoid the "Double-Limit" Adverse-Selection Trap**: Never pair a passive `LONG LIMIT` below spot with a passive `SHORT LIMIT` above spot as a "hedge"—in trending markets, only the losing limit fills while the winning limit sits unfilled.

## 4. Decision & Checkmate Conclave (JEV)
Based on all four sources of information:
- chart geometry (`HTF`, `LTF`, `Pos`, `Range`) and dominant trend read
- multi-track research & falsification checks
- settled trade intelligence (the 5 empirical gain multipliers)
- active book exposure (`PENDING` and `OPEN` trades)

Refine `chart_prediction.svg` and use JEV (`jev_decide`, `jev_classify`, `jev_rerank`, `jev_verify`) to select the optimal execution structure from the **five proven Aster Pro UI setups**:

1. **Setup A — High-Conviction Near-Market Trend Trade (`LIMIT` on bid/ask edge or `MARKET`, with `TP` & `SL`)**:
   - **When to use**: `HTF` trend is clear, `LTF` is aligned (or has already stalled at the `HTF 48h–72h VWAP` shelf), and current spot sits near the structural inflection shelf so a volatility-scaled envelope `SL` and interior-scaled (`0.70×–0.75×`) `TP` offer strong Reward-to-Risk right from current price.
   - **How to execute**: Place a **Near-Market `LIMIT`** (quoted just off current spot on the bid/ask edge to prevent thin-book slippage while guaranteeing fill participation) or a **`MARKET`** order, with explicit structural `TP` and `SL`.

2. **Setup B — MTF Re-Alignment or Fragile-Floor Breakdown `STOP_MARKET` Trigger (`STOP_MARKET` with `TP` & `SL`)**:
   - **When to use**: Either (a) `HTF` is trending down/up while `LTF` is actively counter-bouncing against `HTF`, OR (b) price is pressing a fragile, repeatedly tested support floor in a downtrend (or fragile resistance ceiling in an uptrend) where a passive counter-trend limit order would be catching a falling knife.
   - **How to execute**: Place a **`STOP_MARKET`** trigger just beyond the `LTF` pivot or fragile support/resistance boundary in the `HTF`/breakout direction, with a volatility-scaled structural `SL` and an interior-scaled `TP`. If the level holds or the counter-bounce keeps running, the order never triggers (`$0` loss); if the floor/pivot breaks, you enter immediately with momentum confirmation.

3. **Setup C — Single-Chart Fade + Tight Breakout Flip (`LIMIT` + `STOP_MARKET` Pair)**:
   - **When to use**: Price is testing a major structural resistance or support shelf where a rejection offers high R:R, but a breakout squeeze through the shelf is a genuine threat.
   - **How to execute**:
     - **Leg 1 (`LIMIT` with `TP/SL`)**: Fade the structural shelf with a tight invalidation `SL` placed just outside the shelf and an interior `TP` (`R:R >= 2:1`).
     - **Leg 2 (Opposite-Side `STOP_MARKET` with `TP/SL`)**: Place a `STOP_MARKET` order in the opposite direction triggered at Leg 1's exact `SL` price, with a tight `SL` back inside the shelf and a wide breakout `TP` (`R:R >= 2.5:1`).
     - **Payoff across states**: If the shelf holds, Leg 1 wins and Leg 2 never triggers (`$0`). If price blasts straight through the shelf on a squeeze, Leg 1 takes a small stop and Leg 2 immediately triggers into the breakout momentum to recover the stop and net a profit.

4. **Setup D — Compressed-Coil Breakout Straddle (`LONG STOP_MARKET` + `SHORT STOP_MARKET` Pair)**:
   - **When to use**: Price is tightly compressed inside a multi-session consolidation coil where directional bias is 50/50 (e.g., post-squeeze consolidation with falling coin-denominated OI), and clean air exists beyond both boundaries.
   - **How to execute**: Place a `LONG STOP_MARKET` just above the coil ceiling and a `SHORT STOP_MARKET` just below the coil floor, each with an asymmetric expansion `TP` and `SL` inside the coil. If price chops inside the range, neither triggers; whichever side breaks out only fills when momentum confirms.

5. **Setup E — Cross-Asset or Relative-Strength Dispersion Pair (Market Scans & Portfolio Balancing)**:
   - **When to use**: When scanning the market for multiple opportunities or when adding a trade while the active book already carries directional exposure.
   - **How to execute**: Pair a trend-aligned `SHORT` on a structurally weak, catalyst-impaired asset (e.g., guidance-cut or regulatory-probed equity/crypto at resistance) with a trend-aligned `LONG` on an uncorrelated asset class (e.g., physical commodity with supply-side tailwinds, or an institutional IPO floor / relative-strength leader).

### Aster Pro Web UI Execution Rule (`asterdex.com/en/trade/pro/futures/<SYMBOL>`)
The user executes manually on the Aster Pro Web UI order panel (`Market` | `Limit` | `Stop Limit ▾ -> Stop Market`).
- In the Aster Pro UI, **`Market`**, **`Limit`**, and **`Stop Market`** each have a one-click **`☑ TP/SL`** checkbox (`Take Profit` + `Stop Loss`).
- **`Trailing Stop`** is a separate order tab (`Callback rate` + `Activation price` + `Reduce-Only`) without a `TP/SL` checkbox and **cannot** be combined into a single `Stop Market` order click.
- Therefore, **always specify explicit `--tp` and `--sl` on every `LIMIT`, `MARKET`, `STOP`, or `STOP_MARKET` ticket** (do not combine `STOP_MARKET` with `--trail` in `finalize.py`).

## 5. Finalize
Write the trade(s) with `finalize.py` (creating a separate folder via `new_trade.py` for each leg of a paired setup and linking them with `--group` and `--role`).
`finalize.py` automatically inspects `graphpoints.csv` against the journal's 5 empirical gain guardrails (emitting diagnostic warnings on `stderr` if a setup exhibits top-of-range long chasing, falling-knife passive bidding, counter-LTF passive limit stepping, far-from-spot limit chase, or an under-sized stop envelope) while printing only the clean BRIEF block on `stdout`.

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
  after placement, Aster Pro UI order compatibility), audits pre-trade `graphpoints.csv`
  geometry against the 5 empirical gain guardrails (printing non-blocking warnings to
  `stderr` if a guardrail is breached), writes `trade.toml`, renames the folder, and
  prints a clean BRIEF block to `stdout`.
- `resolve_expired.py` decides the outcome deterministically from `outcome_candles.csv`:
  it refuses candles that do not cover the whole window or have holes longer than 4
  steps; prefer 1m or 5m candles.

Do not reimplement, wrap, or bypass any of these. Do not pass them flags this manual
does not describe.

## Out of scope

- Live execution, order routing, broker connections, position management.
- Dollar capital allocation across accounts (directional correlation and state coverage across active `PENDING`/`OPEN` journal folders is evaluated during Stage 3B & Stage 4).
- Tax, accounting and reporting formats.
