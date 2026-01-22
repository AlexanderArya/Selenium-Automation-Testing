from selenium import webdriver
from selenium.webdriver.common.by import By
import sys
import os
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from test.qa_logger import QADashboardLogger

class TestSelenium:
    def __init__(self):
        self.logger = QADashboardLogger("SeleniumTest", use_json=True)
        self.driver = None
    
    def setup(self):
        self.logger.info("Initializing Chrome WebDriver")
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
    
    def test_google_search(self):
        test_name = "test_google_search"
        self.logger.log_test_start(test_name)
        start_time = time.time()
        
        try:
            self.logger.log_step("Opening Google")
            self.driver.get("https://www.google.com")
            
            self.logger.log_step("Entering search query")
            search_box = self.driver.find_element(By.NAME, "q")
            search_box.send_keys("Selenium Python")
            search_box.submit()
            
            time.sleep(2)
            
            self.logger.log_step("Verifying results")
            assert "Selenium" in self.driver.title
            
            duration = time.time() - start_time
            self.logger.log_test_pass(test_name, duration=duration)
            
        except Exception as e:
            duration = time.time() - start_time
            self.logger.log_test_fail(test_name, error=str(e), duration=duration)
    
    def teardown(self):
        if self.driver:
            self.driver.quit()
        self.logger.generate_summary()
    
    def run(self):
        self.setup()
        self.test_google_search()
        self.teardown()

if __name__ == "__main__":
    test = TestSelenium()
    test.run()