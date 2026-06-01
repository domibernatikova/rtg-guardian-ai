import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(
    page_title="GuardianRX Command Center",
    page_icon="🏥",
    layout="wide"
)

# ===== DESIGN =====

st.markdown("""
<style>

.stApp {
    background: #07111f;
}

.main-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    text-align: center;
}

.sub-title {
    text-align: center;
    color: #94a3b8;
    font-size: 18px;
    margin-bottom: 25px;
}

.live-box {
    background: linear-gradient(135deg,#991b1b,#450a0a);
    padding: 20px;
    border-radius: 18px;
    color: white;
    margin-bottom: 20px;
}

.section-box {
    background: #0f172a;
    padding: 20px;
    border-radius: 18px;
    border: 1px solid #1e293b;
}

</style>
""", unsafe_allow_html=True)

# ===== HLAVIČKA =====

st.markdown("""
<div class="main-title">
🏥 GUARDIANRX COMMAND CENTER
</div>

<div class="sub-title">
AI operační centrum radiologie Moravskoslezského kraje
</div>
""", unsafe_allow_html=True)

# ===== KPI =====

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric("🔴 Kritické případy", "8")

with k2:
    st.metric("⏱ Čekací doba", "14 min")

with k3:
    st.metric("📉 Zrychlení", "43 %")

with k4:
    st.metric("🛡 Shield zásahy", "17")

# ===== LIVE STATUS =====

st.markdown("""
<div class="live-box">
<h3>🔴 LIVE STATUS</h3>

23 radiologických pracovišť online<br>
159 aktivních snímků ve frontách<br>
8 případů vyžaduje okamžitou kontrolu
</div>
""", unsafe_allow_html=True)

# ===== ANALÝZA RTG =====

st.header("🩻 Analýza RTG snímku")

uploaded = st.file_uploader(
    "Nahraj RTG snímek",
    type=["jpg", "jpeg", "png"]
)

if uploaded:

    col1, col2 = st.columns([1,1])

    with col1:
        st.image(uploaded, caption="Nahraný RTG snímek")

    with col2:

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
            15
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
            st.error("🛡 PATIENT SHIELD AKTIVOVÁN")
            level = "🔴 KRITICKÁ"

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

        st.success(f"""
Pravděpodobnost nálezu: {ai_prob} %

Doporučení:
Prioritní kontrola radiologem.

Toto není diagnóza.
Finální rozhodnutí provádí radiolog.
""")

st.divider()

# ===== FRONTA =====

st.header("📋 Inteligentní fronta radiologa")

sample = pd.DataFrame([
    ["P001", 96, 5],
    ["P002", 18, 70],
    ["P003", 81, 12],
    ["P004", 54, 22],
    ["P005", 92, 3],
    ["P006", 30, 65],
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
    0.7*(sample["AI %"]/100)
    + 0.2*(sample["Čeká min"].clip(upper=60)/60)
    + 0.1*0.75
)

sample = sample.sort_values(
    "Priorita",
    ascending=False
)

st.dataframe(
    sample[
        ["Pacient","AI %","Čeká min","Status"]
    ],
    use_container_width=True
)

st.info("""
🛡 Patient Shield:
Pacienti čekající déle než 60 minut jsou automaticky
eskalováni bez ohledu na predikci AI.
""")

st.divider()

# ===== KRAJ =====

st.header("🗺 Krajské operační centrum")

c1, c2, c3 = st.columns(3)

with c1:
    st.error("FN Ostrava\n\n95 % kapacity")

with c2:
    st.success("Karviná\n\n62 % kapacity")

with c3:
    st.warning("Opava\n\n81 % kapacity")

st.markdown("""
### Doporučení AI

Přesměrovat nové popisy RTG z FN Ostrava do Karviné.

Odhadované zkrácení čekací doby: **22 %**
""")

st.divider()

# ===== PREDIKCE =====

st.header("📈 Predikce respirační zátěže")

pred = pd.DataFrame({
    "Okres": [
        "Karviná",
        "Ostrava",
        "Opava",
        "Bruntál"
    ],
    "Nárůst případů (%)": [
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

# ===== FEEDBACK =====

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

    st.success("Feedback uložen.")

st.divider()

st.warning("""
⚠️ AI není diagnostický nástroj.

Slouží pouze k prioritizaci fronty.

Finální rozhodnutí vždy provádí radiolog.
""")
