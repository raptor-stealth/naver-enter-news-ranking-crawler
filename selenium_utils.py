import selenium
from selenium import webdriver



def load_chrome_driver(
    headless=True,
) -> webdriver.chrome.webdriver.WebDriver:
    from webdriver_manager.chrome import ChromeDriverManager
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if headless is True:
        options.add_argument("headless")
    service = selenium.webdriver.chrome.service.Service(ChromeDriverManager().install())
    driver = selenium.webdriver.Chrome(service=service, options=options)
    return driver


def load_firefox_driver(
    headless=True,
):
    options = webdriver.firefox.options.Options()
    if headless is True:
        options.headless = True
    driver = webdriver.Firefox(executable_path="./geckodriver", options=options)
    return driver
