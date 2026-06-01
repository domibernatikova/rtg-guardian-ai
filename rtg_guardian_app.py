
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="RTG Guardian AI", layout="wide")

st.title("🏥 RTG Guardian AI")
st.subheader("Druhý pár očí pro radiology")

st.markdown("Nahraj RTG snímek a simuluj AI priorizaci fronty.")

uploaded = st.file_uploader("RTG snímek", type=["jpg","jpeg","png"])

if uploaded:
    st.image(uploaded, caption="Nahraný snímek", width=300)

    ai_prob = st.slider("Simulovaná pravděpodobnost nálezu (%)", 0, 100, 85)

    waiting = st.slider("Čekací doba (min)", 0, 120, 10)
    workload = st.slider("Vytížení pracoviště (%)", 0, 100, 75)

    ai_score = ai_prob / 100
    waiting_score = min(waiting / 60, 1)
    workload_score = workload / 100

    priority = (
        0.7 * ai_score +
        0.2 * waiting_score +
        0.1 * workload_score
    )

    if waiting > 60:
        level = "🔴 KRITICKÁ (Anti‑Death Queue)"
    elif priority > 0.8:
        level = "🔴 KRITICKÁ"
    elif priority > 0.6:
        level = "🟠 VYSOKÁ"
    elif priority > 0.4:
        level = "🟡 STŘEDNÍ"
    else:
        level = "🟢 NÍZKÁ"

    st.metric("Prioritní skóre", f"{priority:.2f}")
    st.metric("Zařazení", level)

st.divider()

st.header("📋 Fronta radiologa")

sample = pd.DataFrame([
    ["P001", 96, 5],
    ["P002", 18, 70],
    ["P003", 81, 12],
    ["P004", 54, 22],
], columns=["Pacient","AI %","Čeká min"])

sample["Priorita"] = (
    0.7*(sample["AI %"]/100) +
    0.2*(sample["Čeká min"].clip(upper=60)/60) +
    0.1*0.75
)

sample = sample.sort_values("Priorita", ascending=False)

st.dataframe(sample, use_container_width=True)

st.divider()

st.header("✅ Zpětná vazba radiologa")

fb = st.radio("Souhlasíte s AI?", ["ANO","NE"])

if st.button("Uložit feedback"):
    row = pd.DataFrame([[datetime.now(), fb]], columns=["čas","feedback"])
    file = "feedback.csv"

    if Path(file).exists():
        old = pd.read_csv(file)
        pd.concat([old,row]).to_csv(file,index=False)
    else:
        row.to_csv(file,index=False)

    st.success("Feedback uložen.")
