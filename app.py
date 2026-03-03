import streamlit as st
import requests

st.title("AI Digital Media Forensic Scanner")

url = st.text_input("Enter Website URL")

if st.button("Scan Website"):

    response = requests.post(
        "http://127.0.0.1:5000/scan",
        json={"url": url}
    )

    if response.status_code == 200:
        data = response.json()

        st.write("Domain:", data["domain"])
        st.write("IP:", data["ip"])
        st.write("Title:", data["title"])
        st.write("Registrar:", data["registrar"])
        st.write("Created:", data["created"])
        st.write("Expires:", data["expires"])
    else:
        st.error("Scan failed")
