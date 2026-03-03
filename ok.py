import streamlit as st
import os

# --- PAGE CONFIG ---
st.set_page_config(page_title="Office Share & Chat", layout="wide")

# Create a folder for shared files if it doesn't exist
UPLOAD_DIR = "office_shared_files"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# --- SIDEBAR: FILE SHARING ---
with st.sidebar:
    st.header("📁 File Share")
    uploaded_file = st.file_uploader("Upload a file to the office folder", type=["pdf", "docx", "png", "jpg", "xlsx"])
    
    if uploaded_file is not None:
        # Save the file locally
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        st.success(f"Uploaded: {uploaded_file.name}")

    st.divider()
    st.subheader("Shared Files:")
    files = os.listdir(UPLOAD_DIR)
    for file in files:
        st.write(f"📄 {file}")

# --- MAIN AREA: CHAT INTERFACE ---
st.title("💬 Office Chat")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Type a message to your friend..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # (Later, we will add the code here to send this to your friend's screen!)
    response = f"Echo: {prompt}" 
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})