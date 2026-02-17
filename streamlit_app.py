import streamlit as st
from google import genai
from google.genai.types import (
    GenerateContentConfig, ThinkingConfig, Tool, GoogleSearch, Content, Part
)

# ------------------------------
# Page Config
# ------------------------------
st.set_page_config(page_title="Project Alyssa", page_icon="💼")
st.title("Project Alyssa")
st.caption("Filthy-mouthed British financial genius")

# ------------------------------
# API Setup
# ------------------------------
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    persona_text = st.secrets["PERSONA_TEXT"]
    client = genai.Client(api_key=api_key)
except KeyError:
    st.error("GEMINI_API_KEY or PERSONA_TEXT missing from Streamlit secrets!")
    st.stop()

# ------------------------------
# Chat History
# ------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ------------------------------
# User Input
# ------------------------------
if prompt := st.chat_input("Ask your financial advisor..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()

        try:
            contents = [Content(role="user", parts=[Part.from_text(prompt)])]

            tools = [Tool(googleSearch=GoogleSearch())]

            config = GenerateContentConfig(
                thinking_config=ThinkingConfig(thinking_level="HIGH"),
                tools=tools,
                response_mime_type="application/json",
                system_instruction=[Part.from_text(persona_text)]
            )

            # Stream response to UI
            full_response = ""
            for chunk in client.models.generate_content_stream(
                model="gemini-3-pro-preview",
                contents=contents,
                config=config
            ):
                message_placeholder.markdown(chunk.text)
                full_response += chunk.text

            st.session_state.messages.append({"role": "assistant", "content": full_response})

        except Exception as e:
            st.error(f"Gemini 3 Pro Error: {e}")
