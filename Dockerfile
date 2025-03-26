# Use a slim Python base image
FROM python:3.9-slim

# Install system dependencies required by Chrome + Chromedriver
RUN apt-get update && apt-get install -y \
    wget \
    gnupg2 \
    unzip \
    libgconf-2-4 \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgtk-3-0 \
    libnspr4 \
    libx11-xcb1 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxtst6 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install \
    && rm google-chrome-stable_current_amd64.deb

# Install Chromedriver
RUN CHROMEDRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -N https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    mv chromedriver /usr/local/bin/chromedriver && \
    chmod +x /usr/local/bin/chromedriver && \
    rm chromedriver_linux64.zip

# Create an application directory
WORKDIR /app

# Copy in your requirements file (list of Python dependencies)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all other code (e.g., app.py) into the container
COPY . .

# Expose port 8080 (the default Cloud Run port)
ENV PORT 8080
EXPOSE 8080

# Run your Python app (modify if your main file is different)
CMD ["python", "price_finder.py"]


