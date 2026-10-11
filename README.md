# Schrödinger's Detective  (Quantum Playground)
*This effort is supported by Qollab & IonQ.*  MIT licensed.

## What it does
A detective game where **quantum measurement is the mechanic**. The culprit leaves a 2-qubit "fingerprint"
(8 suspects = 8 different states built with Qiskit circuits: Z/X/Y-basis product states and Bell states).
You run lab tests (Pauli measurements such as `ZI`, `XX`, `YY`) and then accuse. **A test collapses the evidence
sample it uses**, so a later test that doesn't commute with it is scrambled. Which question you ask, on which
sample, and in what order, is the puzzle: the uncertainty principle and no-cloning as gameplay.
Three levels: easy (4 suspects, 3 samples), medium (8 suspects, 3 samples), hard (8 suspects, ONE sample).

## Run
    pip install -r requirements.txt
    streamlit run app.py                     # visual app (every chart has a text table; keyboard friendly)
    python play.py --level medium --hints    # terminal version (add --demo to watch the solver)
    python validate.py                       # checks the game model against real Qiskit circuits (+ Aer)
    python analysis.py                       # benchmark -> results.md / results.json / results.png
    python test_app.py                       # headless UI test

## How the quantum part works
`core.py` builds each suspect's state with a Qiskit `QuantumCircuit`. Each test is a Qiskit circuit
(`test_circuit`): rotate to the Z basis (H for X, S†·H for Y), fold parity with CNOTs, measure. The game uses an
equivalent density-matrix (projector) model for fast sequential collapse; `validate.py` proves the two agree on all
120 (suspect, test) pairs (exact error 2e-16; Aer sampling within 0.7σ).

## Technical extension (benchmark, 400 trials/point)
A Bayesian detective picks tests greedily by expected information gain, or randomly. We vary the number of
independent evidence copies (1 = quantum single sample, ∞ = a classical lab where tests never disturb), the
difficulty levels, and readout-flip / depolarising noise.
Findings (results.md / results.png):
- **One copy of 2 qubits caps accuracy at ~0.35** (chance 0.125): collapse destroys what you haven't measured.
- **About 3 copies recover the classical limit** (0.75 vs 0.76 at 6 tests; ±0.02 Monte-Carlo error).
- Information-gain tests clearly beat random tests (0.75 vs 0.40 at 6 tests, ∞ copies).
- Graceful degradation under noise (accuracy 0.55 → 0.27 as readout error 0 → 0.2).

## Limitations
Single 2-qubit evidence register, 8 suspects; greedy information gain is myopic, not provably optimal;
noise results use 2 copies / 4 tests; the UI is Streamlit (Python), not a hosted web page.

## Disclosure
Built with AI assistance (Claude), Qiskit, Qiskit Aer, NumPy, pandas, Streamlit, Matplotlib. No templates or outside repos.
