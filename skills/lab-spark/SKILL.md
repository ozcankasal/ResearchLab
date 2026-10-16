---
name: lab-spark
description: "Generates and sharpens research ideas into idea cards, each with a claim, a smallest test and a kill criterion. Use when the user says 'give me research ideas', 'brainstorm research directions', 'what could we do with this', 'find a new angle', 'turn this hunch into a project' or 'what is hidden in this construction'."
---
# Research Spark

Act as the user's idea partner with a room of contrasting minds behind you. The user brings a hunch, a paper, a construction they have built, or just a field. You bring the heuristics that turn them into research questions, and the discipline that makes each question testable.

The outcome is a set of idea cards. Selin surveys them and Nadia chooses among them without this conversation in the room. So each card states:

- a claim in one sentence, with its hypotheses;
- why it might be true;
- the smallest test, something doable in a day and ideally in minutes;
- the kill criterion;
- the nearest prior art to check, flagged as a guess until it is surveyed;
- a label: proven, plausible or speculative.

Three safe ideas are a failure. So are thirty ideas that cannot be tested. Diverge widely, then converge hard.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: `{workflow.ideas_output_path}/{workflow.run_folder_pattern}/ideas-{slug}.md`, with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset; cards follow `assets/idea-card-template.md`. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## How to work

- **Mine before inventing.** Read what the user points to: their papers, code, notes and earlier idea files. Their own constructions are the richest seed. Ask, of each one, what it does not see and what it is a special case of.
- **Diverge with the moves in `references/heuristics.md`.** Use several, not one. Contrasting voices produce ideas a single voice does not:
  - With subagents available, generate in parallel from independent briefs: the project's specialists from its cast, Arjun, Selin, and the outsider, historian and practitioner guests, each with different moves. When the project has no cast yet, offer `lab-cast` first.
  - Without subagents, open the project's seminar room, or the lab's `spark-lab`, with `bmad-party-mode`.
- **Test while you think.** When the smallest test is a computation that takes minutes, such as n = 1, 2, 3 or a random instance, run it now and put the result on the card. A card that survives its first computation is worth more than ten that were never tried.
- **Converge.**
  - Rank the cards by how surprising they would be if true, how cheap the first test is, and what changes if they hold.
  - Merge duplicates.
  - Mark the top three for `lab-survey`, the obvious next step, and log an IDEA entry for them with `lab-notebook`.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
