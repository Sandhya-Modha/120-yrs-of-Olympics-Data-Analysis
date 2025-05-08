#!/bin/bash

# Make the .streamlit directory
mkdir -p ~/.streamlit/

# Create the config.toml file with necessary settings
echo "\
[server]
port = \$PORT
enableCORS = false
headless = true
" > ~/.streamlit/config.toml

# Upgrade pip to avoid build issues
pip install --upgrade pip

# Install build tools required for many Python packages
pip install setuptools wheel
