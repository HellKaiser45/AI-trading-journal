# Review: LOSS-3.43%_2026-11-21T1042Z_HYPEUSDT

Outcome: LOSS-3.43%
Window: 2026-11-21T10:42:00Z to 2026-11-23T10:42:00Z, 576 candles, step 0:05:00 (outcome_candles.csv)
Fill: LIMIT at 59.75 (candle 2026-11-21T12:15:00Z)
Exit: LOSS at 61.8 (candle 2026-11-21T21:00:00Z)

Rules: LIMIT/STOP/STOP_MARKET fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the pending fill candle is ignored;
expiry price = close of the last candle before expire_at.
