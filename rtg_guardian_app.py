import streamlit as st
import requests

st.set_page_config(
    page_title="GuardianRX AI",
    layout="wide"
)

st.title("🏥 GuardianRX AI")
st.subheader("Test propojení s Hugging Face")

uploaded = st.file_uploader(
    "Nahraj obrázek",
    type=["jpg", "jpeg", "png"]
)

if uploaded:

    st.image(uploaded)

    API_URL = "https://api-inference.huggingface.co/models/microsoft/resnet-50"

    headers = {
        "Authorization": f"Bearer {st.secrets['HF_TOKEN']}"
    }

    with st.spinner("Analyzuji obrázek..."):

        try:

            response = requests.post(
                API_URL,
                headers=headers,
                data=uploaded.getvalue(),
                timeout=60
            )

            st.success("Požadavek odeslán")

            st.write("Status code:")
            st.write(response.status_code)

            st.write("Odpověď:")

            try:
                st.json(response.json())
            except:
                st.write(response.text)

        except Exception as e:
            st.error(str(e))
