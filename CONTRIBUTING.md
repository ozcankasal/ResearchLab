# Contributing to Research Lab

Thank you for helping researchers in your field. You do not need to be a programmer to contribute: the most useful contributions are short TOML and Markdown files written by people who know a field well.

## Ground rules

- **Personas are fictional.** Never voice a real researcher; cite their work instead. Before naming a persona, search that the name does not belong to a known person in the field.
- **Sources are opened, not remembered.** Every factual statement in a pack, playbook or guide comes from a source you have read, with a link.
- **Nothing that hides AI use.** No feature, prompt or wording that disguises AI-generated text, fabricates evidence or weakens disclosure will be merged. See [`ETHICS.md`](ETHICS.md).
- **Plain language.** Many readers are researchers who do not program. Write for them.
- Everyone follows the [code of conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

| Contribution | Where it lives | Skills needed |
|---|---|---|
| A domain pack for your field | `skills/lab-cast/catalogue/packs/<field>.toml` | knowing the field |
| Literature databases for a field | `skills/lab-cast/catalogue/rules.toml` | knowing the field |
| A method playbook | `skills/lab-cast/playbooks/<name>.md` | knowing a method |
| A reviewed language pack for the voice check | starts from `skills/lab-voice/assets/pack-template.toml` | being a fluent reader of the language |
| A translation of the getting-started guide | `docs/getting-started.<language code>.md` | being fluent in the language |
| Bug reports and fixes | anywhere | depends on the bug |

Not sure where to start? Open an issue with the **Add my field** template, and we can work out the pack together.

## Add a domain pack

A pack gives a field ready-made, named experts. Without one, `lab-cast` designs experts for each project. A pack makes them consistent and reviewable.

1. Copy `skills/lab-cast/catalogue/packs/mathematics.toml` to `packs/<your-field>.toml`.
2. Fill in the `[pack]` table:
   - `id`: a short lowercase name, such as `ecology`;
   - `name`: the field's name;
   - `fields`: one or more OECD codes from the `[fos]` table in `rules.toml`, such as `"1.5"` or `"3.2"`;
   - `keywords`: lowercase phrases. With an empty list, the pack joins every project in those fields. With keywords, it joins only when a keyword appears in the project's title, subfields or keywords. A matching subfield is then treated as covered, so the lab generates no extra experts for it.
3. Add two or more `[[persona]]` entries, one of them a skeptic:
   - `code`: `pack-<id>-<role>`, unique in the catalogue;
   - `slot`: `core` (an insider), `skeptic` (knows how claims die in this field) or `translator` (brings in a neighbouring field);
   - `name`, `icon` and `title`;
   - `persona`: two or three sentences giving what they ask for first, the mistakes they catch, and a voice;
   - `playbooks`: optional names of files in `skills/lab-cast/playbooks/`, without `.md`.
4. If the lab doesn't yet name your field's databases, add a `[fields."<code>"]` table with `name` and `search` in `rules.toml`.
5. Run the tests (see below). `test_catalogue_is_well_formed` checks codes, slots, fields and playbooks.
6. Open a pull request. Say how you know the field, and link the sources behind the personas' habits.

## Run the checks

You need [uv](https://docs.astral.sh/uv/). From the repository root, run the tests for the scripts:

```bash
for t in skills/*/scripts/tests; do uv run --with pytest pytest -q -p no:cacheprovider "$t"; done
```

`tools/check.sh` does more. It regenerates the agents, the roster and the README figures, then runs every check. Commit the regenerated files with your change; CI fails when they are stale. Two of its checks need BMad installed in your clone:

- **The manifest check** needs `_bmad/`, which setting BMad up in the clone creates. Point your AI assistant at the clone and ask it to run the `bmad` skill's setup.
- **The skill checks** need the `bmad-toolsmith` skill in `.agents/skills/`.

Without them, `check.sh` skips those checks and says so. Both folders are ignored by git.

To change the core team, the guests or the rooms, edit `tools/cast.py` and run `uv run tools/build_cast.py`. Don't edit the generated files under `skills/lab-agent-*` by hand.

## Pull requests

- Keep each pull request to one change, such as one pack or one fix.
- Fill in the template's checklist.
- Expect questions about sources: they are how the lab stays trustworthy.
