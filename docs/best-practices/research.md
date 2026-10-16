# Research-Method Best Practices: A Source-Backed Digest

*For an AI-assisted lab in quantum computing, mathematics, physics and theoretical CS. Compiled 2026-10-16.*

**How to read this.** Each section has (a) checklist items you can turn into workflow steps, (b) named methods, and (c) source tags like [S12] that point to the Source list at the end. I opened every cited page. Items marked *(synthesis)* are my adaptation of a source to theory or quantum work, not the source's own words. Caveats: the Halmos, Knuth, Whitesides and Klein–Roodman texts were read from third-party copies; the PRL policy is the 2005 revision; I have left out paywalled items whose text I could not read (Nuzzo 2015 and MacCoun & Perlmutter 2015 in *Nature*).

---

## 1. Choosing and framing a research problem

**(a) Checklist**
- [ ] Answer all eight Heilmeier questions in plain language before committing time: objective with no jargon; how it is done today and the limits; what is new and why it will work; who cares; risks; cost; duration; mid-term and final "exams" [S1].
- [ ] Turn Heilmeier Q8 into falsifiable milestones, e.g. "conjecture verified for n ≤ 8 by week 2" *(synthesis)* [S1].
- [ ] Record the *attack*, not just the payoff. Hamming: "It's not the consequence that makes a problem important, it is that you have a reasonable attack" [S2].
- [ ] Keep a list of 10–20 important problems and reserve a weekly "Great Thoughts" slot to check daily work against it [S2].
- [ ] Do not use difficulty as a stand-in for importance. Ask what the result enables and connects. Nielsen: most people "consistently over rate the importance of difficulty" [S3].
- [ ] Run a portfolio: keep any "big problem" on low heat and spend most time on feasible results. Leaving smaller results unwritten is a "strong warning sign" [S4].
- [ ] Novelty test: is the result new and "not simply a marginal extension of previously published work"? Would it interest people across subfield boundaries? [S7]
- [ ] Fix go/kill/hold/recycle criteria before each gate. Gates are forward-looking decisions "where resource commitments are made", not status updates [S6].
- [ ] Be ready to scale back, refocus or shelve, and archive the failed attempt privately: "stubbornly working away at a dead end is not the most efficient use of your time" [S5].
- [ ] For claims on famous problems, be "extraordinarily sceptical" and keep bragging out of the title and abstract [S4].

**(b) Methods**
- **Heilmeier Catechism**: eight questions DARPA uses to vet programmes [S1].
- **Hamming's important-problems list and Great Thoughts Time**: keep the big picture in view every week [S2].
- **Problem-solver vs problem-creator (Nielsen)**: deliberately set time aside to survey the field for larger patterns [S3].
- **Stage-Gate (Cooper)**: stages separated by gates whose outcomes are Go, Kill, Hold or Recycle [S6].

---

## 2. Ideation techniques for math, physics and theory

**(a) Checklist**
- [ ] Run Pólya's prompts: Do you know a related problem? Look at the unknown. Restate the problem and go back to definitions. Try a more general, a more special or an analogous problem. Keep only part of the condition. Did you use all the data? [S8]
- [ ] Ask Tao's "dumb questions": Is the hypothesis necessary? Is the converse true? What if you delete a hypothesis or strengthen the conclusion? What happens in the classical and degenerate cases? Does another method work? [S9]
- [ ] Look for a counterexample before investing in a proof. Even a failed search "can identify the enemy" [S10].
- [ ] Turn the problem around and treat apparent defects as possible assets (Hamming) [S2].
- [ ] When a counterexample appears, classify it first. Global but not local means a hidden lemma. Local but not global means repair the lemma. Both means incorporate the lemma as a hypothesis [S11].
- [ ] Choose a Lakatos repair explicitly and log it. Monster-barring redefines the concept to exclude the counterexample; lemma-incorporation restricts the theorem. Note the cost: restrictions can make a conjecture "nearly empty" [S11].
- [ ] Probe what an invariant cannot see: build pairs of objects it fails to distinguish, and check which hypotheses a proof actually uses. A proof that never uses n > 2 proves too much *(synthesis)* [S12].
- [ ] Fermi-check every scaling claim (qubits, gate counts, runtime). Decompose, estimate the parts, combine, and give upper and lower bounds [S13].
- [ ] Write a recoverable sketch of every interesting argument and failed attempt. These become your stock of analogies [S14].

**(b) Methods**
- **Pólya's four phases**: understand, plan, carry out, look back [S8].
- **Lakatos, *Proofs and Refutations***: monster-barring, exception-barring, lemma-incorporation and proof-generated definitions [S11].
- **Tao's global-error tests**: counterexample to the conclusion, unused hypothesis, parallel argument [S12].
- **Fermi estimation**: order-of-magnitude decomposition with bounds [S13].

---

## 3. Literature and prior-art search

**(a) Checklist**
- [ ] Pick the review type up front: systematic (PRISMA 2020 checklist and flow diagram [S15]); scoping, to map a field (PRISMA-ScR, 20 essential and 2 optional items [S16]); or rapid.
- [ ] Rapid-review shortcuts from Cochrane [S18]:
  - limit the main sources;
  - have at least one search strategy peer-reviewed;
  - pilot screening on 30–50 abstracts;
  - dual-screen at least 20% of abstracts;
  - have a second reviewer re-check every exclusion.
- [ ] Keep a search log that satisfies PRISMA-S (16 items) so the search can be reproduced: every database and platform, full query strings, dates, limits, citation searching and deduplication [S17].
- [ ] Snowball from a seed set: backward through reference lists, forward through citing papers. Include or exclude on the full text and repeat until no new papers appear [S19][S20].
- [ ] Use field syntax rather than keywords alone:
  - **arXiv API**: `ti:`, `au:`, `abs:`, `cat:`, `ANDNOT`, `submittedDate`; at most 30,000 results per query; leave about 3 s between calls [S21].
  - **INSPIRE**: `a`, `t`, `de`, `topcite`, citation searches [S22].
  - **Google Scholar**: `author:`, exact phrases, "Cited by"; at most 1,000 results per query [S23].
  - **MathSciNet**: MR Author IDs, MSC2020, a citation database built from about 650 journals [S24].
  - **zbMATH Open**: 50M citations, links to OEIS and DLMF, swMATH software, about 800k linked arXiv full texts [S25].
- [ ] Handle terminology drift *(synthesis)*:
  - keep a synonym table for each object, listing its name in every field;
  - search by fingerprint as well as by name: integer sequences in the OEIS (enter about 6 terms, starting from the second; then try Superseeker) [S26], and MSC codes and swMATH [S25].
- [ ] Remember the cautionary tale: "Tai's model" (*Diabetes Care*, 1994) re-derived the trapezoidal rule and has been cited more than 500 times [S27].
- [ ] Set "Cited by" alerts on the 3–5 closest papers to catch scoops [S23].
- [ ] For each claimed contribution, record the closest prior result and the exact difference from it *(synthesis)*.

**(b) Methods**
- **PRISMA 2020, PRISMA-ScR and PRISMA-S**: reporting standards for reviews and for the searches behind them [S15–S17].
- **Cochrane rapid review**: a documented abbreviated review [S18].
- **Wohlin snowballing**: iterative backward and forward citation search [S19].
- **Fingerprint search**: OEIS and MSC lookups that bypass naming differences [S25][S26].

---

## 4. Claim verification and fact-checking

**(a) Checklist**
- [ ] Read every source you rely on. Never copy a citation from another paper's reference list. From how misprints propagate through citations, Simkin & Roychowdhury estimate that "only about 20% of citers read the original" [S28].
- [ ] Quote verbatim with a locator (page, section, equation or theorem number), then confirm that the passage supports *your* sentence. In medicine, quotation errors run at 25.4% overall and 11.9% major [S29]. A recalculation with quotations as the denominator gives 14.5%, of which 64.8% are major [S30].
- [ ] Mark secondary citations ("as cited in"). Improper secondary citation occurs in about 10% of cases [S30].
- [ ] Resolve every reference by DOI or arXiv ID against the Crossref REST API (`/works/{doi}`, with `mailto` for the polite pool), and compare authors, title, year, volume and pages [S34].
- [ ] Treat any AI-generated reference as unverified. In one study GPT-3.5 fabricated 55% of citations and GPT-4 18%. Among the real ones, 43% and 24% had substantive errors, mostly in volume, issue, page and date fields [S31].
- [ ] Remember that authors are responsible for "incorrect references" produced by AI, and that significant AI use must be disclosed [S36].
- [ ] Run a retraction check at draft freeze and again at submission. Crossref took over the Retraction Watch database in 2023 (about 50k retractions combined; CSV through the Labs API, plus a GitLab mirror) [S33].
- [ ] Do not rely on the literature to flag retractions: only 5.4% of citation contexts written after a retraction acknowledge it [S32].
- [ ] Tag each citation by function using CiTO, which has 41 sub-properties such as `citesAsEvidence`, `usesMethodIn`, `citesForInformation`, `citesAsRelated`, `critiques` and `extends` [S35].
- [ ] Verify by tier *(synthesis)*:
  - **Load-bearing citations** (evidence, method, data): check that the cited theorem's hypotheses match your use, look for errata, and confirm the result is actually written down correctly [S39].
  - **Comparison-only citations**: a metadata check is enough.

**(b) Methods**
- **CiTO**: an ontology of citation functions [S35].
- **Crossref metadata matching**: DOI-level verification [S34].
- **Retraction Watch database via Crossref**: open retraction data [S33].
- **Claim–citation audit table** *(synthesis)*: one row per claim, with the locator, the verbatim quote, the CiTO function, and the verification status.

---

## 5. Mathematical proof development

**(a) Checklist**
- [ ] Before proving, compute small cases, test classical and degenerate special cases, and search for counterexamples [S9][S10].
- [ ] Recheck any step that suddenly simplifies things: "there is almost certainly a major error" there. Also check whether the method would prove "much stronger statements which are known to be false" [S10].
- [ ] Run Tao's global tests: Does a counterexample to the conclusion exist? Is every hypothesis used? Does a structurally parallel argument prove something false? [S12]
- [ ] Re-run a proof by contradiction without the contradiction assumption. If it still reaches a contradiction, the argument is broken. Rewriting it as a direct proof helps [S10].
- [ ] Write structured, hierarchical proofs whose numbered steps each name the facts they use. Imagine a "curious child" asking "Why?" at every step, and be "ruthlessly suspicious of everything you believe" [S41].
- [ ] Cross-check proven identities and bounds numerically with independently written code. Brent catalogues published errors that computer algebra might have caught [S42].
- [ ] Formalize in Lean/Mathlib when the result is high-profile or subtle, when a key calculation is prone to sign errors (formalize just that step and treat the rest as black boxes), or when the new library material will be reused [S37].
- [ ] Use a blueprint: a dependency graph colour-coded by status that lets several people work in parallel. The PFR project made its whole graph green in about three weeks and found missing hypotheses (2-torsion, non-emptiness) [S37].
- [ ] Budget for the overhead. In the Liquid Tensor Experiment the blueprint was about 2.5 times the length of the lecture notes and surfaced "slight imprecisions". Scholze credits human discussion for much of the confidence gained [S38].
- [ ] Expect holes in results "known to the experts". The FLT formalization found Roby's 1965 Lemma 8 apparently false. The rule there: "have to actually fix it", not just assert that it can be fixed [S39][S40].
- [ ] Treat AI gap-hunting as a source of leads, not verdicts. One automated system reports errors in 9.6% of math.NA papers; the figure is self-reported [S43].

**(b) Methods**
- **Lamport structured proofs**: hierarchical steps with named dependencies [S41].
- **Tao's local/global error taxonomy** [S12].
- **Lean + Mathlib + blueprint**: formal verification of a human-readable plan [S37][S40].
- **Pólya's "looking back"**: check the result, re-derive it differently, reuse the method [S8].

---

## 6. Computational and numerical experiments

**(a) Checklist**
- [ ] Before confirmatory runs, write an analysis plan: hypotheses, metrics, instance families, stopping rule. Label analyses exploratory or confirmatory, because "the same data cannot be used to generate *and* test a hypothesis" [S44].
- [ ] Explore on one set of instances and confirm on a held-out set [S44].
- [ ] Remember the garden of forking paths: multiple-comparison problems arise even when you run only one analysis, if that analysis depended on the data. When preregistration is impractical, follow exploration with a replication planned before publication [S45].
- [ ] Fix and record seeds, and run many of them. In one case, splitting ten seeds into two groups of five produced statistically different results (t = −9.09, p = 0.0016) [S46][S50].
- [ ] Tune baselines with the same budget as your own method, reproduce the baselines' published numbers, and publish code [S46].
- [ ] In quantum ML, include strong classical baselines and ablate the "quantum" part. Out-of-the-box classical models generally beat 12 popular quantum classifiers, and removing entanglement often did no harm [S51].
- [ ] For performance claims [S52]:
  - report runtimes and the time spent tuning;
  - never extrapolate to "imaginary platforms";
  - explain how instances and comparison solvers were chosen.
- [ ] For error bars, state the variability captured, SD vs SEM, and the method used (e.g. bootstrap). Avoid symmetric bars that cross valid bounds [S48].
- [ ] With few runs, report interval estimates, performance profiles and the interquartile mean (IQM) [S47].
- [ ] Never decide on a p-value threshold alone, and report every analysis you ran [S49].
- [ ] Blind where you can: hide the answer, fix the cuts, unblind as a deliberate review step, and disclose any change made after unblinding [S54].
- [ ] Guard against "stopping bias", where debugging stops once the result matches expectations. Klein & Roodman call it "probably the most common kind of bias" in particle physics [S54]. For a dissenting view of blinding, see [S55].
- [ ] Apply Sandve's rules:
  - keep provenance for every result;
  - make no manual edits;
  - archive the exact versions of tools;
  - keep the raw data behind every plot;
  - "connect textual statements to underlying results" [S50].
- [ ] Before submission, answer the 16-item NeurIPS checklist even for physics papers. Omitting it causes a desk reject; answering "no" with a justification does not [S48]. For quantum software, see the lab-package guidelines [S53].

**(b) Methods**
- **COS preregistration and split samples** [S44].
- **Blind analysis**: hidden signal box, hidden answer, adding or removing events, prescaling [S54].
- **rliable / IQM**: robust aggregates for few-run regimes [S47].
- **"How NOT to fool the masses"**: rules for quantum performance claims [S52].

---

## 7. Reproducibility and open science

**(a) Checklist**
- [ ] Archive code and data in a repository with "irrevocable versioning and long-term storage" (e.g. Zenodo, not GitHub alone), with a licence and a README that references the paper [S56].
- [ ] Aim at the ACM badge criteria as applied in systems artifact evaluation [S56]:
  - **Available**: archived as above.
  - **Functional**: a README for each component, the exact environment, dependencies, example inputs.
  - **Reproduced**: one script per experiment, plus a script that rebuilds the paper's tables.
- [ ] Use ACM v1.1 terms, harmonized with NISO [S57]:
  - **repeatable**: same team, same setup;
  - **reproducible**: different team, same setup;
  - **replicable**: different team, different setup.
- [ ] Write the data availability statement using APS categories. "No data or software created" fits only purely mathematical work. Mathematica and Jupyter notebooks need a statement. Cite data and software in the references with a DOI. Avoid hosting only in supplements or on personal sites [S58][S59].
- [ ] Apply FAIR: persistent identifiers (F1), rich metadata (F2), indexing (F4), standard protocols (A1), metadata that outlives the data (A2), qualified references (I3), clear licence and provenance (R1) [S60].
- [ ] Use FAIR4RS for software, which accounts for software being executable and versioned [S61].
- [ ] Add a `CITATION.cff` file (`cff-version: 1.2.0`) with `preferred-citation` pointing to the paper. GitHub shows a "Cite this repository" button, and Zenodo and Zotero read the file [S62][S63].
- [ ] On arXiv:
  - put code and data in `/anc` (ancillary files are tied to a version);
  - choose the licence deliberately, since each version's licence "is irrevocable";
  - explain every replacement in the Comments field, remembering that all versions stay public [S64–S66].

**(b) Methods**
- **ACM Artifact Review and Badging v1.1** [S56][S57].
- **FAIR / FAIR4RS** [S60][S61].
- **APS data availability templates** [S58].
- **Citation File Format** [S62].

---

## 8. Writing papers in math, physics and theoretical CS

**(a) Checklist**
- [ ] Outline first, organized around the data, theorems and figures. "A good outline for the paper is also a good plan for the research program." Revise it throughout the project [S67].
- [ ] Start writing early, as a research tool, and make sure the paper has one clear "ping": one sharp idea [S68].
- [ ] Write a four-sentence abstract: the problem, why it matters, what your solution achieves, what follows from it [S68].
- [ ] Structure the introduction around Widom's questions: What is the problem? Why does it matter? Why is it hard? Why is it unsolved? What are the key parts of the approach, including its limitations? [S69]
- [ ] End the introduction with a bulleted "Summary of Contributions" that gives section pointers [S69].
- [ ] Make contributions refutable ("We prove that…", not "We study…"), and forward-reference the evidence for each claim. Write the contribution list first [S68].
- [ ] Add a "what we do not claim / limitations" paragraph *(synthesis)*. It is required by the NeurIPS Limitations item [S48] and fits Knuth's rule of no superlatives about your own work [S70].
- [ ] Notation discipline [S70]:
  - separate symbols in different formulas with words;
  - never start a sentence with a symbol;
  - write ⇒, ∀ and ∃ as words;
  - define every variable;
  - use one notation per object and one object per notation;
  - avoid subscripted subscripts;
  - number important displays.

  See also Halmos's sections "Think about the alphabet", "Resist symbols" and "Use symbols correctly" [S71].
- [ ] Make theorem statements self-contained, and check that sentences still read smoothly when formulas are replaced by "blah" [S70].
- [ ] Give intuition before details and examples before the general case. Do not narrate your journey of discovery [S68].
- [ ] Be generous to related work. "Credit is not like money", and implying an old idea is yours can sink the paper [S68].
- [ ] Factor arguments into lemmas, and write a rapid prototype draft first [S72].
- [ ] Follow Halmos: say something, speak to someone, organize first, write in spirals, be honest, know when to stop [S71].

**(b) Methods**
- **Whitesides' outline method** [S67].
- **Peyton Jones' seven suggestions** [S68].
- **Widom's five-question introduction** [S69].
- **Knuth's minicourse rules** [S70].
- **Halmos, *How to Write Mathematics*** [S71].

---

## 9. Peer review

**(a) Checklist**
- [ ] Structure reports as Smith suggests [S73]:
  1. recommendation and reasons;
  2. a summary of one to five sentences;
  3. whether the goal is valid and significant;
  4. quality of method, correctness and presentation;
  5. required changes, then suggested ones.
- [ ] Cover Nature's aspects: key results; validity; originality and significance (with references if not original); data and methods; statistics and error bars; conclusions; suggested improvements; references; clarity. Also name the parts outside your expertise [S74].
- [ ] Follow Nature's AI policy as a referee: do not upload manuscripts into generative-AI tools, and declare any AI support. This applies when your lab reviews *other people's* work [S74].
- [ ] For physics letters, apply the PRL tests [S7][S75]:
  - validity, importance, broad interest, accessibility;
  - new theory must make predictions "distinguishable from existing knowledge";
  - "mathematical and computational papers that do not have application to physics are generally not suitable".
- [ ] Pre-empt the usual desk-reject reasons [S75]:
  - too specialized or incremental;
  - poor fit with the journal;
  - sloppy writing;
  - an introduction with no context or motivation;
  - references that are old or mostly self-citations;
  - no punch-line.
- [ ] Ask Smith's closing question: "What did you learn?" Judge against the venue's own standard. Fewer than 1% of papers are "major" and fewer than 10% "good, solid" [S73].
- [ ] Red-team internally [S77]:
  - use a designated devil's advocate;
  - offer bounties for critical errors, with a neutral arbiter;
  - do not make red-team members co-authors (a conflict of interest);
  - list incorporated criticism under methods and unincorporated criticism under limitations.
- [ ] Send the draft to competitors and ask whether you describe their work fairly. Use "friendly guinea pigs": each reader can only read the paper for the first time once [S68].
- [ ] Design simulated review with three or more independent reviewers, and look at how far each one diverges rather than blaming a role *(synthesis)*. Data from *Political Behavior* found that Reviewer 3, not Reviewer 2, was more often the outlier [S76].
- [ ] Treat every criticism as a request to explain more clearly. Fix the paper; do not argue [S68].

**(b) Methods**
- **Smith, "The Task of the Referee"** [S73].
- **Nature report template** [S74].
- **PRL criteria** [S7].
- **Red Team Challenge (Lakens)** [S77].

---

## 10. Project management for a solo or small team

**(a) Checklist**
- [ ] Keep a dated, chronological notebook. Record observations, conclusions and "how you know the experiment failed", and transcribe key conversations [S78].
- [ ] Give every entry a date, subject and protocol, keep a table of contents, and version-control code and models [S79].
- [ ] Lay out projects as `data/`, `results/` (chronological), `doc/`, `src/`, with a `runall` driver script. Make scripts restartable, and have them abort on errors [S78].
- [ ] Log decisions as ADRs: title, context, decision ("We will…"), status (proposed, accepted or superseded), consequences. Never delete a superseded record [S80].
- [ ] Hold a weekly review against the important-problems list and the open kill criteria [S2][S6].
- [ ] Stage-gate each idea *(synthesis)* [S6]: Spark → Framed (Heilmeier answered) → Prior art cleared → Core result (small cases and a proof sketch) → Verified (gap hunt, numerics, or formal proof) → Draft → Internal review → Submit.
- [ ] Map agile terms onto research *(synthesis, using the LabScrum glossary [S83])*:
  - **epic**: a paper or headline claim;
  - **story**: a lemma, an experiment or a literature question, each with acceptance criteria, e.g. "stated with all hypotheses; gap-hunted; numerics agree for n ≤ 8".
- [ ] Keep sprints loose [S83]:
  - short sprint goals can push people towards "easy tasks" and away from long-term work;
  - allow "No update" at stand-ups;
  - Hicks kept 15-minute stand-ups three times a week but dropped sprints.
- [ ] Tailor the process: rigid Scrum can backfire, and one study judged purely theoretical work a poor fit for it [S81][S82].
- [ ] Back up before major rewrites, and keep failed drafts privately [S5][S14].

**(b) Methods**
- **Noble's project layout and notebook** [S78].
- **Schnell's ten notebook rules** [S79].
- **Architecture Decision Records** [S80].
- **SCORE / LabScrum** [S82][S83].
- **Stage-Gate** [S6].

---

## 11. Cognitive biases and failure modes

**(a) Checklist**
- [ ] Start from Feynman: "The first principle is that you must not fool yourself—and you are the easiest person to fool." Report "everything that you think might make it invalid" [S84].
- [ ] Counter confirmation bias. Lamport: our "natural desire to confirm what you already believe" hides gaps [S41]. Hamming: believe enough to start, doubt enough to notice flaws [S2].
- [ ] Forking paths and HARKing: list the space of analysis choices before looking, and never present a hypothesis formed after seeing results as if it had been planned (HARKing) [S45][S85].
- [ ] Stopping bias: fix the checks in advance and keep hunting bugs after the numbers agree. Feynman's account of Millikan's oil-drop measurements drifting slowly to the right value is the classic case [S54][S84].
- [ ] Streetlight effect: research piles up on objects that are already well known (most protein papers study proteins known before 2000), and sprint pressure favours easy tasks. Reserve time for "dark" problems [S89][S83].
- [ ] Sunk cost: past investment pulls you to keep going. Make gate decisions on future value only, and use the gate itself as the moment to weigh "Kill" [S90][S6].
- [ ] Overclaiming ("spin") takes four forms [S88]:
  - misreporting methods;
  - misreporting results;
  - misinterpretation, including overgeneralization;
  - promotional rhetoric.

  Remedies: interpretation by dispassionate reviewers, and plans fixed in advance [S88]. No superlatives about your own work [S70].
- [ ] Before claiming novelty, run the synonym and fingerprint search from §3. Novelty that exists only because of a naming difference is the Tai failure mode [S27].
- [ ] Premortem: assume the project "has just failed" and list the reasons [S87].
- [ ] Bring in critics "before you have fallen in love with your results": "A scientific claim is as reliable as only the most severe criticism it has been able to withstand" [S77].
- [ ] Use adversarial collaboration [S86]:
  - rivals agree in advance which result would count against each view;
  - a trusted arbiter keeps the records;
  - the work ends in a joint paper.

  Kahneman notes that critiques usually attack "the weakest argument of the adversary" [S86].

**(b) Methods**
- **Blind analysis** [S54].
- **Premortem (Klein)** [S87].
- **Red team** [S77].
- **Adversarial collaboration (Kahneman)** [S86].
- **Spin taxonomy (Boutron & Ravaud)** [S88].
- **Preregistration** [S44].

---

## Source list

**§1 Choosing and framing a problem**
- S1. *Heilmeier Catechism*. DARPA. https://www.darpa.mil/about/heilmeier-catechism
- S2. *You and Your Research*. Richard Hamming. https://www.cs.virginia.edu/~robins/YouAndYourResearch.html
- S3. *Principles of Effective Research* (Tech. Note 0404). Michael A. Nielsen. https://www.bumc.bu.edu/preventive-med/files/2020/06/Principls-of-effective-reserache-nielsen-0404.pdf
- S4. *Don't prematurely obsess on a single "big problem" or "big theory"*. Terence Tao. https://terrytao.wordpress.com/career-advice/dont-prematurely-obsess-on-a-single-big-problem-or-big-theory/
- S5. *Use the wastebasket*. Terence Tao. https://terrytao.wordpress.com/career-advice/use-the-wastebasket/
- S6. *The Stage-Gate Model: An Overview*. Stage-Gate International. https://www.stage-gate.com/blog/the-stage-gate-model-an-overview/
- S7. *PRL Editorial Policies and Practices* (rev. 2005). APS. https://journals.aps.org/prl/issues/95/1/deliverables/policies/print

**§2 Ideation**
- S8. *How to Solve It* (summary of 2nd ed.). G. Pólya. https://math.ucr.edu/~res/math133/polya.pdf
- S9. *Ask yourself dumb questions – and answer them!* Terence Tao. https://terrytao.wordpress.com/career-advice/ask-yourself-dumb-questions-and-answer-them/
- S10. *Be sceptical of your own work*. Terence Tao. https://terrytao.wordpress.com/career-advice/be-sceptical-of-your-own-work/
- S11. *Imre Lakatos*. Stanford Encyclopedia of Philosophy. https://plato.stanford.edu/entries/lakatos/
- S12. *On "local" and "global" errors in mathematical papers*. Terence Tao. https://terrytao.wordpress.com/advice-on-writing-papers/on-local-and-global-errors-in-mathematical-papers-and-how-to-detect-them/
- S13. *8.2 Fermi Problems*. UC Berkeley, Sense & Sensibility & Science. https://sensibility.berkeley.edu/index.php/8.2_Fermi_Problems
- S14. *Write down what you've done*. Terence Tao. https://terrytao.wordpress.com/career-advice/write-down-what-youve-done/

**§3 Literature and prior-art search**
- S15. *PRISMA 2020*. PRISMA Group. https://www.prisma-statement.org/prisma-2020
- S16. *PRISMA-ScR*. Tricco et al. https://www.prisma-statement.org/scoping
- S17. *PRISMA-S*. Rethlefsen et al. (2021). https://experts.mcmaster.ca/scholarly-works/2067615
- S18. *Cochrane Rapid Reviews Methods Group guidance*. Garritty et al. (2021). https://pmc.ncbi.nlm.nih.gov/articles/PMC7557165
- S19. *Guidelines for snowballing in systematic literature studies*. Claes Wohlin (2014), record. https://api.openalex.org/works/doi:10.1145%2F2601248.2601268
- S20. *Snowballing* (library guide). Radboud University. https://libguides.ru.nl/literaturesearch/snowball
- S21. *arXiv API User's Manual*. arXiv. https://info.arxiv.org/help/api/user-manual.html
- S22. *INSPIRE paper search*. INSPIRE-HEP. https://help.inspirehep.net/knowledge-base/inspire-paper-search/
- S23. *Google Scholar Search Help*. Google. https://scholar.google.com/intl/en/scholar/help.html
- S24. *About MathSciNet*. AMS. https://mathscinet.ams.org/mathscinet/help/about.html
- S25. *An Overview of zbMATH Open Digital Library*. Deb et al. (2024). https://arxiv.org/html/2410.06948
- S26. *Hints for using the OEIS*. OEIS Foundation. https://oeis.org/hints.html
- S27. *Tai's model*. Wikipedia. https://en.wikipedia.org/wiki/Tai%27s_model

**§4 Claim verification**
- S28. *Read before you cite!* Simkin & Roychowdhury. https://arxiv.org/abs/cond-mat/0212043
- S29. *Quotation accuracy in medical journal articles*. Jergas & Baethge (2015). https://pmc.ncbi.nlm.nih.gov/articles/PMC4627914/
- S30. *Accuracy of cited "facts" in medical research articles*. Scott A. Mogull (2017). https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0184727
- S31. *Fabrication and errors in the bibliographic citations generated by ChatGPT*. Walters & Wilder (2023). https://pmc.ncbi.nlm.nih.gov/articles/PMC10484980/
- S32. *Continued use of retracted papers*. Hsiao & Schneider (2022). https://pmc.ncbi.nlm.nih.gov/articles/PMC9520488/
- S33. *News: Crossref and Retraction Watch*. Crossref (2023). https://crossref.org/blog/news-crossref-and-retraction-watch
- S34. *REST API documentation*. Crossref. https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- S35. *CiTO, the Citation Typing Ontology*. Peroni & Shotton. https://sparontologies.github.io/cito/current/cito.html
- S36. *Content Moderation* (generative-AI policy). arXiv. https://info.arxiv.org/help/moderation/index.html

**§5 Proof development**
- S37. *Formalizing the proof of PFR in Lean4 using Blueprint*. Terence Tao (2023). https://terrytao.wordpress.com/2023/11/18/formalizing-the-proof-of-pfr-in-lean4-using-blueprint-a-short-tour/
- S38. *Half a year of the Liquid Tensor Experiment*. Peter Scholze (Xena blog, 2021). https://xenaproject.wordpress.com/2021/06/05/half-a-year-of-the-liquid-tensor-experiment-amazing-developments/
- S39. *Fermat's Last Theorem — how it's going*. Kevin Buzzard (2024). https://xenaproject.wordpress.com/2024/12/11/fermats-last-theorem-how-its-going/
- S40. *FLT formalisation project*. Kevin Buzzard / Imperial College. https://imperialcollegelondon.github.io/FLT/
- S41. *How to Write a 21st Century Proof*. Leslie Lamport. https://microsoft.com/en-us/research/wp-content/uploads/2016/12/How-to-Write-a-21st-Century-Proof.pdf
- S42. *Some instructive mathematical errors*. Richard P. Brent (2021). https://arxiv.org/abs/2106.07269
- S43. *From Euler to Today: Universal Mathematical Fallibility*. Igor Rivin (2025). https://arxiv.org/abs/2511.10543v1

**§6 Computational experiments**
- S44. *Preregistration*. Center for Open Science. https://www.cos.io/initiatives/prereg
- S45. *The garden of forking paths*. Gelman & Loken (2013). https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf
- S46. *Deep Reinforcement Learning that Matters*. Henderson et al. https://arxiv.org/abs/1709.06560
- S47. *Deep RL at the Edge of the Statistical Precipice*. Agarwal et al. https://arxiv.org/abs/2108.13264
- S48. *NeurIPS Paper Checklist Guidelines*. NeurIPS. https://neurips.cc/public/guides/PaperChecklist
- S49. *ASA statement on p-values* (press release). American Statistical Association (2016). https://www.amstat.org/asa/files/pdfs/p-valuestatement.pdf
- S50. *Ten Simple Rules for Reproducible Computational Research*. Sandve et al. (2013). https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003285
- S51. *Better than classical? Benchmarking QML models*. Bowles, Ahmed & Schuld (2024). https://arxiv.org/abs/2403.07059
- S52. *How NOT to Fool the Masses… Quantum Computers*. Catherine McGeoch (2024). https://arxiv.org/html/2411.08860v1
- S53. *Quantum software experiments: reporting and lab-package guidelines*. Moguel et al. (2024). https://arxiv.org/abs/2405.04192
- S54. *Blind Analysis in Nuclear and Particle Physics*. Klein & Roodman (2005; DOI 10.1146/annurev.nucl.55.090704.151521), copy. https://www.gwern.net/doc/statistics/bias/2005-klein.pdf
- S55. *Blind analysis in physics experiments: Is this trip necessary?* Robert Golub (2023). https://arxiv.org/abs/2311.13542

**§7 Reproducibility and open science**
- S56. *SOSP'25 artifact badges*. sysartifacts. https://sysartifacts.github.io/sosp2025/badges
- S57. *Repeatability, Reproducibility, Replicability, Reusability (4R)…* Hernández González & Colom (2023). https://arxiv.org/html/2312.11028
- S58. *Data Availability Statements*. APS. https://journals.aps.org/authors/data-availability-statements
- S59. *Refreshed Data Availability Policy*. APS News (2024). https://aps.org/about/news/2024/08/refreshed-data-availability-journals
- S60. *FAIR Principles*. GO FAIR Foundation. https://www.gofair.foundation/fair-principles
- S61. *FAIR Principles for Research Software released*. Research Software Alliance (2022). https://www.researchsoft.org/blog/2022-06/
- S62. *Citation File Format*. CFF project. https://citation-file-format.github.io/
- S63. *About CITATION files*. GitHub Docs. https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files
- S64. *Ancillary files*. arXiv. https://info.arxiv.org/help/ancillary_files.html
- S65. *Licenses*. arXiv. https://info.arxiv.org/help/license/index.html
- S66. *Replacing an article*. arXiv. https://info.arxiv.org/help/replace.html

**§8 Writing**
- S67. *Whitesides' Group: Writing a Paper*. George M. Whitesides (2004), copy. https://www.chemistry.nat.fau.eu/files/2019/07/whitesides.pdf
- S68. *How to write a great research paper* (slides). Simon Peyton Jones. https://www.cs.ru.nl/~jhh/archive/2022/secsem/reader/writing-paper.pdf
- S69. *Tips for Writing Technical Papers*. Jennifer Widom. https://cs.stanford.edu/people/widom/paper-writing.html
- S70. *Mathematical Writing*. Knuth, Larrabee & Roberts (1989), copy. https://www.phys.uconn.edu/~rozman/Courses/P2400_14S/downloads/knuth_mathematical_writing.pdf
- S71. *How to Write Mathematics* (section headings only; scanned). Paul R. Halmos (1970). https://faculty.washington.edu/heagerty/Courses/b572/public/HalmosHowToWrite.pdf
- S72. *On writing*. Terence Tao. https://terrytao.wordpress.com/advice-on-writing-papers/

**§9 Peer review**
- S73. *The Task of the Referee*. Alan Jay Smith. https://www.cs.princeton.edu/~jrex/teaching/spring2005/fft/reviewing.html
- S74. *How to Write a Report*. Nature. https://www.nature.com/nature/for-referees/how-to-write-a-report
- S75. *Scientific Publication Process and Writing Referee Reports* (with Antonoyiannakis slides). UIUC PHYS 596. https://courses.grainger.illinois.edu/PHYS596/fa2025/Lectures/HowToWriteRefereeReportFA25.pdf
- S76. *Dear Reviewer 2: Go F' Yourself*. David A. M. Peterson (2020). https://ideas.repec.org/a/bla/socsci/v101y2020i4p1648-1652.html
- S77. *Pandemic researchers — recruit your own best critics*. Daniël Lakens (2020). https://media.nature.com/original/magazine-assets/d41586-020-01392-8/d41586-020-01392-8.pdf

**§10 Project management**
- S78. *A Quick Guide to Organizing Computational Biology Projects*. William S. Noble (2009). https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1000424
- S79. *Ten Simple Rules for a Computational Biologist's Laboratory Notebook*. Santiago Schnell (2015). https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1004385
- S80. *Documenting Architecture Decisions*. Michael Nygard (2011). https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
- S81. *Adapting the scrum framework… in science*. Enric Senabre Hidalgo (2019). https://pmc.ncbi.nlm.nih.gov/articles/PMC6441834/
- S82. *Adapting Scrum to Managing a Research Group*. Hicks & Foster (2010). https://www.cs.umd.edu/~mwh/papers/hicks10score.html
- S83. *A tech tool to help in the lab*. David Adam, *Nature* 573 (2019). https://media.nature.com/original/magazine-assets/d41586-019-02620-6/d41586-019-02620-6.pdf

**§11 Biases and failure modes**
- S84. *Cargo Cult Science*. Richard P. Feynman (1974). https://calteches.library.caltech.edu/51/2/CargoCult.htm
- S85. *HARKing: Hypothesizing After the Results are Known*. Norbert L. Kerr (1998). https://kar.kent.ac.uk/41330
- S86. *Adversarial Collaboration*. Daniel Kahneman (Edge). https://www.edge.org/adversarial-collaboration-daniel-kahneman
- S87. *Performing a Project Premortem*. Gary Klein (HBR, 2007; summary page only). https://hbr.org/2007/09/performing-a-project-premortem
- S88. *Misrepresentation and distortion of research in biomedical literature*. Boutron & Ravaud (2018). https://pmc.ncbi.nlm.nih.gov/articles/5856510
- S89. *The human genome and drug discovery after a decade. Roads (still) not taken*. Isserlin et al. (2011). https://arxiv.org/abs/1102.0448
- S90. *The psychology of sunk cost*. Arkes & Blumer (1985), record. https://api.openalex.org/works/doi:10.1016/0749-5978(85)90049-4
