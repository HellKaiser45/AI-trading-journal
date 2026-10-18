#!/usr/bin/env python3
'''finalize.py: the only legal way to end an agent run on an IDEA folder.

  finalize.py FOLDER --side LONG|SHORT --type MARKET|LIMIT [--price P] --tp X --sl Y --expire-at T [--place-at T]
  finalize.py FOLDER --reject 'reason'

Reads the Jev answers recorded as nodes in FOLDER/decision_tree.dot, writes trade.toml (none for a
rejection), then calls set_status.py so the folder becomes PENDING (LIMIT), OPEN (MARKET) or
REJECTED. Prints the BRIEF block.

A Jev node is ONE line of the dot file with these attributes:
  g1_a [gate=G1, kind=choice, answer=LONG, p=0.71];
  g9_h [gate=G9, kind=noul, answer=setup_holds, p=0.82];
'''
import argparse
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from set_status import FOLDER_RE  # noqa: E402
from stats import TomlError, read_trade_toml, validate_trade  # noqa: E402

NL = chr(10)
GATES = ['G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'G7', 'G8', 'G9']
MIN_NODES = 2      # Jev nodes needed in every gate
MIN_CHOICE = 3     # parallel choice answers needed at G1 and at G9
P_MIN = 0.60       # minimum probability for a decision
AGREE = 1.0        # share of G1 / G9 choice answers that must agree
ATTR_RE = re.compile(r'([a-z_]+)=(?:"([^"]*)"|([^, ]+))')
DT_RE = re.compile(r'^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z$')


def die(msg):
    print('FINALIZE FAILED: ' + msg, file=sys.stderr)
    sys.exit(1)


def q(s):
    return chr(34) + s + chr(34)


def num(x):
    s = ('%.10f' % x).rstrip('0')
    return s + '0' if s.endswith('.') else s


def pct(a, b):
    return (a - b) / b * 100.0


def share(answers):
    return max(answers.count(x) for x in set(answers)) / float(len(answers))


def majority(answers):
    return max(set(answers), key=answers.count)


def resolve(root, folder):
    path = folder if os.path.isdir(folder) else os.path.join(root, folder)
    if not os.path.isdir(path):
        die('folder not found: ' + folder)
    name = os.path.basename(os.path.normpath(path))
    m = FOLDER_RE.match(name)
    if not m or m.group('status') != 'IDEA':
        die('%s is not an IDEA folder' % name)
    return os.path.normpath(path), name, m.group('symbol')


def read_jev(folder):
    path = os.path.join(folder, 'decision_tree.dot')
    if not os.path.isfile(path):
        die('decision_tree.dot is missing')
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    if text.count('{') != text.count('}'):
        die('decision_tree.dot has unbalanced braces')
    out = []
    for raw in text.splitlines():
        s = raw.strip().rstrip(';').strip()
        if s.startswith('//') or '[' not in s or not s.endswith(']'):
            continue
        ident, _, rest = s.partition('[')
        at = dict((k, qv or bv) for k, qv, bv in ATTR_RE.findall(rest[:-1]))
        if 'gate' not in at:
            continue
        try:
            p = float(at.get('p', ''))
        except ValueError:
            p = -1.0
        g, kind, ans = at['gate'], at.get('kind'), at.get('answer')
        if g not in GATES or kind not in ('choice', 'noul') or not ans or not 0.0 <= p <= 1.0:
            die('node %s: a Jev node needs gate=G1..G9, kind=choice|noul, answer=..., p=0..1' % ident.strip())
        out.append((g, kind, ans, p))
    return out


def check_jev(folder, reject, side, etype):
    nodes = read_jev(folder)
    for g in (['G1'] if reject else GATES):
        n = len([x for x in nodes if x[0] == g])
        if n < MIN_NODES:
            die('gate %s has %d Jev nodes in decision_tree.dot, needs %d' % (g, n, MIN_NODES))
    g1 = [(a, p) for g, k, a, p in nodes if g == 'G1' and k == 'choice']
    if len(g1) < MIN_CHOICE:
        die('G1 needs %d choice nodes (parallel calls, shuffled order), found %d' % (MIN_CHOICE, len(g1)))
    if reject:
        return
    a1 = [a for a, p in g1]
    if share(a1) < AGREE:
        die('G1 answers disagree %s: uncertain, use --reject' % a1)
    if majority(a1) != side:
        die('G1 says %s but --side is %s' % (majority(a1), side))
    g9 = [(a, p) for g, k, a, p in nodes if g == 'G9' and k == 'choice']
    if len(g9) < MIN_CHOICE:
        die('G9 needs %d choice nodes (parallel calls, shuffled order), found %d' % (MIN_CHOICE, len(g9)))
    a9 = [a for a, p in g9]
    want = 'GO_' + etype
    if share(a9) < AGREE or majority(a9) != want:
        die('G9 choice nodes must agree on %s, got %s' % (want, a9))
    low = [p for a, p in g9 if a == want and p < P_MIN]
    if low:
        die('G9 %s has answers below %.2f: %s' % (want, P_MIN, low))
    holds = [p for g, k, a, p in nodes if g == 'G9' and k == 'noul' and a == 'setup_holds']
    if not holds or min(holds) < P_MIN:
        die('G9 noul setup_holds is missing or below %.2f' % P_MIN)


def main():
    ap = argparse.ArgumentParser(description='Finish an IDEA folder: PENDING, OPEN or REJECTED.')
    ap.add_argument('--root', default=HERE)
    ap.add_argument('folder')
    ap.add_argument('--reject', metavar='REASON')
    ap.add_argument('--side', type=str.upper, choices=['LONG', 'SHORT'])
    ap.add_argument('--type', dest='etype', type=str.upper, choices=['MARKET', 'LIMIT'])
    ap.add_argument('--price', type=float)
    ap.add_argument('--tp', type=float)
    ap.add_argument('--sl', type=float)
    ap.add_argument('--place-at', dest='place_at')
    ap.add_argument('--expire-at', dest='expire_at')
    a = ap.parse_args()

    path, name, symbol = resolve(a.root, a.folder)
    root = os.path.dirname(os.path.abspath(path))
    toml_path = os.path.join(path, 'trade.toml')

    if a.reject:
        check_jev(path, True, None, None)
        if os.path.exists(toml_path):
            os.remove(toml_path)
        status, note = 'REJECTED', a.reject
    else:
        for k in ('side', 'etype', 'tp', 'sl', 'expire_at'):
            if getattr(a, k) is None:
                die('missing --' + k.replace('_', '-'))
        if a.etype == 'LIMIT' and a.price is None:
            die('LIMIT needs --price')
        if a.etype == 'MARKET' and a.price is not None:
            die('MARKET must not have --price')
        now = datetime.datetime.now(datetime.timezone.utc)
        place_at = a.place_at or now.strftime('%Y-%m-%dT%H:%M:%SZ')
        for v in (place_at, a.expire_at):
            if not DT_RE.match(v):
                die('datetimes must look like 2026-10-19T09:00:00Z, got ' + v)
        if a.expire_at <= place_at:
            die('expire-at must be after place-at')
        up = a.side == 'LONG'
        if (a.sl >= a.tp) if up else (a.tp >= a.sl):
            die('tp and sl are on the wrong sides of each other for a ' + a.side)
        if a.price is not None and not ((a.sl < a.price < a.tp) if up else (a.tp < a.price < a.sl)):
            die('entry price must sit between sl and tp')
        check_jev(path, False, a.side, a.etype)
        lines = ['# trade.toml: written by finalize.py, do not edit by hand',
                 'symbol   = ' + q(symbol), 'side     = ' + q(a.side), '',
                 '[entry]', 'type     = ' + q(a.etype)]
        if a.price is not None:
            lines.append('price    = ' + num(a.price))
        lines += ['', '[exit]', 'tp       = ' + num(a.tp), 'sl       = ' + num(a.sl), '',
                  '[schedule]', 'place_at  = ' + place_at, 'expire_at = ' + a.expire_at, '']
        with open(toml_path, 'w', encoding='utf-8') as fh:
            fh.write(NL.join(lines))
        try:
            validate_trade(read_trade_toml(toml_path))
        except (TomlError, OSError) as e:
            die('generated trade.toml is invalid: %s' % e)
        status = 'PENDING' if a.etype == 'LIMIT' else 'OPEN'
        note = '%s order via finalize.py' % a.etype.lower()

    res = subprocess.run([sys.executable, os.path.join(HERE, 'set_status.py'), '--root', root,
                          name, status, '--note', note],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if res.returncode != 0:
        die('set_status.py refused: ' + res.stderr.strip())
    newname = res.stdout.strip().split(' -> ')[-1]
    if os.path.isdir(os.path.join(root, name)) or not os.path.isdir(os.path.join(root, newname)):
        die('folder rename did not happen as expected')

    if status == 'REJECTED':
        out = ['%s  REJECTED' % symbol, 'Reason: ' + a.reject, 'Folder: ' + newname]
    else:
        entry = '@ ' + num(a.price) if a.price is not None else '@ market'
        out = ['%s  %s  %s %s' % (symbol, a.side, a.etype, entry)]
        if a.price is not None:
            sgn = 1 if up else -1
            out.append('TP %s (%+.2f%%)   SL %s (%+.2f%%)' % (
                num(a.tp), sgn * pct(a.tp, a.price), num(a.sl), sgn * pct(a.sl, a.price)))
        else:
            out.append('TP %s   SL %s' % (num(a.tp), num(a.sl)))
        out.append('Place %s   Expire %s' % (place_at, a.expire_at))
        out.append('Status: %s   Folder: %s' % (status, newname))
    print(NL.join(out))


if __name__ == '__main__':
    main()
