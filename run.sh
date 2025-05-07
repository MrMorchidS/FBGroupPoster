#! /bin/bash


# Create log dir
if [ ! -d "log" ]; then
    mkdir log
fi

# Create log dir
if [ ! -d "images" ]; then
    mkdir images
fi

# Create .venv
if [ ! -d ".venv" ]; then
    apt update > /dev/null 2>&1 ;; apt install virtualenv > /dev/null 2>&1
    virtualenv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install requirements
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
else
    exit 1
fi

# Instll Chromium
if ! python -c "import playwright.chromium" > /dev/null 2>&1; then
    playwright install-deps > /dev/null 2>1
    playwright install chromium > /dev/null 2>&1
else
    exit 1
fi

# Run the Python application
python3 app.py
