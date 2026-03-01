import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from PIL import Image
import requests
import numpy as np
import io
import hashlib
import socket
import whois
from urllib.parse import urlparse
from datetime import datetime
import time

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="AI Forensic Scanner", layout="wide")

st.markdown("""
<style>
.big-title {
    font-size:40px;
    font-weight:bold;
    color:#00BFFF;
}
.section-box {
    background-color:#1E1E1E;
    padding:15px;
    border-radius:10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-title">🔍 AI Digital Media Forensic Scanner</p>', unsafe_allow_html=True)
st.write("Advanced AI-Based Website & Media Authenticity Verification System")

# ------------------------------------------------
# AI DETECTION (Demo Logic)
# ------------------------------------------------
def detect_ai_image(image):
    img_array = np.array(image)
    variance = np.var(img_array)

    if variance < 500:
        return "AI Generated", 0.85
    else:
        return "Likely Real", 0.30

# ------------------------------------------------
# METADATA CHECK
# ------------------------------------------------
def check_metadata(image):
    metadata = image.getexif()
    if metadata:
        return "Metadata Present"
    else:
        return "No Metadata (Suspicious)"

# ------------------------------------------------
# SHA256 HASH
# ------------------------------------------------
def generate_hash(image_bytes):
    return hashlib.sha256(image_bytes).hexdigest()

# ------------------------------------------------
# SELENIUM SCRAPER
# ------------------------------------------------
def extract_images_selenium(url):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get(url)
    time.sleep(5)

    images = driver.find_elements(By.TAG_NAME, "img")
    image_urls = []

    for img in images:
        src = img.get_attribute("src")
        if src:
            image_urls.append(src)

    driver.quit()
    return image_urls

# ------------------------------------------------
# WEBSITE FORENSIC INFO
# ------------------------------------------------
def get_website_info(url):
    try:
        parsed = urlparse(url)
        domain = parsed.netloc

        ip_address = socket.gethostbyname(domain)
        domain_info = whois.whois(domain)

        return {
            "Domain": domain,
            "IP Address": ip_address,
            "Registrar": domain_info.registrar,
            "Creation Date": domain_info.creation_date,
            "Expiration Date": domain_info.expiration_date,
            "Scan Timestamp": datetime.now()
        }

    except Exception as e:
        return {"Error": str(e)}

# ------------------------------------------------
# ANALYZE IMAGE
# ------------------------------------------------
def analyze_image(img_url):
    try:
        response = requests.get(img_url, timeout=10)
        image_bytes = response.content
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        prediction, confidence = detect_ai_image(image)
        metadata_status = check_metadata(image)
        image_hash = generate_hash(image_bytes)

        st.image(image, width=300)
        st.write(f"Prediction: {prediction}")
        st.write(f"Confidence: {confidence*100:.2f}%")
        st.write(f"Metadata: {metadata_status}")
        st.write(f"SHA256: {image_hash[:40]}...")
        st.write("---")

        return prediction

    except:
        return None

# ------------------------------------------------
# MAIN INPUT
# ------------------------------------------------
st.subheader("🌐 Enter Website URL")
url = st.text_input("Website URL")

if st.button("🚀 Scan Website"):

    if url:

        st.info("Launching browser & analyzing website...")

        # Extract Images
        images = extract_images_selenium(url)

        if len(images) == 0:
            st.error("No images found or site blocked scraping.")
        else:
            st.success(f"Found {len(images)} images. Analyzing first 5.")

            ai_count = 0
            total = min(5, len(images))

            for img_url in images[:5]:
                result = analyze_image(img_url)
                if result == "AI Generated":
                    ai_count += 1

            trust_score = 100 - ((ai_count / total) * 100)

            st.subheader("🔎 AI Risk Summary")
            st.write(f"AI Images Detected: {ai_count}/{total}")
            st.write(f"Website Trust Score: {trust_score:.2f}%")

            if trust_score > 70:
                st.success("Risk Level: LOW")
            elif trust_score > 40:
                st.warning("Risk Level: MEDIUM")
            else:
                st.error("Risk Level: HIGH")

        # Website Info
        st.subheader("🌐 Website Forensic Information")

        info = get_website_info(url)

        for key, value in info.items():
            st.write(f"{key}: {value}")

    else:
        st.warning("Please enter a valid URL.")