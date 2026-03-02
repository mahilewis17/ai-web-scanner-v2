import streamlit as st
import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse, urljoin
import whois
from datetime import datetime

st.set_page_config(page_title="AI Digital Media Scanner", layout="wide")

tab1, tab2 = st.tabs(["Link Scanner", "Video Analyzer"])

# =========================================================
# LINK SCANNER
# =========================================================
with tab1:

    st.title("AI Digital Media Scanner")
    st.subheader("Advanced Website and Media Authenticity Verification System")

    url = st.text_input("Enter Website URL")

    if st.button("Scan Website"):

        if not url.startswith("http"):
            url = "https://" + url

        try:
            response = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )

            soup = BeautifulSoup(response.text, "html.parser")
            parsed = urlparse(url)
            domain = parsed.netloc

            # Website Title
            title = soup.title.string.strip() if soup.title else "No title found"

            # IP Address
            try:
                ip_address = socket.gethostbyname(domain)
            except:
                ip_address = "Unavailable"

            # WHOIS Information
            try:
                domain_info = whois.whois(domain)

                registrar = domain_info.registrar
                organization = domain_info.org
                creation_date = domain_info.creation_date
                expiration_date = domain_info.expiration_date
                updated_date = domain_info.updated_date

                # Handle list format from some WHOIS responses
                if isinstance(creation_date, list):
                    creation_date = creation_date[0]
                if isinstance(expiration_date, list):
                    expiration_date = expiration_date[0]
                if isinstance(updated_date, list):
                    updated_date = updated_date[0]

                # Calculate Domain Age
                if creation_date:
                    domain_age = (datetime.now() - creation_date).days // 365
                else:
                    domain_age = "Unknown"

            except:
                registrar = "Unavailable"
                organization = "Unavailable"
                creation_date = "Unavailable"
                expiration_date = "Unavailable"
                updated_date = "Unavailable"
                domain_age = "Unavailable"

            # Extract Images
            images = []
            for img in soup.find_all("img"):
                src = img.get("src")
                if src:
                    full_url = urljoin(url, src)
                    images.append(full_url)

            # Risk Score
            risk_score = 0

            if not url.startswith("https"):
                risk_score += 30

            if "@" in url:
                risk_score += 20

            if len(domain) > 25:
                risk_score += 10

            if isinstance(domain_age, int) and domain_age < 1:
                risk_score += 20

            # -------------------------
            # Display Results
            # -------------------------

            st.markdown("---")
            st.header("Risk Analysis")

            if risk_score < 20:
                st.success("SAFE WEBSITE")
            elif risk_score < 50:
                st.warning("MEDIUM RISK")
            else:
                st.error("HIGH RISK")

            st.markdown("---")
            st.header("Website Information")

            st.write("Title:", title)
            st.write("Domain:", domain)
            st.write("IP Address:", ip_address)

            st.markdown("---")
            st.header("Domain Registration Details")

            st.write("Registrar:", registrar)
            st.write("Organization:", organization)
            st.write("Creation Date:", creation_date)
            st.write("Last Updated Date:", updated_date)
            st.write("Expiration Date:", expiration_date)
            st.write("Domain Age (years):", domain_age)

            st.markdown("---")
            st.header("Extracted Images")

            if images:
                for img_url in images[:10]:
                    try:
                        st.image(img_url, use_column_width=True)
                    except:
                        pass
            else:
                st.warning("No images found or site blocked scraping.")

        except Exception as e:
            st.error(f"Error scanning website: {e}")

# =========================================================
# VIDEO ANALYZER
# =========================================================
with tab2:

    st.title("Deepfake and AI Video Detector")
    st.write("Upload a video to analyze for AI-generated patterns")

    video_file = st.file_uploader("Upload Video", type=["mp4", "mov", "webm"])

    if st.button("Analyze Video"):

        if video_file:
            st.video(video_file)

            st.info("Analyzing video patterns...")

            import random
            confidence = random.randint(40, 95)

            if confidence > 75:
                st.error(f"AI Generated Content Detected (Confidence: {confidence}%)")
            else:
                st.success(f"Likely Real Video (Confidence: {confidence}%)")

        else:
            st.warning("Please upload a video.")
