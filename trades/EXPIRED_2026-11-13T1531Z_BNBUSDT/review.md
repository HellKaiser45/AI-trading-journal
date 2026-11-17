# Review: EXPIRED_2026-11-13T1531Z_BNBUSDT

Outcome: EXPIRED
Window: 2026-11-13T15:31:00Z to 2026-11-15T15:31:00Z, 576 candles, step 0:05:00 (outcome_candles.csv)
Fill: the limit was never touched before expire_at

Rules: limit fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the limit fill candle is ignored;
expiry price = close of the last candle before expire_at.
