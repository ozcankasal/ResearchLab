# Formalization plan (Lean 4 and mathlib)

The outcome is a plan that the lab can execute story by story. It holds a blueprint (a LaTeX dependency graph of definitions and lemmas, each linked to a Lean declaration) and FORMAL stories in the plan. Someone who has not read this conversation should be able to pick up any node and know what "done" means. First decide with the user whether formalization pays off here. It pays off for a statement that is central, subtle, or about to be relied on by others. It rarely pays off for a routine corollary.

## What you cannot infer

- **Project setup.**
  - Run `lake new <name> math`, then `lake update` and `lake exe cache get` for prebuilt mathlib.
  - Commit `lean-toolchain`, the lakefile and `lake-manifest.json`.
  - Bump mathlib deliberately: copy mathlib's toolchain, run `lake update`, then build.
- **Blueprint.** Use leanblueprint: every node carries `\lean{decl}`, `\uses{…}` and `\leanok` when done. CI runs `leanblueprint checkdecls`, so the blueprint cannot name a declaration that does not exist.
- **Stories split by node, in two steps** (the pattern the PFR formalization used):
  1. State the definition or lemma with `sorry`. The node shows as stated, and later nodes can start at once.
  2. Prove it. The node turns green.
- **Definition of Done for a proof story.**
  - `#print axioms` on the target lists only `propext`, `Classical.choice` and `Quot.sound`.
  - There is no `sorryAx`, and no `native_decide` unless approved.
  - CI builds with warnings as errors (`lean-action` with `--wfail`).
- **Search mathlib before writing.** Search by type and by name pattern. A missing library lemma is its own story, small and upstreamable.
- **Feed gaps back.** A gap that formalization exposes in the informal proof goes back into `lab-prove`'s gap list and, for a published paper, into an erratum.

## Hand back

The blueprint skeleton, the FORMAL stories added to the plan (run `lab-plan`'s storyboard to check them), the first node to state, and an estimate of how much of the graph mathlib already covers.

Sources, opened 2026-10-16:

- mathlib as a dependency: <https://leanprover-community.github.io/install/project.html>
- leanblueprint: <https://github.com/PatrickMassot/leanblueprint>
- Tao, "Formalizing the proof of PFR in Lean4 using Blueprint": <https://terrytao.wordpress.com/2023/11/18/formalizing-the-proof-of-pfr-in-lean4-using-blueprint-a-short-tour/>
- Lean reference on axioms: <https://lean-lang.org/doc/reference/latest/Axioms/>
- lean-action: <https://github.com/leanprover/lean-action>
