#!/usr/bin/env python3
'''new_trade.py: create an IDEA trade folder from _template/ (stdlib only).

  new_trade.py [--root ROOT] SYMBOL

No side, no entry type and no trade.toml: those are decided during research and
written by finalize.py.
'''
import argparse
import datetime
import os
import re
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trades'))
SYMBOL_RE = re.compile(r'^[A-Z0-9]+$')


def die(msg, code=1):
    print('error: ' + msg, file=sys.stderr)
    sys.exit(code)


def main():
    ap = argparse.ArgumentParser(description='Create an IDEA trade folder from _template/.')
    ap.add_argument('--root', default=ROOT, help='journal root (default: trades/ next to scripts/)')
    ap.add_argument('symbol')
    args = ap.parse_args()

    symbol = args.symbol.upper()
    if not SYMBOL_RE.match(symbol):
        die('symbol must be uppercase letters/digits: %r' % args.symbol)

    root = args.root
    template = os.path.join(root, '_template')
    if not os.path.isdir(template):
        die('template not found: %s' % template)

    now = datetime.datetime.now(datetime.timezone.utc)
    base = 'IDEA_%s_%s' % (now.strftime('%Y-%m-%dT%H%MZ'), symbol)
    dest = os.path.join(root, base)
    n = 2
    while os.path.exists(dest):
        dest = os.path.join(root, '%s-%d' % (base, n))
        n += 1

    shutil.copytree(template, dest, ignore=shutil.ignore_patterns('trade.toml'))
    fetched = now.strftime('%Y-%m-%dT%H:%MZ')
    for dirpath, _, files in os.walk(dest):
        for fname in files:
            fpath = os.path.join(dirpath, fname)
            with open(fpath, encoding='utf-8') as fh:
                text = fh.read()
            new = text.replace('__FETCHED_AT__', fetched)
            if new != text:
                with open(fpath, 'w', encoding='utf-8') as fh:
                    fh.write(new)

    print(dest)


if __name__ == '__main__':
    main()
