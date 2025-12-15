import os

# Disable Streamlit's module watcher for large libraries like torch
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"

import streamlit as st


import base64


st.set_page_config(page_title="GRAND SONIC JOURNEY", page_icon="🎶", layout="wide")

# Path to your image
current_dir = os.path.dirname(__file__)
bg_image_path = os.path.join(current_dir, "pages", "images", "logo.jpg")

# Convert image to base64
def get_base64_of_bin_file(bin_file):
    with open(bin_file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

bg_base64 = get_base64_of_bin_file(bg_image_path)

# Inject CSS for background
st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_base64}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# App content
st.title("🎶 Musical Multiverse")
st.write("Recommend • Lyrics • Instrumental • Compose")
st.sidebar.success("Select a page from the Pages menu")
