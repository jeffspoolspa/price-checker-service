import os
import time
from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# Function that logs in and gets the price
def get_price(part_number):
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    import subprocess

    # Debug: Check if chromedriver is installed and accessible
    print("⏳ Checking if chromedriver exists...")
    print("PATH:", os.environ.get("PATH"))
    print("which chromedriver:", subprocess.getoutput("which chromedriver"))
    print("Chrome version:", subprocess.getoutput("google-chrome --version"))
    print("Chromedriver version:", subprocess.getoutput("chromedriver --version"))

    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.chrome.webdriver import WebDriver

    driver = webdriver.Remote(command_executor='http://localhost:4444/wd/hub',options=options)


    try:
        wait = WebDriverWait(driver, 60)

        # Go to site
        driver.get("https://pool360.com")

        # Click login buttons
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Log In')]")))
        login_button.click()

        login_form_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Sign In / Register')]")))
        login_form_button.click()

        # Fill in login form
        email_field = wait.until(EC.presence_of_element_located((By.ID, 'signinname')))
        password_field = wait.until(EC.presence_of_element_located((By.ID, 'password')))

        # Use environment variables for credentials
        email_field.send_keys(os.environ.get("SUPPLIER_EMAIL"))
        password_field.send_keys(os.environ.get("SUPPLIER_PASSWORD"))

        # Submit login
        sign_in_button = wait.until(EC.element_to_be_clickable((By.ID, 'next')))
        sign_in_button.click()

        # Search part
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

# Flask entry point
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
