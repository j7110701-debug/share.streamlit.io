import streamlit as st
from groq import Groq
import os
import streamlit.components.v1 as components

st.title("conspiracy.chat.bot")

api_key = None
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("No key in Secrets")
    st.stop()

client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

def text_to_speech(text):
    """Convert text to speech using browser's native Web Speech API"""
    # Escape single quotes and newlines for JavaScript
    safe_text = text.replace("'", "\\'").replace("\n", " ")
    components.html(f"""
        <script>
            const utterance = new SpeechSynthesisUtterance('{safe_text}');
            utterance.rate = 1;
            utterance.pitch = 1;
            window.speechSynthesis.speak(utterance);
        </script>
    """, height=0)

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant":
            # Add speak button for assistant messages
            col1, col2 = st.columns([1, 10])
            with col1:
                st.button("🔊", key=f"speak_{id(m)}", on_click=text_to_speech, args=(m["content"],), help="Read aloud")

if prompt := st.chat_input("Ask something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # try newest models in order
        for model_name in ["openai/gpt-oss-20b", "llama-3.3-70b-versatile", "llama-3.1-8b-instant"]:
            try:
                st.write(f"Trying {model_name}...")
                completion = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt}]
                )
                answer = completion.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
                
                # Auto-play TTS for new responses
                text_to_speech(answer)
                
                break
            except Exception as e:
                st.error(f"{model_name} failed: {e}")
                continue
