# Review: LOSS-1.26%_2026-11-20T1007Z_XRPUSDT

Outcome: LOSS-1.26%
Window: 2026-11-20T10:07:00Z to 2026-11-22T10:07:00Z, 576 candles, step 0:05:00 (outcome_candles.csv)
Fill: LIMIT at 0.95 (candle 2026-11-20T12:00:00Z)
Exit: LOSS at 0.938 (candle 2026-11-20T13:25:00Z)

Rules: LIMIT/STOP/STOP_MARKET fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the pending fill candle is ignored;
expiry price = close of the last candle before expire_at.
