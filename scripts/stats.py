#!/usr/bin/env python3
"""stats.py — summarise trade folders in the journal (stdlib only, Python >= 3.8)."""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trades'))
FOLDER_RE = re.compile(
    r"^(?P<status>WIN\+\d+\.\d{2}%|LOSS-\d+\.\d{2}%|EXPIRED[+-]\d+\.\d{2}%|IDEA|REJECTED|PENDING|OPEN|EXPIRED)"
    r"_(?P<dt>\d{4}-\d{2}-\d{2}T\d{4}Z)_(?P<symbol>[A-Z0-9]+)(?:-\d+)?$"
)
TOML_HEADER = re.compile(r"^\[([A-Za-z_][A-Za-z0-9_]*)\]$")
TOML_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$")
NUMBER = re.compile(r"^[+-]?\d+(\.\d+)?$")
DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
COUNT_ORDER = ["IDEA", "REJECTED", "PENDING", "OPEN", "WIN", "LOSS", "EXPIRED_PCT", "EXPIRED"]
COUNT_LABELS = {"EXPIRED_PCT": "EXPIRED+/-% (in sum)", "EXPIRED": "EXPIRED (bare, never filled)"}


class TomlError(Exception):
    pass


def warn(msg):
    print("warning: " + msg, file=sys.stderr)


def _strip_comment(line):
    in_str = False
    for i, ch in enumerate(line):
        if ch == '"':
            in_str = not in_str
        elif ch == "#" and not in_str:
            return line[:i]
    return line


def _parse_value(raw):
    if len(raw) >= 2 and raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    if NUMBER.match(raw):
        return float(raw)
    if DATETIME.match(raw):
        return raw
    raise TomlError("unsupported value: %r" % raw)


def read_trade_toml(path):
    data = {}
    section = ""
    with open(path, encoding="utf-8") as fh:
        for lineno, raw in enumerate(fh, 1):
            line = _strip_comment(raw).strip()
            if not line:
                continue
            m = TOML_HEADER.match(line)
            if m:
                section = m.group(1)
                continue
            m = TOML_KEY.match(line)
            if not m:
                raise TomlError("line %d: cannot parse %r" % (lineno, line))
            key = (section, m.group(1))
            if key in data:
                raise TomlError("line %d: duplicate key %s" % (lineno, m.group(1)))
            try:
                data[key] = _parse_value(m.group(2).strip())
            except TomlError as e:
                raise TomlError("line %d: %s" % (lineno, e))
    return data


def validate_trade(data):
    def get(section, key, required=True):
        k = (section, key)
        if k not in data:
            if required:
                raise TomlError("missing %s.%s" % (section or "top-level", key))
            return None
        return data[k]

    symbol = get("", "symbol")
    if not isinstance(symbol, str) or not symbol:
        raise TomlError("symbol must be a non-empty string")
    side = get("", "side")
    if side not in ("LONG", "SHORT"):
        raise TomlError("side must be LONG or SHORT")
    etype = get("entry", "type")
    if etype not in ("MARKET", "LIMIT"):
        raise TomlError("entry.type must be MARKET or LIMIT")
    price = get("entry", "price", required=(etype == "LIMIT"))
    if price is not None and not isinstance(price, float):
        raise TomlError("entry.price must be a number")
    if etype == "MARKET" and price is not None:
        raise TomlError("MARKET entry must not have a price")
    for key in ("tp", "sl"):
        v = get("exit", key, required=False)
        if v is not None and not isinstance(v, float):
            raise TomlError("exit.%s must be a number" % key)
    for key in ("place_at", "expire_at"):
        v = get("schedule", key)
        if not isinstance(v, str) or not DATETIME.match(v):
            raise TomlError("schedule.%s must be an unquoted UTC datetime" % key)
    return {"symbol": symbol, "side": side, "etype": etype, "price": price}


def parse_status(status):
    if status.startswith("WIN+"):
        return "WIN", float(status[3:-1])
    if status.startswith("LOSS-"):
        return "LOSS", float(status[4:-1])
    if status.startswith("EXPIRED+") or status.startswith("EXPIRED-"):
        return "EXPIRED_PCT", float(status[7:-1])
    return status, None


def fmt_pct(v):
    return "-" if v is None else "%+.2f%%" % v


def main(argv=None):
    ap = argparse.ArgumentParser(description="Summarise trade folders in the journal.")
    ap.add_argument("root", nargs="?", default=ROOT, help="journal root (default: trades/ next to scripts/)")
    ap.add_argument("--check", action="store_true",
                    help="exit 1 if an IDEA folder remains, or a non-IDEA folder has no log.md")
    args = ap.parse_args(argv)

    root = args.root
    if not os.path.isdir(root):
        print("error: ROOT not found: %s" % root, file=sys.stderr)
        return 1

    rows = []
    for name in sorted(os.listdir(root)):
        path = os.path.join(root, name)
        if name.startswith(".") or name.startswith("_") or not os.path.isdir(path):
            continue
        m = FOLDER_RE.match(name)
        if not m:
            warn("skip %s: malformed folder name" % name)
            continue
        kind, pct = parse_status(m.group("status"))
        info = None
        toml_path = os.path.join(path, "trade.toml")
        if os.path.exists(toml_path):
            try:
                info = validate_trade(read_trade_toml(toml_path))
            except (TomlError, OSError, UnicodeDecodeError) as e:
                warn("skip %s: %s" % (name, e))
                continue
        if info is None:
            entry = "-"
            side = "-"
        else:
            side = info["side"]
            entry = "MKT" if info["etype"] == "MARKET" else "%.2f" % info["price"]
        rows.append({
            "folder": name, "symbol": m.group("symbol"), "side": side, "entry": entry,
            "status": m.group("status"), "kind": kind, "pct": pct,
        })

    # Per-trade table
    header = ("FOLDER", "SYMBOL", "SIDE", "ENTRY", "STATUS", "PCT")
    table = [header] + [
        (r["folder"], r["symbol"], r["side"], r["entry"], r["status"], fmt_pct(r["pct"])) for r in rows
    ]
    widths = [max(len(row[i]) for row in table) for i in range(len(header))]
    for row in table:
        print("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip())
    if not rows:
        print("(no trade folders found)")
    print()

    # Status counts
    counts = {}
    for r in rows:
        counts[r["kind"]] = counts.get(r["kind"], 0) + 1
    print("Status counts:")
    for k in COUNT_ORDER:
        if k in counts:
            print("  %-28s %d" % (COUNT_LABELS.get(k, k), counts[k]))
    print()

    # Metrics (REJECTED and non-% statuses excluded)
    terminal = [r for r in rows if r["pct"] is not None]
    total = sum(r["pct"] for r in terminal)
    wins = [r["pct"] for r in rows if r["kind"] == "WIN"]
    losses = [r["pct"] for r in rows if r["kind"] == "LOSS"]
    expired_pct = sum(1 for r in rows if r["kind"] == "EXPIRED_PCT")
    print("Metrics:")
    print("  Arithmetic sum of terminal %%: %s" % fmt_pct(total if terminal else None) if terminal else
          "  Arithmetic sum of terminal %:  0.00%")
    print("  Expired-with-pct count:       %d" % expired_pct)
    if wins or losses:
        print("  Win rate (WIN/(WIN+LOSS)):    %.1f%%" % (100.0 * len(wins) / (len(wins) + len(losses))))
    else:
        print("  Win rate (WIN/(WIN+LOSS)):    n/a")
    print("  Avg win:                      %s" % (fmt_pct(sum(wins) / len(wins)) if wins else "n/a"))
    print("  Avg loss:                     %s" % (fmt_pct(sum(losses) / len(losses)) if losses else "n/a"))
    print()

    # Per-symbol subtotals
    per_symbol = {}
    for r in terminal:
        per_symbol[r["symbol"]] = per_symbol.get(r["symbol"], 0.0) + r["pct"]
    if per_symbol:
        print("Per-symbol subtotals (terminal %):")
        for sym in sorted(per_symbol):
            print("  %-12s %s" % (sym, fmt_pct(per_symbol[sym])))

    if args.check:
        problems = []
        for r in rows:
            if r["kind"] == "IDEA":
                problems.append("%s: still IDEA" % r["folder"])
            elif not os.path.exists(os.path.join(root, r["folder"], "log.md")):
                problems.append("%s: no log.md (renamed by hand?)" % r["folder"])
            if r["kind"] in ("PENDING", "OPEN") and r["side"] == "-":
                problems.append("%s: no trade.toml" % r["folder"])
        for p in problems:
            warn(p)
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())