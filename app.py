# app.py
from flask import Flask, render_template, request
import subprocess
import socket
import whois
import re

app = Flask(__name__)

def validate_url(url):
    # Basic URL validation using a regular expression
    url_pattern = re.compile(r'^(https?://)?(www\d?\.)?[\w.-]+\.\w{2,3}(/\S*)?$')
    return bool(url_pattern.match(url))

def get_ping_result(url):
    try:
        # Use subprocess to execute the ping command and capture the output
        ping_result = subprocess.Popen(['ping', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ping_output, _ = ping_result.communicate()
        return ping_output.decode('utf-8')
    except Exception as e:
        return str(e)

def get_dns_info(url):
    try:
        # Use socket library to fetch DNS information
        ip_address = socket.gethostbyname(url)
        return socket.gethostbyaddr(ip_address)
    except Exception as e:
        return str(e)

def get_whois_info(url):
    try:
        # Use python-whois library to fetch WHOIS information
        whois_info = whois.whois(url)
        if isinstance(whois_info, list):
            return "No WHOIS information available for this URL."
        else:
            return whois_info.text
    except Exception as e:
        return str(e)

@app.route('/', methods=['GET', 'POST'])
def index():
    url = ""
    ping_result = ""
    whois_info = ""
    dns_info = ""
    error_message = ""

    if request.method == 'POST':
        url = request.form['url']

        if not validate_url(url):
            error_message = "Invalid URL format. Please enter a valid URL."
        else:
            ping_result = get_ping_result(url)
            dns_info = get_dns_info(url)
            whois_info = get_whois_info(url)

    return render_template('index.html', url=url, ping_result=ping_result, whois_info=whois_info, dns_info=dns_info, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)
