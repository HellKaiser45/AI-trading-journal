import json, math, statistics, datetime

def ts2date(ms):
    return datetime.datetime.fromtimestamp(ms/1000, datetime.timezone.utc).strftime('%Y-%m-%d')

# --- Binance daily klines ---
d = json.load(open('raw/binance-1d-klines.json'))
rows = [(ts2date(k[0]), float(k[1]), float(k[2]), float(k[3]), float(k[4]), float(k[5]), float(k[7]), k[8]) for k in d]
closes = [r[4] for r in rows]
rets = [math.log(closes[i]/closes[i-1]) for i in range(1, len(closes))]
sd = statistics.stdev(rets)
print("DAILY (Binance spot, UTC)")
print("rows:", len(rows), "| first:", rows[0][0], "| last:", rows[-1][0])
print("close range:", min(closes), "-", max(closes), "| last close:", closes[-1])
print("high_max:", max(r[2] for r in rows), "| low_min:", min(r[3] for r in rows))
print("daily log-return sigma: %.5f -> annualized %.1f%% (x sqrt(365))" % (sd, sd*math.sqrt(365)*100))
print("mean |daily ret|: %.2f%%" % (100*statistics.mean(abs(r) for r in rets)))
print("30d close-to-close change: %.2f%%" % (100*(closes[-1]/closes[1]-1)))
# ATR14 Wilder on TR
trs = []
for i in range(1, len(rows)):
    h, l, pc = rows[i][2], rows[i][3], rows[i-1][4]
    trs.append(max(h-l, abs(h-pc), abs(l-pc)))
atr = sum(trs[:14])/14
for tr in trs[14:]:
    atr = (atr*13 + tr)/14
print("ATR14 (daily, Wilder): %.4f (%.2f%% of price)" % (atr, 100*atr/closes[-1]))
print("avg daily H-L range: %.2f%%" % (100*statistics.mean((r[2]-r[3])/r[4] for r in rows[1:])))
qs = [r[6] for r in rows]
print("daily quote volume USDT: avg %.1fM | min %.1fM (%s) | max %.1fM (%s)" % (
    statistics.mean(qs)/1e6, min(qs)/1e6, rows[qs.index(min(qs))][0], max(qs)/1e6, rows[qs.index(max(qs))][0]))
bs = [r[5] for r in rows]
print("daily base volume ASTER: avg %.1fM | max %.1fM (%s)" % (statistics.mean(bs)/1e6, max(bs)/1e6, rows[bs.index(max(bs))][0]))
print("last 8 days (date, O/H/L/C, volUSDT):")
for r in rows[-8:]:
    print("  %s O=%.4f H=%.4f L=%.4f C=%.4f V=%.1fM" % (r[0], r[1], r[2], r[3], r[4], r[6]/1e6))
# support/resistance: cluster daily lows/highs
lows = sorted(set(round(r[3],4) for r in rows))
highs = sorted(set(round(r[2],4) for r in rows), reverse=True)
print("lowest daily lows:", lows[:8])
print("highest daily highs:", highs[:8])

# --- CoinGecko 4h OHLC ---
g = json.load(open('raw/coingecko-4h-ohlc.json'))
grows = [(ts2date(k[0]), float(k[1]), float(k[2]), float(k[3]), float(k[4])) for k in g]
gcloses = [r[4] for r in grows]
grets = [math.log(gcloses[i]/gcloses[i-1]) for i in range(1, len(gcloses))]
gsd = statistics.stdev(grets)
print("\n4H (CoinGecko aggregate USD)")
print("rows:", len(grows), "| first:", grows[0][0], "| last:", grows[-1][0])
print("high_max: %.6f | low_min: %.6f | last close: %.6f" % (max(r[2] for r in grows), min(r[3] for r in grows), gcloses[-1]))
print("4h log-return sigma: %.5f -> annualized %.1f%%" % (gsd, gsd*math.sqrt(365*6)*100))
gtrs = []
for i in range(1, len(grows)):
    h, l, pc = grows[i][2], grows[i][3], grows[i-1][4]
    gtrs.append(max(h-l, abs(h-pc), abs(l-pc)))
gatr = sum(gtrs[:14])/14
for tr in gtrs[14:]:
    gatr = (gatr*13 + tr)/14
print("ATR14 (4h): %.4f (%.2f%% of last close)" % (gatr, 100*gatr/gcloses[-1]))
print("avg 4h H-L range: %.2f%%" % (100*statistics.mean((r[2]-r[3])/r[4] for r in grows[1:])))
print("CG last-close premium vs Binance last close: %.2f%%" % (100*(gcloses[-1]/closes[-1]-1)))
