#!/bin/bash
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
streamlit run admin/app.py --server.port 8501 &
streamlit run seller/app.py --server.port 8502 &
