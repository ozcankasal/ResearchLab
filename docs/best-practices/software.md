# Research Software Best Practices: Source-Backed Digest

Scope: Python scientific and quantum-simulation code, plus Lean. Compiled 2026-10-16. Bracketed tags such as [S12] point to the Source list at the end, and every tag is a page that was opened. Items marked *(derived)* are my synthesis from the cited material, not a direct claim of a source.

---

## 1. Scientific computing practice

**(a) Checklist**
1. Write code for human readers: consistent, meaningful names and a consistent style [S1].
2. Make small, incremental changes under version control. Commit everything created by hand [S1, S2].
3. Give every datum and constant one authoritative representation. Modularise; don't copy and paste [S1].
4. Add assertions for preconditions, postconditions and invariants: "fail early, fail often" [S1, S3].
5. Turn every bug into a test case before fixing it [S1, S3].
6. Make it correct before making it fast. Profile first, and keep the simple version as a test oracle for the optimised one [S1].
7. Document interfaces and reasons, not mechanics. Refactor instead of explaining convoluted code [S1].
8. Ship a small example dataset with a known correct output [S2].
9. State dependencies explicitly. Add a README, a LICENSE and a CITATION file. Deposit in a DOI-issuing repository [S2].
10. Use pre-merge code review, plus pair programming for tricky parts [S1].
11. Automate tests and run them regularly in CI. Measure coverage. Have someone review the test code [S5].

**(b) Named practices / tools**
- **Defensive programming** – assertions as executable documentation; initialise from data, not arbitrary constants [S3].
- **Test-first** – Software Carpentry teaches writing tests before the function to reduce confirmation bias [S3].
- **Turing Way test taxonomy** – smoke, unit, integration, system, acceptance/regression and runtime tests [S4, S5].

**Note.** "Good enough practices" deliberately *excludes* unit tests, CI, coverage and code review, saying they "usually aren't compelling for solo exploratory work" [S2]. A lab that publishes numerical claims is past that threshold. Treat the 2017 list as the floor and the 2014 list as the target.

**(c) Sources:** S1–S5.

---

## 2. Testing numerical and scientific code

**(a) Checklist**
1. Never use `==` on floats. Choose `rtol` *and* `atol` deliberately and record why in a comment [S6, S7, S8].
2. Know each library's semantics:
   - `numpy.testing.assert_allclose` checks `|actual−desired| ≤ atol + rtol·|desired|`, with defaults `rtol=1e-7` and `atol=0`. It is asymmetric, so put the reference in `desired` [S6].
   - `math.isclose` is symmetric, with `rel_tol=1e-9` and `abs_tol=0` [S7].
   - The Scientific Python guide prefers `pytest.approx` [S21].
3. When comparing to zero, set an explicit `atol`. "No value is small relative to zero" [S7, S8]. If you need a loose tolerance, fix the algorithm's stability rather than widening epsilon [S8].
4. Use `strict=True` in `assert_allclose` so that shape and dtype mismatches fail. Otherwise a scalar broadcasts and an empty array "equals" a scalar [S6].
5. Use property-based tests for invariants: round-trips, conservation laws, and agreement between the optimised code and a slow, clearly correct version [S11].
   - Bound float strategies and decide on NaN/inf explicitly [S10].
   - Pin regressions with `@example`. The Hypothesis database is only a cache [S9].
6. Write metamorphic relations where no oracle exists, e.g. sin(x)=sin(π−x), symmetry, scaling or permutation invariance [S12, S13].
7. Use analytic or closed-form oracles first. For discretised solvers, run order-of-accuracy tests:
   - Use the method of manufactured solutions [S17].
   - Compute the observed order as p = log(ε₁/ε₂)/log r on refined grids and assert it matches the formal order [S18].
   - Check that you are in the asymptotic range [S18].
8. Stochastic code needs two layers:
   - A seeded deterministic test, which is fast, but brittle when the number of draws changes [S16].
   - A distributional test over many runs with a tolerance [S16].
9. Fixed seeds are a workaround, not a fix. Dutta et al. found **461 tests in 114 ML projects that fail without their seeds** [S14]. Calibrate assertion bounds (FLEX uses extreme-value theory) or pick the number of reruns for a target confidence [S15].
10. Budget the false-failure rate *(derived)*:
    - With per-test significance α and k statistical assertions, P(spurious red CI) ≈ 1−(1−α)^k.
    - Use a small α (e.g. 1e-4) with enough samples. Run unseeded statistical suites nightly, not on every push.
11. Seed with `SeedSequence` and `default_rng`, and spawn child streams for parallel workers. Never use `seed + worker_id` [S19].
12. Store golden numbers with tolerances (`num_regression` or `ndarrays_regression`). Regenerate only with `--force-regen` plus a reviewed commit [S20, S22].

**(b) Named practices / tools**
- **pytest + `pytest.approx`**:
  - Strict config: `--strict-markers`, `--strict-config`, `xfail_strict`.
  - `filterwarnings=error` [S21].
- **Hypothesis** – generation plus shrinking. `derandomize` is on by default in CI. `@reproduce_failure` replays a failing case [S9, S11].
- **Metamorphic testing** – checks relations between the outputs of transformed inputs, which addresses the oracle problem [S12].
- **MMS / order-of-accuracy verification** – analytic and manufactured solutions "remain the most powerful methods for code verification" [S17].
- **pytest-regressions** – golden-file fixtures. The first run creates the file, which you then commit [S20, S22].
- **FLEX** – derives tolerance bounds for flaky stochastic tests from extreme-value theory [S15].

**(c) Sources:** S6–S22.

---

## 3. Testing and verifying quantum programs

**(a) Checklist**
1. **Fix the bit-order convention in every test name and docstring.**
   - Qiskit is little-endian: qubit 0 is the rightmost bit of a count key [S29].
   - Qiskit primitives' `BitArray` defaults to big-endian [S29].
   - "MSB-LSB convention mismatch" and "incorrect qubit order" are named quantum-specific bug patterns [S26].
2. Unitary equivalence on small n:
   - `Operator.equiv` (up to global phase; default rtol 1e-5, atol 1e-8) [S28].
   - `cirq.testing.assert_allclose_up_to_global_phase` [S32].
   - Account for layouts and final permutations after transpilation (`Operator.from_circuit(..., final_layout=...)`, `assert_circuits_have_same_unitary_given_final_permutation`) [S28, S32].
3. Protocol consistency for custom gates: `assert_implements_consistent_protocols`, `assert_decompose_is_consistent_with_unitary`, `assert_qasm_is_consistent_with_unitary` [S32].
4. Statistical assertions on samplers [S23]:
   - Huang & Martonosi use a chi-square goodness-of-fit test for "classical" (one outcome) and "superposition" (uniform) states, and contingency-table chi-square tests for entanglement.
   - They reject at p ≤ 0.05 with ensembles as small as 16 shots.
   - A large p-value does not prove correctness.
   - For CI, raise the shot count and lower α (see §2.10).
5. Projection-based assertions check membership in a subspace with few measurements. Consider them for hardware runs [S24].
6. Mirror-circuit tests *(adapted from [S27])*:
   - Run C, then C†, with random Pauli frames. On a correct stack this yields one deterministic, classically computable bit string.
   - Proctor et al. scaled this to benchmarking 225 simulated qubits.
   - As a regression test, it checks the inverse, decomposition and transpilation at sizes beyond full-unitary comparison.
7. Differential testing across stacks or simulators:
   - Generate semantics-preserving variants and compare their output distributions with a K-S test or cross-entropy [S35].
   - Formal equivalence checking of compiled versus source circuits: MQT QCEC (decision diagrams, ZX-calculus, simulation) [S33, S34].
8. Seed the transpiler (`seed_transpiler`) and the simulator separately, and log both. Transpilation has stochastic passes [S30].
9. Test for "wrong output" bugs, not just crashes:
   - Quantum-specific bugs (39.9% of 223 platform bugs) more often give wrong outputs.
   - Only 16 application bugs in that study were caught by failing tests [S26].
10. Seed the test suite with real bug classes:
    - Bugs4Q has 36 reproducible Qiskit bugs [S25].
    - Huang & Martonosi list six bug types, from wrong initial values to faulty uncomputation ("mirroring") [S23].
11. Resource-estimate sanity:
    - State all the layers: logical counts, the QEC code and factories, physical parameters and the error budget [S37, S38].
    - Check that declared and decomposed counts agree (Qualtran's `assert_equivalent_bloq_counts` asserts "consistent bloq counts") [S36].
    - Check monotonic scaling in problem size against a published estimate *(derived)*.

**(b) Named practices / tools**
- **Qiskit `quantum_info`** – `Operator`, `Statevector`, `.equiv` [S28].
- **`cirq.testing`** – global-phase-aware asserts, protocol-consistency checks, random circuits and unitaries [S32].
- **MQT QCEC** – equivalence checker for verifying compilation flows [S33, S34].
- **QDiff** – differential testing of Qiskit, Cirq and PyQuil [S35].
- **Qualtran** – bloqs, resource counting, and a `qualtran.testing` module [S36].
- **Microsoft Quantum resource estimator** – layered application, architecture and QEC models with a Pareto frontier of qubits against runtime [S38].
- **Qiskit's own CI policy**:
  - The suite fails on `DeprecationWarning`.
  - User-facing changes need a `reno` release note [S31].

**(c) Sources:** S23–S38.

---

## 4. Research software engineering (RSE)

**(a) Checklist**
1. Use the `src/` layout and `pyproject.toml`. Tests then run against the installed package, and you can't accidentally import the working tree [S39].
2. Commit the lock file:
   - `uv.lock` is universal (cross-platform) and "should be checked into version control" [S40].
   - Export to standard `pylock.toml` (PEP 751) for tool-neutral installs [S40, S41].
3. Run Ruff for lint and format, with a curated rule set (`B, I, ARG, C4, PL, PT, RUF, UP, NPY…`) [S43].
4. Run mypy with `strict = true` on `src`, with per-module overrides rather than global relaxations [S43].
5. Use pre-commit hooks pinned to tags and kept fresh with `autoupdate` or pre-commit.ci. Include codespell [S43].
6. CI on GitHub Actions:
   - Least-privilege `GITHUB_TOKEN` and SHA-pinned third-party actions [S45].
   - Note that SHA-pinned actions get **no Dependabot alerts**, so track advisories some other way [S45].
7. Publish with PyPI Trusted Publishing and build attestations [S44].
8. Write numpydoc docstrings (Parameters, Returns, Raises, Notes, References, Examples). Mark random output in doctests [S46].
9. Version with SemVer:
   - Declare the public API.
   - `0.y.z` means "anything MAY change" [S47].
   - Keep a curated CHANGELOG with an `Unreleased` section. "Don't dump git logs" [S48].
10. Add a `CITATION.cff`. GitHub renders it as BibTeX, and Zenodo uses it for record metadata [S50].
11. Add an OSI licence. Permissive licences (MIT/BSD/Apache-2.0) maximise reuse; copyleft (GPL/LGPL/MPL) keeps derivatives open. Check with your institution, which may own the code [S54].
12. Map the project to FAIR4RS:
    - F1.2: a distinct ID per version.
    - R1.1: a clear licence.
    - R1.2: provenance.
    - R2: qualified references to dependencies [S49].

**(b) Named practices / tools**
- **Scientific Python Development Guide** and the **cookie** template, plus **sp-repo-review** to audit a repo against the guide [S42].
- **SPEC 0** – drop Python versions 3 years after release and core packages after 2 years [S53].
- **uv** – resolver, environment manager and lock file [S40].
- **Zenodo–GitHub integration** – archives each GitHub release and mints a DOI. The repo must be public and should carry a licence [S51].
- **Software Heritage**:
  - Save Code Now, a browser extension, or a webhook archives the repo [S56].
  - **SWHIDs** are intrinsic, hash-based identifiers that can point down to a line range in a file [S56, S57].
  - SWHID is now **ISO/IEC 18670:2025** [S58].

**(c) Sources:** S39–S58.

---

## 5. Code review (adapted to scientific code)

**(a) Checklist** (Google's categories [S59] plus scientific additions *(derived from S1, S8, S17, S26)*)
1. **Design and scope.** The diff does one thing. About 100 lines is reasonable and 1000 is usually too many. Refactors go in separate changes [S61].
2. **Mathematical correctness.** Each formula traces to an equation number or reference in a comment or docstring. The reviewer re-derives at least one non-trivial step.
3. **Units and conventions:**
   - Units are stated.
   - So are sign and phase conventions, normalisation, ħ=1 choices, and bit/qubit ordering, which is a known quantum bug pattern [S26, S29].
   - Angles are stated as radians or degrees.
   - Endianness is checked at every boundary between libraries.
4. **Numerical stability.** Look for cancellation, poorly conditioned solves, accumulation order and dtype downcasts. No tolerance should be loosened to make a test pass [S8].
5. **Test adequacy:**
   - Tests would fail if the code broke [S59].
   - The oracles are independent of the implementation (analytic values, metamorphic relations, a reference implementation), not output pasted from the code [S64].
6. **Randomness.** Seeds and streams are explicit. Statistical thresholds and false-failure rates are stated.
7. **Reproducibility.** Dependency changes are reflected in the lock file. Golden-file updates are justified in the PR text.
8. **Every line read.** If only part was reviewed, say which part [S59].
9. **Approval threshold.** Approve once the change "definitely improves the overall code health". Prefix optional points with "Nit:". Technical facts outrank opinions [S60].

**(b) Named practices**
- **Google eng-practices** – what to look for, the standard of review, and small changes (CLs) [S59–S61].
- **Just-in-time small reviews** – scientists respond best to small reviews of each change rather than end-of-project reviews [S62].
- **Writer/reviewer split with a fresh context** – have a separate agent or session review the diff against the plan *(derived)*.

**(c) Sources:** S59–S62, S64.

---

## 6. Agile and spec-driven development with AI coding agents (small or solo teams)

**(a) Checklist**
1. Write stories to INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable. Tasks are SMART [S63].
2. Write acceptance criteria as Given/When/Then. "Then" steps should be side-effect-free queries [S65]. For numerical stories, "Then" names the oracle and the tolerance *(derived)*.
3. Keep a written Definition of Done. Items that don't meet it return to the backlog [S66].
4. Follow Canon TDD:
   - Keep a test list.
   - Write one failing test.
   - Make it pass.
   - Optionally refactor.
   - Repeat [S64].
5. Banned moves [S64]:
   - Deleting assertions.
   - Writing tests with no assertions.
   - **Pasting computed output into expected values.**
6. Specs come first [S68]:
   - Specify, then plan, then tasks, then implement, with a human check at each phase.
   - A good spec names the files and interfaces, states what is out of scope, and ends with an end-to-end verification step *(derived)*.
7. Size the process to the problem. Böckeler saw a spec tool turn a small bug into 4 user stories with 16 acceptance criteria [S69].
8. Give the agent a runnable check (tests, build, linter). Require evidence, i.e. the command and its output, not claims of success *(derived)*.
9. Keep diffs small and commit often:
   - DORA finds that small batches and strong version control amplify AI's benefits [S72].
   - The 2025 DORA report frames AI as "an amplifier" of existing practices [S72].
10. **Guard against tests that assert the implementation:**
    - LLM-generated oracles "mainly capture the actual program behavior" [S70].
    - Write or review oracles from the spec, have one session write tests and another write code *(derived)*, and use mutation testing to find weak tests [S73].
11. **Guard against hallucinated APIs and packages:**
    - Code LLMs hallucinate package names in at least 5.2% of samples (commercial models) and 21.7% (open models) [S71].
    - Check every new dependency against PyPI and the lock file, and check every new API against the docs.
12. Keep a human review gate. Developer perception is unreliable: METR measured a 19% slowdown while developers believed they had been sped up by 20%. That was with early-2025 tools, and METR now marks the result as dated [S74].

**(b) Named practices / tools**
- **INVEST / SMART** [S63], **Given-When-Then / BDD** [S65], **Definition of Done** [S66], **Canon TDD** [S64].
- **Spec Kit** (constitution, specify, plan, tasks); **Kiro** and **Tessl** take the spec-first or spec-as-source approach [S68, S69].
- **mutmut** – mutation testing for Python. A surviving mutant marks an untested behaviour [S73].

**(c) Sources:** S63–S66, S68–S74.

---

## 7. Benchmarking and performance claims

**(a) Checklist** (Hoefler & Belli's 12 rules [S76], condensed)
1. Report absolute times alongside any speedup. State whether the baseline is the best serial code or a 1-process parallel run. 38% of surveyed speedup papers omitted the absolute base.
2. Justify any subset of benchmarks you report. Report all results, not the best.
3. Summarise costs with the arithmetic mean and rates with the harmonic mean. Avoid averaging ratios; if unavoidable, use the geometric mean.
4. Say whether the data are deterministic. If not, report confidence intervals. Only 2 of 95 surveyed papers did.
5. Don't assume normality. Compare with statistically sound methods (non-overlapping CIs, ANOVA). Consider medians or tail percentiles.
6. Document every varying factor and the full setup (hardware, software, flags).
7. Show upper bounds such as the ideal-scaling line or peak.
8. Plot enough to interpret the result. Connect points only where interpolation is valid.
9. Warm up and isolate:
   - Pin CPUs and fix frequency; turn Turbo off. Keep ASLR enabled [S80].
   - Warm-up and minimum-rounds options exist in pytest-benchmark [S82].
10. Microbenchmarks versus claims:
    - `timeit` advises taking the **min** of repeats, because higher values usually reflect interference [S81].
    - For published claims, report the distribution (S76 rules 5–8). *(Derived reconciliation: min for micro-optimisation, distributions for claims.)*
11. Randomise the setup (environment size, link order) to detect measurement bias. None of 133 surveyed systems papers handled it adequately [S79].
12. Use fair baselines:
    - No unoptimised competitor, no 32-bit versus 64-bit comparisons, and no projecting to systems you didn't run on [S75, S77].
    - For quantum, report runtimes including tuning time, no "imaginary platforms", and no cherry-picking [S78].

**(b) Named practices / tools**
- **Bailey's "Twelve ways"** (1991):
  - Quote only kernels.
  - Scale problem size silently.
  - Compare against old or unoptimised code.
  - Run on a dedicated system against a busy one [S75].
- **Hager's 2010 update** – log-scale obfuscation, quietly using weak scaling, irrelevant metrics instead of time-to-solution, and ignoring affinity [S77].
- **McGeoch's 2024 quantum version** – four cautions for quantum benchmarking [S78].
- **pyperf** (system tuning), **pytest-benchmark** (`--benchmark-compare-fail=min:5%` as a CI gate) [S80, S82].

**(c) Sources:** S75–S82.

---

## 8. Lean / formal verification in a research codebase

**(a) Checklist**
1. Create the project with `lake new <name> math`, then `lake update` and `lake exe cache get` for prebuilt mathlib [S83].
2. Commit `lean-toolchain`, `lakefile.*` and `lake-manifest.json`. The manifest pins dependency revisions and "should normally be checked into source control" [S84].
3. Bump mathlib deliberately:
   - Copy mathlib's `lean-toolchain`, then run `lake update`, then `lake exe mk_all && lake build` [S83].
   - Blueprint projects use `lake -R -Kenv=dev update` [S83].
4. Keep a blueprint in LaTeX:
   - Each node carries `\lean{decl}`, `\uses{...}` and `\leanok`.
   - Run `leanblueprint checkdecls` in CI so the blueprint can't cite missing declarations [S85].
5. **Split stories by blueprint node** [S86]:
   - Story A states the definition or lemma with `sorry`. Its done-check is that the node shows as "stated".
   - Story B proves it. Its done-check is that the node turns green.
   - Stating before proving lets work proceed in parallel, because later nodes don't wait on earlier proofs.
6. Claim work on a node before starting it (PFR used Zulip) to avoid duplicated effort [S86].
7. Definition of Done for a proof story:
   - `#print axioms` on the target shows only `propext`, `Classical.choice` and `Quot.sound`.
   - No `sorryAx`, and no `native_decide` compiler-trust axioms unless approved [S87].
8. CI with `leanprover/lean-action`:
   - Mathlib cache and `.lake` caching.
   - `build-args: --wfail` so warnings fail the build, which catches `sorry`.
   - `mk_all-check` so every file is imported [S88].
9. Use a template repo with build, blueprint, docs, Pages and release-on-toolchain-bump workflows [S89].
10. Expect formalisation to expose gaps in the informal maths: PFR found missing hypotheses [S86]. Record each one as a paper erratum *(derived)*.

**(b) Named practices / tools**
- **Lake + elan + mathlib cache** [S83, S84].
- **leanblueprint** – plasTeX blueprints with a coloured dependency graph [S85].
- **LeanArchitect** (ITP 2026) – generates blueprint data from annotations in the Lean source, which keeps LaTeX and Lean in sync and helps AI tooling [S90].
- **lean-action** – the standard GitHub Action [S88].

**(c) Sources:** S83–S90.

---

## 9. Release engineering for research

**(a) Checklist**
1. Tag releases with annotated, ideally signed, tags. Never move a published tag. "Admit you screwed up, and use a different name" [S91].
2. Aim for reproducible builds: the same source, environment and instructions give bit-identical artifacts [S92]. At minimum, the lock file and toolchain are pinned and the artifact hashes are recorded *(derived)*.
3. Make a GitHub release, which Zenodo turns into a **version DOI**.
   - **Cite the version DOI** in papers. The concept DOI resolves to the latest version and suits documentation [S52, S55].
   - Don't encode version numbers in DOIs [S52].
4. Also archive to Software Heritage and quote a SWHID for the exact commit [S56].
5. arXiv source package [S93]:
   - The `.bbl` must have the same name as the main `.tex` and be produced by the same backend.
   - TeX Live 2025 (the default) accepts only bbl format 3.3.
   - Include `.ind` and `.gls`.
   - Exclude `.aux`, `.log` and `.pdf` outputs and unused figures.
   - Hidden files are deleted.
   - Embedded JavaScript means rejection.
6. Strip LaTeX comments, because they are public in the arXiv source download. arxiv-latex-cleaner also drops unused images [S95].
7. Put code and data snapshots in arXiv's `anc/` directory if useful. Files there are tied to one article version and aren't indexed [S94].
8. Write a code availability statement:
   - Nature requires a separate "Code availability" section and recommends deposit in a DOI-minting repository (Zenodo, Code Ocean) with an OSI licence [S99].
   - PLOS expects documented, licensed code, accessible without login [S98].
9. Artifact evaluation:
   - Aim for ACM *Available*: permanent public retrieval; "GitHub, GitLab … not adequate" on its own [S97].
   - *Functional*: documented, consistent, complete, exercisable [S96, S97].
   - *Reusable* and *Results Reproduced* (results obtained within tolerance) [S96, S97].
10. Run the release checklist *(derived)*:
    - CHANGELOG moved out of Unreleased.
    - Version bumped and `CITATION.cff` updated.
    - Clean CI at the tag.
    - Golden numbers regenerated only with a documented reason.
    - Paper figures regenerated from the tagged commit by one script.

**(b) Named practices / tools**
- **Zenodo DOI versioning** [S52]; **Software Heritage / SWHID** [S56–S58].
- **arxiv-latex-cleaner** [S95]; **reproducible-builds.org** definition [S92].
- **ACM badges** (v1.1, quoted via SIGIR and CCS pages) [S96, S97].

**(c) Sources:** S52–S58, S91–S99.

---

## Source list

*Note: the ACM badging policy page returned HTTP 403, so ACM definitions are cited through SIGIR and CCS pages that quote it. The ICST'22 seeds paper is cited from its conference abstract page because its PDF text could not be extracted.*

| # | Title | Author(s) | URL |
|---|---|---|---|
| S1 | Best Practices for Scientific Computing (PLoS Biol 2014) | Wilson, Aruliah et al. | https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745 |
| S2 | Good enough practices in scientific computing (PLoS Comput Biol 2017) | Wilson, Bryan, Cranston, Kitzes, Nederbragt, Teal | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510 |
| S3 | Programming with Python: Defensive Programming | Software Carpentry | https://swcarpentry.github.io/python-novice-inflammation/10-defensive.html |
| S4 | Code Testing (chapter intro) | The Turing Way Community | https://book.the-turing-way.org/reproducible-research/testing |
| S5 | Checklist for Code Testing | The Turing Way Community | https://book.the-turing-way.org/reproducible-research/testing/testing-checklist |
| S6 | numpy.testing.assert_allclose | NumPy developers | https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html |
| S7 | PEP 485 – A Function for testing approximate equality | C. Barker | https://peps.python.org/pep-0485/ |
| S8 | Comparing Floating Point Numbers, 2012 Edition | B. Dawson | https://randomascii.wordpress.com/2012/02/25/comparing-floating-point-numbers-2012-edition/ |
| S9 | Hypothesis API reference | Hypothesis developers | https://hypothesis.readthedocs.io/en/latest/reference/api.html |
| S10 | Hypothesis strategies reference | Hypothesis developers | https://hypothesis.readthedocs.io/en/latest/reference/strategies.html |
| S11 | Hypothesis tutorial: Introduction | Hypothesis developers | https://hypothesis.readthedocs.io/en/latest/tutorial/introduction.html |
| S12 | A Survey on Metamorphic Testing (IEEE TSE 2016) | Segura, Fraser, Sánchez, Ruiz-Cortés | https://eprints.whiterose.ac.uk/110335/1/segura16-tse.pdf |
| S13 | Testing Scientific Software: A Systematic Literature Review | Kanewala, Bieman | https://arxiv.org/abs/1804.01954 |
| S14 | To Seed or Not to Seed? (ICST 2022) | Dutta, Arunachalam, Misailovic | https://icst2022.vrain.upv.es/details/icst-2022-papers/16/To-Seed-or-Not-to-Seed-An-Empirical-Analysis-of-Usage-of-Seeds-for-Testing-in-Machin |
| S15 | FLEX: Fixing Flaky Tests in ML Projects by Updating Assertion Bounds (ESEC/FSE 2021) | Dutta, Shi, Misailovic | https://2021.esec-fse.org/details/fse-2021-papers/84/FLEX-Fixing-Flaky-Tests-in-Machine-Learning-Projects-by-Updating-Assertion-Bounds |
| S16 | Challenges and Exceptional Cases in testing | The Turing Way Community | https://book.the-turing-way.org/reproducible-research/testing/testing-exceptions |
| S17 | Nalu verification: Introduction | Nalu developers (Sandia) | https://nalu.readthedocs.io/en/latest/source/verification/introduction.html |
| S18 | Code verification using the Method of Manufactured Solutions (TKT4140) | NTNU course notes | https://fredf.folk.ntnu.no/teaching/chapter1MMS.html |
| S19 | NumPy random: Parallel Random Number Generation | NumPy developers | https://numpy.org/doc/stable/reference/random/parallel.html |
| S20 | pytest-regressions API | pytest-regressions developers | https://pytest-regressions.readthedocs.io/en/latest/api.html |
| S21 | Scientific Python Dev Guide: Testing with pytest | Scientific Python community | https://learn.scientific-python.org/development/guides/pytest/ |
| S22 | pytest-regressions overview | pytest-regressions developers | https://pytest-regressions.readthedocs.io/en/latest/overview.html |
| S23 | Statistical Assertions for Validating Patterns and Finding Bugs in Quantum Programs (ISCA 2019) | Huang, Martonosi | https://arxiv.org/abs/1905.09721 (full text: https://ar5iv.labs.arxiv.org/html/1905.09721) |
| S24 | Proq: Projection-based Runtime Assertions for Debugging on a Quantum Computer | Li, Zhou, Yu, Ding, Ying, Xie | https://arxiv.org/abs/1911.12855 |
| S25 | Bugs4Q: A Benchmark of Real Bugs for Quantum Programs | Zhao, Zhao, Miao, Lan | https://arxiv.org/abs/2108.09744 |
| S26 | Bugs in Quantum Computing Platforms: An Empirical Study (OOPSLA 2022) | Paltenghi, Pradel | https://arxiv.org/abs/2110.14560 (full text: https://ar5iv.labs.arxiv.org/html/2110.14560) |
| S27 | Scalable randomized benchmarking of quantum computers using mirror circuits (PRL 2022) | Proctor, Seritan, Rudinger, Nielsen, Blume-Kohout, Young | https://arxiv.org/abs/2112.09853 (full text: https://ar5iv.labs.arxiv.org/html/2112.09853) |
| S28 | qiskit.quantum_info.Operator | IBM Quantum / Qiskit | https://quantum.cloud.ibm.com/docs/en/api/qiskit/qiskit.quantum_info.Operator |
| S29 | Bit-ordering in Qiskit | IBM Quantum / Qiskit | https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering |
| S30 | qiskit.compiler.transpile | IBM Quantum / Qiskit | https://quantum.cloud.ibm.com/docs/en/api/qiskit/compiler |
| S31 | Qiskit CONTRIBUTING.md | Qiskit developers | https://github.com/Qiskit/qiskit/blob/main/CONTRIBUTING.md |
| S32 | cirq.testing module | Google Quantum AI | https://quantumai.google/reference/python/cirq/testing |
| S33 | MQT QCEC documentation | Munich Quantum Toolkit (TUM) | https://mqt.readthedocs.io/projects/qcec/en/latest/ |
| S34 | Advanced Equivalence Checking for Quantum Circuits | Burgholzer, Wille | https://arxiv.org/abs/2004.08420 |
| S35 | QDiff: Differential Testing for Quantum Software Stacks (README) | Wang, Zhang, Xu, Kim (UCLA SEAL) | https://github.com/UCLA-SEAL/QDiff |
| S36 | Qualtran docs; qualtran.testing | Google Quantum AI | https://qualtran.readthedocs.io/en/latest/ ; https://qualtran.readthedocs.io/en/latest/reference/qualtran/testing.html |
| S37 | Assessing requirements to scale to practical quantum advantage | Beverland et al. | https://arxiv.org/abs/2211.07629 |
| S38 | Introduction to the resource estimator | Microsoft | https://learn.microsoft.com/en-us/azure/quantum/intro-to-resource-estimation |
| S39 | src layout vs flat layout | PyPA | https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/ |
| S40 | uv: Project structure and files (uv.lock) | Astral | https://docs.astral.sh/uv/concepts/projects/layout/ |
| S41 | PEP 751 – A file format to record Python dependencies | B. Cannon | https://peps.python.org/pep-0751/ |
| S42 | Scientific Python Development Guide (home) | Scientific Python community | https://learn.scientific-python.org/development/ |
| S43 | Scientific Python Dev Guide: Style and static checks | Scientific Python community | https://learn.scientific-python.org/development/guides/style/ |
| S44 | Scientific Python Dev Guide: GitHub Actions for pure Python | Scientific Python community | https://learn.scientific-python.org/development/guides/gha-pure/ |
| S45 | Secure use reference (GitHub Actions) | GitHub | https://docs.github.com/en/actions/reference/security/secure-use |
| S46 | numpydoc style guide | numpydoc maintainers | https://numpydoc.readthedocs.io/en/latest/format.html |
| S47 | Semantic Versioning 2.0.0 | T. Preston-Werner | https://semver.org/ |
| S48 | Keep a Changelog 1.1.0 | O. Lacan | https://keepachangelog.com/en/1.1.0/ |
| S49 | Introducing the FAIR Principles for research software (Sci Data 2022) | Barker, Chue Hong et al. | https://pmc.ncbi.nlm.nih.gov/articles/PMC9562067 |
| S50 | Citation File Format | CFF maintainers | https://citation-file-format.github.io/ |
| S51 | Referencing and citing content (Zenodo DOI) | GitHub | https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content |
| S52 | What is DOI versioning? | Zenodo | https://support.zenodo.org/help/en-gb/1-upload-deposit/97-what-is-doi-versioning |
| S53 | SPEC 0 — Minimum Supported Dependencies | Scientific Python | https://scientific-python.org/specs/spec-0000/ |
| S54 | A Quick Guide to Software Licensing for the Scientist-Programmer (PLoS CB 2012) | Morin, Urban, Sliz | https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1002598 |
| S55 | Citable versioning | The Turing Way Community | https://book.the-turing-way.org/communication/citable/citable-versioning |
| S56 | How to archive and reference your code (HOWTO) | Software Heritage | https://www.softwareheritage.org/howto-archive-and-reference-your-code/ |
| S57 | Saving Research Software: Supporting Open Science | Software Heritage | https://www.softwareheritage.org/save-and-reference-research-software/ |
| S58 | SWHID (ISO/IEC 18670:2025) | SWHID working group | https://www.swhid.org/ |
| S59 | What to look for in a code review | Google | https://google.github.io/eng-practices/review/reviewer/looking-for.html |
| S60 | The Standard of Code Review | Google | https://google.github.io/eng-practices/review/reviewer/standard.html |
| S61 | Small CLs | Google | https://google.github.io/eng-practices/review/developer/small-cls.html |
| S62 | Code Review For and By Scientists | Petre, Wilson | https://arxiv.org/abs/1407.5648 |
| S63 | INVEST in Good Stories, and SMART Tasks | B. Wake | https://xp123.com/invest-in-good-stories-and-smart-tasks/ |
| S64 | Canon TDD | K. Beck | https://newsletter.kentbeck.com/p/canon-tdd |
| S65 | GivenWhenThen | M. Fowler | https://martinfowler.com/bliki/GivenWhenThen.html |
| S66 | The Scrum Guide (2020) | Schwaber, Sutherland | https://scrumguides.org/scrum-guide.html |
| S68 | Spec-driven development with AI: Spec Kit | GitHub Blog | https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/ |
| S69 | Understanding Spec-Driven-Development: Kiro, spec-kit, and Tessl | B. Böckeler | https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html |
| S70 | Can we find bugs using LLM-generated oracles? | Konstantinou, Degiovanni, Papadakis | https://arxiv.org/abs/2410.21136 |
| S71 | We Have a Package for You! Package Hallucinations by Code-Generating LLMs (USENIX Sec 2025) | Spracklen et al. | https://arxiv.org/abs/2406.10279 |
| S72 | Introducing DORA's inaugural AI Capabilities Model; DORA 2025 report page | Google Cloud DORA | https://cloud.google.com/blog/products/ai-machine-learning/introducing-doras-inaugural-ai-capabilities-model ; https://dora.dev/research/2025/dora-report/ |
| S73 | mutmut documentation | mutmut maintainers | https://mutmut.readthedocs.io/en/latest/ |
| S74 | Measuring the Impact of Early-2025 AI on Experienced OSS Developer Productivity | METR | https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ |
| S75 | Twelve Ways to Fool the Masses When Giving Performance Results on Parallel Computers (1991) | D. H. Bailey | https://www.davidhbailey.com/dhbpapers/twelve-ways.pdf |
| S76 | Scientific Benchmarking of Parallel Computing Systems (SC15) | Hoefler, Belli | https://htor.inf.ethz.ch/publications/img/hoefler-scientific-benchmarking.pdf ; https://htor.inf.ethz.ch/publications/index.php?pub=222 |
| S77 | Thirteen modern ways to fool the masses with performance results on parallel computers (2010) | G. Hager | https://blogs.fau.de/hager/files/2010/07/thirteen-ways-eihecs6.pdf |
| S78 | How NOT to Fool the Masses When Giving Performance Results for Quantum Computers | C. McGeoch | https://arxiv.org/abs/2411.08860 |
| S79 | Producing Wrong Data Without Doing Anything Obviously Wrong! (ASPLOS 2009) | Mytkowicz, Diwan, Hauswirth, Sweeney | https://sape.inf.usi.ch/publications/asplos09 |
| S80 | pyperf: Tune the system for benchmarks | pyperf developers | https://pyperf.readthedocs.io/en/latest/system.html |
| S81 | timeit — Measure execution time | Python Software Foundation | https://docs.python.org/3/library/timeit.html |
| S82 | pytest-benchmark usage | pytest-benchmark developers | https://pytest-benchmark.readthedocs.io/en/latest/usage.html |
| S83 | Using Mathlib as a dependency (Lean projects) | Lean community | https://leanprover-community.github.io/install/project.html |
| S84 | Lean reference: Lake | Lean FRO | https://lean-lang.org/doc/reference/latest/Build-Tools-and-Distribution/Lake/ |
| S85 | leanblueprint | P. Massot | https://github.com/PatrickMassot/leanblueprint |
| S86 | Formalizing the proof of PFR in Lean4 using Blueprint: a short tour | T. Tao | https://terrytao.wordpress.com/2023/11/18/formalizing-the-proof-of-pfr-in-lean4-using-blueprint-a-short-tour/ |
| S87 | Lean reference: Axioms | Lean FRO | https://lean-lang.org/doc/reference/latest/Axioms/ |
| S88 | lean-action | Lean FRO | https://github.com/leanprover/lean-action |
| S89 | LeanProject (blueprint-driven template) | P. Monticone | https://github.com/pitmonticone/LeanProject |
| S90 | LeanArchitect: Automating Blueprint Generation for Humans and AI (ITP 2026) | Zhu, Monticone, Welleck, Avigad | https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ITP.2026.25 |
| S91 | git-tag documentation | Git project | https://git-scm.com/docs/git-tag |
| S92 | Definitions (reproducible builds) | Reproducible Builds project | https://reproducible-builds.org/docs/definition/ |
| S93 | Submitting TeX/LaTeX | arXiv | https://info.arxiv.org/help/submit_tex.html |
| S94 | Ancillary files | arXiv | https://info.arxiv.org/help/ancillary_files.html |
| S95 | arxiv-latex-cleaner | Google Research | https://github.com/google-research/arxiv-latex-cleaner |
| S96 | ACM SIGIR Artifact Badging (quotes ACM v1.1) | ACM SIGIR | https://sigir.org/general-information/acm-sigir-artifact-badging/ |
| S97 | CCS 2025 Call for Artifacts (quotes ACM policy) | ACM SIGSAC | https://sigsac.org/ccs/CCS2025/call-for-artifacts/ |
| S98 | Materials, Software and Code Sharing | PLOS ONE | https://journals.plos.org/plosone/s/materials-software-and-code-sharing |
| S99 | Reporting standards and availability of data, materials, code and protocols | Nature Portfolio | https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards |
