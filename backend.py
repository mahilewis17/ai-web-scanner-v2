from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse
import whois
import numpy as np
from PIL import Image

app = Flask(__name__)

# -------- WEBSITE SCAN API --------
@app.route("/scan", methods=["POST"])
def scan():

    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "No URL provided"}), 400

    if not url.startswith("http"):
        url = "https://" + url

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, "html.parser")

        parsed = urlparse(url)
        domain = parsed.netloc

        ip_address = socket.gethostbyname(domain)

        domain_info = whois.whois(domain)

        return jsonify({
            "domain": domain,
            "ip": ip_address,
            "title": soup.title.string if soup.title else "No Title",
            "registrar": str(domain_info.registrar),
            "created": str(domain_info.creation_date),
            "expires": str(domain_info.expiration_date)
        })

    except Exception as e:
        return jsonify({"error": "Scan failed"}), 500


if __name__ == "__main__":
    app.run(debug=True)
