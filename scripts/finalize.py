#!/usr/bin/env python3
'''finalize.py: the only legal way to end an agent run on an IDEA folder.

  finalize.py FOLDER --side LONG|SHORT --type MARKET|LIMIT|STOP|STOP_MARKET [--price P] [--ref-price R] [--tp X] --sl Y [--trail R] --expire-at T [--place-at T] [--group G] [--role R]
  finalize.py FOLDER --reject 'reason'

Takes the decision as parameters, checks the numbers are coherent, audits pre-trade graphpoints.csv
geometry against the journal's 5 empirical gain guardrails (emitting non-blocking warnings on stderr),
writes trade.toml (none for a rejection), then calls set_status.py so the folder becomes PENDING
(LIMIT/STOP/STOP_MARKET), OPEN (MARKET) or REJECTED. Prints the BRIEF block on stdout.
'''
import argparse
import datetime
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'trades'))
sys.path.insert(0, HERE)
from set_status import FOLDER_RE  # noqa: E402
from stats import ENTRY_TYPES, TomlError, read_pretrade_geometry, read_trade_toml, validate_trade, warn  # noqa: E402

NL = chr(10)
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


def resolve(root, folder):
    path = folder if os.path.isdir(folder) else os.path.join(root, folder)
    if not os.path.isdir(path):
        die('folder not found: ' + folder)
    name = os.path.basename(os.path.normpath(path))
    m = FOLDER_RE.match(name)
    if not m or m.group('status') != 'IDEA':
        die('%s is not an IDEA folder' % name)
    return os.path.normpath(path), name, m.group('symbol')


def audit_pretrade_guardrails(path, side, etype, entry_px, tp, sl, place_at):
    """Emit non-blocking stderr warnings if the proposed ticket violates the 5 empirical gain multipliers."""
    g = read_pretrade_geometry(path, place_at)
    if not g:
        return
    spot = g['spot']
    pos = g['pos']
    htf = g['htf_ret']
    ltf = g['ltf_ret']
    rng = g['range_pct']
    ref = entry_px if entry_px is not None else spot

    # 1. Range-Position & Falling-Knife Filter
    if side == 'LONG' and pos > 0.80 and etype == 'LIMIT':
        warn('guardrail #1 (top-of-range LONG): pre-trade Pos=%.2f (>0.80 of chart range); '
             'historical top-quintile LONG LIMITs had 0%% win rate — consider SHORT STOP_MARKET breakdown or wait' % pos)
    if side == 'LONG' and etype in ('LIMIT', 'MARKET') and pos > 0.05 and (ltf < -0.5 or htf < -1.5):
        warn('guardrail #1 (falling-knife LONG): HTF=%+.2f%%, LTF=%+.2f%%, Pos=%.2f; '
             'counter-trend LONG LIMITs in declining trends suffer 100%% adverse fill — consider SHORT STOP_MARKET breakdown trigger' % (
                 htf, ltf, pos))

    # 2. Near-Market Limit Execution (anti-unfilled-chase)
    if etype == 'LIMIT' and entry_px is not None and spot > 0:
        dist_pct = abs(entry_px - spot) / spot * 100.0
        if dist_pct > 1.50:
            warn('guardrail #2 (far passive LIMIT): entry is %.2f%% away from pre-trade spot (%s vs %s); '
                 'historical far limits missed ~44%% of winning trend moves — prefer near-market LIMIT (0.1%%-0.3%%) or STOP_MARKET' % (
                     dist_pct, num(entry_px), num(spot)))

    # 3. Multi-Timeframe Counter-Bounce Conflict
    if side == 'SHORT' and etype in ('LIMIT', 'MARKET') and ltf > 1.50 and pos < 0.85:
        warn('guardrail #3 (LTF counter-bounce in progress): LTF=%+.2f%% against SHORT bias; '
             'stepping in front of an expanding LTF bounce with LIMIT risks early stop-out — consider SHORT STOP_MARKET below LTF pivot' % ltf)
    if side == 'LONG' and etype in ('LIMIT', 'MARKET') and ltf < -1.50 and pos > 0.15:
        warn('guardrail #3 (LTF down-impulse in progress): LTF=%+.2f%% against LONG bias; '
             'consider LONG STOP_MARKET above LTF pivot instead of passive LIMIT' % ltf)

    # 4. Volatility-Scaled Structural Envelope Stop
    if ref > 0 and sl is not None:
        sl_dist_pct = abs(sl - ref) / ref * 100.0
        min_env = max(1.40, min(3.20, 0.15 * rng))
        if sl_dist_pct < min_env:
            warn('guardrail #4 (tight stop inside noise): SL distance is %.2f%% (chart 5d range is %.1f%%, recommended envelope >= %.2f%%); '
                 'tight stops caused 4/4 historical short stop-outs before TP' % (sl_dist_pct, rng, min_env))


def main():
    ap = argparse.ArgumentParser(description='Finish an IDEA folder: PENDING, OPEN or REJECTED.')
    ap.add_argument('--root', default=ROOT)
    ap.add_argument('folder')
    ap.add_argument('--reject', metavar='REASON')
    ap.add_argument('--side', type=str.upper, choices=['LONG', 'SHORT'])
    ap.add_argument('--type', dest='etype', type=str.upper, choices=list(ENTRY_TYPES))
    ap.add_argument('--price', type=float)
    ap.add_argument('--ref-price', dest='ref_price', type=float,
                    help='optional current market reference price for MARKET orders (validates TP/SL & prints %%)')
    ap.add_argument('--tp', type=float)
    ap.add_argument('--sl', type=float)
    ap.add_argument('--trail', type=float, help='TRAILING_STOP_MARKET callback rate in percent')
    ap.add_argument('--place-at', dest='place_at')
    ap.add_argument('--expire-at', dest='expire_at')
    ap.add_argument('--group', help='optional checkmate group identifier')
    ap.add_argument('--role', help='optional checkmate leg role')
    a = ap.parse_args()

    path, name, symbol = resolve(a.root, a.folder)
    root = os.path.dirname(os.path.abspath(path))
    toml_path = os.path.join(path, 'trade.toml')

    if a.reject:
        if os.path.exists(toml_path):
            os.remove(toml_path)
        status, note = 'REJECTED', a.reject
    else:
        for k in ('side', 'etype', 'sl', 'expire_at'):
            if getattr(a, k) is None:
                die('missing --' + k.replace('_', '-'))
        if a.tp is None and a.trail is None:
            die('missing exit target: provide --tp and/or --trail')
        if a.trail is not None and a.trail <= 0:
            die('--trail callback rate must be positive')
        if a.etype in ('STOP', 'STOP_MARKET') and a.trail is not None:
            die('%s cannot be combined with --trail in a single Aster Pro UI order (use --tp and --sl)' % a.etype)
        if a.etype != 'MARKET' and a.price is None:
            die('%s needs --price' % a.etype)
        if a.etype == 'MARKET' and a.price is not None:
            die('MARKET must not have --price (use --ref-price if you want percentage display)')
        now = datetime.datetime.now(datetime.timezone.utc)
        place_at = a.place_at or now.strftime('%Y-%m-%dT%H:%M:%SZ')
        for v in (place_at, a.expire_at):
            if not DT_RE.match(v):
                die('datetimes must look like 2026-10-19T09:00:00Z, got ' + v)
        if a.expire_at <= place_at:
            die('expire-at must be after place-at')
        up = a.side == 'LONG'
        if a.tp is not None:
            if (a.sl >= a.tp) if up else (a.tp >= a.sl):
                die('tp and sl are on the wrong sides of each other for a ' + a.side)
        check_px = a.price if a.price is not None else a.ref_price
        if check_px is not None:
            if (a.sl >= check_px) if up else (check_px >= a.sl):
                die('sl is on the wrong side of entry price for a ' + a.side)
            if a.tp is not None and not ((a.sl < check_px < a.tp) if up else (a.tp < check_px < a.sl)):
                die('entry price must sit between sl and tp')

        audit_pretrade_guardrails(path, a.side, a.etype, check_px, a.tp, a.sl, place_at)

        lines = ['# trade.toml: written by finalize.py, do not edit by hand',
                 'symbol   = ' + q(symbol), 'side     = ' + q(a.side), '',
                 '[entry]', 'type     = ' + q(a.etype)]
        if a.price is not None:
            lines.append('price    = ' + num(a.price))
        lines += ['', '[exit]']
        if a.tp is not None:
            lines.append('tp       = ' + num(a.tp))
        lines.append('sl       = ' + num(a.sl))
        if a.trail is not None:
            lines.append('trail    = ' + num(a.trail))
        lines += ['', '[schedule]', 'place_at  = ' + place_at, 'expire_at = ' + a.expire_at]
        if a.group or a.role:
            lines += ['', '[checkmate]']
            if a.group:
                lines.append('group    = ' + q(a.group))
            if a.role:
                lines.append('role     = ' + q(a.role))
        lines.append('')
        with open(toml_path, 'w', encoding='utf-8') as fh:
            fh.write(NL.join(lines))
        try:
            validate_trade(read_trade_toml(toml_path))
        except (TomlError, OSError) as e:
            die('generated trade.toml is invalid: %s' % e)
        status = 'OPEN' if a.etype == 'MARKET' else 'PENDING'
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
        ref = a.price if a.price is not None else a.ref_price
        entry = '@ ' + num(a.price) if a.price is not None else (
            '@ market (~%s)' % num(a.ref_price) if a.ref_price is not None else '@ market')
        out = ['%s  %s  %s %s' % (symbol, a.side, a.etype, entry)]
        sgn = 1 if up else -1
        parts = []
        if a.tp is not None:
            if ref is not None:
                parts.append('TP %s (%+.2f%%)' % (num(a.tp), sgn * pct(a.tp, ref)))
            else:
                parts.append('TP %s' % num(a.tp))
        if ref is not None:
            parts.append('SL %s (%+.2f%%)' % (num(a.sl), sgn * pct(a.sl, ref)))
        else:
            parts.append('SL %s' % num(a.sl))
        if a.trail is not None:
            parts.append('TRAIL %s%%' % num(a.trail))
        out.append('   '.join(parts))
        out.append('Place %s   Expire %s' % (place_at, a.expire_at))
        out.append('Status: %s   Folder: %s' % (status, newname))
    print(NL.join(out))


if __name__ == '__main__':
    main()
