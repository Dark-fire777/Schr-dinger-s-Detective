# Schrödinger's Detective

*This effort is supported by Qollab & IonQ.* MIT licensed.

**Short description:**
A detective game where quantum measurement is the mechanic: each lab test collapses the evidence, scrambling later tests. Includes Qiskit circuits, model validation, and a benchmark of how many evidence copies a detective needs.

## What it does
The culprit leaves a 2-qubit quantum fingerprint (8 suspects = 8 states built with Qiskit circuits: Z/X/Y-basis
product states and Bell states). You run lab tests (Pauli measurements like `ZI`, `XX`, `YY`). **A test collapses
the evidence sample it uses**, so a later test that doesn't commute with it is scrambled. Choosing which question to
ask, on which sample, and in what order is the puzzle: the uncertainty principle and no-cloning as gameplay.

## What problem it explores
How much does measurement disturbance cost an investigator, and how many independent copies of the evidence are
needed to recover from it? (Also a teaching tool for non-commuting observables.)

## How to run
Run `main.py` (Python / Qiskit project). It prints: fingerprint cards and Qiskit circuits; a validation that the game
model matches Qiskit circuits on all 120 (suspect, test) pairs; a collapse demo; a scripted hard case solved by an
information-gain detective; and a benchmark. Raise `TRIALS` at the top for tighter error bars.

## Method
Tests are Qiskit circuits (H for X, S†·H for Y, CNOT parity folding, measure). Sequential collapse uses an equivalent
projector model validated against the circuits (error 2e-16). The detective is Bayesian and chooses tests by expected
information gain. Evidence "copies" = independent samples; unlimited copies = a classical, non-disturbing lab.

## Results (full run, 400 cases per row; `main.py` default is a quicker 200)
One sample caps accuracy at ~0.35 (chance 0.125). About 3 samples recover the classical limit (0.75 vs 0.76 at 6
tests, ±0.02). Information-gain tests beat random tests (0.75 vs 0.40). Accuracy degrades gracefully with readout error.

## Limitations
Single 2-qubit register, 8 suspects; greedy information gain is myopic, not provably optimal; text output only.

## Disclosure
Built with AI assistance (Claude), Qiskit, NumPy. No templates or outside repos.
