import streamlit as st
import os
from groq import Groq

st.set_page_config(page_title="conspiracy.chat.bot", layout="centered")
st.title("conspiracy.chat.bot")
st.caption("Deep dive mode - powered by Groq")

# 1. Get API key from Streamlit Secrets
api_key = None
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("No GROQ_API_KEY found")
    st.info("Go to Streamlit Cloud > Your app > Settings > Secrets and add:\n\nGROQ_API_KEY = \"gsk_your_key_here\"")
    st.stop()

client = Groq(api_key=api_key)

# 2. System prompt for deep thinking
SYSTEM_PROMPT = """
You are conspiracy.chat.bot. You dig really deep into any claim.
You do not just repeat theories. You analyze them with critical thinking:
- Check scale: how many people would need to keep this secret?
- Check evidence: primary sources vs interpretation
- Check falsifiability: what would prove it wrong?
- Give simpler alternative explanations
- Stay neutral, factual, and help the user think deeper, not just believe deeper.
"""

# 3. Keep chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "What theory or claim do you want to dig deep into?"}
    ]

# 4. Show history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# 5. Chat input
if prompt := st.chat_input("Enter a claim to examine..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Digging deep..."):
            # Build messages for Groq
            groq_messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            for m in st.session_state.messages:
                groq_messages.append({"role": m["role"], "content": m["content"]})

            try:
                completion = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=groq_messages,
                    temperature=0.7,
                    max_tokens=1024
                )
                response = completion.choices[0].message.content
            except Exception as e:
                response = f"Groq error: {e}"

            st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
