# Lab 04 tests: the Verifier on the known answer (Checkpoint 2)

The agent team is [team.py](team.py), a LangGraph graph in code: the steps, the Research Analyst, the
Financial Analyst, the Investment Advisor, the Strategy Manager, then the [Verifier](verifier.py) on
every run. Each test below copies a saved Costco run, changes the copy's `report.md`, and runs only the
Verifier on it:

```
python team.py --verify-only output/<copy>
```

## The four tests

| Test | Run folder | What changed in the copy's report | Lab 04 expects | The Verifier's mark |
|---|---|---|---|---|
| 1. The seeded error | [COST_20261103_084759_seeded_eps](output/COST_20261103_084759_seeded_eps/verified_report_20261103_090927.md) | Line 29, core claim 5: diluted EPS $20.76 became **$21.76**, its source line changed to match: `Diluted \| $21.76 \| $18.21 \| $16.56` | that EPS marked wrong and corrected to the 10-K's figure, with the 10-K's per-share line beside it | **Wrong**, corrected to **$20.76**, with the 10-K line `Diluted \| $20.76 \| $18.21 \| $16.56` (us-gaap:EarningsPerShareDiluted, 2025-09-01 to 2026-08-30). It is the only number marked wrong. |
| 2. The invented number | [COST_20261103_084759_invented_growth](output/COST_20261103_084759_invented_growth/verified_report.md) | Line 65, added: revenue growth of **14.14%** = 303,154.0 / 275,235.0 - 1, four points above what those two quoted figures give | marked wrong or unsupported, with the arithmetic from the quoted inputs beside it | **Wrong**, corrected to **10.14%**, with the arithmetic `303,154.0 / 275,235.0 - 1` |
| 3. The clean report | [COST_20261103_084759](output/COST_20261103_084759/verified_report_20261103_085842.md) | nothing | all eleven core claims marked correct | **All eleven core claims and the P/E correct.** Of 153 numbers: 149 correct, 0 wrong, 2 unsupported, 2 prices not checked. The 2 unsupported are real gaps: line 84 states the prior year's debt ($75.0 million and $5,713.0 million) with no source, and the Verifier shows the 10-K line for each. |
| 4. The skip test | [team.py](team.py) | (nothing; this test reads the code) | no way to run the agent team without the Verifier | **None.** The only options are a ticker, `--peers`, `--price` and `--verify-only`, and the graph's only edge to the end comes from the Verifier. [tests/test_team.py](tests/test_team.py) checks both. |

## The same order on every run

Run 1 ([COST_20261103_084759](output/COST_20261103_084759)) and run 2
([COST_20261103_085932](output/COST_20261103_085932)) printed the same nodes in the same order, and
each saved its own folder; run 2 left run 1 untouched. In run 2, the Financial Analyst asked for six
ratios. The Manager computed them in code and used its one send-back to return them, so run 2 shows
the retry slot: Financial Analyst, then Strategy Manager, a second time. Each node's input and output
is in the run's `nodes/` folder, numbered in the order the nodes ran.

## What changed in the Verifier along the way

- Run 1's first verification ([verified_report.md](output/COST_20261103_084759/verified_report.md))
  marked 45 numbers unsupported. Most were summary sentences that restate a number the report
  sources elsewhere. A restated number now carries the source of the line it repeats; a quote the
  filing does not contain gets no such pass. The later file is the current result.
- Run 2's verification ([verified_report.md](output/COST_20261103_085932/verified_report.md)) marked
  line 135's 12.44% wrong in error. The Verifier had recomputed the side of the arithmetic written
  with variable names; it now recomputes the side written in numbers, and a test covers it. The same
  verification correctly marked line 136's "about 2.5 points" unsupported, because the model computed
  that number itself.
- The seeded copy's first verification marked the EPS wrong and corrected it, but cited an MD&A
  sentence that repeats the figure. The Verifier now prefers the statement's own per-share row, as in
  the later file linked above.

## Check of test 1 against the 10-K

- The filing: Costco's FY2026 10-K, accession 0000909832-26-000093, [on EDGAR](https://www.sec.gov/Archives/edgar/data/909832/000090983226000093/cost-20260830.htm).
- The line: in the income statement, under "NET INCOME PER COMMON SHARE:", the row
  `Diluted | $20.76 | $18.21 | $16.56`, for the 52 weeks ended August 30, 2026, August 31, 2025 and
  September 1, 2024.
- The result: the filing states diluted EPS of $20.76 for fiscal 2026. The seeded $21.76 is wrong,
  and the Verifier's correction, $20.76 beside this same per-share line, is the filing's own figure.

This is a learning exercise, not financial advice.
AI assistance: Claude Code. I verified the sources myself; the judgments are mine.
Any remaining errors are my own.
