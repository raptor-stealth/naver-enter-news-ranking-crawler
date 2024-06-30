import selenium
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


def load_chrome_driver(
    headless=True,
) -> selenium.webdriver.chrome.webdriver.WebDriver:
    options = selenium.webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if headless is True:
        options.add_argument("headless")
    driver = selenium.webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    return driver
