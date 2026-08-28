import streamlit as st

st.title("conspiracy.chat.bot - Deep Dive Mode")

theory = st.text_input("Enter a claim you want to examine:")

if theory:
    st.subheader("Deep analysis framework")
    st.markdown(f"""
    **Claim:** {theory}
    
    **1. Scale Check:** How many people would need to be involved and silent?
    **2. Source Check:** Is this from primary evidence or secondary interpretation?
    **3. Falsifiability:** What evidence would prove this *wrong*? Does that evidence exist?
    **4. Alternative:** What is the non-conspiracy explanation?
    """)
