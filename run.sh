#!/bin/bash

echo "=== NetZero Letter Generator ==="
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Starting application..."
streamlit run app.py
