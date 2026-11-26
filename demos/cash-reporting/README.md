# We finish Monday £4,500 in credit. Can we fund Friday’s supplier run?

I’ve used sample remittance and payment dates. Thursday opens at £12,000, including an advance already received from the factor. On a £10,000 settlement the factor retains £8,500, leaving £1,500 coming into the bank. Friday’s £14,000 supplier run takes available cash to **minus £500**. A £5,000 receipt on Monday restores the balance to £4,500.

I’d ask finance to confirm Friday funding or agree a revised payment schedule. Counting the full £10,000 settlement would double-count the advance. Looking only at the period-end balance would hide the shortfall.

**Client work I delivered.** I prepared monthly cash-flow reporting from Xero including invoice-finance availability. I built this daily example to show how the timing of individual movements can change a payment decision.

Run `python cash.py` and `python -m unittest -v`. Amounts are whole GBP. The scenario assumes the stated settlement dates and no overdraft. It covers daily balances with one movement per day; intraday settlement order and facility headroom would need their own evidence.

## What if the factor pays on Tuesday?

If the £1,500 remittance slips from Thursday to the following Tuesday, I still expect the same cash in total. The question is how much I can release on Friday. Run `python cash.py --delay-remittance` from this folder to replay the delay.

| Closing cash | Original dates | Delayed remittance |
| --- | ---: | ---: |
| Friday, after the supplier run | −£500 | −£2,000 |
| Monday, after the customer receipt | £4,500 | £3,000 |
| Tuesday, after all receipts have cleared | £4,500 | £4,500 |

With £12,000 available on Friday and no overdraft, I’d need £2,000 of confirmed funding to release the full £14,000 run. Otherwise I’d agree which payments to defer with the suppliers concerned. Moving the date of the remittance adds £1,500 to Friday’s funding gap.

[Back to my portfolio](../../README.md)
