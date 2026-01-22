"""
QA Automation Logger - Terintegrasi dengan Dashboard
Gunakan logger ini di script test automation Anda untuk mengirim data ke dashboard
"""

import logging
import json
import os
from datetime import datetime
from pathlib import Path

class QADashboardLogger:
    """
    Custom logger untuk QA Automation yang terintegrasi dengan dashboard
    
    Contoh Penggunaan:
    -----------------
    from qa_logger import QADashboardLogger
    
    logger = QADashboardLogger("MyTestSuite")
    
    # Log test execution
    logger.log_test_start("test_login")
    logger.log_test_pass("test_login", duration=2.5)
    logger.log_test_fail("test_checkout", duration=3.2, error="Element not found")
    """
    
    def __init__(self, test_suite_name, log_dir="logs", use_json=True):
        """
        Inisialisasi logger
        
        Args:
            test_suite_name: Nama test suite
            log_dir: Direktori untuk menyimpan log
            use_json: True untuk format JSON, False untuk format text
        """
        self.test_suite_name = test_suite_name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.use_json = use_json
        
        # Setup logger
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_ext = "json" if use_json else "log"
        self.log_file = self.log_dir / f"{test_suite_name}_{timestamp}.{log_ext}"
        
        # Setup Python logger untuk format text
        if not use_json:
            self.logger = logging.getLogger(test_suite_name)
            self.logger.setLevel(logging.DEBUG)
            
            handler = logging.FileHandler(self.log_file, encoding='utf-8')
            formatter = logging.Formatter(
                '%(asctime)s - %(levelname)s - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            
            # Console handler
            console = logging.StreamHandler()
            console.setFormatter(formatter)
            self.logger.addHandler(console)
        
        self.test_results = []
        self.start_time = datetime.now()
    
    def _write_json_log(self, level, message, **kwargs):
        """Write log entry dalam format JSON"""
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'level': level,
            'message': message,
            'test_suite': self.test_suite_name,
            **kwargs
        }
        
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
        
        # Print ke console
        print(f"[{log_entry['timestamp']}] {level}: {message}")
    
    def info(self, message, **kwargs):
        """Log pesan INFO"""
        if self.use_json:
            self._write_json_log('INFO', message, **kwargs)
        else:
            self.logger.info(message)
    
    def warning(self, message, **kwargs):
        """Log pesan WARNING"""
        if self.use_json:
            self._write_json_log('WARNING', message, **kwargs)
        else:
            self.logger.warning(message)
    
    def error(self, message, **kwargs):
        """Log pesan ERROR"""
        if self.use_json:
            self._write_json_log('ERROR', message, **kwargs)
        else:
            self.logger.error(message)
    
    def debug(self, message, **kwargs):
        """Log pesan DEBUG"""
        if self.use_json:
            self._write_json_log('DEBUG', message, **kwargs)
        else:
            self.logger.debug(message)
    
    def log_test_start(self, test_name):
        """Log dimulainya sebuah test"""
        self.info(f"Starting test: {test_name}")
    
    def log_test_pass(self, test_name, duration=None):
        """Log test yang PASSED"""
        message = f"Test PASSED: {test_name}"
        if duration:
            message += f" | duration: {duration}s"
        
        self.info(message, test_name=test_name, status='passed', duration=duration)
        self.test_results.append({
            'name': test_name,
            'status': 'passed',
            'duration': duration
        })
    
    def log_test_fail(self, test_name, error=None, duration=None):
        """Log test yang FAILED"""
        message = f"Test FAILED: {test_name}"
        if error:
            message += f" | error: {error}"
        if duration:
            message += f" | duration: {duration}s"
        
        self.error(message, test_name=test_name, status='failed', error=error, duration=duration)
        self.test_results.append({
            'name': test_name,
            'status': 'failed',
            'duration': duration,
            'error': error
        })
    
    def log_test_skip(self, test_name, reason=None):
        """Log test yang di-skip"""
        message = f"Test SKIPPED: {test_name}"
        if reason:
            message += f" | reason: {reason}"
        
        self.warning(message, test_name=test_name, status='skipped', reason=reason)
    
    def log_assertion(self, description, expected, actual, passed):
        """Log hasil assertion"""
        status = "PASSED" if passed else "FAILED"
        message = f"Assertion {status}: {description} | Expected: {expected}, Actual: {actual}"
        
        if passed:
            self.debug(message)
        else:
            self.error(message)
    
    def log_step(self, step_description):
        """Log langkah test"""
        self.debug(f"Step: {step_description}")
    
    def log_screenshot(self, test_name, screenshot_path):
        """Log lokasi screenshot"""
        self.info(f"Screenshot captured for {test_name}: {screenshot_path}")
    
    def generate_summary(self):
        """Generate dan log summary hasil test"""
        end_time = datetime.now()
        total_duration = (end_time - self.start_time).total_seconds()
        
        total_tests = len(self.test_results)
        passed = sum(1 for t in self.test_results if t['status'] == 'passed')
        failed = sum(1 for t in self.test_results if t['status'] == 'failed')
        
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0
        
        summary = f"""
========================================
TEST EXECUTION SUMMARY
========================================
Test Suite: {self.test_suite_name}
Total Tests: {total_tests}
Passed: {passed}
Failed: {failed}
Pass Rate: {pass_rate:.2f}%
Total Duration: {total_duration:.2f}s
========================================
        """
        
        self.info(summary.strip())
        
        return {
            'test_suite': self.test_suite_name,
            'total_tests': total_tests,
            'passed': passed,
            'failed': failed,
            'pass_rate': pass_rate,
            'total_duration': total_duration
        }


# ============================================
# CONTOH PENGGUNAAN DENGAN SELENIUM
# ============================================

def example_selenium_integration():
    """
    Contoh integrasi dengan Selenium test
    """
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    import time
    
    # Inisialisasi logger
    logger = QADashboardLogger("SeleniumTestSuite", use_json=True)
    
    logger.info("Initializing Selenium WebDriver")
    
    try:
        # Setup driver
        driver = webdriver.Chrome()
        logger.info("Chrome WebDriver initialized successfully")
        
        # Test Case 1: Login Test
        test_name = "test_user_login"
        logger.log_test_start(test_name)
        start_time = time.time()
        
        try:
            logger.log_step("Navigating to login page")
            driver.get("https://example.com/login")
            
            logger.log_step("Entering credentials")
            driver.find_element(By.ID, "username").send_keys("testuser")
            driver.find_element(By.ID, "password").send_keys("password123")
            
            logger.log_step("Clicking login button")
            driver.find_element(By.ID, "login-btn").click()
            
            time.sleep(2)
            
            # Verify login
            logger.log_step("Verifying successful login")
            assert "dashboard" in driver.current_url
            
            duration = time.time() - start_time
            logger.log_test_pass(test_name, duration=duration)
            
        except Exception as e:
            duration = time.time() - start_time
            logger.log_test_fail(test_name, error=str(e), duration=duration)
            logger.log_screenshot(test_name, f"screenshots/{test_name}_fail.png")
        
        # Test Case 2: Search Test
        test_name = "test_product_search"
        logger.log_test_start(test_name)
        start_time = time.time()
        
        try:
            logger.log_step("Entering search term")
            search_box = driver.find_element(By.ID, "search")
            search_box.send_keys("laptop")
            search_box.submit()
            
            time.sleep(2)
            
            logger.log_step("Verifying search results")
            results = driver.find_elements(By.CLASS_NAME, "product-item")
            logger.log_assertion("Search results count", "greater than 0", len(results), len(results) > 0)
            
            duration = time.time() - start_time
            logger.log_test_pass(test_name, duration=duration)
            
        except Exception as e:
            duration = time.time() - start_time
            logger.log_test_fail(test_name, error=str(e), duration=duration)
        
        driver.quit()
        logger.info("WebDriver closed successfully")
        
    except Exception as e:
        logger.error(f"Critical error during test execution: {str(e)}")
    
    finally:
        # Generate summary
        summary = logger.generate_summary()
        logger.info(f"Test execution completed. Check dashboard for detailed results.")


# ============================================
# CONTOH PENGGUNAAN DENGAN PYTEST
# ============================================

def example_pytest_integration():
    """
    Contoh integrasi dengan pytest menggunakan conftest.py
    
    Buat file conftest.py di root project pytest Anda:
    """
    
    conftest_code = '''
import pytest
from qa_logger import QADashboardLogger

@pytest.fixture(scope="session")
def qa_logger():
    """Fixture untuk QA Dashboard Logger"""
    logger = QADashboardLogger("PytestTestSuite", use_json=True)
    yield logger
    logger.generate_summary()

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook untuk mencatat hasil setiap test"""
    outcome = yield
    report = outcome.get_result()
    
    if report.when == "call":
        logger = QADashboardLogger("PytestTestSuite", use_json=True)
        
        if report.passed:
            logger.log_test_pass(item.nodeid, duration=report.duration)
        elif report.failed:
            logger.log_test_fail(
                item.nodeid, 
                error=str(report.longrepr), 
                duration=report.duration
            )
        elif report.skipped:
            logger.log_test_skip(item.nodeid, reason=str(report.longrepr))
    '''
    
    return conftest_code


if __name__ == "__main__":
    print("QA Dashboard Logger - Integration Examples")
    print("=" * 60)
    print("\n1. Untuk Selenium Tests:")
    print("   python qa_logger.py")
    print("\n2. Untuk Pytest Integration:")
    print("   Lihat function example_pytest_integration() untuk kode conftest.py")
    print("\n" + "=" * 60)
    
    # Uncomment untuk menjalankan contoh
    # example_selenium_integration()