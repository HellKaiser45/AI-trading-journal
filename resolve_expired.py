#!/usr/bin/env python3
'''resolve_expired.py: settle PENDING / OPEN folders whose expire_at has passed.

  resolve_expired.py --list [--now T]
  resolve_expired.py FOLDER [--now T] [--dry-run]

--list prints one line per expired PENDING/OPEN folder: what market data to fetch.
FOLDER needs FOLDER/outcome_candles.csv (header time,open,high,low,close; UTC; any timeframe,
the finer the better) covering place_at to expire_at. The script replays the fill model,
renames the folder through set_status.py (PENDING -> OPEN -> result when a limit filled)
and writes review.md.
'''
import argparse
import csv
import datetime
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from set_status import FOLDER_RE  # noqa: E402
from stats import TomlError, read_trade_toml, validate_trade  # noqa: E402

UTC = datetime.timezone.utc
NL = chr(10)
TIME_COLS = ('time', 'timestamp', 'open_time', 'datetime', 'date')


def die(msg):
    print('RESOLVE FAILED: ' + msg, file=sys.stderr)
    sys.exit(1)


def parse_time(s):
    s = s.strip()
    if s.isdigit():
        v = int(s)
        if v > 10 ** 11:
            v //= 1000
        return datetime.datetime.fromtimestamp(v, UTC)
    d = datetime.datetime.fromisoformat(s.replace(' ', 'T').replace('Z', '+00:00'))
    return d.replace(tzinfo=UTC) if d.tzinfo is None else d.astimezone(UTC)


def ts(d):
    return d.strftime('%Y-%m-%dT%H:%M:%SZ')


def px(x):
    return '-' if x is None else ('%.10f' % x).rstrip('0').rstrip('.')


def load_trade(path):
    try:
        d = read_trade_toml(os.path.join(path, 'trade.toml'))
        info = validate_trade(d)
    except (TomlError, OSError) as e:
        die('bad trade.toml in %s: %s' % (path, e))
    info['tp'] = d.get(('exit', 'tp'))
    info['sl'] = d.get(('exit', 'sl'))
    info['place_at'] = parse_time(d[('schedule', 'place_at')])
    info['expire_at'] = parse_time(d[('schedule', 'expire_at')])
    return info


def load_candles(path, t0, t1):
    f = os.path.join(path, 'outcome_candles.csv')
    if not os.path.isfile(f):
        die('outcome_candles.csv is missing in ' + path)
    rows = {}
    with open(f, newline='', encoding='utf-8') as fh:
        rd = csv.DictReader(fh)
        rd.fieldnames = [x.strip().lower() for x in (rd.fieldnames or [])]
        tcol = None
        for c in TIME_COLS:
            if c in rd.fieldnames:
                tcol = c
                break
        if tcol is None or any(c not in rd.fieldnames for c in ('open', 'high', 'low', 'close')):
            die('outcome_candles.csv needs a header with time,open,high,low,close')
        for r in rd:
            try:
                rows[parse_time(r[tcol])] = tuple(float(r[k]) for k in ('open', 'high', 'low', 'close'))
            except (ValueError, KeyError, TypeError):
                die('unreadable row in outcome_candles.csv: %r' % (r,))
    times = sorted(t for t in rows if t0 <= t < t1)
    if len(times) < 2:
        die('fewer than 2 candles between place_at and expire_at')
    gaps = [b - a for a, b in zip(times, times[1:])]
    step = min(gaps)
    if times[0] - t0 > 2 * step or t1 - times[-1] > 2 * step:
        die('candles do not cover place_at to expire_at (step %s): fetch the full window' % step)
    if max(gaps) > 4 * step:
        die('candle series has holes longer than 4 steps: fetch it again')
    return [(t,) + rows[t] for t in times], step


def replay(info, candles):
    # candle = (time, open, high, low, close)
    up = info['side'] == 'LONG'
    tp, sl, entry = info['tp'], info['sl'], info['price']

    def touches_tp(c):
        return tp is not None and ((c[2] >= tp) if up else (c[3] <= tp))

    def touches_sl(c):
        return sl is not None and ((c[3] <= sl) if up else (c[2] >= sl))

    fill_i, fill_px, tp_from = 0, None, 0
    if info['etype'] == 'LIMIT':
        fill_i = None
        for i, c in enumerate(candles):
            if (c[3] <= entry) if up else (c[2] >= entry):
                fill_i = i
                break
        if fill_i is None:
            return {'kind': 'EXPIRED', 'pct': 0.0}
        fill_px, tp_from = entry, fill_i + 1   # TP in the fill candle: order unknown, ignored
    else:
        fill_px = candles[0][1]

    def done(kind, exit_px, i):
        p = (exit_px - fill_px) / fill_px * 100.0
        return {'kind': kind, 'pct': p if up else -p, 'fill_i': fill_i, 'fill_px': fill_px,
                'exit_i': i, 'exit_px': exit_px}

    for i in range(fill_i, len(candles)):
        c = candles[i]
        if touches_sl(c):                       # SL first: a candle touching both is a LOSS
            return done('LOSS', sl, i)
        if i >= tp_from and touches_tp(c):
            return done('WIN', tp, i)
    return done('EXPIRED_PCT', candles[-1][4], len(candles) - 1)


def status_of(res):
    k, p = res['kind'], res['pct']
    if k == 'WIN':
        return 'WIN+%.2f%%' % abs(p)
    if k == 'LOSS':
        return 'LOSS-%.2f%%' % abs(p)
    if k == 'EXPIRED_PCT':
        return 'EXPIRED%s%.2f%%' % ('-' if p <= -0.005 else '+', abs(p))
    return 'EXPIRED'


def set_status(root, name, status, note):
    r = subprocess.run([sys.executable, os.path.join(HERE, 'set_status.py'), '--root', root,
                        name, status, '--note', note],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if r.returncode != 0:
        die('set_status.py refused %s -> %s: %s' % (name, status, r.stderr.strip()))
    return r.stdout.strip().split(' -> ')[-1]


def write_review(path, final, res, candles, step, info):
    lines = ['# Review: ' + os.path.basename(path), '', 'Outcome: ' + final,
             'Window: %s to %s, %d candles, step %s (outcome_candles.csv)' % (
                 ts(info['place_at']), ts(info['expire_at']), len(candles), step)]
    if 'fill_i' in res:
        lines.append('Fill: %s at %s (candle %s)' % (
            info['etype'], px(res['fill_px']), ts(candles[res['fill_i']][0])))
        lines.append('Exit: %s at %s (candle %s)' % (
            res['kind'], px(res['exit_px']), ts(candles[res['exit_i']][0])))
    else:
        lines.append('Fill: the limit was never touched before expire_at')
    lines += ['', 'Rules: limit fills at its price on touch; TP and SL fill at their level on touch;',
              'a candle touching both is a LOSS; TP in the limit fill candle is ignored;',
              'expiry price = close of the last candle before expire_at.']
    with open(os.path.join(path, 'review.md'), 'w', encoding='utf-8') as fh:
        fh.write(NL.join(lines) + NL)


def main():
    ap = argparse.ArgumentParser(description='Settle expired PENDING/OPEN folders.')
    ap.add_argument('--root', default=HERE)
    ap.add_argument('folder', nargs='?')
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--now')
    ap.add_argument('--dry-run', action='store_true')
    a = ap.parse_args()
    now = parse_time(a.now) if a.now else datetime.datetime.now(UTC)
    root = os.path.abspath(a.root)

    if a.list or not a.folder:
        found = 0
        for name in sorted(os.listdir(root)):
            m = FOLDER_RE.match(name)
            path = os.path.join(root, name)
            if not m or m.group('status') not in ('PENDING', 'OPEN') or not os.path.isdir(path):
                continue
            info = load_trade(path)
            if info['expire_at'] > now:
                continue
            found += 1
            print('FOLDER=%s SYMBOL=%s SIDE=%s TYPE=%s ENTRY=%s TP=%s SL=%s FROM=%s TO=%s' % (
                name, info['symbol'], info['side'], info['etype'], px(info['price']),
                px(info['tp']), px(info['sl']), ts(info['place_at']), ts(info['expire_at'])))
        if not found:
            print('nothing to resolve')
        return

    path = os.path.abspath(a.folder if os.path.isdir(a.folder) else os.path.join(root, a.folder))
    name = os.path.basename(path)
    root = os.path.dirname(path)
    m = FOLDER_RE.match(name)
    if not os.path.isdir(path) or not m or m.group('status') not in ('PENDING', 'OPEN'):
        die('%s is not a PENDING or OPEN folder' % name)
    info = load_trade(path)
    if info['expire_at'] > now:
        die('%s has not expired yet (expire_at %s)' % (name, ts(info['expire_at'])))
    candles, step = load_candles(path, info['place_at'], info['expire_at'])
    res = replay(info, candles)
    final = status_of(res)
    if m.group('status') == 'OPEN' and res['kind'] == 'EXPIRED':
        die('journal says OPEN but the candles never reach the limit: check by hand')
    if a.dry_run:
        print('%s would become %s' % (name, final))
        return
    cur = name
    if m.group('status') == 'PENDING' and res['kind'] != 'EXPIRED':
        cur = set_status(root, cur, 'OPEN', 'limit filled in candle %s' % ts(candles[res['fill_i']][0]))
    notes = {'WIN': 'tp touched', 'LOSS': 'sl touched', 'EXPIRED_PCT': 'still open at expire_at',
             'EXPIRED': 'never filled by expire_at'}
    cur = set_status(root, cur, final, notes[res['kind']] + ' (resolve_expired.py)')
    write_review(os.path.join(root, cur), final, res, candles, step, info)
    print('%s -> %s' % (name, cur))


if __name__ == '__main__':
    main()