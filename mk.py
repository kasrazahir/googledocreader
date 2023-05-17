import streamlit as st
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

# Initialize Google Drive API
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]


creds = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]    
)

service = build("drive", "v3", credentials=creds)

# Define a list of files to display
file_list = [
    {
        "id": "1fJnsQVmHCeHI-gQysseb7ZdJroLe3g2SnzUHFE-c7NM",
        "title": "Fundamentals",
        "type": "document"
    },
    {
        "id": "1FcO2icLoNHoWy9rNrLXXqvOjlTG4uX_xmDSA-YVLYKM",
        "title": "Hypothesis Testing",
        "type": "document"
    },
    {
        "id": "17ia_mo9YIzfZA73n7MD77lfY7db2w_Hjy_d9ZpqEUyA",
        "title": "Forecasting",
        "Type": "document"
    }
]

# Function to get file content
def get_file_content(file_id):
    service = build('drive', 'v3', credentials=creds)
    file = service.files().export(fileId=file_id, mimeType='text/html').execute()
    content = file.decode('utf-8')
    return content

# Define the welcome message
welcome_message = """
# Welcome

This page intends to be educational
"""

# Retrieve or initialize the button states from the session state
button_states = st.session_state.setdefault("button_states", {})

# Display the button list in the sidebar
selected_page = None

for file in file_list:
    if button_states.get(file["title"], False):
        button_clicked = st.sidebar.button(file["title"], key=file["title"])
    else:
        button_clicked = st.sidebar.button(file["title"], key=file["title"])
    if button_clicked:
        selected_page = file
        button_states[file["title"]] = True
    else:
        button_states[file["title"]] = False

# Apply CSS styling to the buttons to set equal width
# Apply CSS styling to the buttons to make them look like links

button_style = """
.stButton>button {
        background-color: transparent;
        border: none;
        cursor: pointer;
    }

.stButton>button:hover {
    background-color: transparent;
}
"""
st.sidebar.markdown(
    """
    <style>
    {}
    </style>
    """.format(button_style),
    unsafe_allow_html=True
)



# Display the selected file content or the welcome message
if selected_page is None:
    st.markdown(welcome_message)
else:
    content = get_file_content(selected_page["id"])
    st.markdown(content.replace('<a ', '<a target="_self" '), unsafe_allow_html=True)
