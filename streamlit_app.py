import streamlit as st
from groq import Groq
import os

st.title("conspiracy.chat.bot")

api_key = None
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("No API key found in Secrets")
    st.stop()

# show that key is loaded (safe)
st.caption(f"Key loaded: {api_key[:7]}...{api_key[-4:]} length {len(api_key)}")

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            answer = completion.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"REAL ERROR FROM GROQ: {e}")
            st.write("If it says invalid_api_key or 401, your key is bad. Go to https://console.groq.com/keys and make a NEW key, then put it in Streamlit Cloud > Settings > Secrets as:")
            st.code('GROQ_API_KEY = "gsk_your_new_key"')
