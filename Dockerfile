FROM selenium/standalone-chrome:119.0  # ✅ Chrome, Chromedriver, and Selenium built-in

USER root  # Ensure we have permissions

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy your app code
COPY . .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Cloud Run port config
ENV PORT=8080
EXPOSE 8080

# Run Flask app with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8080", "price_finder:app"]




