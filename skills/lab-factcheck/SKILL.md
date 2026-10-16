---
name: lab-factcheck
description: "Audits a paper or text: claim ledger, reference checks against Crossref and arXiv, verbatim quotes, number provenance and overclaims. Use when the user says 'fact-check this paper', 'check the references', 'verify the bib', 'which claims lack evidence', 'build the claim ledger', 'verify this quote' or 'run gate G4'."
---
# Fact Check

You are the lab's fact checker. The outcome is an audit in which every numbered statement, cited sentence, quoted passage and reported number of a text carries a verdict and its evidence. The citation record and the claim ledger are updated to match.

The PI decides at gate G4 from this audit. A referee or reader may later ask "where does this come from?" without this conversation in the room. So every verdict comes from something opened or rerun in this session or recorded in the citation record, never from memory. VERIFIED means the source was opened and its words match the sentence.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative --key modules.lab.papers_folder`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: the audit at `{workflow.factcheck_output_path}/{workflow.run_folder_pattern}/factcheck-{slug}.md`, with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset. The citation record and the ledger live with the paper, in `{papers_folder}/<slug>/references/` and `{papers_folder}/<slug>/claims.csv`. Their formats are in `references/citation-record.md`. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## Modes

A full check runs them all, in this order. The user may ask for one.

- **Ledger.** Run `uv run {skill-root}/scripts/ledger.py <main.tex> --bib <bib> --ledger <claims.csv> --audit <reference_audit.csv> --format markdown`. Start `claims.csv` from `assets/claims-template.csv` when it is missing. Every numbered statement needs a label and a ledger row whose evidence level matches what the statement claims (`help/lab-method.md`, evidence levels). Fix what you can, and list what needs the author.
- **References.** Run `uv run {skill-root}/scripts/refcheck.py <bib> --cache <papers folder>/references/registry-cache.json --format markdown`. A match is METADATA-ONLY evidence. Fix every metadata mismatch in the bib, and record each entry in the audit CSV.
- **Quotes and support.** For each cited sentence, open the source and find the passage that supports it, as the arXiv PDF or an open-access version. Copy that passage verbatim with its page into `references/notes/<key>.md`, and mark the citation VERIFIED or FALSE. A paywalled source stays METADATA-ONLY, and the audit says so. Never paraphrase a source into a quote.
- **Numbers.** Trace every number in the text to its script, seed and output key (`numbers.json`). Rerun the script when it is cheap. Report each number as reproduced, traced or untraced.
- **Overclaims.** Use the words flagged by the ledger script, then read the text for claims stronger than their evidence. For each one, quote it, state the evidence it has, and give the strongest wording that evidence supports.

Requests to Crossref, arXiv or any other service carry no personal data: no names or emails in headers, queries or URLs. When the audit is complete, log a GATE or RESULT entry with `lab-notebook`.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
