FROM selenium/standalone-chrome:119.0

USER root

# Install Python3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy your test script and entrypoint script into the container
COPY test_selenium.py .
COPY run_test.sh .

# Ensure the entrypoint script is executable
RUN chmod +x run_test.sh

# Use the entrypoint script as the CMD
CMD ["./run_test.sh"]





