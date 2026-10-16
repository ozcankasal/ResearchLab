# Resource estimate

The outcome is an end-to-end resource estimate that someone else could recompute, layer by layer, from stated inputs. It is read by the PI deciding whether the work is worth doing, and by a referee checking whether the claim is realistic.

Give one table per layer, each assumption with its source:

- **Algorithm.** Logical qubits, gate counts by type (T or Toffoli count, rotations with their synthesis precision) and depth, as functions of the problem size and the precision ε.
- **Data in and out.** The state-preparation or oracle cost, the number of shots or amplitude-estimation rounds for the precision required, and the classical pre- and post-processing.
- **Error correction.** The code (surface or LDPC), the distance chosen for a target logical error rate, magic-state factories, and the physical qubits and runtime that result. State the physical error rate and the cycle time assumed.
- **Without error correction.** The error-mitigation overhead in shots, for example the sampling overhead of probabilistic error cancellation or extrapolation, and the depth beyond which the signal is lost to noise.
- **Wall clock and comparison.** Total runtime on the assumed hardware, against the best classical runtime on the same instance.

## Checks

- Declared counts equal decomposed counts. Compile a small instance and count.
- Counts scale as the algorithm's analysis says, across three sizes.
- Compare with a published estimate for a similar task where one exists. Open and quote it; a large disagreement needs an explanation.

## Hand back

The tables, the dominant cost, the size at which the quantum approach would break even with the classical one under the stated assumptions (or why it never does), and the assumption the answer is most sensitive to.

Tools: Microsoft's quantum resource estimator for layered estimates, and Qualtran for bloq-level counting with consistency checks.
