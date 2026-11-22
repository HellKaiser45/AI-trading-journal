#!/usr/bin/env python3
"""stats.py — summarise trade folders in the journal (stdlib only, Python >= 3.8)."""
import argparse
import csv
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trades'))
FOLDER_RE = re.compile(
    r"^(?P<status>WIN\+\d+\.\d{2}%|LOSS-\d+\.\d{2}%|EXPIRED[+-]\d+\.\d{2}%|IDEA|REJECTED|PENDING|OPEN|EXPIRED)"
    r"_(?P<dt>\d{4}-\d{2}-\d{2}T\d{4}Z)_(?P<symbol>[A-Z0-9]+)(?:-(\d+))?$"
)
TOML_HEADER = re.compile(r"^\[([A-Za-z_][A-Za-z0-9_]*)\]$")
TOML_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.+)$")
NUMBER = re.compile(r"^[+-]?\d+(\.\d+)?$")
DATETIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ENTRY_TYPES = ("MARKET", "LIMIT", "STOP", "STOP_MARKET")
COUNT_ORDER = ["IDEA", "REJECTED", "PENDING", "OPEN", "WIN", "LOSS", "EXPIRED_PCT", "EXPIRED"]
COUNT_LABELS = {"EXPIRED_PCT": "EXPIRED+/-% (in sum)", "EXPIRED": "EXPIRED (bare, never filled)"}
UTC = datetime.timezone.utc


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
    if etype not in ENTRY_TYPES:
        raise TomlError("entry.type must be one of %s" % ", ".join(ENTRY_TYPES))
    price = get("entry", "price", required=(etype != "MARKET"))
    if price is not None and not isinstance(price, float):
        raise TomlError("entry.price must be a number")
    if etype == "MARKET" and price is not None:
        raise TomlError("MARKET entry must not have a price")
    for key in ("tp", "sl", "trail"):
        v = get("exit", key, required=False)
        if v is not None and not isinstance(v, float):
            raise TomlError("exit.%s must be a number" % key)
    tp = get("exit", "tp", required=False)
    sl = get("exit", "sl", required=True)
    trail = get("exit", "trail", required=False)
    if trail is not None and trail <= 0:
        raise TomlError("exit.trail must be positive")
    if etype in ("STOP", "STOP_MARKET") and trail is not None:
        raise TomlError("%s entry cannot be combined with exit.trail in a single Aster Pro UI order" % etype)
    for key in ("place_at", "expire_at"):
        v = get("schedule", key)
        if not isinstance(v, str) or not DATETIME.match(v):
            raise TomlError("schedule.%s must be an unquoted UTC datetime" % key)
    group = get("checkmate", "group", required=False)
    role = get("checkmate", "role", required=False)
    return {
        "symbol": symbol, "side": side, "etype": etype, "price": price,
        "tp": tp, "sl": sl, "trail": trail,
        "place_at": get("schedule", "place_at"),
        "expire_at": get("schedule", "expire_at"),
        "group": group, "role": role,
    }


def _parse_iso(s):
    s = s.strip()
    if s.isdigit():
        v = int(s)
        if v > 10 ** 11:
            v //= 1000
        return datetime.datetime.fromtimestamp(v, UTC)
    d = datetime.datetime.fromisoformat(s.replace(" ", "T").replace("Z", "+00:00"))
    return d.replace(tzinfo=UTC) if d.tzinfo is None else d.astimezone(UTC)


def read_pretrade_geometry(folder_path, place_at_str=None):
    """Extract pre-trade chart geometry (HTF trend, LTF momentum, range position, range span) from graphpoints.csv."""
    gp_path = os.path.join(folder_path, "graphpoints.csv")
    if not os.path.isfile(gp_path):
        return None
    cutoff = None
    if place_at_str:
        try:
            cutoff = _parse_iso(place_at_str)
        except Exception:
            cutoff = None
    if cutoff is None:
        m = FOLDER_RE.match(os.path.basename(os.path.normpath(folder_path)))
        if m:
            dt_tok = m.group("dt")  # YYYY-MM-DDTHHMMZ
            try:
                cutoff = _parse_iso("%s:%s:00Z" % (dt_tok[:13], dt_tok[13:15]))
            except Exception:
                cutoff = None
    pts = []
    try:
        with open(gp_path, encoding="utf-8") as fh:
            lines = [ln for ln in fh if ln.strip() and not ln.lstrip().startswith("#")]
        rd = csv.DictReader(lines)
        for row in rd:
            norm = {k.strip().lower().replace(" ", "_"): v for k, v in row.items() if k}
            t_raw = norm.get("timestamp") or norm.get("time")
            p_raw = norm.get("close_price") or norm.get("close") or norm.get("price")
            if not t_raw or not p_raw:
                continue
            t = _parse_iso(t_raw)
            p = float(p_raw)
            if cutoff is None or t <= cutoff:
                pts.append((t, p))
    except Exception:
        return None
    if len(pts) < 4:
        return None
    pts.sort(key=lambda x: x[0])
    prices = [x[1] for x in pts]
    spot = prices[-1]
    hi, lo = max(prices), min(prices)
    if spot <= 0 or hi <= lo:
        return None
    htf_ret = (spot - prices[0]) / prices[0] * 100.0
    q_idx = max(0, len(prices) - max(2, len(prices) // 4))
    ltf_ret = (spot - prices[q_idx]) / prices[q_idx] * 100.0
    pos = (spot - lo) / (hi - lo)
    range_pct = (hi - lo) / spot * 100.0
    return {
        "spot": spot,
        "high": hi,
        "low": lo,
        "htf_ret": htf_ret,
        "ltf_ret": ltf_ret,
        "pos": pos,
        "range_pct": range_pct,
        "n_points": len(pts),
    }


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
                    help="exit 1 if an IDEA folder remains, or a PENDING/OPEN folder has no trade.toml")
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
            etype = "-"
        else:
            side = info["side"]
            etype = info["etype"]
            if etype == "MARKET":
                entry = "MKT"
            elif etype in ("STOP", "STOP_MARKET"):
                entry = "STP %.2f" % info["price"]
            else:
                entry = "%.2f" % info["price"]
        geom = read_pretrade_geometry(path, info.get("place_at") if info else None)
        rows.append({
            "folder": name, "path": path, "symbol": m.group("symbol"), "side": side, "etype": etype,
            "entry": entry, "status": m.group("status"), "kind": kind, "pct": pct,
            "info": info, "geom": geom,
            "group": info.get("group") if info else None,
            "role": info.get("role") if info else None,
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

    # Side & Execution Breakdown (Settled Trades)
    placed_settled = [r for r in rows if r["kind"] in ("WIN", "LOSS", "EXPIRED_PCT", "EXPIRED")]
    if placed_settled:
        print("Execution & Side Breakdown (settled orders):")
        for s_label in ("SHORT", "LONG"):
            s_rows = [r for r in placed_settled if r["side"] == s_label]
            if not s_rows:
                continue
            s_filled = [r for r in s_rows if r["pct"] is not None]
            s_unfilled = [r for r in s_rows if r["kind"] == "EXPIRED"]
            s_sum = sum(r["pct"] for r in s_filled)
            s_pos = sum(1 for r in s_filled if r["pct"] > 0)
            print("  %-6s placed: %2d | filled: %2d (%d pos / %d neg, sum %s) | unfilled: %2d" % (
                s_label, len(s_rows), len(s_filled), s_pos, len(s_filled) - s_pos,
                fmt_pct(s_sum), len(s_unfilled)))
        # Pre-trade geometry cohort intelligence
        aligned = []
        knife_or_top = []
        for r in placed_settled:
            g = r["geom"]
            if not g:
                continue
            if r["side"] == "LONG" and (g["pos"] > 0.80 or g["ltf_ret"] < 0.0 or g["htf_ret"] < -1.5):
                if g["pos"] > 0.05:
                    knife_or_top.append(r)
                    continue
            aligned.append(r)
        if aligned or knife_or_top:
            al_filled = [r for r in aligned if r["pct"] is not None]
            kt_filled = [r for r in knife_or_top if r["pct"] is not None]
            print("  Pre-trade geometry cohorts:")
            if al_filled:
                al_pos = sum(1 for r in al_filled if r["pct"] > 0)
                print("    Trend/Capitulation-Aligned (%2d orders, %2d filled): %d pos / %d neg, sum %s" % (
                    len(aligned), len(al_filled), al_pos, len(al_filled) - al_pos,
                    fmt_pct(sum(r["pct"] for r in al_filled))))
            if kt_filled:
                kt_pos = sum(1 for r in kt_filled if r["pct"] > 0)
                print("    Top-Chasing/Falling-Knife LONGs (%2d orders, %2d filled): %d pos / %d neg, sum %s" % (
                    len(knife_or_top), len(kt_filled), kt_pos, len(kt_filled) - kt_pos,
                    fmt_pct(sum(r["pct"] for r in kt_filled))))
        print()

    # Per-symbol subtotals
    per_symbol = {}
    for r in terminal:
        per_symbol[r["symbol"]] = per_symbol.get(r["symbol"], 0.0) + r["pct"]
    if per_symbol:
        print("Per-symbol subtotals (terminal %):")
        for sym in sorted(per_symbol):
            print("  %-12s %s" % (sym, fmt_pct(per_symbol[sym])))

    # Active book exposure summary (PENDING + OPEN)
    active = [r for r in rows if r["kind"] in ("PENDING", "OPEN")]
    if active:
        longs = [r for r in active if r["side"] == "LONG"]
        shorts = [r for r in active if r["side"] == "SHORT"]
        print()
        print("Active book exposure (PENDING + OPEN):")
        print("  Total active: %d (%d LONG, %d SHORT)" % (len(active), len(longs), len(shorts)))
        for r in active:
            extra = ""
            if r["group"] or r["role"]:
                extra = " [%s]" % "/".join(x for x in (r["group"], r["role"]) if x)
            print("  %-12s %-5s %-11s %-12s (%s)%s" % (
                r["symbol"], r["side"], r["etype"], r["entry"], r["status"], extra))
        if len(active) >= 2 and (len(longs) == 0 or len(shorts) == 0):
            warn("active book is 100%% one-directional (%d LONG, %d SHORT) — avoid correlated one-way squeeze risk" % (
                len(longs), len(shorts)))
        elif abs(len(longs) - len(shorts)) >= 2:
            warn("active book has directional skew (%d LONG vs %d SHORT) — check correlated exposure before adding same-side tickets" % (
                len(longs), len(shorts)))
        # Detect naive passive double-limit straddles on the same symbol
        by_sym = {}
        for r in active:
            by_sym.setdefault(r["symbol"], []).append(r)
        for sym, srows in sorted(by_sym.items()):
            lim_long = any(x["etype"] == "LIMIT" and x["side"] == "LONG" for x in srows)
            lim_short = any(x["etype"] == "LIMIT" and x["side"] == "SHORT" for x in srows)
            if lim_long and lim_short:
                warn("%s has both LONG LIMIT and SHORT LIMIT active (double-limit adverse-selection trap: trending moves fill only the loser)" % sym)

    if args.check:
        problems = []
        for r in rows:
            if r["kind"] == "IDEA":
                problems.append("%s: still IDEA" % r["folder"])
            if r["kind"] in ("PENDING", "OPEN") and r["side"] == "-":
                problems.append("%s: no trade.toml" % r["folder"])
        for p in problems:
            warn(p)
        return 1 if problems else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
