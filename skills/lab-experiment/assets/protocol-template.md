# Protocol: {experiment name} ({story ID}, claim {C-ID})

Frozen on: {YYYY-MM-DD, commit} · Author: {…}

## Question and predictions

{What the experiment settles. The prediction if the claim holds, and the result that would count against it (the kill criterion).}

## Metrics

| Metric | Definition | Units |
|---|---|---|

## Instances

- Development set (exploration allowed): {…}
- Held-out set (confirmatory only): {…}
- How chosen: {…}

## Methods compared

| Method | Role (ours / baseline / ablation) | Tuning budget | Published numbers reproduced? |
|---|---|---|---|

## Runs

Seeds: {how many, SeedSequence root}. Repetitions: {…}. Hardware and environment: {lock file commit, machine}.

## Analysis plan

{Interval or test, multiple-comparison handling, stopping rule, what is reported for every instance.}

## Blinding

{What is hidden until the analysis is frozen, or why blinding is not possible here.}
