---
name: lab-survey
description: "Surveys prior art and literature with a rerunnable search log, snowballing, terminology-drift and fingerprint searches, and a verdict per idea. Use when the user says 'who did this before', 'literature review', 'prior-art search', 'survey the field', 'is this new', 'run a terminology-drift search' or works on a LIT story."
---
# Prior-Art Survey

You find what is already known before the lab spends time on it. The outcome is a dossier with a verdict per idea or claim. ALIVE means no prior art found. ALIVE-NARROW means prior art covers part of it: say which part and state the exact difference. DEAD means already done, with the source.

The dossier comes with a search log that someone else could rerun, and reading notes that quote sources verbatim. The PI decides gate G1 from it, the brief cites it, and the paper's related-work section is written from it, all without this conversation in the room. So a source enters the dossier only once it has been opened, and the log says just as clearly what was not searched.

Novelty that exists only because a field uses a different name is the commonest failure. One paper re-derived the trapezoidal rule under a new name and has been cited hundreds of times. The survey's job is to rule that out.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: `{workflow.survey_output_path}/{workflow.run_folder_pattern}/survey-{slug}.md` from `assets/survey-template.md`, with notes in `notes/` beside it; `{output_folder}` and `{active_initiative}` are filled in and `/{active_initiative}` is dropped when unset. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## How to work

1. **Choose the depth.** Use a rapid scan for a G1 decision, a scoping review to map a field, and a systematic review only when the paper is itself a review. Say which, since it sets how many sources and screeners are enough.
2. **Write the object down by its defining property, then build the synonym table.** List the object's names in every field where it could live. Plan both name searches and fingerprint searches: integer sequences in the OEIS, MSC codes in zbMATH, a formula or invariant written out in full. Search the databases the project's plan (`cast-*/plan.json`) lists for its fields, plus any the subject needs. Read `references/search-protocol.md` for the syntax of each source and the log format.
3. **Search, screen and snowball.** Run the queries and log every one, then screen titles and abstracts. From the closest three to five papers, snowball backward and forward until no new relevant paper appears. Use independent subagents for separate fields when they are available. Each subagent returns its log and the papers it opened.
4. **Read and note.** For each paper that bears on a claim, open it and quote the passage verbatim with its page. Record the closest prior result and the exact difference from ours. A remembered title stays a lead until it is opened. A source that turns out to be retracted, or to have an erratum, is flagged.
5. **Give a verdict per idea.** Use ALIVE, ALIVE-NARROW (with the narrowed claim) or DEAD. Add the searches not run, and why. Offer `lab-killtest` for gate G1, and log the outcome with `lab-notebook`.

Requests to search services carry no personal data: no names or emails in headers, queries or URLs. Respect their rate limits.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
