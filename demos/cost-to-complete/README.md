# The programme slips two weeks. What does that actually cost?

I worked with a quantity surveyor and directors to reconcile project costs. I built this example using sample programme, quote and ledger figures to show the question I’d ask before changing a forecast: **which costs are already in it?**

The contract value is £60,000. The previous £50,000 final-cost forecast included four weeks of plant at £1,000. The revised quote is six weeks at £1,100. Finance has already accrued £1,100 for the first of those six weeks.

| Forecast bridge | Amount |
| --- | ---: |
| Extra two weeks at the revised rate | +£2,200 |
| Rate increase on the original four weeks | +£400 |
| Increase in forecast final cost | **+£2,600** |
| Revised final cost and margin | **£52,600 cost · £7,400 margin** |

I’d put £6,600 against the whole hire period. Of that, £1,100 is already in actual costs, leaving **£5,500 still to recognise**. Adding £5,500 to the old forecast would count the previous allowance twice. If finance books another week, the remaining cost drops again while the forecast final cost stays the same.

**What runs here.** Run `python forecast.py` and `python -m unittest -v` from this folder. Inspect the [forecast inputs](forecast.json). The bridge replaces one allowance in a whole-job forecast and assumes all other costs and contract revenue stay fixed.

**Where I’d use AI.** Pull the effective dates and scope from a supplier revision and compare them with the programme. The project manager must confirm that the new rate covers all six weeks and that the accrual relates to this hire. The local calculation starts from those confirmed assumptions.

[Read the actual program output](expected-output.txt)

[Back to my portfolio](../../README.md)
