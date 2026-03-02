import streamlit as st
import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse
import re
import math

st.set_page_config(page_title="AI Forensic Link Scanner", layout="centered")

st.title("🛡 AI Digital Forensic Link Intelligence System")
st.markdown("---")

url = st.text_input("Enter Website URL")

if st.button("🚀 Analyze Link", use_container_width=True):

    if not url:
        st.warning("Please enter a URL")
        st.stop()

    if not url.startswith("http"):
        url = "https://" + url

    risk_score = 0
    reasons = []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=6, allow_redirects=True)
        soup = BeautifulSoup(response.text, "html.parser")

        parsed = urlparse(url)
        domain = parsed.netloc

        # ======================
        # IP ADDRESS CHECK
        # ======================
        try:
            ip_address = socket.gethostbyname(domain)
        except:
            ip_address = "Unknown"

        st.subheader("🌐 Website Information")
        st.write("Domain:", domain)
        st.write("IP Address:", ip_address)
        st.write("Status Code:", response.status_code)

        # ======================
        # SECURITY CHECKS
        # ======================

        # HTTP instead of HTTPS
        if url.startswith("http://"):
            risk_score += 15
            reasons.append("Uses insecure HTTP")

        # Domain too long
        if len(domain) > 30:
            risk_score += 10
            reasons.append("Suspicious long domain")

        # Too many hyphens
        if domain.count("-") > 2:
            risk_score += 10
            reasons.append("Too many hyphens in domain")

        # IP-based URL
        if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
            risk_score += 20
            reasons.append("IP-based URL detected")

        # Suspicious keywords
        suspicious_words = [
            "login", "verify", "secure", "update",
            "bank", "free", "bonus", "win", "account"
        ]

        for word in suspicious_words:
            if word in url.lower():
                risk_score += 8
                reasons.append(f"Suspicious keyword: {word}")

        # Redirect check
        if len(response.history) > 2:
            risk_score += 10
            reasons.append("Multiple redirects detected")

        # ======================
        # URL ENTROPY CHECK
        # ======================
        def calculate_entropy(string):
            prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
            entropy = -sum([p * math.log2(p) for p in prob])
            return entropy

        entropy = calculate_entropy(domain)
        if entropy > 4:
            risk_score += 15
            reasons.append("High randomness in domain name")

        # ======================
        # AI CONTENT CHECK
        # ======================
        page_text = soup.get_text().lower()

        ai_keywords = [
            "ai generated", "chatgpt", "openai",
            "deepfake", "midjourney"
        ]

        if any(word in page_text for word in ai_keywords):
            risk_score += 5
            reasons.append("AI-generated content indicators found")

        # ======================
        # FINAL SCORE
        # ======================

        if risk_score > 100:
            risk_score = 100

        st.markdown("---")
        st.subheader("📊 Risk Assessment")

        st.progress(risk_score)

        st.write("Risk Score:", risk_score, "%")

        if risk_score >= 60:
            st.error("🔴 HIGH RISK WEBSITE")
        elif risk_score >= 30:
            st.warning("🟡 MEDIUM RISK WEBSITE")
        else:
            st.success("🟢 SAFE WEBSITE")

        st.markdown("### 🔍 Risk Indicators Found")
        if reasons:
            for r in reasons:
                st.write("•", r)
        else:
            st.write("No major red flags detected.")

    except Exception:
        st.error("Unable to analyze this link.")
