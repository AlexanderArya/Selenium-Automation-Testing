from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config.config import HEADLESS


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    
    if HEADLESS:
        options.add_argument("--headless=new")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )
    

    return driver
 