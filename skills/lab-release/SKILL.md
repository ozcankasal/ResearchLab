---
name: lab-release
description: "Prepares a release: the disclosure and ownership gate, the deposit bundle and its records for Zenodo, arXiv and code. Use when the user says 'release this', 'put it on Zenodo', 'prepare the arXiv submission', 'package the code', 'make a CITATION.cff', 'Zenodo metadata' or 'run gate G5'."
---
# Release

You take the lab's work out of the building. The outcome is a deposit folder: the paper PDF with its metadata set, the LaTeX source, the code bundle and a step-by-step `ZENODO-STEPS.md`. The folder sits outside the project repository unless the user says otherwise, and the bundle is proven to run from a clean copy. The records that go with it are the title, a plain-text description, keywords, subjects, licences, related identifiers and a `CITATION.cff`.

The user uploads from the folder without this conversation in the room, and the public reads the record for years. So nothing private leaves: no third-party PDFs, no extracted texts, no secrets and no unreleased experiments. Nothing irreversible happens before the disclosure check: a DOI cannot be deleted.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative --key modules.lab.papers_folder --key modules.lab.author --key modules.lab.affiliation --key modules.lab.orcid`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: the deposit folder the manifest names. The manifest is `release.toml` at the project root, written from `assets/release-template.toml`. Write only under `{project-root}` and in that deposit folder: this skill's folder may be a link into the shared lab source, which stays read-only.

## How to work

1. **Gate G5, disclosure and ownership.** Ask the user, and record each answer in the notebook:
   - **Patent.** Does any result need patent protection before it is public? Some patent systems, Europe's among them, give no grace period.
   - **Rights.** Who owns the work: an employer, a funder or co-authors? Who must approve the release?
   - **Data.** Does any data carry privacy or contract limits?
   - **AI use.** What does the venue's policy on AI-assisted writing and code ask the authors to disclose? Collect the project's AI-USE entries from the notebook and draft the disclosure statement from them for the author to check and adapt. The record says it truthfully.

   - **The plan's gates.** Is every G5 condition in the project's plan (`cast-*/plan.json`) met?

   Stop at any unresolved "no". Offer the `steering-committee` room to settle it.
2. **Check gate G4.** The ledger, the references and the numbers must already be clean (`lab-factcheck`). If they are not, offer that first.
3. **Build the bundle.**
   - Write `release.toml`.
   - Run `uv run {skill-root}/scripts/bundle.py release.toml --dry-run --format markdown`, and fix every error.
   - Build with `--verify "uv run pytest -q"`, or whatever command the project's README gives, so the code is proven to run from a clean copy.
   - Read `references/release-checklist.md` for Zenodo, arXiv and code specifics.
4. **Write the records.**
   - Title, plain-text description, keywords, subjects, licences, version and related identifiers, using the user's name, affiliation and ORCID from config.
   - Run the voice pass (`lab-voice`) on the description.
   - Fill in `ZENODO-STEPS.md` from `assets/ZENODO-STEPS-template.md` and `CITATION.cff` from `assets/CITATION-template.cff`.
5. **Hand over.** Say what to upload and in which order, and what to do with the DOI afterwards. Log a GATE entry with `lab-notebook`. Uploading and publishing are the user's own steps, and so is any commit.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
