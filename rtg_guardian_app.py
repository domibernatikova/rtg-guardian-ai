import streamlit as st
import requests

st.set_page_config(page_title="GuardianRX AI", layout="wide")

st.title("🏥 GuardianRX AI")
st.subheader("AI analýza RTG hrudníku")

uploaded = st.file_uploader(
    "Nahraj RTG snímek",
    type=["jpg", "jpeg", "png"]
)

if uploaded:

    st.image(uploaded, caption="Nahraný RTG snímek")

    API_URL = "https://api-inference.huggingface.co/models/lxyuan/vit-xray-pneumonia-classification"

    headers = {
        "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
    }

    with st.spinner("AI analyzuje RTG..."):

        response = requests.post(
            API_URL,
            headers=headers,
            data=uploaded.getvalue(),
            timeout=60
        )

    st.write("Status:", response.status_code)

    try:
        st.json(response.json())
    except Exception:
        st.write(response.text)
