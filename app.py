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

scan = st.button("🚀 Scan Website", use_container_width=True)

if scan:

    if not url:
        st.warning("Please enter a website URL")
        st.stop()

    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        # ⛔ Add timeout so it never freezes
        response = requests.get(url, headers=headers, timeout=5)

        soup = BeautifulSoup(response.text, "html.parser")

        parsed = urlparse(url)
        domain = parsed.netloc

        # -----------------------
        # IP ADDRESS
        # -----------------------
        try:
            ip_address = socket.gethostbyname(domain)
        except:
            ip_address = "Unable to fetch"

        st.markdown("## 🌐 Website Information")
        st.write("**Domain:**", domain)
        st.write("**IP Address:**", ip_address)

        if soup.title:
            st.write("**Title:**", soup.title.string)

        # -----------------------
        # RISK ANALYSIS
        # -----------------------
        risk_score = 0

        if "http://" in url:
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

        # -----------------------
        # AI CONTENT
