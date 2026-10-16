# Search protocol

## Sources and their syntax

| Source | Strength | Syntax and limits |
|---|---|---|
| arXiv API (`export.arxiv.org/api/query`) | physics, math, CS preprints | field prefixes `ti:`, `au:`, `abs:`, `cat:`; `AND`, `OR`, `ANDNOT`; `submittedDate:[YYYYMMDDTTTT TO …]`; at most 30 000 results per query; about 3 s between calls |
| INSPIRE-HEP | high-energy and quantum physics, citations | `a`, `t`, `de`, `topcite`, `refersto:` for forward citations |
| zbMATH Open | mathematics since 1868, MSC codes, swMATH software | MSC classification, author profiles, links to arXiv full texts, OEIS and DLMF |
| MathSciNet | reviewed mathematics literature | MR author IDs, MSC2020, its own citation database (needs a subscription) |
| Semantic Scholar and OpenAlex APIs | cross-field, citation graph | search plus references and citations of a paper, for snowballing |
| Crossref API | metadata, DOIs, journal articles | `/works?query=`; `/works/{doi}` |
| Google Scholar (manual) | broad recall, "Cited by" | `author:`, exact phrases; at most 1000 results; set alerts on the closest papers |
| OEIS | fingerprint search by integer sequence | enter about six terms, from the second term on; try Superseeker when there is no hit |
| Espacenet and Google Patents | patents | CPC classes for the technology and the application domain |
| PubMed/MEDLINE, Cochrane Library, ClinicalTrials.gov | medicine and health | MeSH terms; trial registries for unpublished and ongoing trials |
| Scopus, Web of Science | all fields, citation graph | field tags and citation searches (subscription) |
| SSRN, RePEc/IDEAS, PsycINFO, ERIC | economics, psychology, education | each database's subject headings |
| JSTOR, PhilPapers, MLA International Bibliography, archive catalogues | humanities | subject headings; for archives, the finding aids |

The project's plan (`cast-*/plan.json`) lists the databases its fields call for. Treat the list as the minimum to search, not the limit.

## The search log

Each search adds one line:

`date · source · exact query · limits (years, categories) · hits · screened · kept · notes`

At the end of the survey, also record:

- the databases not searched, and why;
- how duplicates were removed;
- the snowballing rounds, with how many new papers each one added.

This is the core of the PRISMA-S reporting items. It lets a stranger rerun the search.

## Screening

- Screen on title and abstract first, and on full text for inclusion.
- Pilot the inclusion criteria on the first 30 to 50 results before screening the rest.
- With subagents available, have a second screener check a sample of the exclusions.

## Snowballing

- Start from the closest three to five papers.
- **Backward:** go through their reference lists.
- **Forward:** go through the papers that cite them.
- Include on full text, and repeat until a round adds nothing relevant.

## Retractions and corrections

Before a source becomes load-bearing, check it for a retraction or erratum on the publisher's page. Crossref now publishes the Retraction Watch data openly. Citing papers rarely mention a retraction, so do not rely on them to flag it.

Sources, opened 2026-10-16 (see the lab repository's `docs/best-practices/research.md` for the full list):

- Rethlefsen et al., PRISMA-S (2021): <https://experts.mcmaster.ca/scholarly-works/2067615>
- arXiv API user manual: <https://info.arxiv.org/help/api/user-manual.html>
- OEIS hints: <https://oeis.org/hints.html>
- Wikipedia, "Tai's model": <https://en.wikipedia.org/wiki/Tai%27s_model>
- Crossref and Retraction Watch (2023): <https://crossref.org/blog/news-crossref-and-retraction-watch>
