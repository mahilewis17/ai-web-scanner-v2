import streamlit as st
import whois
import socket
import requests
from urllib.parse import urlparse
from datetime import datetime
from bs4 import BeautifulSoup
from openai import OpenAI

# 🔑 Add your OpenAI API key here
client = OpenAI(api_key="YOUR_OPENAI_API_KEY")

st.set_page_config(page_title="AI Domain & Content Analyzer", layout="centered")

st.title("🌐 AI Domain & Content Analyzer")
st.write("Analyze website details + detect AI-generated content")

url = st.text_input("Enter Website URL")

def extract_domain(url):
    parsed = urlparse(url)
    domain = parsed.netloc
    if domain.startswith("www."):
        domain = domain.replace("www.", "")
    return domain

def get_website_text(url):
    response = requests.get(url, timeout=10)
    soup = BeautifulSoup(response.text, "html.parser")
    
    title = soup.title.string if soup.title else "No title found"
    
    # Get visible text
    paragraphs = soup.find_all("p")
    content = " ".join([p.get_text() for p in paragraphs])
    
    return title, content[:3000]  # limit to 3000 chars

def detect_ai_content(text):
    prompt = f"""
    Analyze the following text and determine if it is likely AI-generated or human-written.
    Respond with:
    - Probability (AI %)
    - Short reason
    
    Text:
    {text}
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content

if st.button("Analyze"):
    if url:
        try:
            domain = extract_domain(url)

            # IP
            ip_address = socket.gethostbyname(domain)

            # WHOIS
            domain_info = whois.whois(domain)

            registrar = domain_info.registrar
            creation_date = domain_info.creation_date
            expiration_date = domain_info.expiration_date
            updated_date = domain_info.updated_date

            if isinstance(creation_date, list):
                creation_date = creation_date[0]
            if isinstance(expiration_date, list):
                expiration_date = expiration_date[0]

            if creation_date:
                age = (datetime.now() - creation_date).days // 365
            else:
                age = "Unavailable"

            # Website content
            title, content = get_website_text(url)

            # AI Detection
            ai_result = detect_ai_content(content)

            # Display Results
            st.subheader("📌 Domain Details")
            st.write(f"**Domain:** {domain}")
            st.write(f"**IP Address:** {ip_address}")
            st.write(f"**Registrar:** {registrar if registrar else 'Unavailable'}")
            st.write(f"**Creation Date:** {creation_date if creation_date else 'Unavailable'}")
            st.write(f"**Expiration Date:** {expiration_date if expiration_date else 'Unavailable'}")
            st.write(f"**Domain Age (Years):** {age}")

            st.subheader("📰 Website Info")
            st.write(f"**Title:** {title}")

            st.subheader("🤖 AI Content Detection")
            st.write(ai_result)

        except Exception as e:
            st.error("Error fetching data. Website may block scraping or have privacy protection.")
    else:
        st.warning("Please enter a valid URL.")
