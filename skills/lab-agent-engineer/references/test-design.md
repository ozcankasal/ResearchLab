# Test design for numerical and quantum code

The outcome is a test plan, and then the tests, for the code the user names. A reviewer who has read only the paper and the plan must be able to see which test guards which statement, and why each tolerance is what it is. The standards are in `help/research-software.md` of the `bmod-lab` record beside this skill. Read its testing sections before planning.

## What to produce

- **A table, one row per behaviour.** Each row gives:
  - the statement or contract, quoted from the paper or docstring;
  - the oracle: closed form, independent implementation, metamorphic relation, convergence order, golden number, or statistical test;
  - the tolerance, as `rtol` and `atol`, with the reason;
  - the seed policy;
  - the test name.
- **For quantum code,** add the bit-order convention, the global-phase handling and the transpiler and simulator seeds for each test.
- **For statistical tests,** add the number of samples, α and the resulting false-failure rate per CI run. Tests that cannot be cheap and reliable run nightly rather than on every push.
- **The tests themselves,** written before or beside the code, never by pasting the code's current output into expected values. When a golden number is the only oracle available, say so in the test's docstring and keep its regeneration behind a reviewed commit.

## What you cannot infer

- The lab's convention: every numbered statement the code touches has a test named after it, for example `test_mirror_preserves_kernels_and_reflects_winding`, and the paper's reproducibility appendix lists the mapping.
- Run the tests with the mutation tester (`uv run --with mutmut mutmut run`) once they pass. A surviving mutant in core numerics is a missing test.

## Hand back

The plan table, the test files written, the command that runs them, and any behaviour left without an independent oracle, named as a risk.
