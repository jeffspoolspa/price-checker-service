#!/bin/bash
# Start the Selenium server in the background
/opt/bin/entry_point.sh &

# Wait for the Selenium server to initialize (adjust sleep time if needed)
sleep 10

# Run your test script
python3 test_selenium.py
