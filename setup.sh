#!/bin/bash

mkdir -p ~/.streamlit/

echo "\
[server]
port = \$PORT
enableCORS = false
headless = true
" > ~/.streamlit/config.toml

pip install --upgrade pip
pip install -r requirements.txt
