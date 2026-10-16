# Building or reviewing a physical model

The outcome is a model card. The mathematician proves against it, the computational scientist simulates it, and the referee attacks it, all without this conversation. So the card makes every choice visible, together with the reason it is safe.

The card holds:

- **Degrees of freedom and scales.** What is kept and what is neglected, and the dimensionless ratio that justifies each neglect. Add an order-of-magnitude value for each ratio in the regime of interest.
- **Symmetries and conservation laws.** Name the symmetry group and the conserved charges, which ones the model preserves and which it breaks, and whether it breaks them explicitly or spontaneously. Note which results depend on a symmetry and so fail when noise breaks it.
- **Units and conventions.** The units system (ħ = 1 or not), sign and phase conventions, normalisation, and the basis and qubit order for anything that will be coded.
- **Limits with known answers.** Small and large size, weak and strong coupling, the classical limit, zero noise and full noise. For each limit, give the known answer and whether the model reproduces it.
- **Observables.** What a measurement would record, with its noise, the number of repetitions it needs, and the knob an experimentalist would turn.
- **The regime of validity.** Where the model is trusted, and the first effect that breaks it.

Run the checks the card names. Dimensional analysis and the limiting cases are computations, not assertions: show them, or write a short script.

## Hand back

The card, the checks that passed and failed, and the single assumption the model's conclusions lean on hardest.
