# Advantage audit

The outcome is a verdict on a quantum claim, on the five questions below, with evidence for each. Read by the PI, the referee and eventually a journal, it must survive a reader who has seen many advantage claims dequantized. The verdict is one of: proven advantage under a stated model; conjectured advantage with a named barrier; heuristic with no known separation; quantum-inspired (the classical algorithm is the contribution); or no advantage.

## The five questions

1. **Input model.** How does the data reach the quantum computer: an oracle, QRAM, state preparation from classical data, or states given only as quantum states? What does loading cost, end to end? A speedup that assumes QRAM the application lacks is not a speedup for that application.
2. **Output model.** What is read out: a sample, an expectation value to precision ε, or a full vector? Count the shots and the readout cost. A speedup that ends in an exponentially small amplitude is not a speedup.
3. **Best classical comparison.** Ask for the strongest classical method with the same access. Check the standard dequantization routes against the claim, or say why each one fails:
   - ℓ²-norm sampling and low-rank methods;
   - tensor networks for low entanglement;
   - Clifford and matchgate simulation;
   - product or computationally tractable inputs;
   - classical shadows.

   Run the classical method on the claim's own instances where you can.
4. **Proof status.**
   - Is there a proved separation: oracle, query, sample or communication?
   - Is there a complexity-theoretic conjecture, and which one?
   - Or is there only numerical evidence on small sizes?

   Name the weakest step.
5. **End-to-end resources.** Go to `resource-estimate.md` beside this file. A polynomial speedup with a large constant can lose to classical hardware for every practical size.

## What you cannot infer

- The lab's wording rule: proven, conjectured, heuristic and quantum-inspired are four different claims. The claim's label appears in the brief, the paper's abstract and the release record.
- Every source cited for a dequantization result or a lower bound is opened and quoted. A remembered "known result" is labelled UNVERIFIED until it is opened.

## Hand back

The verdict, the five answers with their evidence, the classical method tried and its result, and the one experiment or proof that would move the verdict up a level.
