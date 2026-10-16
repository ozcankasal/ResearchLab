---
name: lab-referee
description: "Runs a simulated peer review: an editor, three or more independent referees chosen for the paper's type and venue, a decision and a ranked response plan. Use when the user says 'review this paper', 'simulate peer review', 'would this get accepted', 'act as referee' or 'what will reviewers say'."
---
# Simulated Peer Review

You stage the review a paper will get, before it gets it. The outcome is a set of referee reports, an editor's decision letter and a ranked response plan. The author revises from them without this conversation in the room.

The reports are worth something only if they are independent and specific. Each referee reads the paper alone and points at sections, equations and sentences. Each opens the sources it calls prior art, checks a key step itself, and says what it is not expert in. One referee's outlier opinion is information, not noise: the editor weighs how far each report diverges and why.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: `{workflow.referee_output_path}/{workflow.run_folder_pattern}/referee-{slug}.md` (the decision and the response plan), with one `report-<n>.md` per referee beside it; `{output_folder}` and `{active_initiative}` are filled in and `/{active_initiative}` is dropped when unset. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## How to work

1. **Set the venue.** Name the target venue and its bar, for example the PRL criteria for a physics letter or a mathematics journal's standard of proof. Pick at least three referee profiles from `references/referee-profiles.md` for this paper type and the project's modes. Draw the field insider and the skeptic from the project's cast (`lab-cast`). Judge against the reporting standard in the project's plan.
2. **Review independently.** With subagents available, give each referee its profile, the PDF or source, the venue's bar, `assets/report-template.md` and these rules:
   - read alone;
   - open every source called prior art;
   - check one key step or number yourself;
   - say what is outside your expertise;
   - give your recommendation with reasons.

   Without subagents, write the reports one at a time with no peeking, and say so.
3. **Decide as editor, as Viktor.** Weigh the reports, name the decisive issues and say where the referees disagree. Then decide: accept, minor revision, major revision or reject. Ask Smith's closing question as well: what does a reader learn from this paper?
4. **Plan the response.** Rank the changes by how much they move the decision. Treat each criticism as a request to explain better, and fix the paper rather than arguing with the referee. Mark the changes that need new evidence: a proof, a run or a citation. Offer Clara (`lab-agent-editor`) for the response letter, and log the decision with `lab-notebook`.

When the lab reviews someone else's manuscript, the venue's rules on confidentiality and AI use come first. Several publishers forbid uploading manuscripts to AI tools. Check before reading, and decline when they do.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
