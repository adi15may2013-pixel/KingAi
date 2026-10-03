import streamlit as st
from groq import Groq

st.set_page_config(page_title="King AI", page_icon="👑")
st.markdown("<h2 style='text-align: center;'>👑 King AI Assistant</h2>", unsafe_allow_html=True)
st.caption("24/7 Cloud AI Assistant")

CREATOR_NAME = "Aaditya Singh"
CREATOR_BIO = "a smart student of Class 8"

# API Key Streamlit Cloud के Secrets से आएगी
api_key = st.secrets.get("GROQ_API_KEY", "")
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": f"Hello! I am King AI, created by {CREATOR_NAME}. How can I help you today?"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

user_input = st.chat_input("Ask King AI anything...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # क्रिएटर का नाम सुरक्षित रखने के लिए
    creator_keywords = ["who developed", "who created", "who made", "who is your developer", "kisne banaya", "tumhe kisne banaya"]
    is_creator_query = any(k in user_input.lower() for k in creator_keywords)

    with st.chat_message("assistant"):
        if is_creator_query:
            reply = f"I was created and developed by {CREATOR_NAME}, {CREATOR_BIO}."
            st.write(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
        else:
            with st.spinner("Thinking..."):
                try:
                    system_prompt = f"You are King AI, created solely by {CREATOR_NAME}, {CREATOR_BIO}. If asked in Hindi, reply in Hindi. Otherwise reply in English."
                    response = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ]
                    )
                    reply = response.choices[0].message.content
                    st.write(reply)
                    st.session_state.messages.append({"role": "assistant", "content": reply})
                except Exception as e:
                    st.error(f"Error: {e}")