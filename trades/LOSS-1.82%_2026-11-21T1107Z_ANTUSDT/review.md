# Review: LOSS-1.82%_2026-11-21T1107Z_ANTUSDT

Outcome: LOSS-1.82%
Window: 2026-11-21T11:07:00Z to 2026-11-23T11:07:00Z, 576 candles, step 0:05:00 (outcome_candles.csv)
Fill: LIMIT at 87.95 (candle 2026-11-21T11:30:00Z)
Exit: LOSS at 89.55 (candle 2026-11-21T13:35:00Z)

Rules: LIMIT/STOP/STOP_MARKET fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the pending fill candle is ignored;
expiry price = close of the last candle before expire_at.
