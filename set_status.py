#!/usr/bin/env python3
"""set_status.py — rename a trade folder to a new status and log the transition (stdlib only)."""
import argparse
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
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


def main():
    ap = argparse.ArgumentParser(description="Rename a trade folder to a new status and log it.")
    ap.add_argument("--root", default=HERE, help="journal root (default: script directory)")
    ap.add_argument("folder", help="folder name (or path) of the trade")
    ap.add_argument("new_status", help="e.g. OPEN, WIN+5.32%%, LOSS-2.10%%, EXPIRED+0.00%%")
    ap.add_argument("--note", default=None, help="short note appended to the log line")
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
        print("warning: transition %s -> %s is not in the state machine" % (old_status, new_status),
              file=sys.stderr)

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

    ts = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%MZ")
    line = "%s %s → %s" % (ts, old_status, new_status)
    if args.note:
        line += " — %s" % args.note
    log_path = os.path.join(newpath, "log.md")
    prefix = ""
    if os.path.exists(log_path) and os.path.getsize(log_path) > 0:
        with open(log_path, "rb") as fh:
            fh.seek(-1, os.SEEK_END)
            if fh.read(1) != b"\n":
                prefix = "\n"
    with open(log_path, "a", encoding="utf-8") as fh:
        fh.write(prefix + line + "\n")

    print("%s -> %s" % (name, newname))


if __name__ == "__main__":
    main()
