import streamlit as st
from groq import Groq
import os

st.title("conspiracy.chat.bot")
st.write("If you see this, the install worked!")

# get key
api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
if not api_key:
    st.warning("App is installed! Now just add your GROQ_API_KEY in Streamlit Secrets.")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    st.write(f"{m['role']}: {m['content']}")

prompt = st.text_input("Ask something")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    chat = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    answer = chat.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": answer})
    st.rerun()
