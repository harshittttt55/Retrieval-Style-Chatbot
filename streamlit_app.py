import streamlit as st
from datetime import datetime
from scripts.dataset_loader import load_qa_pairs, get_response

# -------------------------
# Load QA pairs
qa_pairs, qa_dict, questions_normalized = load_qa_pairs()

# -------------------------
# Page config & styling
st.set_page_config(page_title="Retrieval Chatbot", layout="wide")
st.markdown("""
<style>
body {
    background-color: #000000;
    color: white;
}
.stTextInput > div > div > input {
    background-color: #333333;
    color: white;
}
.stButton > button {
    background-color: #555555;
    color: white;
}
</style>
""", unsafe_allow_html=True)

st.title("Retrieval-Style Chatbot")

# -------------------------
# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []
if "suggestions" not in st.session_state:
    st.session_state.suggestions = []

# -------------------------
# Function to send a message
def send_message(msg=None):
    if msg is None:
        msg = st.session_state.input_text.strip()
    if not msg:
        return
    now = datetime.now().strftime("%H:%M")
    answer, suggestions = get_response(msg, qa_pairs, qa_dict, questions_normalized)

    st.session_state.history.append(("You", msg, now))
    st.session_state.history.append(("Assistant", answer, now))
    st.session_state.suggestions = suggestions

    st.session_state.input_text = ""  # clear input

# -------------------------
# Chat container
chat_container = st.container()
with chat_container:
    for sender, msg, timestamp in st.session_state.history:
        if sender == "You":
            st.markdown(
                f"<div style='background-color:gray; padding:10px; border-radius:15px; margin:5px 0; width:60%; float:right; box-shadow:1px 1px 5px #ccc'>{msg} <span style='font-size:10px; color:black; float:right'>{timestamp}</span></div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background-color:gray; padding:10px; border-radius:15px; margin:5px 0; width:60%; float:left; box-shadow:1px 1px 5px #ccc'>{msg} <span style='font-size:10px; color:black; float:right'>{timestamp}</span></div>",
                unsafe_allow_html=True
            )

# -------------------------
# Suggested questions
if st.session_state.suggestions:
    st.markdown("**You may also ask:**")
    cols = st.columns(len(st.session_state.suggestions))
    for i, s in enumerate(st.session_state.suggestions):
        def suggestion_callback(msg=s):
            send_message(msg)
        cols[i].button(s, key=f"suggestion_{i}_{hash(s)}", on_click=suggestion_callback)

# -------------------------
# Fixed input box at the bottom
st.markdown("<div style='position:fixed; bottom:0; width:100%; background-color:#000000; padding:10px 0; z-index:1000'></div>", unsafe_allow_html=True)
st.text_input("Type a message", key="input_text", placeholder="Type here...", on_change=send_message)
st.button("Send", on_click=send_message)
