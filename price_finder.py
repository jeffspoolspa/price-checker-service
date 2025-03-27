import os
import time
import requests
import subprocess
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Wait for the Selenium Grid to be ready (port 4444)
def wait_for_selenium():
    for i in range(10):
        try:
            response = requests.get("http://localhost:4444/wd/hub/status")
            if response.status_code == 200 and response.json()["value"]["ready"]:
                print("✅ Selenium is ready!")
                return
        except Exception as e:
            print(f"⏳ Waiting for Selenium... ({i+1}/10)")
        time.sleep(1)
    raise Exception("❌ Selenium server not responding after 10 seconds.")

# Function that logs in and gets the price
def get_price(part_number):
    wait_for_selenium()

    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Debug system info
    print("🧪 Checking environment setup:")
    print("PATH:", os.environ.get("PATH"))
    print("which chromedriver:", subprocess.getoutput("which chromedriver"))
    print("Chrome version:", subprocess.getoutput("google-chrome --version"))
    print("Chromedriver version:", subprocess.getoutput("chromedriver --version"))

    # Connect to the running Selenium server
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=options
    )

    try:
        wait = WebDriverWait(driver, 60)

        # Step 1: Open pool360 and log in
        driver.get("https://pool360.com")
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log In')]")))
        login_button.click()

        login_form_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sign In / Register')]")))
        login_form_button.click()

        email_field = wait.until(EC.presence_of_element_located((By.ID, 'signinname')))
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))
        email_field.send_keys(os.environ.get("SUPPLIER_EMAIL"))
        password_field.send_keys(os.environ.get("SUPPLIER_PASSWORD"))

        sign_in_button = wait.until(EC.element_to_be_clickable((By.ID, 'next')))
        sign_in_button.click()

        # Step 2: Search part number
        search_box = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Enter keyword, item #, or part #']")))
        search_box.send_keys(part_number)

        first_option = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@data-test-selector='autocompleteProducts_PartNumber'])[1]")))
        first_option.click()

        product_price = wait.until(EC.visibility_of_element_located((By.XPATH, "(//span[@data-test-selector='productPrice_unitNetPrice'])")))
        return product_price.text

    except Exception as e:
        return f"Error: {str(e)}"

    finally:
        time.sleep(2)
        driver.quit()

# Endpoint to receive part number and return price
@app.route('/lookup', methods=['POST'])
def lookup():
    data = request.get_json()
    part_number = data.get("part_number")

    if not part_number:
        return jsonify({"error": "No part number provided"}), 400

    price = get_price(part_number)
    return jsonify({"part_number": part_number, "price": price})

# Flask entry point for local testing
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)


# Flask entry point
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
