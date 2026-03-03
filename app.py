import streamlit as st
import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse, urljoin
import os
from PIL import Image
import cv2
import numpy as np

st.set_page_config(page_title="AI Digital Risk Scanner", layout="centered")

st.title("AI Digital Media Forensic Scanner")
st.markdown("---")

# ---------------- WEBSITE SCANNER ----------------

url = st.text_input("Enter Website URL")

if st.button("Scan Website", use_container_width=True):

    if not url:
        st.warning("Please enter a website URL")
    else:

        if not url.startswith("http"):
            url = "https://" + url

        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            response = requests.get(url, headers=headers, timeout=5)
            soup = BeautifulSoup(response.text, "html.parser")

            parsed = urlparse(url)
            domain = parsed.netloc

            try:
                ip_address = socket.gethostbyname(domain)
            except:
                ip_address = "Unable to fetch"

            st.markdown("Website Information")
            st.write("Domain:", domain)
            st.write("IP Address:", ip_address)

            if soup.title:
                st.write("Title:", soup.title.string)

            # Risk analysis
            risk_score = 0

            if url.startswith("http://"):
                risk_score += 2

            if len(domain) > 30:
                risk_score += 1

            if domain.count("-") > 2:
                risk_score += 1

            if response.status_code != 200:
                risk_score += 2

            st.markdown("Risk Analysis")

            if risk_score >= 4:
                st.error("High Risk Website")
            elif risk_score >= 2:
                st.warning("Medium Risk Website")
            else:
                st.success("Safe Website")

        except:
            st.error("Unable to scan this website.")


# ---------------- FILE UPLOAD DEEPFAKE CHECK ----------------

st.markdown("---")
st.subheader("Upload Media for AI / Deepfake Detection")

uploaded_file = st.file_uploader(
    "Upload image, video or audio file",
    type=["jpg", "jpeg", "png", "mp4", "mp3"]
)

if uploaded_file is not None:

    file_type = uploaded_file.type
    file_name = uploaded_file.name.lower()

    st.write("File Name:", uploaded_file.name)
    st.write("File Type:", file_type)

    # Display media
    if "image" in file_type:
        image = Image.open(uploaded_file)
        st.image(image, use_column_width=True)

    elif "video" in file_type:
        st.video(uploaded_file)

    elif "audio" in file_type:
        st.audio(uploaded_file)

    if st.button("Analyze Media"):

        deepfake_score = 0

        # Simple filename check
        suspicious_words = ["ai", "generated", "deepfake", "synthetic"]

        if any(word in file_name for word in suspicious_words):
            deepfake_score += 2

        # Basic image noise detection
        if "image" in file_type:
            image_array = np.array(image)
            variance = np.var(image_array)

            if variance < 50:  # very smooth images often AI
                deepfake_score += 1

        # Final Result
        if deepfake_score >= 2:
            st.error("High Probability of AI Generated / Deepfake Media")
        elif deepfake_score == 1:
            st.warning("Possible AI Manipulated Media")
        else:
            st.success("No Strong AI Manipulation Indicators Found")
