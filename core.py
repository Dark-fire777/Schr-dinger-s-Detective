"""Schrodinger's Detective - game engine (Qiskit + numpy).
The culprit leaves a 2-qubit 'fingerprint' state. Each lab test is a Pauli measurement on that
evidence; measuring COLLAPSES it, so later tests on non-commuting observables lose information.
Test label 'XZ' = Pauli X on qubit 0 and Z on qubit 1 ('I' = untouched)."""
import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, DensityMatrix, Pauli

def _suspects():
    S = {}
    def add(name, f):
        qc = QuantumCircuit(2); f(qc); S[name] = qc
    add("Butler",    lambda q: None)                                   # |0>|0>
    add("Chef",      lambda q: (q.h(0), q.h(1)))                       # |+>|+>
    add("Gardener",  lambda q: q.h(1))                                 # |0>|+>
    add("Maid",      lambda q: q.h(0))                                 # |+>|0>
    add("Doctor",    lambda q: (q.h(0), q.cx(0, 1)))                   # Bell Phi+
    add("Banker",    lambda q: (q.h(0), q.cx(0, 1), q.x(1)))           # Bell Psi+
    add("Lawyer",    lambda q: (q.h(0), q.s(0), q.h(1), q.s(1)))       # |+i>|+i>
    add("Neighbour", lambda q: (q.x(0), q.x(1), q.h(1)))               # |1>|->
    return S

CIRCUITS = _suspects()
NAMES = list(CIRCUITS)
RHO0 = np.array([DensityMatrix(Statevector(qc)).data for qc in CIRCUITS.values()])   # (8,4,4)
QUESTIONS = [a + b for a in "IXYZ" for b in "IXYZ" if a + b != "II"]                # 15 tests
I4 = np.eye(4)
PROJ = {}
for q in QUESTIONS:
    P = Pauli(q[::-1]).to_matrix()                      # qiskit is little-endian
    PROJ[q] = {+1: (I4 + P) / 2, -1: (I4 - P) / 2}

def dossier(i):
    """Tests whose result is certain (+1/-1) for suspect i - the player's 'fingerprint card'."""
    out = []
    for q in QUESTIONS:
        e = np.real(np.trace(RHO0[i] @ (PROJ[q][1] - PROJ[q][-1])))
        if abs(e) > 0.999: out.append(f"{q}={'+' if e > 0 else '-'}")
    return out

def kraus(rhos, q, r, e=0.0):
    """Report r in {+1,-1} for test q with readout-flip prob e. Unnormalised, so trace = probability."""
    Pr, Pm = PROJ[q][r], PROJ[q][-r]
    return (1 - e) * Pr @ rhos @ Pr + e * Pm @ rhos @ Pm

def entropy(p):
    p = p[p > 1e-12]; return float(-(p * np.log2(p)).sum())

LEVELS = {  # suspects (indices into NAMES), evidence copies, test budget
    "easy":   dict(suspects=[0, 1, 4, 6], copies=3, budget=4),
    "medium": dict(suspects=list(range(8)), copies=3, budget=5),
    "hard":   dict(suspects=list(range(8)), copies=1, budget=3),
}

def test_circuit(q, measure=True):
    """Qiskit circuit that measures Pauli string q (rotate to Z basis, fold parity onto one qubit)."""
    qc = QuantumCircuit(2, 1 if measure else 0)
    sup = [i for i, ch in enumerate(q) if ch != "I"]
    for i, ch in enumerate(q):
        if ch == "X": qc.h(i)
        elif ch == "Y": qc.sdg(i); qc.h(i)
    for j in sup[1:]: qc.cx(j, sup[0])
    if measure: qc.measure(sup[0], 0)
    return qc

class Lab:
    """The true evidence: `copies` independent samples of the culprit's fingerprint (None = unlimited fresh samples,
    i.e. a 'classical' lab where tests never disturb)."""
    def __init__(self, suspect, rng, e=0.0, p=0.0, copies=1):
        self.rng, self.e, self.copies = rng, e, copies
        self.rho0 = (1 - p) * RHO0[suspect] + p * I4 / 4
        self.rho = [self.rho0.copy() for _ in range(copies or 1)]
    def ask(self, q, copy=0):
        base = self.rho0 if self.copies is None else self.rho[copy]
        pp = float(np.real(np.trace(kraus(base, q, +1, self.e))))
        r = +1 if self.rng.random() < pp else -1
        if self.copies is not None:
            k = kraus(base, q, r, self.e); self.rho[copy] = k / np.real(np.trace(k))
        return r

class Belief:
    """Detective's Bayesian belief over suspects, using exactly the lab's measurement model."""
    def __init__(self, e=0.0, p=0.0, copies=1, suspects=None):
        self.e, self.copies = e, copies
        self.rho0 = (1 - p) * RHO0 + p * I4 / 4
        self.cs = [self.rho0.copy() for _ in range(copies or 1)]
        self.lik = np.zeros(len(NAMES)); self.lik[list(range(len(NAMES)) if suspects is None else suspects)] = 1
        self.lik /= self.lik.sum()
    def posterior(self): return self.lik / self.lik.sum()
    def _w(self, q, r, c):
        base = self.rho0 if self.copies is None else self.cs[c]
        return self.lik * np.real(np.trace(kraus(base, q, r, self.e), axis1=1, axis2=2))
    def update(self, q, r, c=0):
        base = self.rho0 if self.copies is None else self.cs[c]
        k = kraus(base, q, r, self.e); w = np.real(np.trace(k, axis1=1, axis2=2))
        self.lik = self.lik * w; self.lik /= self.lik.sum()
        if self.copies is not None:
            self.cs[c] = np.where(w[:, None, None] > 1e-12, k / np.maximum(w, 1e-12)[:, None, None], base)
    def expected_entropy(self, q, c=0):
        H = 0.0
        for r in (+1, -1):
            w = self._w(q, r, c); P = w.sum()
            if P > 1e-12: H += P * entropy(w / P)
        return H
    def best_question(self, rng):
        cands = [(q, c) for q in QUESTIONS for c in range(self.copies or 1)]
        H = np.array([self.expected_entropy(q, c) for q, c in cands])
        return cands[int(rng.choice(np.flatnonzero(H <= H.min() + 1e-9)))]
    def accuse(self, rng):
        p = self.posterior(); return int(rng.choice(np.flatnonzero(p >= p.max() - 1e-9)))

# Pre-rendered once at import (the UI shows these; avoids building circuits inside Streamlit's script threads).
TEST_DRAWINGS = {q: str(test_circuit(q).draw("text")) for q in QUESTIONS}
