# Release checklist

## Paper PDF

- Built from the tagged state, with no build warnings and no undefined references.
- PDF title and author set in `hypersetup`.
- No draft or confidential notices left in the text.

## LaTeX source and arXiv

- Ship `main.tex`, `references.bib`, the figures it uses and, for arXiv, the `.bbl`. The `.bbl` must have the same name as the main `.tex` and must come from the same backend; TeX Live 2025 accepts only bbl format 3.3.
- Leave out `.aux`, `.log`, the compiled PDF and unused figures. Hidden files are deleted.
- **Comments are public** in the arXiv source download. Strip them (`arxiv-latex-cleaner` also drops unused images). The bundle script flags TODO, FIXME, private and confidential comments.
- The arXiv licence is irrevocable for each version, so choose it deliberately.
- Code or data can go in `anc/`. Explain every replacement in the Comments field, because all versions stay public.

## Code bundle

- Tracked source only:
  - README with the regenerate commands;
  - licence, MIT by default;
  - `pyproject.toml` and the lock file;
  - `src/`, `tests/` and the figures script, `{project-root}/scripts/figures.py`;
  - the paper source;
  - the citation record: the paper's `reference_audit.csv` and its notes folder.
- Never include `references/pdf/` or `references/txt/` (third-party text), secrets, caches, or experiments the paper does not use.
- Verify by unpacking into a fresh folder and running the tests: `bundle.py --verify`.
- Write a `CITATION.cff` (`cff-version: 1.2.0`) with a `preferred-citation` pointing to the paper.

## Zenodo

- **Resource type:** Publication › Preprint for the paper. Software for a separate code record.
- **Licence:** CC BY 4.0 for the paper; the code keeps its own licence file.
- **DOIs:**
  - Every version gets its own DOI. The concept DOI resolves to the latest version.
  - Cite a version DOI when the exact version matters, as with code behind numbers, and the concept DOI when you mean the work in general.
  - A published DOI cannot be deleted; only new versions can be added.
- **Related identifiers:** "References" for papers the work builds on; "Is supplemented by" for the code; "Is identical to" for the arXiv version once it exists.
- **GitHub integration:** it archives each release automatically, but only for public repositories. GitHub alone does not count as archived.

## Availability statements

- **Code availability:** name the repository, the version DOI and the licence.
- **Data:** name the data, or say that no data were generated. For purely mathematical work, say so.

## Artifact level to aim for

- **Available:** archived with a DOI.
- **Functional:** documented, complete and runnable.
- **Reproduced:** one script regenerates every number within the stated tolerances.

Sources, opened 2026-10-16:

- arXiv, submitting TeX/LaTeX: <https://info.arxiv.org/help/submit_tex.html>
- arXiv, ancillary files: <https://info.arxiv.org/help/ancillary_files.html>
- arxiv-latex-cleaner: <https://github.com/google-research/arxiv-latex-cleaner>
- Zenodo, DOI versioning: <https://support.zenodo.org/help/en-gb/1-upload-deposit/97-what-is-doi-versioning>
- Citation File Format: <https://citation-file-format.github.io/>
- ACM badges (as quoted by SIGIR): <https://sigir.org/general-information/acm-sigir-artifact-badging/>
- APS data availability statements: <https://journals.aps.org/authors/data-availability-statements>
- Nature Portfolio reporting standards: <https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards>
