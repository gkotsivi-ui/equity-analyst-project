# FIN 67110 equity research desk

The desk of Francis & Zhang (2026), Section 3.1, for any U.S. company that files with SEC EDGAR.
A ticker goes in. The desk finds the latest 10-K, 10-Q and earnings release, reads the statements
as XBRL data, computes the core ratios in code, and four roles write a five-part report.
Nothing in the code names a company: the ticker is an argument.

- `team.py`: the agent team (Lab 04), a LangGraph graph in code with a Verifier on every run.
- `verifier.py`: the Verifier, which checks every sourced number in a report against the saved filings and facts.
- `roles/`: each role's instructions, one file per role.
- `lab02_desk.py`: the seven steps, from SEC EDGAR, with no model.
- `lab03_app.py`: the seven steps, then the four roles of Figure 1 on Anthropic's API, then the report.
- `prices.py`: a closing price for P/E, from financialdatasets.ai.
- `check_env.py` and `set_keys.py`: check `.env`, and save pasted keys into it.

## The agent team

```mermaid
flowchart LR
    S[The steps<br/>filings, facts, ratios<br/>code, no model] --> RA[Research Analyst<br/>one model call]
    RA --> FA[Financial Analyst<br/>one model call]
    FA --> IA[Investment Advisor<br/>one model call]
    IA --> SM[Strategy Manager<br/>checklist in code]
    SM -. a failing part, once .-> RA
    SM -. a failing part, once .-> FA
    SM -. a failing part, once .-> IA
    SM --> VF[Verifier<br/>every run, no flag turns it off]
    VF --> R[verified report<br/>with its table of marks]
```

The order is the same on every run, and code decides every edge. A role the Manager sends back
returns to the Manager, and no role runs more than two times in one run. Each role receives only the
JSON the graph gives it: the task, the context and the expected output.

## Setup

Python 3.11 or newer. In this folder:

```
python -m pip install -r requirements.txt
copy .env.example .env
```

On a Mac, use `cp .env.example .env`. Then fill in `.env`; it is never committed.

| Setting | Needed for | Value |
|---|---|---|
| `SEC_USER_AGENT` | every step | your name and email; EDGAR requires it on every request |
| `API_KEY` | Lab 03 | an Anthropic API key from platform.claude.com, starting with `sk-ant-` |
| `MODEL`, `EFFORT` | optional | the model and effort for the roles; defaults `claude-opus-5-5` and `medium` |
| `FINANCIAL_DATASETS_API_KEY` | optional | the key for closing prices; without it, pass `--price` |
| `AI_TOOLS` | optional | the AI tools named on each report's AI-assistance line |

Check it with `python check_env.py`. It prints the first four characters of the key and your User-Agent.

## Run

The agent team, with the Verifier on every run (Lab 04):

```
python team.py COST --peers WMT,TGT,BJ --price <close>
python team.py --verify-only output/<run folder>
```

The node names print in the graph's order, then the path of the verified report. `--verify-only` runs
the Verifier on a saved run and nothing else.

The seven steps only (Lab 02):

```
python lab02_desk.py COST --peers WMT,TGT,BJ --price <close>
python lab02_desk.py COST --step 4
```

The seven steps, then the four roles and the report (Lab 03):

```
python lab03_app.py AAPL --peers MSFT,GOOGL,DELL
python lab03_app.py COST --peers WMT,TGT,BJ --price <close>
```

Replace `<close>` with the closing price, for example `--price 1012.35`.

Expect the seven steps, then the four role names, then the path of the report. Without `--price`, the
desk uses the last close before the release was accepted, from financialdatasets.ai. One close by date:

```
python prices.py COST 2026-10-27
```

Each run writes `output/<TICKER>_<date>_<time>/`:

| File | What it holds |
|---|---|
| `10K_*.txt`, `10Q_*.txt`, `8K_*.txt` | the three documents as plain text; the 8-K file is Exhibit 99.1, the earnings release |
| `facts.json`, `ratios.json`, `peer_facts.json` | each fact with its tag, period and filing; each ratio with its arithmetic |
| `report.md` | the five-part report; line 1 names the filings and their accession numbers, line 2 the run time |
| `verified_report.md`, `verification.json` | the report with the Verifier's table of marks under its first line (Lab 04) |
| `nodes/` | each node's input and output, numbered in the order the nodes ran (Lab 04) |
| `roles.json` | every JSON hand-off between the Strategy Manager and the roles (Lab 03) |
| `audit.md` | a blank audit table for the human sign-off |

## Reports in this repository

| Company | Report | What it read |
|---|---|---|
| Microsoft (MSFT), the partner's pick for Checkpoint 1 | [output/MSFT_20261101_182330/report.md](output/MSFT_20261101_182330/report.md) | FY2026 10-K, Q1 FY2027 10-Q, and the Oct 28, 2026 earnings release |
| Costco (COST), the Lab 03 known answer, at the Oct 27, 2026 close of $992.13 | [output/COST_20261101_201319/report.md](output/COST_20261101_201319/report.md) | FY2026 10-K, Q3 FY2026 10-Q, and the Sep 24, 2026 earnings release |

## How the numbers are kept honest

1. Step 2 reads each filing's "Accepted" time from its EDGAR index page, in Eastern time. The earnings
   8-K is the newest 8-K that reports Item 2.02; newer 8-Ks without it are printed as skipped.
2. Step 4 reads full fiscal years only. When a concept has several candidate tags, the tag whose
   latest year is newest wins; a tie goes to total revenues (`Revenues`) before net sales. Every
   concept is read for revenue's fiscal year, and step 4 prints whether every period end equals the
   10-K's fiscal year end.
3. Step 5 is the calculator. Debt includes its current portion; return on equity uses average equity.
4. Step 6 prints the release's revenue and diluted EPS lines as the release states them.
5. The Strategy Manager is a checklist in code. It sends each analyst only its JSON packet. It checks
   that each Research Analyst quote appears word for word in the filings, and that each Financial
   Analyst number appears in the data the desk gave it. It runs requested ratios in code and sends a
   failing part back to its role once. Problems that remain are listed at the end of the report.
6. The roles run on Claude Opus 5.5 with Anthropic's server-side fallback, which re-runs a declined
   request on another model. `roles.json` records which model served each call.
7. The Verifier receives only the compiled report, the saved filing texts and the saved facts. It
   skips the Investment Advisor's thesis. A model lists each number with the source the report gives
   it. Code then checks each one: a number sourced to an XBRL tag and period against the facts file;
   a quoted line against the filing text, allowing for spacing and formatting; a ratio by recomputing
   its arithmetic. A model then checks that each quoted line states that number for that period, in
   that definition. Each number is marked correct, wrong or unsupported. A number with no source is
   unsupported, unless it repeats a number the report sources elsewhere. A wrong number is corrected
   from the filings, with the real line or tag beside it.

## Tests

```
python -m unittest discover -s tests
```

The tests need no network and no key. They cover the tag trap, the full-year filter, the table text,
the quote and number checks, the calculator, and a full Strategy Manager run against a fake model.
For the agent team, they check the fixed node order, the single send-back, and that every path to the
end runs the Verifier with no option to turn it off. They also check the Verifier's marks on a seeded
EPS, an invented growth rate, a price and an unsourced number.

This is a learning exercise, not financial advice.
AI assistance: Claude Code. I verified the sources myself; the judgments are mine.
Any remaining errors are my own.
