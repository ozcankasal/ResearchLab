# Classifying a project

Read this when the user asks how the lab classifies a project, what a research mode or sensitivity means, or why a specialist, guardian, story type or gate was chosen. The classification decides who joins the project and what the other workflows expect, so it is confirmed with the researcher before anything is cast. It has four axes and keywords.

## Field

Codes from the OECD Fields of Science and Technology (the full list is in `lab-cast/catalogue/rules.toml`). There are six areas:

1. natural sciences;
2. engineering and technology;
3. medical and health sciences;
4. agricultural sciences;
5. social sciences;
6. humanities.

Each area has numbered fields, such as 1.1 Mathematics, 3.3 Health sciences, 5.2 Economics and business or 6.1 History and archaeology. An interdisciplinary project lists every field it draws on. Subfields are written in the field's own words; they decide which domain experts are cast.

## Mode: how the project produces knowledge

| Mode | Looks like | Brings |
|---|---|---|
| formal | definitions, theorems, proofs, formal models | proof stories, a formal-verification specialist, a small-case calculator, a proof room |
| computational | simulation, numerical analysis, machine learning | experiment and code stories, a simulation and ML methods specialist |
| experimental | controlled experiments in a laboratory or the field | experiment and data stories, an experimental design specialist |
| observational | existing data, surveys, cohorts, registries | study and data stories, a causal-inference specialist |
| qualitative | interviews, ethnography, document and text analysis | study and data stories, a qualitative-methods specialist |
| design | building and evaluating an artifact, system or method | code and study stories, a design and evaluation specialist |
| synthesis | systematic or scoping reviews, meta-analysis | literature and data stories, an evidence-synthesis specialist |
| archival | primary sources, archives, historical records | literature and data stories, an archives specialist |

Most projects have two or three modes.

## Outputs

Paper, software, dataset, patent and report. Software and datasets add release conditions. A patent brings the IP officer and a publish-versus-protect decision at gate G2.

## Sensitivities

| Sensitivity | Applies when | Brings |
|---|---|---|
| human-participants | people are recruited, observed, interviewed or experimented on | the research ethics officer; approval before recruitment |
| personal-data | data relate to identifiable people, including pseudonymised records | the data protection officer; lawful basis, minimisation, no personal data in deposits |
| animals | animals are used | the ethics officer; animal ethics approval |
| clinical | patients, treatments or diagnostics | ethics and data protection; registration where required |
| dual-use | results could be misused for harm | the security and dual-use reviewer; a disclosure review before release |
| commercial | ownership, confidentiality or a patent is at stake | the IP officer; ownership settled before disclosure |
| regulated | a regulator governs the domain (finance, health, law) | the IP officer and the data protection officer; the rules named at gate G2 |

When in doubt, list the sensitivity. A guardian who has nothing to object to costs one sentence; a missing one can cost the project.

Source for the field codes: Wikipedia, "Fields of Science and Technology", opened 2026-10-16: <https://en.wikipedia.org/wiki/Fields_of_Science_and_Technology>. That page describes the OECD classification of 2002, revised in 2007.
