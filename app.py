import streamlit as st
import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse
import whois
import re
import math
import statistics

st.set_page_config(page_title="AI Digital Forensic Intelligence System", layout="wide")

st.title("🛡 AI Digital Forensic Intelligence System")
st.markdown("---")

url = st.text_input("Enter Website URL")

if st.button("🚀 Analyze Website", use_container_width=True):

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

        # ============================
        # BASIC INFO
        # ============================

        try:
            ip_address = socket.gethostbyname(domain)
        except:
            ip_address = "Unknown"

        st.subheader("🌐 Website Information")
        st.write("Domain:", domain)
        st.write("IP Address:", ip_address)
        st.write("Status Code:", response.status_code)

        # ============================
        # DOMAIN OWNER (WHOIS)
        # ============================

        st.subheader("👤 Domain Ownership")

        try:
            domain_info = whois.whois(domain)
            st.write("Registrar:", domain_info.registrar)
            st.write("Organization:", domain_info.org)
            st.write("Country:", domain_info.country)
            st.write("Creation Date:", domain_info.creation_date)
        except:
            st.warning("WHOIS information not available.")

        # ============================
        # LINK RISK ENGINE
        # ============================

        if url.startswith("http://"):
            risk_score += 15
            reasons.append("Insecure HTTP protocol")

        if len(domain) > 30:
            risk_score += 10
            reasons.append("Unusually long domain")

        if domain.count("-") > 2:
            risk_score += 10
            reasons.append("Multiple hyphens in domain")

        if re.match(r"\d+\.\d+\.\d+\.\d+", domain):
            risk_score += 20
            reasons.append("IP-based URL detected")

        if len(response.history) > 2:
            risk_score += 10
            reasons.append("Multiple redirects detected")

        # Entropy check
        def entropy(string):
            prob = [float(string.count(c)) / len(string) for c in dict.fromkeys(list(string))]
            return -sum([p * math.log2(p) for p in prob])

        if entropy(domain) > 4:
            risk_score += 15
            reasons.append("High domain randomness")

        # ============================
        # AI TEXT DETECTION ENGINE
        # ============================

        st.subheader("🤖 AI Text Analysis")

        text = soup.get_text()
        words = text.split()

        ai_score = 0

        if len(words) > 100:

            sentences = [s for s in re.split(r'[.!?]', text) if len(s.split()) > 3]
            lengths = [len(s.split()) for s in sentences]

            if len(lengths) > 1:
                variance = statistics.variance(lengths)
            else:
                variance = 0

            unique_ratio = len(set(words)) / len(words)
            repetition_ratio = 1 - unique_ratio

            if variance < 20:
                ai_score += 20

            if repetition_ratio > 0.4:
                ai_score += 20

            if "chatgpt" in text.lower() or "ai generated" in text.lower():
                ai_score += 20

        if ai_score > 100:
            ai_score = 100

        st.progress(ai_score)
        st.write("AI Probability Score:", ai_score, "%")

        if ai_score > 40:
            st.warning("Text shows AI-like statistical patterns")
        else:
            st.success("Text appears human-like")

        # ============================
        # FINAL RISK SCORE
        # ============================

        if risk_score > 100:
            risk_score = 100

        st.subheader("🚨 Website Risk Score")
        st.progress(risk_score)
        st.write("Risk Score:", risk_score, "%")

        if risk_score >= 60:
            st.error("🔴 HIGH RISK")
        elif risk_score >= 30:
            st.warning("🟡 MEDIUM RISK")
        else:
            st.success("🟢 SAFE")

        st.markdown("### 🔍 Risk Indicators Found")
        if reasons:
            for r in reasons:
                st.write("•", r)
        else:
            st.write("No major red flags detected.")

        # ============================
        # SOURCE CODE
        # ============================

        st.subheader("🧾 Website Source Code")

        with st.expander("Click to View HTML Source Code"):
            st.code(response.text, language="html")

    except Exception:
        st.error("Unable to analyze website.")
