# Reporting standard for computational experiments

## Before the confirmatory run

- **Hypotheses and predictions.** State them with the claim ID, and say what result would count against the claim.
- **Metrics.** Define each metric exactly, with units.
- **Instances.** Give the families and sizes, how they were chosen, and which are development instances and which are held out.
- **Seeds and repetitions.** Give the number of seeds and how it was chosen. With few runs, plan interval estimates, performance profiles or the interquartile mean, not a single mean.
- **The analysis plan.** Give the statistical test or interval method, the correction for multiple comparisons, and the stopping rule.

## Uncertainty

- Say what the error bar captures (seeds, instances, shots or bootstrap resamples), whether it is a standard deviation or a standard error, and how it was computed.
- Do not decide on a p-value threshold alone, and report every analysis that was run.
- Splitting runs into groups of seeds can by itself produce "significant" differences, so compare methods on the same seeds and instances.

## Performance and advantage claims

- Report absolute times as well as speedups, and name the baseline: the best serial code or a one-process run.
- Report results for all instances, not the best ones. Justify any subset that is shown.
- Summarise costs with the arithmetic mean and rates with the harmonic mean. Avoid means of ratios; if you must use one, use the geometric mean.
- Give confidence intervals for non-deterministic timings. Warm up, pin the hardware settings and record the full setup.
- For quantum claims:
  - include tuning time in runtimes;
  - do not extrapolate to hardware that does not exist;
  - say how instances and comparison solvers were chosen;
  - compare against strong classical models, which in published benchmarks often beat the quantum ones, and ablate the quantum part.

## Stopping bias and blinding

People stop debugging when the numbers look right. Fix the checks in advance, and keep looking for bugs after the numbers agree with expectations. Where possible, hide the target quantity until the analysis is frozen.

## Provenance (Sandve's rules, condensed)

- Every result has a script, a seed and a commit. There are no manual edits to outputs.
- Keep the raw data behind every plot.
- Link every statement in the text to its result, here a `numbers.json` key.

Sources, opened 2026-10-16 (full list in the lab repository's `docs/best-practices/research.md`):

- Center for Open Science, preregistration: <https://www.cos.io/initiatives/prereg>
- Gelman and Loken, "The garden of forking paths": <https://sites.stat.columbia.edu/gelman/research/unpublished/p_hacking.pdf>
- Henderson et al., "Deep Reinforcement Learning that Matters": <https://arxiv.org/abs/1709.06560>
- Agarwal et al., "Deep RL at the Edge of the Statistical Precipice": <https://arxiv.org/abs/2108.13264>
- NeurIPS paper checklist: <https://neurips.cc/public/guides/PaperChecklist>
- Bowles, Ahmed and Schuld, "Better than classical? Benchmarking quantum machine learning models": <https://arxiv.org/abs/2403.07059>
- McGeoch, "How NOT to Fool the Masses When Giving Performance Results for Quantum Computers": <https://arxiv.org/html/2411.08860v1>
- Hoefler and Belli, "Scientific Benchmarking of Parallel Computing Systems": <https://htor.inf.ethz.ch/publications/img/hoefler-scientific-benchmarking.pdf>
- Klein and Roodman, "Blind Analysis in Nuclear and Particle Physics" (copy): <https://www.gwern.net/doc/statistics/bias/2005-klein.pdf>
