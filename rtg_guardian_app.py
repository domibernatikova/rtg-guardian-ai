
import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="GuardianRX Command Center",
    page_icon="🏥",
    layout="wide"
)
st.markdown("""
<style>

.main {
    background-color: #07111f;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
    color: white;
    text-align: center;
}

.subtitle {
    text-align: center;
    color: #9aa6b2;
    font-size: 18px;
    margin-bottom: 30px;
}

.metric-card {
    background: linear-gradient(135deg,#0f172a,#1e293b);
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #334155;
    box-shadow: 0 0 15px rgba(0,255,255,0.08);
}

.alert-card {
    background: linear-gradient(135deg,#7f1d1d,#450a0a);
    padding: 18px;
    border-radius: 16px;
    color:white;
    border-left: 6px solid #ef4444;
}

.success-card {
    background: linear-gradient(135deg,#052e16,#14532d);
    padding: 18px;
    border-radius: 16px;
    color:white;
    border-left: 6px solid #22c55e;
}

</style>
""", unsafe_allow_html=True)
# HLAVIČKA

st.title("🏥 GUARDIANRX COMMAND CENTER")
st.caption("AI operační centrum radiologie Moravskoslezského kraje")

# KPI

c1, c2, c3, c4 = st.columns(4)

c1.metric("🔴 Kritické případy", "8")
c2.metric("⏱ Průměrná čekací doba", "14 min")
c3.metric("📉 Zkrácení čekání", "43 %")
c4.metric("🛡 Patient Shield", "17")

st.info("""
23 radiologických pracovišť online.

AI právě monitoruje 159 snímků.

8 případů vyžaduje okamžitou kontrolu.
""")

st.divider()

# ANALÝZA RTG

st.header("🩻 Analýza RTG snímku")

uploaded = st.file_uploader(
    "Nahraj RTG snímek",
    type=["jpg", "jpeg", "png"]
)

if uploaded:

    st.image(uploaded, caption="Nahraný RTG snímek", width=350)

    ai_prob = st.slider(
        "Pravděpodobnost nálezu (%)",
        0,
        100,
        85
    )

    waiting = st.slider(
        "Čekací doba (min)",
        0,
        120,
        10
    )

    workload = st.slider(
        "Vytížení pracoviště (%)",
        0,
        100,
        75
    )

    ai_score = ai_prob / 100
    waiting_score = min(waiting / 60, 1)
    workload_score = workload / 100

    priority = (
        0.7 * ai_score +
        0.2 * waiting_score +
        0.1 * workload_score
    )

    if waiting > 60:
        st.error(
            "🛡 PATIENT SHIELD AKTIVOVÁN — pacient automaticky povýšen."
        )
        level = "🔴 KRITICKÁ"

    elif priority > 0.8:
        level = "🔴 KRITICKÁ"

    elif priority > 0.6:
        level = "🟠 VYSOKÁ"

    elif priority > 0.4:
        level = "🟡 STŘEDNÍ"

    else:
        level = "🟢 NÍZKÁ"

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Prioritní skóre",
            f"{priority:.2f}"
        )

    with col2:
        st.metric(
            "Zařazení",
            level
        )

    st.success(f"""
Pravděpodobnost nálezu: {ai_prob} %

Doporučení AI:
Prioritní kontrola radiologem.

Toto není diagnóza.
Finální rozhodnutí provádí radiolog.
""")

st.divider()

# FRONTA

st.header("📋 Inteligentní fronta radiologa")

sample = pd.DataFrame([
    ["P001", 96, 5],
    ["P002", 18, 70],
    ["P003", 81, 12],
    ["P004", 54, 22],
    ["P005", 92, 3],
    ["P006", 30, 65]
], columns=["Pacient", "AI %", "Čeká min"])

def status(ai, wait):

    if wait > 60:
        return "🛡 Patient Shield"

    if ai > 85:
        return "🔴 Kritický"

    if ai > 60:
        return "🟠 Vysoká"

    return "🟢 Rutinní"

sample["Status"] = sample.apply(
    lambda row: status(
        row["AI %"],
        row["Čeká min"]
    ),
    axis=1
)

sample["Priorita"] = (
    0.7 * (sample["AI %"] / 100)
    + 0.2 * (sample["Čeká min"].clip(upper=60) / 60)
    + 0.1 * 0.75
)

sample = sample.sort_values(
    "Priorita",
    ascending=False
)

st.dataframe(
    sample[
        ["Pacient", "AI %", "Čeká min", "Status"]
    ],
    use_container_width=True
)

st.divider()

# KRAJ

st.header("🗺 Stav pracovišť v kraji")

st.markdown("""
### FN Ostrava
🔴 Vytížení 95 %

### Karviná
🟢 Vytížení 62 %

### Opava
🟡 Vytížení 81 %

### Frýdek-Místek
🟢 Vytížení 58 %

### Doporučení AI
Přesměrovat nové popisy do Karviné.
""")

st.divider()

# PREDIKCE

st.header("📈 Predikce respirační zátěže")

pred = pd.DataFrame({
    "Okres": [
        "Karviná",
        "Ostrava",
        "Opava",
        "Bruntál"
    ],
    "Růst případů (%)": [
        18,
        12,
        5,
        8
    ]
})

st.bar_chart(
    pred.set_index("Okres")
)

st.divider()

# FEEDBACK

st.header("✅ Zpětná vazba radiologa")

fb = st.radio(
    "Souhlasíte s prioritizací AI?",
    ["ANO", "NE"]
)

if st.button("Uložit feedback"):

    row = pd.DataFrame(
        [[datetime.now(), fb]],
        columns=["čas", "feedback"]
    )

    file = "feedback.csv"

    if Path(file).exists():

        old = pd.read_csv(file)

        pd.concat(
            [old, row]
        ).to_csv(
            file,
            index=False
        )

    else:
        row.to_csv(
            file,
            index=False
        )

    st.success(
        "Feedback uložen."
    )

st.divider()

st.warning("""
AI není diagnostický nástroj.

Slouží pouze k prioritizaci fronty.

Finální rozhodnutí vždy provádí radiolog.
""")
