# Research-software standards

The bar for code that backs a claim in a paper. Read it when the user asks about research code standards, testing numerical or quantum code, or reproducibility. `bmad-build` loads it in a project once that project's override is set (last section).

## The bar

Code that backs a published claim must let a stranger do three things: rerun it from a clean checkout, see which test checks which statement, and get the same numbers within stated tolerances. Treat "Good enough practices" (Wilson et al. 2017) as the floor and "Best practices for scientific computing" (Wilson et al. 2014) as the target. Unit tests, CI and review are part of the standard here, because the lab publishes numerical claims.

## Layout and environment

- **Layout.** Use the src layout with `pyproject.toml`. Tests run against the installed package (PyPA).
- **Lock file.** Commit `uv.lock`. "One command regenerates everything" means `uv sync`, then `uv run pytest`, then the project's figures script run with `uv run`, `{project-root}/scripts/figures.py`.
- **Figures.** `scripts/figures.py` writes every figure and `numbers.json` from a fixed seed. Every number quoted in a paper is a key in that file.
- **Repository files.** Add a README with those commands, a licence (MIT by default; check employer ownership first) and a `CITATION.cff`.
- **Tooling.** Use Ruff for lint and format, and mypy on `src` when the project grows past a few modules (Scientific Python Development Guide).

## Tests for numerical code

- **Tolerances.**
  - Never compare floats with `==`.
  - State `rtol` and `atol` and say why.
  - `numpy.testing.assert_allclose` defaults to `atol=0` and is asymmetric, so the reference goes in `desired`.
  - Any comparison with zero needs an explicit `atol`, because no value is small relative to zero.
  - Use `strict=True` so shapes and dtypes cannot silently broadcast.
- **Oracles, strongest first.**
  1. Closed forms and analytic cases.
  2. Independent slow implementations.
  3. Metamorphic relations: symmetries, invariances, scalings.
  4. Order-of-accuracy tests for discretisations, using manufactured solutions and the observed order p = log(e₁/e₂)/log r.
  5. Stored golden numbers, regenerated only in a reviewed commit with a reason.
- **Statements are oracles.** Each numbered statement the code touches gets a test named after it, and the paper's reproducibility appendix maps statements to tests.
- **Property-based tests.** Use Hypothesis for invariants, with bounded float strategies and NaN/inf decided explicitly.
- **Randomness.**
  - Seed with `numpy.random.default_rng` and `SeedSequence`, and spawn child streams for parallel work, never `seed + i`.
  - A seeded test catches regressions. A distributional test over many runs catches wrong statistics.
  - Fixed seeds alone hide flakiness: one study found 461 tests in 114 ML projects that fail once their seeds are removed.
  - Budget the false-failure rate of statistical assertions: with k tests at level α, a spurious red build has probability 1 − (1 − α)^k.

## Tests for quantum code

- **Bit order.** Write the bit-order convention in every test.
  - Qiskit count keys are little-endian, while its primitives' `BitArray` defaults to big-endian.
  - Qubit-order mix-ups are a named bug pattern.
  - Most quantum-specific bugs produce wrong output, not crashes.
- **Small n.** Check unitary or statevector equivalence up to global phase: `Operator.equiv` in Qiskit, `cirq.testing.assert_allclose_up_to_global_phase` in Cirq. Account for the layout and final permutation after transpilation.
- **Large n.** Use mirror circuits: run C and then C† with random Pauli frames, so that a correct stack returns one known bit string. Formal equivalence checking of compiled circuits is another option (MQT QCEC).
- **Sampled output.** Use statistical assertions, such as chi-square for distributions and contingency tables for correlations. Use enough shots and a small α, and remember that a large p-value is not proof of correctness.
- **Seeds.** Seed the transpiler and the simulator separately, and log both.
- **Resource estimates.** State every layer: logical counts, code and factories, physical error rates, and the error budget. Check that declared and decomposed gate counts agree.

## Working with AI coding agents

- **Write the spec first.** It names the files and interfaces, what is out of scope, and an end-to-end check.
- **Keep diffs small,** and give the agent a runnable check. Ask for the command and its output as evidence, not a claim of success.
- **Tests are written from the statement, not from the code.**
  - LLM-generated oracles tend to capture what the code does rather than what it should do.
  - Pasting computed output into expected values is a named TDD mistake.
  - Have one session write the tests and another the code, and use mutation testing (mutmut) to find tests that would not notice a bug.
- **Check every new dependency** against PyPI and the lock file, and every new API against its documentation. Code models invent package names at measurable rates.
- **Review independently.** Use `bmad-code-review` with a fresh context. The reviewer re-derives at least one formula and checks units, conventions (signs, phases, normalisation, ħ, bit order) and numerical stability.

## Story Definition of Done (CODE)

- Every acceptance criterion maps to a named test.
- Tolerances are stated with reasons.
- `uv run pytest` passes from the lock file.
- `scripts/figures.py` still regenerates `numbers.json` unchanged, or the change is explained in the story.
- The review is done.
- No new dependency has been left unverified.

## Giving bmad-build these standards in a project

Add the file as a persistent fact of `bmad-build` with a team override in the project:

```toml
# {project-root}/_bmad/custom/bmad-build.toml
[workflow]
persistent_facts = ["file:{project-root}/.agents/skills/bmod-lab/help/research-software.md"]
```

`tools/install_lab.py` writes this override when it links the lab into a project. To change it later, use `bmad-customize`.

## Sources

Every source below was opened on 2026-10-16. The full digest is in the lab repository's `docs/best-practices/software.md`.

- Wilson et al., "Best Practices for Scientific Computing", PLoS Biol 2014: <https://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.1001745>
- Wilson et al., "Good enough practices in scientific computing", PLoS Comput Biol 2017: <https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005510>
- NumPy, `assert_allclose`: <https://numpy.org/doc/stable/reference/generated/numpy.testing.assert_allclose.html>
- PEP 485: <https://peps.python.org/pep-0485/>
- NumPy, parallel random number generation: <https://numpy.org/doc/stable/reference/random/parallel.html>
- Dutta et al., "To Seed or Not to Seed?", ICST 2022: <https://icst2022.vrain.upv.es/details/icst-2022-papers/16/To-Seed-or-Not-to-Seed-An-Empirical-Analysis-of-Usage-of-Seeds-for-Testing-in-Machin>
- NTNU notes on the method of manufactured solutions: <https://fredf.folk.ntnu.no/teaching/chapter1MMS.html>
- Huang and Martonosi, "Statistical Assertions for Validating Patterns and Finding Bugs in Quantum Programs", ISCA 2019: <https://arxiv.org/abs/1905.09721>
- Paltenghi and Pradel, "Bugs in Quantum Computing Platforms", OOPSLA 2022: <https://arxiv.org/abs/2110.14560>
- Proctor et al., mirror-circuit benchmarking, PRL 2022: <https://arxiv.org/abs/2112.09853>
- Qiskit, bit ordering: <https://quantum.cloud.ibm.com/docs/en/guides/bit-ordering>
- `cirq.testing`: <https://quantumai.google/reference/python/cirq/testing>
- MQT QCEC: <https://mqt.readthedocs.io/projects/qcec/en/latest/>
- Scientific Python Development Guide: <https://learn.scientific-python.org/development/>
- uv project layout and lock file: <https://docs.astral.sh/uv/concepts/projects/layout/>
- Kent Beck, "Canon TDD": <https://newsletter.kentbeck.com/p/canon-tdd>
- Konstantinou et al., LLM-generated test oracles: <https://arxiv.org/abs/2410.21136>
- Spracklen et al., package hallucinations, USENIX Security 2025: <https://arxiv.org/abs/2406.10279>
- Google engineering practices, code review: <https://google.github.io/eng-practices/review/reviewer/looking-for.html>
