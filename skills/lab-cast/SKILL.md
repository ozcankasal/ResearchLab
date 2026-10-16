---
name: lab-cast
description: "Classifies a research project by field, method, outputs and sensitivities, then casts its specialists, guardians and rooms and sets its story types, reporting standards and search databases. Use when the user says 'start a new project', 'classify this project', 'cast experts for this project', 'who should be in the room for this field', 'add a specialist for' or 'the project moved into a new field'; the PI runs it when a project starts."
---
# Classification and Casting

The lab's eight core assistants work in every field. A project also needs people who know its field and its methods from the inside: the schools and their quarrels, the standard names for things, the folklore results, and the referee who would reject the paper. It may also need guardians, for example when people, personal data or dual-use material are involved.

The outcome is three things:

- the project's **profile**: a classification of the project;
- its **plan**: what that classification implies;
- its **cast**: specialists and rooms, written into the project's own party-mode customization.

The other workflows read the plan, without this conversation in the room, to know which story types, reporting standard, search databases and extra gate conditions apply. `bmad-party-mode` and the Expert Desk use the cast. So the cast must meet a bar:

- the classification is one the researcher confirmed;
- every specialist is grounded in real, verified works;
- no persona speaks as a real person.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: the folder `{workflow.cast_output_path}/{workflow.run_folder_pattern}/`, with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset. It holds `profile.toml`, `plan.json` and the cast sheet `cast-{slug}.md` (from `assets/cast-template.md`). The personas and rooms go into the project's `_bmad/custom/bmad-party-mode.toml`. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## How to work

1. **Classify.** Read the brief, the idea cards or the researcher's description. Fill `profile.toml` from `assets/profile-template.toml`:
   - the fields, as OECD Fields of Science codes;
   - the subfields, in the field's own words;
   - the research modes;
   - the outputs;
   - the sensitivities;
   - the keywords.

   `help/classification.md` in the `bmod-lab` record beside this skill defines each axis. Ask only what you cannot read, and have the researcher confirm the classification: everything downstream follows from it.
2. **Plan.** Run `uv run {skill-root}/scripts/cast_plan.py <profile.toml> --format json > plan.json` and fix any errors it reports. The plan names:
   - the method specialists for the modes and the guardians for the sensitivities, all of them fixed, named personas;
   - any optional expert presets (`catalogue/packs/`) that match the project;
   - the generation slots: the subfields that no preset covers, usually all of them;
   - the story types, the reporting standards, the search databases, the extra gate conditions and the project rooms.
3. **Design the domain experts.** For each generation slot, design a domain expert following `references/casting.md` (slots, contrast rules, the rule for real people), with `references/domain-seeds.md` as a starting point. Ground each one in two to five real works. Open them, or check their metadata on Crossref or arXiv, and record the verification level. A work you could not check stays out.
4. **Read back.** Show the cast as a table: name, where it came from (core, guardian, method, preset, or designed), the question each asks, and the rooms. Show the plan's story types, standards and gates too. Adjust with the researcher.
5. **Write.**
   - Write the cast sheet.
   - Assemble the party-mode block: `cast_plan.py <profile.toml> --format toml` gives the catalogue personas and rooms; add the generated experts as `[[workflow.party_members]]` with codes `x-<slug>-<role>`, and append their codes to the rooms as the plan's `add_generated` says.
   - Invoke the `bmad-customize` skill to merge the block into `{project-root}/_bmad/custom/bmad-party-mode.toml` as a team override. Entries merge by `code` and `id`, so existing ones stay. If `bmad-customize` is not installed, offer `npx skills add bmad-code-org/BMAD-METHOD --skill bmad-customize`.
6. **Log and offer.** Log a DECISION entry with `lab-notebook`, then offer the project's seminar room (`bmad-party-mode --party <slug>-seminar`) or the Expert Desk (`lab-agent-expert`).

When the project moves into a new field or method, update the profile and run again: new specialists are added, and the ones that no longer fit leave the rooms. Never rename a persona's code.

Prose you write for others follows the lab's voice guide, `help/voice.md` in the `bmod-lab` record beside this skill, and the responsible-use rules in `help/responsible-use.md` there: the researcher is the author, nothing is fabricated, and AI help that reaches a project output is logged as an AI-USE entry with `lab-notebook`.

Run `{workflow.on_complete}` last.
