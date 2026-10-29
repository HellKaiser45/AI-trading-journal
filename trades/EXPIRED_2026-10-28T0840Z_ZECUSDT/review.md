# Review: EXPIRED_2026-10-28T0840Z_ZECUSDT

Outcome: EXPIRED
Window: 2026-10-28T08:58:30Z to 2026-10-29T02:40:00Z, 212 candles, step 0:05:00 (outcome_candles.csv)
Fill: the limit was never touched before expire_at

Rules: limit fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the limit fill candle is ignored;
expiry price = close of the last candle before expire_at.
