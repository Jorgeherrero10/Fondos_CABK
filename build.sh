#!/bin/bash

# Install Python dependencies
pip install -r requirements.txt

# Create .streamlit directory if it doesn't exist
mkdir -p .streamlit

# Copy config if needed
if [ ! -f .streamlit/config.toml ]; then
    echo "Creating Streamlit config..."
fi

echo "Build complete!"
