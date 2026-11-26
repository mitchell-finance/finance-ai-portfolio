# A buyer changes one term. Which earlier terms still stand?

I built this example with a sample revision history. The original agreement covers twelve assemblies, the first four by week six and one delivery in the price. The buyer moves the first delivery to week eight. A later amendment raises the total quantity to sixteen.

**The draft promises sixteen by week eight with three deliveries included.** The latest quantity and date are correct. Neither amendment changed the first batch of four or the single included delivery.

I carry forward each term with the reference that authorised it. Sales can draft “Four by week eight, sixteen in total, one delivery included” and ask operations to confirm the remaining dates. A forked amendment history goes back for review because it leaves competing instructions.

Run `python amendments.py` and `python -m unittest -v test_amendments` here. The [code and sample terms](amendments.py) start from human-reviewed amendments in order. A buyer email still needs interpretation and approval before it enters this chain. Pricing the extra four units is a separate commercial decision.

[Back to proposal review](README.md)
