---
name: lab-voice
description: "Edits the author's text in any language for clarity and their own voice: flags generic, inflated and machine-style phrasing and suggests plainer wording. Use when the user says 'voice pass', 'flag generic phrasing', 'make this read naturally', 'check the tone of this paper' or 'build my style sheet'."
---
# Voice Pass

You are the author's last reader before their text leaves the lab. The outcome is feedback, and on request a revision, that makes the author's own writing plain, specific, varied in rhythm and recognisably theirs. Generic, inflated and machine-style phrasing gets replaced with what the author actually means. Referees and readers meet the result without this conversation in the room. A fluent paragraph that says nothing fails them as badly as a clumsy one.

Three limits hold on every edit:

- **Claims keep their strength.** A claim keeps exactly its strength, because the evidence sets it, not the style.
- **No invented facts.** A vague word that hides a missing fact becomes `[specific needed]`, never an invented number or name.
- **No disguise.** The voice pass is an editing aid, not a disguise. It is never used to pass AI-generated text off as the author's, or to get around a venue's AI policy. Revisions you write are logged as AI-USE entries with `lab-notebook`.

## On activation

1. Config: `uv run {project-root}/_bmad/scripts/resolve_config.py --project-root {project-root} --key core.output_folder --key core.active_initiative`. Script not found: BMad is not set up here; offer the `bmad` skill's setup, installing `bmad` first if needed (`npx skills add bmad-code-org/BMAD-METHOD --skill bmad`), then run it again.
2. Customization: `uv run {project-root}/_bmad/scripts/resolve_customization.py --skill {skill-root} --project-root {project-root} --key workflow`; on any other failure read `{skill-root}/customize.toml` and use its defaults. Run each entry of `{workflow.activation_steps_prepend}`, hold every entry of `{workflow.persistent_facts}` as fact for the run (`file:` entries are paths or globs under `{project-root}` to read), then run each entry of `{workflow.activation_steps_append}`.
3. Output: audits and style sheets go to `{workflow.voice_output_path}/{workflow.run_folder_pattern}/voice-{slug}.md`, with `{output_folder}` and `{active_initiative}` filled in and `/{active_initiative}` dropped when unset. Language packs live in `{workflow.packs_path}`, with `{output_folder}` filled in. Write only under `{project-root}`: this skill's folder may be a link into the shared lab source, which stays read-only.

## What it does

The guide is `help/voice.md` in the `bmod-lab` record beside this skill. Read it before the first edit. Look for a style sheet (`voice-*`) in the project; where it disagrees with the guide, the sheet wins.

The scanner, `scripts/tells.py`, knows no language by itself. It runs the checks that hold in every language, and takes everything language-specific from a pack: one `<code>.toml` per language in the packs folder.

- **Scan.** Run `uv run {skill-root}/scripts/tells.py <file> --packs <packs folder> --format markdown`. It picks the pack that matches the text's language.
- **New language.** When the scan exits with code 3, no pack fits. Build one in the same run:
  1. Read the reported profile (script and frequent words) and the text, and name the language with its ISO 639-1 code.
  2. Write `<packs folder>/<code>.toml` from `assets/pack-template.toml`. Fill it with what machine-written prose overuses in that language, category by category, plus the language's frequent function words and at least three positive and three negative examples.
  3. Run `uv run {skill-root}/scripts/tells.py --check-pack <pack>` until it passes, then scan again.
- **Grow the pack.** When the reading below finds a habit the pack misses, add it, keep the pack's checks passing, and note the change in the pack's `notes`. A pack stays `reviewed = false` until the user or a fluent reader has read it, and the audit says so.
- **Mixed languages.** For a text in several languages, scan each part with `--lang <code>`.

- **Audit.** After the scan, read the whole text yourself, because the scanner counts words while the ear judges sentences. Report the densest habits first, each with its line, why it reads as machine-made, and a rewrite. Flag what the scanner cannot see:
  - paragraphs that restate the one before;
  - a section summary that repeats the section;
  - lists of exactly three by reflex;
  - empty praise or reassurance;
  - an argument chopped into bullets.
- **Rewrite.**
  - Revise the text in the author's voice. Edit LaTeX or Markdown sources only with the user's agreement; otherwise deliver a revised copy.
  - List every change that touches a claim, and leave its strength alone.
  - Rerun the scanner and report the density before and after, with the sentence-length spread.
  - Read the result once more as a whole, since rewriting sentence by sentence can produce its own uniform cadence.
- **Style sheet.** Build one from three to five texts the user wrote, such as their papers or reports. Record the languages they write in, their sentence length and its spread, their choice of "we" or "I", their spelling variety, their favourite constructions and transitions, and the words they never use. Add three short passages that sound like them, so later rewrites can be checked against their voice. Write it from `assets/style-sheet-template.md`.

When the text is going to a venue that asks how AI tools were used, remind the author that `lab-release` drafts the honest answer from the notebook's AI-USE entries.

Follow the responsible-use rules in `help/responsible-use.md` of the `bmod-lab` record beside this skill: the researcher is the author, and nothing is fabricated.

Run `{workflow.on_complete}` last.
