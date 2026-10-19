#!/usr/bin/env python3
"""set_status.py — rename a trade folder to a new status (stdlib only). The folder name is the record."""
import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trades'))
STATUS_RE = re.compile(
    r"^(?:WIN\+\d+\.\d{2}%|LOSS-\d+\.\d{2}%|EXPIRED[+-]\d+\.\d{2}%|IDEA|REJECTED|PENDING|OPEN|EXPIRED)$"
)
FOLDER_RE = re.compile(
    r"^(?P<status>WIN\+\d+\.\d{2}%|LOSS-\d+\.\d{2}%|EXPIRED[+-]\d+\.\d{2}%|IDEA|REJECTED|PENDING|OPEN|EXPIRED)"
    r"_(?P<dt>\d{4}-\d{2}-\d{2}T\d{4}Z)_(?P<symbol>[A-Z0-9]+)(?:-\d+)?$"
)
# State machine over status kinds (terminal kinds have no outgoing edges).
ALLOWED = {
    "IDEA": {"REJECTED", "PENDING", "OPEN"},
    "PENDING": {"OPEN", "EXPIRED"},
    "OPEN": {"WIN", "LOSS", "EXPIRED_PCT"},
}


def die(msg, code=1):
    print("error: " + msg, file=sys.stderr)
    sys.exit(code)


def kind_of(status):
    if status.startswith("WIN+"):
        return "WIN"
    if status.startswith("LOSS-"):
        return "LOSS"
    if status.startswith("EXPIRED+") or status.startswith("EXPIRED-"):
        return "EXPIRED_PCT"
    return status

def entry_type(path):
    try:
        with open(os.path.join(path, 'trade.toml'), encoding='utf-8') as fh:
            m = re.search(r'^[ ]*type[ ]*=[ ]*.(MARKET|LIMIT)', fh.read(), re.M)
    except OSError:
        return None
    return m.group(1) if m else None


def main():
    ap = argparse.ArgumentParser(description="Rename a trade folder to a new status.")
    ap.add_argument("--root", default=ROOT, help="journal root (default: trades/ next to scripts/)")
    ap.add_argument("folder", help="folder name (or path) of the trade")
    ap.add_argument("new_status", help="e.g. OPEN, WIN+5.32%%, LOSS-2.10%%, EXPIRED+0.00%%")
    ap.add_argument("--note", default=None, help="accepted for compatibility; not recorded")
    ap.add_argument("--force", action="store_true", help="suppress the state-machine warning")
    args = ap.parse_args()

    root = args.root
    if not os.path.isdir(root):
        die("ROOT not found: %s" % root)

    path = args.folder if os.path.isdir(args.folder) else os.path.join(root, args.folder)
    if not os.path.isdir(path):
        die("folder not found: %s" % args.folder)
    name = os.path.basename(os.path.normpath(path))

    m = FOLDER_RE.match(name)
    if not m:
        die("not a valid trade folder name: %s" % name)

    new_status = args.new_status
    if not STATUS_RE.match(new_status):
        die("invalid status: %r" % new_status)

    old_status = m.group("status")
    dt = m.group("dt")
    symbol = m.group("symbol")
    if new_status == old_status:
        die("folder already has status %s" % old_status)

    old_kind, new_kind = kind_of(old_status), kind_of(new_status)
    if not args.force and new_kind not in ALLOWED.get(old_kind, set()):
        die('transition %s -> %s is not in the state machine (--force to override)' % (old_status, new_status))
    if old_status == 'IDEA' and new_status in ('PENDING', 'OPEN'):
        etype = entry_type(path)
        if etype is None:
            die('no valid trade.toml: use finalize.py, not set_status.py, to leave IDEA')
        if new_status == 'PENDING' and etype != 'LIMIT':
            die('PENDING needs entry.type = LIMIT (MARKET goes straight to OPEN)')
        if new_status == 'OPEN' and etype != 'MARKET':
            die('IDEA -> OPEN needs entry.type = MARKET (LIMIT goes to PENDING)')
    if new_status == 'REJECTED' and os.path.exists(os.path.join(path, 'trade.toml')):
        die('REJECTED folders must not contain trade.toml')

    base = "%s_%s_%s" % (new_status, dt, symbol)
    candidate = base
    n = 2
    while os.path.exists(os.path.join(root, candidate)):
        candidate = "%s-%d" % (base, n)
        n += 1
    newname = candidate
    newpath = os.path.join(root, newname)

    check = FOLDER_RE.match(newname)
    if not check or check.group("dt") != dt or check.group("symbol") != symbol:
        die("internal error: date/symbol tokens would change; refusing rename")

    os.rename(path, newpath)

    print("%s -> %s" % (name, newname))


if __name__ == "__main__":
    main()
