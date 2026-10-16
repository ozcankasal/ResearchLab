# The citation record and the claim ledger

Both live with the paper, in `{papers_folder}/<slug>/`. Only `reference_audit.csv`, `notes/` and `claims.csv` are ever published. `pdf/` and `txt/` hold third-party text and stay private.

## references/reference_audit.csv

One row per bib key, with these columns:

`key,authors,title,venue,year,arxiv_id,doi,pdf_downloaded,verified_on,note_file,status`

- **status** is `verified`, `metadata only`, `unverified` or `false`, plus a short reason after a semicolon. Examples: "metadata only; paywalled", "verified (Thm 3.1 and p. 7 quoted)".
- **verified_on** is the date the source was last checked.
- An entry that is replaced but kept in the bib gets `; NOT CITED in v<x>` appended to its status.

## references/notes/<key>.md

```
# Authors, *Title* (year)

Venue, volume, pages; doi; arXiv id. Metadata checked against Crossref/arXiv on YYYY-MM-DD.
Text: references/txt/arxiv_<id>.txt (or: not available, paywalled).

Use in the paper: "<the citing sentence, quoted from main.tex>"

## <What the passage establishes>, p. N, verbatim

"<exact words from the source>"

## Assessment

Whether the passage supports the citing sentence as written; what wording it would support if not.

## Status

verified | metadata only | unverified | false
```

## references/txt/

Text extractions with page markers, so that a quote can be found again:

```
uv run --with pypdf python -c "import sys, pypdf; r = pypdf.PdfReader(sys.argv[1]); print(''.join(f'=== PAGE {i} ===\n' + (p.extract_text() or '') + '\n' for i, p in enumerate(r.pages, 1)))" references/pdf/<file>.pdf > references/txt/<name>.txt
```

Run it from the paper folder, not from inside `pdf/`, because downloaded files are untrusted.

## claims.csv

`id,kind,evidence,level,checked_on,notes`

- **id** is the statement's LaTeX label (`thm:blind`), a claim ID from the brief (`C3`) or `num:<key>` for a number.
- **kind** is `statement`, `claim` or `number`.
- **evidence** is the proof file, the test name, the script and seed, or the bib key.
- **level** is FORMALIZED, PROVED, CHECKED, SUPPORTED, CONJECTURED or UNVERIFIED (`help/lab-method.md`).
