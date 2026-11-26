# Review: EXPIRED_2026-11-22T1100Z_UNIUSDT

Outcome: EXPIRED
Window: 2026-11-22T11:00:00Z to 2026-11-24T11:00:00Z, 576 candles, step 0:05:00 (outcome_candles.csv)
Fill: the stop_market order was never triggered before expire_at

Rules: LIMIT/STOP/STOP_MARKET fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the pending fill candle is ignored;
expiry price = close of the last candle before expire_at.
