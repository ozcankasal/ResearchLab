# How claims die

Pick the attacks that fit the claim's kind and the project's modes. Each attack names its owner and the check that settles it. Where the owner reads "domain expert", "method specialist" or "guardian", use the project's own cast from `lab-cast`.

## Novelty, in every field

- **Same object, other name.** Owners: Selin, Lucien, the domain translator. The idea exists in a neighbouring field under another name. The lab's own history has examples: multiple-quantum coherences in NMR, the pole problem in nuclear physics, and a "new" rule for computing areas that was the trapezoidal rule. Write the object down by its defining property and search every field's name for it (`lab-survey` terminology-drift search).
- **Consequence of known work.** Owners: the domain skeptic, the core expert. The claim follows quickly from a published result, a standard model or a classic study. Derive it from the strongest nearby result; if that is short, the claim is a corollary.
- **Published or patented.** Owners: Selin, Hannah. Check the field's databases from the project's plan, preprint servers and patent databases. A preprint posted by the researcher counts as prior art for a patent.

## Substance, by mode

| Mode | Attack | Owner | Check |
|---|---|---|---|
| formal | counterexample, trivial reduction, hidden assumption | the formal specialists, the domain expert, Viktor | exhaustive small cases; the boundary of every hypothesis; every assumption the proof uses, listed against the statement |
| computational | numerical artifact, leakage, weak baseline | Arjun, the simulation specialist, Grace | other seeds, refinement, held-out data, a tuned strongest baseline with error bars |
| experimental | missing control, unblinded measurement, instrument error | the experimental design specialist, Arjun | the control condition, who knew the assignment, the calibration and the error budget |
| observational | confounding, selection bias, reverse causation | the causal-inference specialist, Grace | the causal diagram, a negative control, a sensitivity analysis |
| qualitative | unrepresentative sampling, unchecked coding, researcher bias | the qualitative-methods specialist | the sampling frame, a second coder or member check, a reflexivity note |
| design | no realistic task, no fair comparison, no user | the design specialist, Emre | evaluation on real tasks against the best existing tool, with real users |
| synthesis | incomplete search, unassessed bias, heterogeneity ignored | the evidence-synthesis specialist, Selin | the search log, risk-of-bias tables, heterogeneity statistics |
| archival | anachronism, second-hand quotation, missing provenance | the archives specialist, Lucien | the primary source itself, its date and context, the chain of custody |

## Field-specific attacks

The project's domain experts, designed or preset, bring their field's own ways for claims to die, for example:

- **Quantum claims** (quantum pack):
  - dequantization by a classical method with the same access;
  - a wrong input model, where data loading erases the speedup;
  - a scaling wall, where cost grows exponentially through a margin or a shot count.
- **Physical claims** (physics pack): no observable distinguishes the claim from its negation, or it fails in a known limit.
- **Economic claims:** no credible identification strategy.
- **Clinical claims:** surrogate outcomes, or no registration.
- **Historical arguments:** reading the present into the past.

Ask each domain expert for the two ways their field most often kills a claim like this one.

## Consequence

- **Nobody cares.** Owner: Emre. If the claim is true, no decision, theory or practice changes. Name the reader who would act differently, and how.
- **Overclaim.** Owner: Marta. The words exceed the evidence: "first", "proves", "causes", "advantage", a universal statement. Check each strong word against the evidence level.
- **Cannot be checked.** Owner: Marta. The evidence cannot be rerun or inspected. Check whether another person could reproduce it from the repository and the archive alone.
- **Should not be done this way.** Owners: the guardians. The study lacks approval or consent, uses data unlawfully, or creates misuse risk that has not been addressed. This kills the plan, not the idea: fix it before going on.

A precise map of where a claim dies is a result. Record it, with the narrowed claim that survives, if any.
