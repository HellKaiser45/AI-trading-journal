# Review: LOSS-1.45%_2026-11-04T1516Z_SOLUSDT

Outcome: LOSS-1.45%
Window: 2026-11-04T15:20:33Z to 2026-11-06T06:00:00Z, 463 candles, step 0:05:00 (outcome_candles.csv)
Fill: LIMIT at 96.4 (candle 2026-11-04T15:25:00Z)
Exit: LOSS at 95 (candle 2026-11-04T19:00:00Z)

Rules: limit fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the limit fill candle is ignored;
expiry price = close of the last candle before expire_at.
