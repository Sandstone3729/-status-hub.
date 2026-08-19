import datetime
import ipaddress
import requests
import streamlit as st

st.set_page_config(
    page_title="IT Operations Portal",
    layout="wide"
)

st.sidebar.markdown("**IT Service Desk**")
st.sidebar.info("Environment: **PROD-US-EAST**")
st.sidebar.caption(f"System Time: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M EST')}")

st.title("IT Infrastructure & Service Desk Operations Portal")
st.write("Essential tools for network management, user provisioning, and endpoint diagnostic checks.")

st.divider()

# Section 1: User Onboarding Account Generator
st.markdown("**1. User Provisioning & Credential Generator**")
st.write("Generate standardized active directory usernames, email addresses, and temporary passphrases for new hires.")

col1, col2 = st.columns(2)

with col1:
    first_name = st.text_input("First Name:", "John")
    department = st.selectbox("Department:", ["IT / Systems", "Administration", "Clinical Operations", "Finance", "Human Resources"])

with col2:
    last_name = st.text_input("Last Name:", "Smith")
    domain = st.text_input("Company Domain:", "enterprise.org")

if st.button("Generate Provisioning Profile"):
    clean_first = first_name.strip().lower()
    clean_last = last_name.strip().lower()
    
    if clean_first and clean_last:
        username = f"{clean_first[0]}{clean_last}"
        email = f"{clean_first}.{clean_last}@{domain}"
        temp_pass = f"Welcome{datetime.datetime.now().year}!{clean_last.capitalize()}"
        
        c1, c2, c3 = st.columns(3)
        c1.metric("SamAccountName", username)
        c2.metric("User Principal Name", email)
        c3.metric("Temp Password", temp_pass)
        
        st.code(f"""
# PowerShell Script to Create Account
New-ADUser -Name "{first_name} {last_name}" -SamAccountName "{username}" -UserPrincipalName "{email}" -Department "{department}" -AccountPassword (ConvertTo-SecureString "{temp_pass}" -AsPlainText -Force) -Enabled $true
        """, language="powershell")
    else:
        st.error("Please enter both a first and last name.")

st.divider()

# Section 2: IPv4 Subnet Calculator
st.markdown("**2. Network Subnet & IP Calculator**")
st.write("Calculate network boundaries, broadcast addresses, and usable host capacity for network configuration.")

ip_input = st.text_input("Enter IP with CIDR Notation (e.g., 192.168.1.0/24):", "10.0.0.0/22")

if st.button("Calculate Subnet"):
    try:
        net = ipaddress.ip_network(ip_input, strict=False)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Subnet Mask", str(net.netmask))
        m2.metric("Network Address", str(net.network_address))
        m3.metric("Broadcast Address", str(net.broadcast_address))
        m4.metric("Usable Host Count", f"{net.num_addresses - 2:,}")
        
        hosts = list(net.hosts())
        if hosts:
            st.info(f"**Usable Range:** {hosts[0]} - {hosts[-1]}")
    except ValueError:
        st.error("Invalid CIDR format. Example of valid format: 192.168.1.0/24")

st.divider()

# Section 3: Web Service & API Probe
st.markdown("**3. Endpoint Service Health Monitor**")
st.write("Probe web services and HTTP APIs to verify network status and response latency.")

target_url = st.text_input("Enter URL / Endpoint to Probe:", "https://google.com")

if st.button("Check Service Status"):
    with st.spinner("Pinging endpoint..."):
        try:
            res = requests.get(target_url, timeout=4)
            status_code = res.status_code
            latency = round(res.elapsed.total_seconds() * 1000, 2)
            
            p1, p2, p3 = st.columns(3)
            if status_code == 200:
                p1.success(f"Status: {status_code} OK")
            else:
                p1.warning(f"Status: {status_code}")
                
            p2.metric("Latency", f"{latency} ms")
            p3.metric("Server Header", res.headers.get("Server", "Hidden / Unknown"))
            
        except Exception as e:
            st.error(f"Connection Failed: {e}")