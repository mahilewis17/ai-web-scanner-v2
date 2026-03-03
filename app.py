import streamlit as st
import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse, urljoin
import re

st.set_page_config(page_title="AI Digital Risk Scanner", layout="centered")

st.title("🔍 AI Digital Media Forensic Scanner")
st.markdown("---")

url = st.text_input("Enter Website URL")

if st.button("🚀 Scan Website", use_container_width=True):

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

            # IP Address
            try:
                ip_address = socket.gethostbyname(domain)
            except:
                ip_address = "Unable to fetch"

            st.markdown("## 🌐 Website Information")
            st.write("Domain:", domain)
            st.write("IP Address:", ip_address)

            if soup.title:
                st.write("Title:", soup.title.string)

            # ---------------- RISK ANALYSIS ----------------
            risk_score = 0

            if url.startswith("http://"):
                risk_score += 2

            if len(domain) > 30:
                risk_score += 1

            if domain.count("-") > 2:
                risk_score += 1

            if response.status_code != 200:
                risk_score += 2

            st.markdown("## 🚨 Risk Analysis")

            if risk_score >= 4:
                st.error("🔴 HIGH RISK WEBSITE")
            elif risk_score >= 2:
                st.warning("🟡 MEDIUM RISK WEBSITE")
            else:
                st.success("🟢 SAFE WEBSITE")

            # ---------------- AI DETECTION ----------------
            st.markdown("## 🤖 AI Content Detection")

            page_text = soup.get_text().lower()

            ai_keywords = [
                "ai generated",
                "chatgpt",
                "artificial intelligence",
                "deepfake",
            ]

            ai_found = any(word in page_text for word in ai_keywords)

            if ai_found:
                st.warning("⚠️ Possible AI Generated Content Detected")
            else:
                st.success("No Strong AI Content Indicators Found")

            # ---------------- IMAGES ----------------
            st.markdown("## 🖼 Image Analysis")

            images = soup.find_all("img")
            st.write("Total Images Found:", len(images))

            shown = 0

            for img in images:
                if shown >= 3:
                    break

                src = img.get("src")
                if src:
                    full_url = urljoin(url, src)
                    try:
                        st.image(full_url, width=250)
                        shown += 1
                    except:
                        pass

            if shown == 0:
                st.info("No displayable images or site blocks loading.")

            # ---------------- LINKS ----------------
            st.markdown("## 📊 Page Summary")
            links = soup.find_all("a", href=True)
            st.write("Total Links Found:", len(links))

        except requests.exceptions.Timeout:
            st.error("⛔ Website took too long to respond.")
        except Exception:
            st.error("🔴 Unable to scan this website.")
