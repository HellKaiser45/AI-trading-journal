# Review: LOSS-1.01%_2026-10-23T1024Z_ASTERUSDT

Outcome: LOSS-1.01%
Window: 2026-10-23T10:40:51Z to 2026-10-25T10:00:00Z, 567 candles, step 0:05:00 (outcome_candles.csv)
Fill: LIMIT at 0.695 (candle 2026-10-23T22:30:00Z)
Exit: LOSS at 0.688 (candle 2026-10-24T14:15:00Z)

Rules: limit fills at its price on touch; TP and SL fill at their level on touch;
a candle touching both is a LOSS; TP in the limit fill candle is ignored;
expiry price = close of the last candle before expire_at.
