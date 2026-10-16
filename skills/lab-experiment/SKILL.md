---
name: lab-experiment
description: "Runs a computational experiment, from a protocol written before the run to a report with uncertainties, baselines and ablations. Use when the user says 'design an experiment', 'run a simulation', 'benchmark this', 'test this numerically', 'preregister the analysis' or works on an EXP story."
---
# Computational Experiment

You run experiments whose numbers mean what the text will say. The outcome is an experiment folder with three parts:

- a protocol, written and committed before the confirmatory run;
- the scripts and seeds that produce every number;
- a report that separates confirmatory from exploratory results and lists every deviation from the protocol.

The fact checker traces each number to it, the referee attacks it, and the paper quotes it, all without this conversation in the room. The usual failures are well known:

- an analysis chosen after seeing the data;
- a weak or untuned baseline;
- one seed;
- error bars that do not say what they measure;
- debugging that stops as soon as the numbers look right.

The protocol exists to prevent them.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: `{workflow.experiment_output_path}/{workflow.run_folder_pattern}/` holding `protocol.md` and `experiment-{slug}.md` (the report), with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset. Scripts go in the project's `scripts/`, and numbers go into its `numbers.json`. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## How to work

1. **Protocol.** Write it from `assets/protocol-template.md` with the user. Use `references/reporting.md`, and the reporting standard and gate conditions in the project's plan (`cast-*/plan.json`). For studies with people or personal data, approvals come before any recruitment. Explore freely on a development set first. Then freeze the protocol, commit it, and only afterwards run the confirmatory analysis on held-out instances.
2. **Baselines.** Build the strongest comparison you can: tuned with the same budget as our method, and checked against its published numbers where those exist. When the claim is an advantage over existing methods, include the strongest alternatives the project's specialists name, and an ablation that removes the new ingredient. For quantum claims, the quantum pack's advantage-audit playbook lists the classical methods.
3. **Run.** Use scripted runs with seeds from `SeedSequence`, enough seeds to estimate the spread, the environment pinned by the lock file, and outputs written to `numbers.json` and figures by script, never by hand. Where it is possible, fix every check before looking at the target quantity: blind the answer, then unblind as a recorded step.
4. **Report.** Write it from `assets/report-template.md`:
   - every metric with its uncertainty and what that uncertainty captures;
   - the number of runs and analyses tried;
   - deviations from the protocol;
   - confirmatory results and exploratory findings, labelled separately;
   - the conclusion stated against the claim's kill criterion.
5. **Hand over.** Offer Arjun's statistics review or the `build-room`. Log a RESULT entry, or a DEAD-END with its reason, using `lab-notebook`.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
