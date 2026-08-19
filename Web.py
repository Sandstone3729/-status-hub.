import re
import requests  # pyright: ignore[reportMissingModuleSource]
import streamlit as st  # pyright: ignore[reportMissingImports]

st.set_page_config(
    page_title="Security & IR Toolkit",
    layout="wide"
)

st.sidebar.markdown("**Security Toolkit**")
st.sidebar.info("Status: **ACTIVE**")

st.title("Security Operations & Incident Response Toolkit")

# Section 1: Live Global Threat Feed
st.markdown("**1. Global Cyber Threat Feed**")
st.write("Live vulnerability and threat updates pulled from CISA.")

if st.button("Fetch Latest Threats"):
    with st.spinner("Connecting to CISA feed..."):
        try:
            url = "https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json"
            res = requests.get(url, timeout=5).json()
            vulnerabilities = res.get("vulnerabilities", [])[:5]
            
            for v in vulnerabilities:
                st.warning(f"**{v['cveID']}** - {v['vulnerabilityName']}")
                st.caption(f"Vendor: {v['vendorProject']} | Added: {v['dateAdded']}")
                st.write(v['shortDescription'])
                st.divider()
        except Exception as e:
            st.error(f"Failed to load feed: {e}")

st.divider()

# Section 2: Password & Entropy Analyzer
st.markdown("**2. Password Security & Entropy Tester**")
st.write("Evaluate password complexity and mathematical entropy.")

user_pass = st.text_input("Enter test string:", type="password")

if user_pass:
    length = len(user_pass)
    has_upper = bool(re.search(r'[A-Z]', user_pass))
    has_lower = bool(re.search(r'[a-z]', user_pass))
    has_digit = bool(re.search(r'\d', user_pass))
    has_special = bool(re.search(r'[^A-Za-z0-9]', user_pass))
    
    score = sum([has_upper, has_lower, has_digit, has_special])
    
    col1, col2 = st.columns(2)
    col1.metric("Character Length", length)
    
    if length < 8 or score < 2:
        col2.error("Weak Structure")
    elif length >= 12 and score >= 3:
        col2.success("Strong Structure")
    else:
        col2.warning("Moderate Structure")

st.divider()

# Section 3: Interactive Log Parser
st.markdown("**3. Raw Log Parser & IP Extractor**")
st.write("Paste server logs to extract IP addresses and identify failed access attempts.")

sample_log = """192.168.1.50 - - [19/Aug/2026:10:00:01] "GET /admin HTTP/1.1" 401 512
203.0.113.195 - - [19/Aug/2026:10:00:05] "POST /login HTTP/1.1" 403 230
198.51.100.24 - - [19/Aug/2026:10:01:12] "GET /index.html HTTP/1.1" 200 4500
203.0.113.195 - - [19/Aug/2026:10:01:15] "POST /login HTTP/1.1" 403 230"""

log_data = st.text_area("Paste Log File Text:", sample_log, height=150)

if st.button("Analyze Logs"):
    ip_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
    found_ips = re.findall(ip_pattern, log_data)
    failed_attempts = re.findall(r'(\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b).*?(?:401|403)', log_data)
    
    c1, c2 = st.columns(2)
    c1.metric("Total IPs Found", len(set(found_ips)))
    c2.metric("Failed Login Attempts (401/403)", len(failed_attempts))
    
    st.write("**Extracted IP Addresses:**")
    st.json(list(set(found_ips)))