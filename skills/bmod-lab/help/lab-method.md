# The Lab Method

The procedure the lab uses to support a research project at each stage, from shaping a question to releasing results. The researcher does the research and makes every decision; the lab plans, questions, checks and documents (`help/responsible-use.md`). Read it when the user asks how the lab works, which phase a project is in, what a gate requires, what a story type means, or what "done" is.

Contents: the rules · the lifecycle · the gates · the claim register · story types and their Definition of Done · evidence levels · where things live.

## The lab rules

1. **Every claim gets a kill criterion before it gets time.** A question nobody can fail at is not research.
2. **Riskiest first.** Plan so that the claim most likely to die is tested first and most cheaply.
3. **Dead ends are results.** Every killed idea, failed proof and negative experiment goes into the notebook with its reason.
4. **Cite only what you opened.** A remembered title is a lead, not a source. Quotes are verbatim, with page numbers.
5. **Every number regenerates.** A script, a seed and a committed output file stand behind every number in a paper.
6. **Label every claim.** Proved, checked or conjectured. For quantum work, also say whether it is a proven advantage, a heuristic, quantum-inspired or classical.
7. **Say what you do not claim.** Every brief and every paper has a non-claims list.
8. **Contrast before consensus.** An idea faces at least one adversarial reading (Viktor, the tribunal, or independent subagents) before the lab commits to it.
9. **Disclose deliberately.** Check novelty and ownership at the release gate before anything is posted, presented or deposited. Some patent systems, Europe's among them, give no grace period.
10. **Personas are fictional and requests are private.** Lab voices never put invented words in the mouths of real people. Requests to external APIs carry no personal data.
11. **The researcher is the author.** AI tools cannot be authors or take responsibility for the work. The lab's agents propose and check; the researcher decides, writes and signs (`help/responsible-use.md`).
12. **Record and disclose AI help.** AI assistance that reaches anything leaving the project is logged as an AI-USE entry in the notebook. `lab-release` turns those entries into the disclosure statement the venue asks for.
13. **Clear prose, never disguise.** Prose is plain, specific and in the author's own voice (`help/voice.md`). The voice pass edits for clarity; it is never used to pass AI-generated text off as the author's.

## The lifecycle

Phases describe the kind of work, not a march: a small question may go from Spark straight to Prove, and any phase may send the project back to an earlier one. The PI (`lab-agent-pi`) recommends the smallest path that settles the next open claim.

| # | Phase | Skill | Artifact | Lead | Typical room |
|---|---|---|---|---|---|
| 0 | Cast | `lab-cast` | `cast-<slug>`: the project's classification (`profile.toml`), its plan (`plan.json`), its specialists and rooms | Nadia | — |
| 0 | Spark | `lab-spark` | `ideas-<slug>`: idea cards | Nadia | spark-lab |
| 1 | Survey | `lab-survey` | `survey-<slug>`: dossier, search log, prior-art verdict per idea | Selin | — |
| 2 | Frame | `lab-frame` | `brief-<slug>`: the research brief and claim register | Nadia | steering-committee |
| 3 | Plan | `lab-plan` | `plan-<slug>`: epics, stories, dependency graph | Nadia | — |
| 4 | Work | `lab-prove`, `lab-experiment`, `bmad-build`, `lab-survey` | proofs, experiments, studies, datasets, code with tests, literature notes | the researcher with Arjun, Lena, Selin and the project's specialists (Expert Desk) | the project's rooms, build-room |
| 5 | Verify | `lab-factcheck`, `lab-referee`, `lab-killtest` | `factcheck-<slug>`, `referee-<slug>`, `killtest-<slug>` | Marta, Viktor | tribunal, editorial-board |
| 6 | Write | `lab-write` | the paper project in `{papers_folder}/<slug>/` | Clara | editorial-board |
| 7 | Release | `lab-release` | deposit bundle and records (Zenodo, arXiv, code) | Lena, Clara | steering-committee |
| — | Notebook | `lab-notebook` | `notebook-<slug>`: decisions, results, dead ends, digests | everyone | — |

Casting classifies the project by field, mode, outputs and sensitivities, once when it starts and again whenever its work enters a new field or method. The plan it produces decides which story types, reporting standard, search databases and extra gate conditions apply (`lab-cast/references/classification.md`), and the project's rooms and kill tests include its specialists and guardians. The two exits share phases 0–3. **Paper exit**: Work → Verify → Write → Release. **Code exit**: CODE epics through `bmad-build`, then `bmad-code-review`, then a release of the software with its own citation record.

## The gates

A gate is a decision written into the notebook: verdict, owner, date, and the kill criterion that would reopen it. `lab-killtest` runs gates G1 and G3. The steering committee decides G2 and G5.

| Gate | When | Passes when |
|---|---|---|
| G1 Novelty | after Survey | Each idea that goes forward has the verdict ALIVE or ALIVE-NARROW. Its nearest prior art is cited at VERIFIED or METADATA-ONLY, and the terminology-drift search was done. |
| G2 Commit | after Frame | Every claim in the brief has evidence planned and a kill criterion. The Heilmeier answers are written. Non-claims are listed. Publish-versus-protect is decided. Every G2 condition in the project's plan is met, such as ethics approval before recruitment or a data management plan. |
| G3 Claim | when a claim's stories are done | The claim survived its kill test as ALIVE or ALIVE-NARROW. The register is updated to the narrowed statement. |
| G4 Submission | before posting or submitting | The ledger maps every numbered statement and every cited sentence to evidence. References are at VERIFIED or METADATA-ONLY, with any METADATA-ONLY listed. Every number regenerates. Simulated review recommends at worst minor revision. The overclaim audit is clean. |
| G5 Release | before anything leaves the lab | The disclosure and ownership check is done. Every G5 condition in the project's plan is met. The AI-use statement is drafted from the notebook. The bundle rebuilds and runs from a clean copy. Metadata is ready (title, abstract, keywords, subjects, licence, related identifiers). |

## The claim register

The research brief holds the register; the plan and the paper refer to its IDs. One row per claim:

| Field | Meaning |
|---|---|
| ID | `C1`, `C2`, … stable for the life of the project |
| Statement | One sentence, falsifiable, with its hypotheses |
| Kind | theorem, conjecture, algorithm, numerical, empirical, qualitative, historical, engineering, survey |
| Evidence planned | proof, formal proof, test, experiment, citation |
| Kill criterion | The observation or argument that would make it false or uninteresting |
| Status | open, supported, narrowed (with the new statement), dead (with the reason) |
| Level | the evidence level reached (below) |

## Story types and their Definition of Done

`lab-plan` writes one file per story, typed by its prefix. Each has acceptance criteria that someone other than its author can check.

| Type | Work | Done when |
|---|---|---|
| `THM` / `LEM` | a theorem or lemma | Statement with all hypotheses. Small cases checked by a committed script. Proof written. Gap list empty. Independent adversarial reading passed. A test exercises any computable content. |
| `EXP` | a computational or laboratory experiment | Protocol written before the run. Script, seed or raw data committed. Results with uncertainty. Deviations from the protocol recorded. Numbers written to `numbers.json`. |
| `STUDY` | an empirical study with participants, records or texts | Protocol and analysis plan written first, and preregistered when confirmatory. Approvals the plan requires obtained. Sampling and consent documented. Reported to the standard the plan names. |
| `DATA` | collecting, curating or releasing a dataset | Data management plan. Provenance and licence recorded. Personal data handled as the plan's gates require. Documentation and FAIR metadata written. |
| `CODE` | software | Acceptance criteria as tests. Built with `bmad-build` under the lab standards. Reviewed. Tests pass from the lock file. |
| `LIT` | a literature question | Search log. Every source opened. Notes with verbatim quotes and pages. Audit rows written. |
| `FORMAL` | a Lean formalization | Statement compiles. Remaining `sorry`s listed. Blueprint node linked. |
| `WRITE` | a section of the paper | Drafted. Every claim in it maps to a ledger row. Notation table updated. |
| `DECIDE` | a spike or gate | The decision, with its kill criterion, is in the notebook. |

## Evidence levels

For claims, from strongest to weakest:

- **FORMALIZED**: checked by Lean.
- **PROVED**: a written proof that passed an independent adversarial reading.
- **CHECKED**: tested numerically or by code on stated cases.
- **SUPPORTED**: a cited source, quoted verbatim and opened.
- **CONJECTURED**: believed, with reasons, but not established.
- **UNVERIFIED**: not checked.

For citations:

- **VERIFIED**: source opened, quoted words match the citing sentence.
- **METADATA-ONLY**: the record was checked against Crossref or arXiv, but the text was not read, for example behind a paywall.
- **UNVERIFIED**: not checked.
- **FALSE**: checked, and it does not support the sentence.

For kill tests:

- **ALIVE**: survives as stated.
- **ALIVE-NARROW**: survives in a narrower form, which replaces it.
- **DEAD**: killed, with the reason logged.

## Where things live

- Lab documents: `{output_folder}/{active_initiative}/<type>-<slug>/<type>-<slug>.md`, without the initiative segment when none is active. Use one `notebook-` per project.
- Papers: `{papers_folder}/<slug>/` holds the following.
  - `main.tex` and `references.bib`.
  - `figures/` with `numbers.json`.
  - `references/` holds the citation record:
    - `reference_audit.csv`, one row per key;
    - `notes/<key>.md`, with verbatim fragments and page locators;
    - `txt/` and `pdf/`, private and never redistributed.
  - `claims.csv`, the claim ledger.
- Code: the project's repository, in src layout, with `tests/` and `scripts/figures.py`. The figures script regenerates every figure and number from a fixed seed.
