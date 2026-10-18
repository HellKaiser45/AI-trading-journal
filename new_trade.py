#!/usr/bin/env python3
"""new_trade.py — create an IDEA trade folder from _template/ (stdlib only)."""
import argparse
import datetime
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SYMBOL_RE = re.compile(r"^[A-Z0-9]+$")
PRICE_LINE_RE = re.compile(r"^price[ \t]*=[ \t]*__PRICE__[^\n]*\n", re.MULTILINE)


def die(msg, code=1):
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(description="Create an IDEA trade folder from _template/.")
    ap.add_argument("--root", default=HERE, help="journal root (default: script directory)")
    ap.add_argument("symbol")
    ap.add_argument("side", type=str.upper, choices=["LONG", "SHORT"])
    ap.add_argument("entry_type", type=str.upper, choices=["MARKET", "LIMIT"])
    ap.add_argument("--price", type=float)
    args = ap.parse_args()

    symbol = args.symbol.upper()
    if not SYMBOL_RE.match(symbol):
        die("symbol must be uppercase letters/digits: %r" % args.symbol)
    if args.entry_type == "LIMIT":
        if args.price is None:
            die("LIMIT entry requires --price")
        if args.price <= 0:
            die("--price must be > 0")
    elif args.price is not None:
        die("--price is only valid with LIMIT")

    root = args.root
    template = os.path.join(root, "_template")
    if not os.path.isdir(template):
        die("template not found: %s" % template)

    now = datetime.datetime.now(datetime.timezone.utc)
    base = "IDEA_%s_%s" % (now.strftime("%Y-%m-%dT%H%MZ"), symbol)
    dest = os.path.join(root, base)
    n = 2
    while os.path.exists(dest):
        dest = os.path.join(root, "%s-%d" % (base, n))
        n += 1

    shutil.copytree(template, dest)
    fetched = now.strftime("%Y-%m-%dT%H:%MZ")

    for dirpath, _, files in os.walk(dest):
        for fname in files:
            fpath = os.path.join(dirpath, fname)
            with open(fpath, encoding="utf-8") as fh:
                text = fh.read()
            new = text.replace("__FETCHED_AT__", fetched)
            if fname == "trade.toml":
                new = new.replace("__SYMBOL__", symbol).replace("__SIDE__", args.side)
                new = new.replace("__TYPE__", args.entry_type)
                if args.entry_type == "LIMIT":
                    new = new.replace("__PRICE__", repr(args.price))
                else:
                    new = PRICE_LINE_RE.sub("", new)
            if new != text:
                with open(fpath, "w", encoding="utf-8") as fh:
                    fh.write(new)

    print(dest)


if __name__ == "__main__":
    main()
