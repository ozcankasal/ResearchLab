# Depositing on Zenodo

This folder is self-contained and lives outside the paper repository.

| File | Upload? | What it is |
|---|---|---|
| `{pdf}` | yes | the paper, {pages} pages, PDF title and author set |
| `latex-source.tar.gz` | optional | the LaTeX source |
| `{code zip}` | optional | the reference implementation v{version} ({n} files: source, tests, figure script, README, licence, citation record) |
| `ZENODO-STEPS.md` | no | this file |

## Steps

1. Log in at https://zenodo.org.
2. Click **New upload**.
3. Drag the files you are uploading into the box.
4. Paste the metadata below.
5. Click **Save draft**, then **Preview**, and check the title, the name, the affiliation and that the PDF opens.
6. Click **Publish**. The DOI is live at once and cannot be deleted; later changes are new versions.
7. Put the DOI in the repository README and in `CITATION.cff`.

## Metadata

**Resource type**: Publication › Preprint

**Title**: {title}

**Creators**: {Surname, Given}. Affiliation: {affiliation}. ORCID: {orcid}.

**Description** (plain text):

{description}

**Licence**: CC BY 4.0 (the code in the zip keeps its MIT licence).

**Keywords**: {one per line}

**Subjects**: {e.g. Quantum Physics; Mathematical Physics}

**Version**: {version}

**Related identifiers**: {DOI, relation}

**AI-use statement**: {what AI tools were used for and what the authors did with the output, compiled from the notebook's AI-USE entries at gate G5 and checked by the authors}
