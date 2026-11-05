# AI trading journal

A git-tracked journal of trade ideas produced by an AI agent from chart screenshots. Each idea is a folder: the agent reads the chart, forecasts the price path, decides with a probability engine, writes the trade, and later gets graded against real market candles by a deterministic script.

It is a mock journal and a framework: nothing is ever sent to an exchange, and nothing here is financial advice.

## How it works

```
 chart image(s)
      │
      ▼
 1. chart analysis  extract points ─► find structure ─► forecast the price path
      │
      ▼
 2. searches        only the questions the decision engine marks material
      │
      ▼
 3. learning pass   the settled trades' recap.md ─► lessons for levels, stops, fills, expiry
      │
      ▼
 4. decision        Jev (calibrated probabilities): direction, entry, TP, SL, expiry, go / reject
      │
      ▼
      finalize.py ─► PENDING / OPEN / REJECTED folder (+ trade.toml)
      │
      ▼
      after expiry: real candles ─► resolve_expired.py ─► WIN / LOSS / EXPIRED ± %
      │
      ▼
      recap.md (post-mortem: what happened, why, what to change) ─► feeds the next run
      │
      ▼
      stats.py
```

Key ideas:

- **The chart is the pillar.** The agent extracts the data points from the screenshot, finds supports, resistances, trendlines and patterns, and produces a numeric forecast, not only a trade. Every folder holds the history and the predicted path, drawn on a second SVG with a color code (history blue, prediction orange, entry yellow, TP green, SL red).
- **The AI decides, scripts only measure.** Decisions come from Jev, a decision engine that returns calibrated probabilities for choices and yes/no questions. The scripts do not judge any decision: they name folders, write `trade.toml`, and settle trades from real candles.
- **Grading is objective.** Outcomes are computed by `resolve_expired.py` with a fixed fill model, never by the agent.
- **Research follows the horizon.** Searches are driven by questions that can change the forecast inside the trade's horizon, so a 15m chart does not get a generic fundamentals sweep.
- **The journal learns from itself.** Every settled folder carries a `recap.md` — why the trade was taken, why those levels, what the market actually did (measured from the real candles), what worked, what failed, and the lessons. The run order is fixed: 1. chart analysis → 2. searches → 3. learning pass over the settled recaps → 4. decision. Past outcomes therefore tune how a forecast is executed (levels, stops, fill assumptions, expiry) without shaping the forecast itself.
- **The history stays readable.** A recap is capped at ~2,200 characters with a one-line `TL;DR`, so the whole settled history can be skimmed before every decision instead of growing into an unreadable archive.

## Repository layout

```
agent/system_prompt.md          the agent's system prompt
skills/trading-journal/SKILL.md operating manual for the agent (formats, rules, scripts, fill model)
scripts/                        stdlib-only Python helpers
trades/                         one folder per trade idea; trades/_template/ seeds new ones
.githooks/pre-commit            runs the consistency check before each commit
```

## A trade folder

The folder name carries the status: `STATUS_YYYY-MM-DDTHHMMZ_SYMBOL`, for example `PENDING_2026-10-19T0900Z_BTCUSDT` or `WIN+5.32%_2026-10-19T0900Z_BTCUSDT`.

| File | What it is |
|---|---|
| `chart.svg` | SVG replica of the chart image |
| `graphpoints.csv` | the chart points: extracted history, then the forecast after the folder time |
| `chart_prediction.svg` | the chart completed with the forecast and the trade lines |
| `research_log.txt` | dated findings that bear on the forecast, with links |
| `decision_tree.dot` | free-form record of the agent's reasoning |
| `trade.toml` | the trade (side, entry, TP, SL, schedule), written by `finalize.py` |
| `outcome_candles.csv` | real candles used to settle the trade |
| `review.md` | written by `resolve_expired.py` when the trade settles |
| `recap.md` | written on every terminal folder (≤ 2,200 characters, `TL;DR` on line 2): the idea, the plan, the measured path, what worked and what failed, the right trade, and the lessons — the input to the next run's learning pass |

Lifecycle:

```
IDEA -> REJECTED
IDEA -> PENDING (limit order) -> OPEN -> WIN+x% | LOSS-x% | EXPIRED±x%
                              -> EXPIRED (never filled)
IDEA -> OPEN (market order)   -> WIN+x% | LOSS-x% | EXPIRED±x%
```

The full format, state machine and rules are in [`skills/trading-journal/SKILL.md`](skills/trading-journal/SKILL.md).

## Quick start

Requirements: Python 3.8 or newer. No dependencies.

```sh
git clone https://github.com/HellKaiser45/AI-trading-journal.git
cd AI-trading-journal
git config core.hooksPath .githooks       # optional: run the check before each commit

python3 scripts/new_trade.py BTCUSDT      # create an IDEA folder
python3 scripts/finalize.py IDEA_<date>_BTCUSDT --side LONG --type LIMIT --price 60000 --tp 62000 --sl 58500 --expire-at 2026-10-20T21:00:00Z
python3 scripts/resolve_expired.py --list # trades whose expiry has passed
python3 scripts/stats.py                  # results summary
python3 scripts/stats.py --check          # journal consistency check
```

| Script | Purpose |
|---|---|
| `new_trade.py` | creates an IDEA folder from `trades/_template/` |
| `finalize.py` | turns an IDEA into PENDING, OPEN or REJECTED from the parameters it is given |
| `resolve_expired.py` | settles expired trades from real candles using the fill model |
| `set_status.py` | renames a folder through the allowed state machine |
| `stats.py` | per-trade and aggregate results, consistency check |

## Running the agent

The agent is any LLM agent with web access, file and shell tools, and the Jev decision tool.

1. Use [`agent/system_prompt.md`](agent/system_prompt.md) as its system prompt.
2. Give it the [`trading-journal` skill](skills/trading-journal/SKILL.md) so it knows the formats and scripts.
3. Give it a chart screenshot. It creates the folder, analyses, researches, decides and finalizes. When it runs, it also settles any expired trades.

Research tools may write run folders called `research-logs/`; they are git-ignored.

## Results and metrics

- Per-trade result is the price move on one unit of the asset: LONG `(exit - entry) / entry * 100`, SHORT the reverse. No leverage.
- The total is the arithmetic sum of all settled trades, read as "% of one stake". No compounding.
- Win rate is wins over wins plus losses; expired trades are counted separately and rejected ones are excluded.

## Fill model and limits

Backtest-only semantics: all-or-nothing fills, no fees, funding, slippage or partial fills, one identical stake per trade.

- A LIMIT fills when price touches the level (a pullback or retest); a MARKET fills at the next candle's open.
- TP and SL fill at their level on touch. If one candle touches both, it counts as a loss.
- Out of scope: breakout (stop) entries, trailing stops, compounding, fees.

## Contributing

Issues and pull requests are welcome. Keep scripts stdlib-only, keep the folder format stable (it is what the agent and the scripts share), and run `python3 scripts/stats.py --check` before committing.

## License

Apache 2.0, see [LICENSE](LICENSE).
