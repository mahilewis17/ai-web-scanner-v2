import streamlit as st
import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse

st.set_page_config(page_title="AI Web Scanner", layout="wide")

st.title("🔍 AI Digital Media Forensic Scanner")
st.subheader("Advanced AI-Based Website & Media Authenticity Verification System")

url = st.text_input("Enter Website URL")

if st.button("🚀 Scan Website"):

    if not url.startswith("http"):
        url = "https://" + url

    try:
        # Add browser-like headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
        }

        st.info("Analyzing website...")

        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        st.success("Website Loaded Successfully ✅")

        # --------------------
        # Website Title
        # --------------------
        st.markdown("## 🌐 Website Information")

        if soup.title:
            st.write("**Title:**", soup.title.string)
        else:
            st.write("No title found.")

        # --------------------
        # Domain & IP Info
        # --------------------
        parsed_url = urlparse(url)
        domain = parsed_url.netloc

        try:
            ip_address = socket.gethostbyname(domain)
        except:
            ip_address = "Unable to fetch IP"

        st.write("**Domain:**", domain)
        st.write("**IP Address:**", ip_address)

        # --------------------
        # Extract Images
        # --------------------
        st.markdown("## 🖼 Images Found")

        images = soup.find_all("img")

        if images:
            for img in images[:10]:  # Limit to first 10 images
                img_url = img.get("src")

                if img_url:
                    if img_url.startswith("//"):
                        img_url = "https:" + img_url
                    elif img_url.startswith("/"):
                        img_url = url + img_url

                    st.image(img_url, width=300)
        else:
            st.warning("No images found or site blocked scraping.")

        # --------------------
        # Extract Links
        # --------------------
        st.markdown("## 🔗 Links Found")

        links = soup.find_all("a", href=True)

        if links:
            for link in links[:20]:  # Limit to first 20 links
                st.write(link["href"])
        else:
            st.write("No links found.")

    except Exception as e:
        st.error(f"Error scanning website: {e}")
