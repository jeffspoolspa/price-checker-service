FROM selenium/standalone-chrome:119.0

USER root

# Install Python3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Set working directory
WORKDIR /app

# Copy the test script into the container
COPY test_selenium.py .

# Run the test script when the container starts
CMD ["python3", "test_selenium.py"]





