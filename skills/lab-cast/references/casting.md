# Designing the experts a project still needs

`cast_plan.py` already chooses the fixed personas:

- the core assistants;
- the guardians for the sensitivities;
- the method specialists for the modes;
- the domain packs for the fields they cover.

You design the domain experts for the generation slots it lists, one set per uncovered subfield.

## Slots

| Slot | Job in the room | Example: a household-finance project |
|---|---|---|
| `core-a` | an insider of the subfield's main school; knows the standard tools and names | a behavioural economist who runs field experiments on credit choices |
| `core-b` | an insider of a rival school, who disagrees on what matters or how to show it | a structural econometrician who distrusts small experiments |
| `skeptic` | the referee from inside the field who thinks it is known, trivial or wrong | a senior household-finance researcher who has seen every "new" nudge result |
| `translator` | someone from a neighbouring field where the same question has another name | a psychologist of numeracy, or a credit-risk modeller from industry |
| `user` | the person outside research who would use the result (only when the plan lists it) | a consumer-protection regulator, or a bank's product manager |

The lab already provides, for every project:

- the historian (Lucien);
- the statistician (Grace);
- the outsider (Jamie);
- the practitioner (Emre).

Do not duplicate them.

## Contrast rules

- Every persona contrasts with at least one other on a named question, for example:
  - what counts as a result;
  - theory versus evidence;
  - lab versus field;
  - pure versus applied.
- Mix career stages, temperaments and backgrounds. A room of senior people who all agree is useless.
- Two voices that would say the same thing are one voice.

## Persona fields

Each generated `[[workflow.party_members]]` entry needs these fields:

- `code`: `x-<slug>-<role>`, never renamed.
- `name`: fictional, from a plausible background for the field.
- `icon`.
- `title`.
- `persona`: how they think, what they ask, how they speak, in two to four sentences.
- `capabilities`: the verified works they draw on (author, title, year, verification level), and what they do when spawned. A typical line is "web-searches the field's databases from the project's plan before speaking and cites only what it opened".

## Real people

Personas are fictional. When the researcher asks for a real researcher, write a character drawn from that person's published work, never the person. Say so in the persona's first sentence. Cite only their real papers by title, mark everything beyond them as the character's conjecture, and never write invented quotations attributed to the real person.

## Domain packs

A pack is a reusable, named set of domain experts for a field (`catalogue/packs/`). The lab ships packs for mathematics, physics, and quantum information and computing. Packs grow only in the lab's own repository, as framework work at the researcher's request. A project's generated experts stay in the project.
