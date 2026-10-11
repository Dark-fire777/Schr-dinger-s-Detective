"""Visual app: streamlit run app.py   (Qiskit engine in core.py; accessible: every chart has a text table)"""
import numpy as np, pandas as pd, streamlit as st, core as C
st.set_page_config(page_title="Schrödinger's Detective", layout="wide")

def new_case(level):
    L = C.LEVELS[level]; rng = np.random.default_rng(); culprit = int(rng.choice(L["suspects"]))
    st.session_state.update(level=level, rng=rng, culprit=culprit, lab=C.Lab(culprit, rng, copies=L["copies"]),
                            belief=C.Belief(copies=L["copies"], suspects=L["suspects"]), log=[], result=None)

level = st.sidebar.selectbox("Difficulty", list(C.LEVELS), index=1)
if st.sidebar.button("New case", key="new") or "lab" not in st.session_state or st.session_state.level != level: new_case(level)
S = st.session_state; L = C.LEVELS[S.level]; cp = L["copies"]; left = L["budget"] - len(S.log)
hints = st.sidebar.checkbox("Show detective's probability board", value=False)

st.title("🕵️ Schrödinger's Detective")
st.write("The culprit left a quantum fingerprint on two clue-qubits. Run lab tests (Pauli measurements), then accuse. "
         "**Each test collapses the evidence sample it uses**, so later tests that don't commute with it get scrambled.")
st.subheader("Fingerprint cards")
st.dataframe(pd.DataFrame([{"Suspect": C.NAMES[i], "Certain test results (− means −1)": "  ".join(C.dossier(i))} for i in L["suspects"]]), hide_index=True)

st.subheader(f"Lab — {left} test(s) left, {cp} evidence sample(s)")
c1, c2, c3 = st.columns(3)
q = c1.selectbox("Test", C.QUESTIONS, key="q", help="e.g. ZI = Z on qubit 0; XX = X on both qubits")
smp = c2.selectbox("Evidence sample", list(range(1, cp + 1)), key="smp", disabled=cp == 1)
c3.write(""); run = c3.button("Run test", key="run", disabled=left <= 0 or S.result is not None)
if run:
    r = S.lab.ask(q, smp - 1); S.belief.update(q, r, smp - 1)
    S.log.append({"#": len(S.log) + 1, "Test": q, "Sample": smp, "Result": "+1" if r > 0 else "-1"}); st.rerun()
with st.expander("Qiskit circuit for this test"):
    st.code(C.TEST_DRAWINGS[q])
if S.log: st.table(pd.DataFrame(S.log).set_index("#"))
if hints:
    board = pd.DataFrame({"Suspect": [C.NAMES[i] for i in L["suspects"]], "Probability": [float(S.belief.posterior()[i]) for i in L["suspects"]]})
    st.bar_chart(board.set_index("Suspect")); st.dataframe(board.assign(Probability=board.Probability.map("{:.0%}".format)), hide_index=True)

st.subheader("Accuse")
who = st.selectbox("Culprit", [C.NAMES[i] for i in L["suspects"]], key="who")
if st.button("Accuse", key="accuse", disabled=S.result is not None):
    S.result = (who == C.NAMES[S.culprit]); st.rerun()
if S.result is True: st.success("Case closed — correct!")
elif S.result is False: st.error(f"Wrong. It was the {C.NAMES[S.culprit]}.")
