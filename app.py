import streamlit as st
import os
from dotenv import load_dotenv
from assistant import GeminiAssistant

# Load environment variables
load_dotenv(override=True)

# App Configuration
st.set_page_config(page_title="Gemini Assistant", layout="centered")

def initialize_assistant():
    """Initializes the Gemini assistant."""
    assistant_name = os.getenv("ASSISTANT_NAME", "Gemini Assistant")
    api_key = os.getenv("GEMINI_API_KEY", "")
    
    if "assistant" not in st.session_state:
        st.session_state.assistant = GeminiAssistant(name=assistant_name, api_key=api_key)
        st.session_state.history = []

def render_chat():
    """Renders the chat interface."""
    assistant = st.session_state.assistant
    
    st.title(f"✨ {assistant.name}")
    st.markdown("Sizning 100% mukammal ishlaydigan aqlli yordamchingiz.")
    
    if assistant.error:
        st.error(assistant.error)
        
    # File uploader
    uploaded_files = st.file_uploader(f"Fayl yuklash (Rasmlar, PDF hujjatlar yoki Audio)", 
                                      accept_multiple_files=True,
                                      key="uploader")
                                      
    # Display history
    for message in st.session_state.history:
        with st.chat_message(message["role"]):
            for part in message["parts"]:
                 if isinstance(part, str):
                     st.markdown(part)
                 else:
                     st.info(f"Biriktirilgan fayl: {part['name']}")

    # Chat input
    if prompt := st.chat_input("Xabar yozing..."):
        
        # User message
        st.session_state.history.append({
            "role": "user", 
            "parts": [prompt] + [{"name": f.name} for f in uploaded_files]
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
            for f in uploaded_files:
                 st.info(f"Biriktirilgan fayl: {f.name}")
                 
        # Assistant response
        with st.chat_message("model"):
            chat_session = assistant.get_chat_session(st.session_state.history[:-1])
            stream = assistant.send_message_stream(chat_session, prompt, files=uploaded_files)
            response = st.write_stream(stream)
            
        st.session_state.history.append({"role": "model", "parts": [response]})
        st.rerun()

    # Clear chat button
    st.divider()
    if st.button("Suhbat tarixini tozalash", key="clear"):
        st.session_state.history = []
        st.rerun()

def main():
    initialize_assistant()
    render_chat()

if __name__ == "__main__":
    main()
