FROM python:3.11-slim

# Install system dependencies required by Chromium and Xvfb
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright and the actual Chromium browser binaries
RUN python -m playwright install --with-deps chromium

COPY main.py .

EXPOSE 8000

# Tell Chromium which virtual screen to look at
ENV DISPLAY=:99

# Clear any leftover display locks, start the virtual monitor, then launch Uvicorn
CMD rm -f /tmp/.X99-lock && Xvfb :99 -screen 0 1280x1024x24 & uvicorn main:app --host 0.0.0.0 --port 8000
