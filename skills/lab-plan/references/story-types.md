# Story types

The project's plan (`cast-*/plan.json`) lists the types its classification calls for; use those. Each type has an owner by default and a pattern for acceptance criteria that someone other than the author can check. Acceptance criteria name the artifact and the check, never an intention ("works", "is correct", "looks good").

| Type | Default owner | Acceptance criteria look like |
|---|---|---|
| `THM`, `LEM` | the researcher, with the project's formal or domain specialists through the Expert Desk (`lab-agent-expert`) | The statement with all hypotheses is in `proof-<slug>.md`. `scripts/check_<name>.py` verifies the claim on all instances up to size k with seed s. The proof has no step marked open in its gap list. An adversarial reading (`lab-killtest` or the proof room) found no gap. A test in `tests/` exercises the statement's computable content. |
| `EXP` | `lab-agent-methods` | `protocol.md` is committed before the first run. `scripts/<exp>.py --seed s` regenerates `numbers.json` keys a, b, c. The report gives each metric with an uncertainty and the number of runs. Deviations from the protocol are listed. Confirmatory and exploratory results are labelled. |
| `CODE` | `lab-agent-engineer`, built with `bmad-build` | Given/When/Then criteria, each one a named test. The tests state their tolerances and why. `uv run pytest` passes from the lock file. Review is done with `bmad-code-review`. Each public function the paper relies on has a test tied to its statement. |
| `LIT` | `lab-agent-librarian` | The search log has its sources, queries, dates and screening counts. Each kept paper has a note with verbatim quotes and pages. The audit rows are written. A verdict per question is given. |
| `FORMAL` | the formal-verification specialist (Expert Desk) with the formalization playbook | `lake build` passes. The Lean statement matches the informal one, checked by a second reader. The remaining `sorry`s are listed with their blueprint nodes. |
| `STUDY` | `lab-agent-methods`, with the project's method specialist and guardians | The protocol and analysis plan are committed before data collection, and preregistered when confirmatory. The approvals the plan's gates require are on file. Sampling, consent and data handling are documented. The report follows the plan's reporting standard. |
| `DATA` | `lab-agent-engineer` | A data management plan exists. Provenance, licence and the codebook are recorded. Personal data are handled as the plan's gates require. Documentation and FAIR metadata are written. The dataset validates against its schema. |
| `WRITE` | the researcher, with `lab-agent-editor` for feedback | The section is drafted in `main.tex`. Every claim in it has a ledger row in `claims.csv`. The notation table is updated. The paper builds with no warnings about undefined references. |
| `DECIDE` | `lab-agent-pi` | A time box is set. The question is answered or the time box ran out. A DECISION entry with a reopen condition is in the notebook. |

## Writing CODE stories for bmad-build

`bmad-build` takes a story file directly. Give it what it cannot infer:

- the paper's statement the code must satisfy, quoted;
- the module and function names that exist;
- the tolerance and seed conventions;
- where the result must land, such as `numbers.json` keys, figures and tests;
- the lab's research-software standards, from `help/research-software.md` of the `bmod-lab` record.

Keep each CODE story small enough for one build session, about one public function with its tests.

## Sizes

- S fits in an afternoon.
- M takes one or two days.
- L takes up to a week.

An L story is split unless its parts cannot be checked separately.
