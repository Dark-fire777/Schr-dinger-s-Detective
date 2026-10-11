"""Terminal game: python play.py [--level easy|medium|hard] [--seed N] [--hints] [--demo]"""
import argparse, numpy as np, core as C
ap = argparse.ArgumentParser()
ap.add_argument("--level", default="medium", choices=C.LEVELS); ap.add_argument("--seed", type=int, default=None)
ap.add_argument("--hints", action="store_true", help="show the probability board after each test")
ap.add_argument("--demo", action="store_true", help="auto-play with the information-gain solver")
a = ap.parse_args(); L = C.LEVELS[a.level]; rng = np.random.default_rng(a.seed)
culprit = int(rng.choice(L["suspects"])); lab = C.Lab(culprit, rng, copies=L["copies"]); belief = C.Belief(copies=L["copies"], suspects=L["suspects"])
cp = L["copies"]
print(f"\n=== SCHRODINGER'S DETECTIVE ({a.level}) ===")
print("The culprit left a quantum fingerprint on two clue-qubits. Run lab tests, then accuse.")
print("'ZI' = Pauli Z on qubit 0, 'XX' = X on both qubits. Each test COLLAPSES the sample it is run on:")
print("a later test that doesn't commute with it gets scrambled. " + (f"You have {cp} separate evidence samples (1..{cp})." if cp > 1 else "You have ONE evidence sample - choose carefully."))
print("\nFingerprint cards (results that are certain for each suspect; '-' means -1):")
for n, i in enumerate(L["suspects"], 1): print(f"  {n}. {C.NAMES[i]:<10} " + "  ".join(C.dossier(i)))
print(f"\nTests available: {' '.join(C.QUESTIONS)}\nYou have {L['budget']} tests." + (" Enter e.g. 'ZZ 2' (test ZZ on sample 2)." if cp > 1 else "") + "\n")
for k in range(L["budget"]):
    if a.demo: q, c = belief.best_question(rng); print(f"Test {k+1}> {q}" + (f" {c+1}" if cp > 1 else ""))
    else:
        while True:
            t = input(f"Test {k+1}> ").split()
            if not t: continue
            q = t[0].upper(); c = int(t[1]) - 1 if len(t) > 1 and t[1].isdigit() else 0
            if q in C.QUESTIONS and 0 <= c < cp: break
            print("  invalid - try again")
    r = lab.ask(q, c); belief.update(q, r, c); print(f"   result: {'+1' if r > 0 else '-1'}")
    if a.hints or a.demo: print("   board: " + "  ".join(f"{C.NAMES[i]}:{p:.0%}" for i, p in enumerate(belief.posterior()) if i in L["suspects"]))
if a.demo: guess = belief.accuse(rng); print("Accusing:", C.NAMES[guess])
else:
    guess = -1
    while guess not in L["suspects"]:
        try: guess = L["suspects"][int(input(f"Accuse (1-{len(L['suspects'])})> ")) - 1]
        except (ValueError, IndexError): guess = -1
print("\n" + ("CASE CLOSED - correct!" if guess == culprit else f"Wrong. It was the {C.NAMES[culprit]}.") + "\n")
