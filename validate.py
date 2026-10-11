"""Validate the game's density-matrix measurement model against real Qiskit circuits (all 8 suspects x 15 tests)."""
import numpy as np, core as C
from qiskit.quantum_info import Statevector
from qiskit_aer import AerSimulator
from qiskit import transpile
worst_exact, worst_sigma, sim, SH = 0.0, 0.0, AerSimulator(), 8000
for i, (name, prep) in enumerate(C.CIRCUITS.items()):
    for q in C.QUESTIONS:
        model = float(np.real(np.trace(C.PROJ[q][1] @ C.RHO0[i])))
        sup = [k for k, ch in enumerate(q) if ch != "I"][0]
        sv = Statevector(prep.compose(C.test_circuit(q, measure=False)))
        exact = float(sv.probabilities([sup])[0]); worst_exact = max(worst_exact, abs(exact - model))
        qc = prep.compose(C.test_circuit(q)); cnt = sim.run(transpile(qc, sim), shots=SH, seed_simulator=1).result().get_counts()
        est = cnt.get("0", 0) / SH; sd = max(np.sqrt(max(model * (1 - model), 1e-4) / SH), 1e-3)
        worst_sigma = max(worst_sigma, abs(est - model) / sd)
print(f"120 (suspect,test) pairs | max |exact circuit - model| = {worst_exact:.2e} | max Aer deviation = {worst_sigma:.1f} sigma")
assert worst_exact < 1e-9 and worst_sigma < 5
print("VALIDATION PASSED")
