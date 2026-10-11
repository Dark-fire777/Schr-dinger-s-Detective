"""Benchmark. Q1: how many copies of the evidence does a detective need? (copies=1 is the quantum single-sample
lab, copies=None is a classical non-disturbing lab).  Q2: difficulty levels.  Q3: noise robustness."""
import json, numpy as np, core as C
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
KMAX, TRIALS = 6, 50

def run(strategy="greedy", copies=1, e=0.0, p=0.0, suspects=None, seed=0, kmax=KMAX):
    rng = np.random.default_rng(seed); sus = suspects or list(range(8)); ok = np.zeros(kmax); n = 0
    for s in sus:
        for _ in range(TRIALS):
            lab = C.Lab(s, rng, e, p, copies); b = C.Belief(e, p, copies, sus); n += 1
            for k in range(kmax):
                if strategy == "greedy": q, c = b.best_question(rng)
                else: q, c = C.QUESTIONS[int(rng.integers(15))], int(rng.integers(copies or 1))
                b.update(q, lab.ask(q, c), c); ok[k] += (b.accuse(rng) == s)
    return (ok / n).tolist()

res = {"copies": {}, "random": {}, "levels": {}, "readout_error": {}, "depolarising": {}}
for c in [1, 2, 3, 5, None]:
    res["copies"]["inf (classical lab)" if c is None else str(c)] = run(copies=c); print("copies", c, np.round(res["copies"]["inf (classical lab)" if c is None else str(c)], 2), flush=True)
res["random"]["1"] = run("random", 1); res["random"]["inf"] = run("random", None)
for name, L in C.LEVELS.items():
    res["levels"][name] = run(copies=L["copies"], suspects=L["suspects"], kmax=L["budget"])[-1]; print(name, res["levels"][name], flush=True)
for e in [0, .02, .05, .1, .2]: res["readout_error"][e] = run(copies=2, e=e, kmax=4)[-1]
for p in [0, .1, .2, .4, .6]: res["depolarising"][p] = run(copies=2, p=p, kmax=4)[-1]
json.dump(res, open("results.json", "w"), indent=1)

md = ["## P(correct accusation) vs tests used, 8 suspects (chance 0.125), greedy information-gain detective", "| Evidence copies | " + " | ".join(f"K={k}" for k in range(1, KMAX + 1)) + " |", "|---|" + "---|" * KMAX]
md += [f"| {k} | " + " | ".join(f"{x:.2f}" for x in v) + " |" for k, v in res["copies"].items()]
md += [f"| random tests, 1 copy | " + " | ".join(f"{x:.2f}" for x in res["random"]["1"]) + " |", f"| random tests, inf copies | " + " | ".join(f"{x:.2f}" for x in res["random"]["inf"]) + " |"]
md += ["", "## Difficulty levels (greedy detective, final accuracy within budget)", "| Level | Suspects | Copies | Tests | Accuracy |", "|---|---|---|---|---|"]
md += [f"| {n} | {len(L['suspects'])} | {L['copies']} | {L['budget']} | {res['levels'][n]:.2f} |" for n, L in C.LEVELS.items()]
md += ["", "## Noise (2 copies, 4 tests)", "| Readout flip prob | Accuracy |", "|---|---|"] + [f"| {k} | {v:.2f} |" for k, v in res["readout_error"].items()]
md += ["", "| Depolarising p | Accuracy |", "|---|---|"] + [f"| {k} | {v:.2f} |" for k, v in res["depolarising"].items()]
open("results.md", "w").write("\n".join(md)); print("\n".join(md))

fig, ax = plt.subplots(1, 2, figsize=(11, 4)); ks = range(1, KMAX + 1)
for k, v in res["copies"].items(): ax[0].plot(ks, v, marker="o", label=f"{k} copies" if k[0] != "i" else "unlimited (classical)")
ax[0].plot(ks, res["random"]["1"], "k--", label="random tests, 1 copy"); ax[0].axhline(1 / 8, c="gray", ls=":")
ax[0].set_xlabel("tests used"); ax[0].set_ylabel("P(correct accusation)"); ax[0].legend(fontsize=7); ax[0].set_title("Evidence copies vs accuracy")
ax[1].plot(list(map(str, res["readout_error"])), list(res["readout_error"].values()), marker="o", label="readout flip prob")
ax[1].plot(list(map(str, res["depolarising"])), list(res["depolarising"].values()), marker="s", label="depolarising p")
ax[1].set_ylim(0, 1.02); ax[1].set_title("Noise robustness (2 copies, 4 tests)"); ax[1].legend(); plt.tight_layout(); plt.savefig("results.png", dpi=130)
