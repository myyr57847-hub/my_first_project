import streamlit as st
import os
from datetime import datetime

# --- 1. SETUP FILTERS & PATHS ---
# Using a relative path so it works on both your PC and the Cloud
UPLOAD_DIR = "shared_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- 2. PAGE CONFIG ---
st.set_page_config(page_title="Dharam Office Hub", layout="wide", page_icon="🚀")

st.title("🚀 Office Chat & File Share")
st.markdown("---")

# --- 3. SIDEBAR: FILE MANAGEMENT ---
with st.sidebar:
    st.header("📁 File Cabinet")
    uploaded_file = st.file_uploader("Upload a file to share with friends", type=None)
    
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded: {uploaded_file.name}")

    st.divider()
    st.subheader("Shared Files List")
    
    # List all files and add a download button for each
    all_files = os.listdir(UPLOAD_DIR)
    if not all_files:
        st.info("No files uploaded yet.")
    for filename in all_files:
        file_path = os.path.join(UPLOAD_DIR, filename)
        with open(file_path, "rb") as f:
            st.download_button(
                label=f"⬇️ Download {filename}",
                data=f,
                file_name=filename,
                key=filename # Unique key for Streamlit
            )

# --- 4. MAIN CHAT AREA ---
# We use st.session_state to keep the chat alive during your current session
if "messages" not in st.session_state:
    st.session_state.messages = []

# Ask for user name
user_name = st.text_input("Enter your Name:", value="User", key="user_name")

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(f"**{message['name']}**: {message['content']}")

# Chat input logic
if prompt := st.chat_input("Write a message..."):
    # Add user message to state
    st.session_state.messages.append({"role": "user", "name": user_name, "content": prompt})
    
    # Immediately show the message
    st.rerun()