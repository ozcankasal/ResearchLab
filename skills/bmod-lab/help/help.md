# Research Lab knowledge

This document covers the skills of the `lab` module: a research-assistance lab for any field, from mathematics and physics to medicine, economics and history. It helps a researcher plan, question, verify and document their own work through fixed phases and gates. The researcher does the research and is the only author; the lab's agents propose, check and challenge (`help/responsible-use.md`). The module covers what each skill gives the user, when to recommend it, and what to offer next.

## How the lab works

Every project starts with `lab-cast`, which classifies it by field, research mode, outputs and sensitivities and brings in the specialists, guardians, story types and standards that classification calls for (`help/classification.md`). It then moves through Spark, Survey, Frame, Plan, Work, Verify, Write and Release. Gates sit between the phases, and a lab notebook runs alongside. Phases describe the kind of help, not a mandatory march. Recommend the smallest path that settles the next open claim, and say which gate it serves. `help/lab-method.md` has the rules, gates, story types and evidence levels.

The lab's agents are people to talk to, and each owns a menu. Nadia, the PI (`lab-agent-pi`), is the default way in when the user does not know where to start. The workflow skills can also be invoked directly.

## The agents

Eight core assistants, fixed and named, work in every project:

- `lab-agent-pi`, **Nadia**, Principal Investigator. Use her to start a project (she runs `lab-cast` first), ask what to do next, see where a project stands, or call a lab meeting.
- `lab-agent-methods`, **Arjun**, Methods Scientist. Covers study and experiment design, sample size, statistics, benchmarks and reproduction from a clean checkout, in any field.
- `lab-agent-engineer`, **Lena**, Research Software Engineer. Covers research code through `bmad-build`, test design, datasets, repository and environment setup, and releases.
- `lab-agent-librarian`, **Selin**, Research Librarian. Covers prior art, literature surveys, snowballing, terminology drift and finding the source of a claim.
- `lab-agent-factchecker`, **Marta**, Fact Checker. Covers claim ledgers, reference checks, number provenance and overclaim audits.
- `lab-agent-referee`, **Viktor**, Referee and Red Team. Covers kill tests, premortems, steelman-then-attack and simulated peer review.
- `lab-agent-editor`, **Clara**, Scientific Editor. Covers editorial feedback on the author's paper, abstract and keywords, notation, referee replies and release records.
- `lab-agent-voice`, **Ruth**, Voice Editor. Covers generic or machine-style phrasing, tone, and the author's style sheet.

The **Expert Desk** (`lab-agent-expert`) puts the user in conversation with the project's own specialists: the domain experts, method specialists and guardians `lab-cast` chose. Recommend it when the user asks for an expert in the project's field, or names one of the project's specialists.

## The workflows

- `lab-cast` classifies the project by field (OECD codes), research mode, outputs and sensitivities. A tested script turns the classification into a plan. The plan brings in three kinds of specialist:
  - method specialists for the modes, such as a causal-inference specialist for observational work;
  - guardians for the sensitivities, such as the research ethics officer when people take part;
  - domain experts designed for the project's own subfields, in any field, plus any optional expert presets that match it.

  The plan also sets the story types, reporting standards, search databases and extra gate conditions the other workflows follow. The cast and project rooms go into the project's own `bmad-party-mode` customization. Recommend `lab-cast` when a project starts, when its work enters a new field or method, or when the user asks for experts. Afterwards offer the project's seminar room, the Expert Desk or `lab-spark`.
- `lab-spark` turns a hunch, a paper or a question into idea cards: a one-sentence claim, its smallest test and its kill criterion. Recommend it when the user wants new ideas or has a vague direction. Afterwards offer `lab-survey` on the best cards.
- `lab-survey` produces a prior-art and literature dossier with a rerunnable search log and a verdict per idea. Recommend it before any time is committed to an idea, and whenever someone asks "who did this before". Afterwards offer `lab-killtest` (gate G1) or `lab-frame`.
- `lab-frame` writes the research brief: the Heilmeier answers, the claim register with kill criteria, non-claims and risks. Recommend it once an idea survives the survey. Afterwards offer the steering committee for gate G2, then `lab-plan`.
- `lab-plan` breaks the brief into epics and typed stories (THM, LEM, EXP, CODE, LIT, FORMAL, WRITE, DECIDE), ordered riskiest first, with a status board. Recommend it after the brief. Afterwards offer the first ready story to its owner. CODE stories go to `bmad-build`.
- `lab-prove` develops a proof through statement, small-case checks, sketch, gap hunt and write-up, ending in an adversarial reading. Recommend it for THM and LEM stories, or whenever the user asks "is this true" about a mathematical claim.
- `lab-experiment` runs a computational experiment through a protocol written before the run, then results with uncertainty and a report. Recommend it for EXP stories, simulations, benchmarks and numerical checks.
- `lab-killtest` is a stage-gate kill test: a steelman, independent attacks, then a verdict of ALIVE, ALIVE-NARROW or DEAD per claim. Recommend it at gates G1 and G3, before any big commitment, and when the user asks whether an idea survives.
- `lab-factcheck` maps statements and cited sentences to evidence, checks references against Crossref and arXiv, traces numbers and audits overclaims. Recommend it before submission (gate G4) and after major edits.
- `lab-referee` runs a simulated peer review: an editor, independent referees chosen for the paper's type, a decision and a response plan. Recommend it before submission.
- `lab-write` supports the author's own paper. It sets up the LaTeX project in the lab's house style, builds the outline from the brief, ledger and results, checks claims, notation and the build, and gives feedback on the author's drafts. It writes a draft only on request, marked for the author to rewrite. Recommend it once claims are at least CHECKED. Afterwards offer `lab-factcheck` and `lab-referee`.
- `lab-release` prepares the release: the deposit bundle and its records for Zenodo, arXiv and code. Recommend it after gate G4, starting with the disclosure check (gate G5).
- `lab-voice` gives text a voice pass, in any language. It audits the text with a scanner for machine-writing habits plus a full reading, building a language pack on the spot for a language it has not met. It rewrites in the author's voice without changing any claim's strength, and builds the author's style sheet from their own writing. Recommend it before anything leaves the lab (papers, abstracts, release records, letters) and whenever the user asks whether a text sounds like AI. `lab-write` and `lab-release` call it at the end.
- `lab-notebook` is the lab notebook. It logs decisions, results and dead ends, reports status and the next step, and writes a weekly digest. Recommend it after every gate and whenever the user asks where things stand.

## Rooms for bmad-party-mode

Each project gets its own rooms from `lab-cast`: a seminar, a tribunal and, for formal work, a proof room. They mix the project's specialists with the lab's assistants and live in the project's `_bmad/custom/bmad-party-mode.toml`. The module's roster adds six general rooms, opened with `bmad-party-mode --party <id>`:

- `spark-lab` is for divergent ideas.
- `tribunal` is for adversarial kill tests. It works best in subagent mode.
- `build-room` is for code, data and reproducibility.
- `editorial-board` is for reading the author's draft.
- `steering-committee` is for go/no-go decisions, priorities and publish versus protect.
- `integrity-board` is for ethics approvals, personal data, misuse risk and disclosure timing.

`help/personas.md` describes the cast.

## Where things land

Lab documents land in `{output_folder}/{active_initiative}/<type>-<slug>/`. Paper projects land in the folder chosen at setup as `modules.lab.papers_folder`. The author name, affiliation and ORCID used in papers and release records are `modules.lab.author`, `modules.lab.affiliation` and `modules.lab.orcid`. `bmad setup lab` shows and changes the answers.

## More detail

This document should be enough to route the user. Read a topic file only when the question is about its subject.

| Topic file | Read when the user asks about |
|---|---|
| `help/classification.md` | How projects are classified (fields, modes, outputs, sensitivities), and why a specialist, guardian, story type or gate was chosen. |
| `help/lab-method.md` | The phases, gates, lab rules, claim register, story types, Definition of Done, evidence levels, or where files live. |
| `help/personas.md` | Who is in the lab, the guests, which room or voice to call for a situation, contrasting voices and how to keep them independent. |
| `help/research-software.md` | Standards for research code, giving `bmad-build` the lab standards in a project, testing numerical or quantum code, or reproducibility of code. |
| `help/evidence-and-citations.md` | How claims and citations are verified, the citation record (`reference_audit.csv`, notes), the claim ledger, or fact-checking rules. |
| `help/responsible-use.md` | Authorship, AI disclosure, ethics, integrity, what the lab will and will not do, peer-review confidentiality, AI-USE notebook entries. |
| `help/voice.md` | Tone, AI tells, natural language, the author's style sheet, or prose habits in a particular language and the language packs. |
| `help/new-project.md` | Starting a new research project with the lab, installing the lab in another repository, or the project layout. |
