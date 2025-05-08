mkdir -p ~/.streamlit/

echo "\
[server]\n\
port = $PORT\n\
enableCORS = false\n\
headless = true\n\
\n\
" > ~/.streamlit/config.toml
#!/bin/bash

# Upgrade pip to avoid build issues
pip install --upgrade pip

# Install build tools
pip install setuptools wheel
