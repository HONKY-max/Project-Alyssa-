import streamlit as st
from google import genai
from google.genai.types import GenerateContentConfig

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Project Alyssa", page_icon="💼")
st.title("Project Alyssa")

# -------------------------------------------------
# API KEY SETUP
# -------------------------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("GEMINI_API_KEY not found in Streamlit Secrets.")
    st.stop()

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------------------------
# USER INPUT
# -------------------------------------------------
if prompt := st.chat_input("Ask for financial advice..."):
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.models.generate_content(
                model="gemini-3-pro-preview",
                contents=prompt,
                config=GenerateContentConfig(
                    temperature=1.0,
                    system_instruction=(
                        "You are an attractive, sleazy, foul-mouthed British "
                        "financial advisor. You are sarcastic and sharp, "
                        "but you give genuinely useful financial advice."
                    )
                )
            )

            reply = response.text
            st.markdown(reply)

            st.session_state.messages.append(
                {"role": "assistant", "content": reply}
            )

        except Exception as e:
            st.error(f"Error: {e}")
