import streamlit as st
import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse, urljoin
import random

st.set_page_config(page_title="AI Scanner", layout="wide")

tab1, tab2 = st.tabs(["🔗 Link Scanner", "🎥 Video Analyzer"])

# ===============================
# LINK SCANNER
# ===============================
with tab1:

    st.title("🔍 AI Digital Media Scanner")

    url = st.text_input("Enter Website URL")

    if st.button("🚀 Scan Website"):

        if not url:
            st.warning("Enter a URL first")
        else:
            if not url.startswith("http"):
                url = "https://" + url

            try:
                headers = {"User-Agent": "Mozilla/5.0"}
                response = requests.get(url, headers=headers, timeout=5)
                soup = BeautifulSoup(response.text, "html.parser")

                domain = urlparse(url).netloc

                try:
                    ip = socket.gethostbyname(domain)
                except:
                    ip = "Not Found"

                st.subheader("🌐 Website Info")
                st.write("Domain:", domain)
                st.write("IP Address:", ip)

                if soup.title:
                    st.write("Title:", soup.title.string)

                # Risk check
                risk = 0
                if url.startswith("http://"):
                    risk += 2
                if "-" in domain:
                    risk += 1
                if response.status_code != 200:
                    risk += 2

                st.subheader("🚨 Risk Level")

                if risk >= 4:
                    st.error("🔴 HIGH RISK")
                elif risk >= 2:
                    st.warning("🟡 MEDIUM RISK")
                else:
                    st.success("🟢 SAFE")

                # AI detection
                st.subheader("🤖 AI Content Check")

                text = soup.get_text().lower()
                keywords = ["chatgpt", "ai generated", "openai", "deepfake"]

                if any(k in text for k in keywords):
                    st.warning("⚠ Possible AI Generated Content")
                else:
                    st.success("No obvious AI content detected")

                # Show images
                st.subheader("🖼 Images")

                images = soup.find_all("img")
                st.write("Total Images:", len(images))

                count = 0
                for img in images:
                    if count >= 3:
                        break
                    src = img.get("src")
                    if src:
                        full = urljoin(url, src)
                        st.image(full, width=250)
                        count += 1

            except:
                st.error("Unable to scan this website")

# ===============================
# VIDEO ANALYZER
# ===============================
with tab2:

    st.title("🎥 Deepfake & AI Video Detector")

    option = st.radio("Choose Option", ["Upload Video", "Video URL"])

    video_file = None
    video_url = None

    if option == "Upload Video":
        video_file = st.file_uploader("Upload Video", type=["mp4", "mov", "webm"])
    else:
        video_url = st.text_input("Enter Video URL")

    if st.button("👁 Analyze Video"):

        if not video_file and not video_url:
            st.warning("Upload video or enter URL")
        else:
            score = random.randint(1, 100)

            st.subheader("🔬 Deepfake Analysis")
            st.progress(score)

            if score > 70:
                st.error(f"🔴 High Deepfake Risk ({score}%)")
            elif score > 40:
                st.warning(f"🟡 Medium Risk ({score}%)")
            else:
                st.success(f"🟢 Low Risk ({score}%)")

            st.info("Demo AI model (simulated result)")
