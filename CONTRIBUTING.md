# Contributing to Research Lab

Thank you for helping researchers in your field. The lab already works in any field without changes: for each project it designs domain experts for that project's subfields. What makes it sharper is knowledge from people who work in a field. You don't need to be a programmer to share it; most contributions are a few lines in a plain text file, and you can also just describe them in an issue.

## Ground rules

- **Personas are fictional.** Never voice a real researcher; cite their work instead. Before naming a persona, search that the name does not belong to a known person in the field.
- **Sources are opened, not remembered.** Every factual statement in a contribution, such as a database, a standard, a playbook or a persona's habits, comes from a source you have read, with a link.
- **Nothing that hides AI use.** No feature, prompt or wording that disguises AI-generated text, fabricates evidence or weakens disclosure will be merged. See [`ETHICS.md`](ETHICS.md).
- **Plain language.** Many readers are researchers who do not program. Write for them.
- Everyone follows the [code of conduct](CODE_OF_CONDUCT.md).

## Ways to contribute

| Contribution | Where it lives | Skills needed |
|---|---|---|
| Your field's literature databases and archives | `skills/lab-cast/catalogue/rules.toml` | knowing the field |
| Reporting standards your venues expect | `skills/lab-cast/catalogue/rules.toml` | knowing the field |
| A method playbook | `skills/lab-cast/playbooks/<name>.md` | knowing a method |
| A reviewed language pack for the voice check | starts from `skills/lab-voice/assets/pack-template.toml` | being a fluent reader of the language |
| A translation of the getting-started guide | `docs/getting-started.<language code>.md` | being fluent in the language |
| Bug reports and fixes | anywhere | depends on the bug |
| Expert presets for a field (optional, advanced) | `skills/lab-cast/catalogue/packs/<field>.toml` | knowing the field well |

Not sure where to start? Open an issue with the **Improve the lab for my field** template and describe your field in plain words. We can turn it into the right files together.

## Share your field's databases

When `lab-cast` plans a project, it tells the librarian where to search. General sources such as OpenAlex, Semantic Scholar and Google Scholar are always included; a field can add its own. To add yours, find your field's OECD code in the `[fos]` table of `rules.toml`, then add or extend its entry:

```toml
[fields."1.6"]
name = "Biological sciences"
search = ["PubMed", "bioRxiv"]
```

Reporting standards belong to research modes rather than fields, in the `reporting` line of each `[modes.<mode>]` table. Suggest a change there when your field's standard is missing.

## Expert presets (optional)

No field needs a preset. Without one, `lab-cast` designs the domain experts for each project: two from rival schools, a skeptic and a translator for each subfield. A preset only keeps named experts ready, so that the same people return in every project in a field and can be reviewed once by people who know it. The three presets in the lab, for mathematics, physics and quantum computing, are there mainly as examples of the format.

To write one:

1. Copy `skills/lab-cast/catalogue/packs/mathematics.toml` to `packs/<your-field>.toml`.
2. Fill in the `[pack]` table:
   - `id`: a short lowercase name, such as `ecology`;
   - `name`: the field's name;
   - `fields`: one or more OECD codes from the `[fos]` table in `rules.toml`, such as `"1.5"` or `"3.2"`;
   - `keywords`: lowercase phrases. With an empty list, the preset joins every project in those fields. With keywords, it joins only when a keyword appears in the project's title, subfields or keywords; a matching subfield then gets the preset's experts instead of designed ones.
3. Add two or more `[[persona]]` entries, one of them a skeptic:
   - `code`: `pack-<id>-<role>`, unique in the catalogue;
   - `slot`: `core` (an insider), `skeptic` (knows how claims fail in this field) or `translator` (brings in a neighbouring field);
   - `name`, `icon` and `title`;
   - `persona`: two or three sentences giving what they ask for first, the mistakes they catch, and a voice;
   - `playbooks`: optional names of files in `skills/lab-cast/playbooks/`, without `.md`.
4. Run the tests (see below). `test_catalogue_is_well_formed` checks codes, slots, fields and playbooks.
5. Open a pull request. Say how you know the field, and link the sources behind the personas' habits.

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

- Keep each pull request to one change, such as one field's databases, one playbook or one fix.
- Fill in the template's checklist.
- Expect questions about sources: they are how the lab stays trustworthy.
