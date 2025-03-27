from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

# Connect to the Selenium server running on localhost:4444
driver = webdriver.Remote(
    command_executor='http://localhost:4444/wd/hub',
    desired_capabilities=DesiredCapabilities.CHROME
)

# Navigate to a website
driver.get("https://www.google.com")
print("Page Title:", driver.title)

# Quit the driver
driver.quit()

