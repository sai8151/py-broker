#!/bin/bash
streamlit run admin/app.py --server.port 8501 &
streamlit run seller/app.py --server.port 8502 &