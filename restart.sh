#!/bin/bash
# iptables -P INPUT ACCEPT
# iptables -P FORWARD ACCEPT
# iptables -P OUTPUT ACCEPT

# Kill any processes running on ports 8501 and 8502
fuser -k 8501/tcp
fuser -k 8502/tcp

streamlit run admin/app.py --server.port 8501 &
streamlit run seller/app.py --server.port 8502 &
