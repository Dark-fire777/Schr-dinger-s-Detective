from streamlit.testing.v1 import AppTest
at = AppTest.from_file("app.py", default_timeout=60).run(); assert not at.exception, at.exception
for lvl in ["easy", "medium", "hard"]:
    at.sidebar.selectbox[0].set_value(lvl).run(); assert not at.exception
    at.selectbox(key="q").set_value("ZZ").run(); at.button(key="run").click().run(); assert not at.exception
    assert len(at.table) == 1; at.button(key="accuse").click().run(); assert not at.exception
    assert at.success or at.error
print("APP OK")
