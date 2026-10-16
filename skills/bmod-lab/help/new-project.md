# Starting a project with the lab

Read this when the user asks how to start a new research project, how to install the lab in another repository, or how a lab project is laid out.

## In a repository that already has the lab

1. Set an initiative per project with the `bmad` skill ("set the active initiative to <slug>"), so each project's documents stay in their own folder.
2. Talk to Nadia ("talk to Nadia, I have an idea about …"), or run `lab-spark` directly.
3. Follow her recommendation. A typical first week runs Spark, Survey, the G1 kill test, Frame, the G2 steering decision and Plan, and then the riskiest story starts.

## Installing the lab in another repository

The lab's source lives in the ResearchLab repository under `skills/`. In the target repository:

1. Run the installer, or ask the AI assistant to follow `BOOTSTRAP.md` in the lab, which runs it:
   `uv run <ResearchLab>/tools/install_lab.py <target-repository> --author "<name>" --affiliation "<affiliation>"`.
2. The installer does four things:
   - installs BMad, with its core tools and method modules, if it is missing;
   - links every `lab-*` skill and `bmod-lab` into the target's shared `.agents/skills/` folder, and into each assistant's own skills folder that holds BMad, so the target always runs the current version of the lab;
   - registers the `lab` module with the author, affiliation, ORCID and papers folder;
   - gives `bmad-build` the lab's research-software standards (`help/research-software.md`).
3. Running it again is safe: it keeps earlier answers and removes its own links to skills the lab has retired. Where links are not allowed, it copies the skills instead.

## Project layout

```
<repository>/
  _bmad-output/<initiative>/      lab documents: ideas-, survey-, brief-, plan-, notebook-, …
  papers/<slug>/                  main.tex, references.bib, figures/ (numbers.json),
                                  references/ (reference_audit.csv, notes/, txt/, pdf/), claims.csv
  src/<package>/                  research code (src layout)
  tests/                          one test per numbered statement the code touches
  scripts/figures.py              regenerates every figure and number from a fixed seed
  pyproject.toml, uv.lock         pinned environment
```

Keep `references/pdf/` and `references/txt/` out of any public deposit: they hold third-party copyrighted text.
