# Review: LOSS-8.00%_2026-11-16T1137Z_XMRUSDT

Outcome: LOSS-8.00%
Window: 2026-11-16T11:46:32Z to 2026-11-21T12:00:00Z, 1442 candles, step 0:05:00 (outcome_candles.csv)
Fill: LIMIT at 490.56 (candle 2026-11-17T03:10:00Z)
Exit: LOSS at 451.32 (candle 2026-11-20T14:50:00Z)

Rules: LIMIT/STOP/STOP_MARKET fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the pending fill candle is ignored;
expiry price = close of the last candle before expire_at.
