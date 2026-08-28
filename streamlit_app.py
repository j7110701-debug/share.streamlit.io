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
    st.error("Add GROQ_API_KEY in Secrets")
    st.stop()

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
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a deep dive analyst."},
                {"role": "user", "content": prompt}
            ]
        )
        answer = completion.choices[0].message.content
        st.markdown(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
