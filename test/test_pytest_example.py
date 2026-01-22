import pytest
import sys
import os
import time

# Use a relative import so this module can import the sibling `qa_logger`
# when the `test` directory is treated as a package (there is `test/__init__.py`).
from test.qa_logger import QADashboardLogger

@pytest.fixture(scope="module")
def logger():
    return QADashboardLogger("PytestSuite", use_json=True)

def test_addition(logger):
    test_name = "test_addition"
    logger.log_test_start(test_name)
    start_time = time.time()
    
    try:
        result = 2 + 2
        assert result == 4
        
        duration = time.time() - start_time
        logger.log_test_pass(test_name, duration=duration)
    except:
        duration = time.time() - start_time
        logger.log_test_fail(test_name, error="Addition failed", duration=duration)
        raise

def test_subtraction(logger):
    test_name = "test_subtraction"
    logger.log_test_start(test_name)
    start_time = time.time()
    
    try:
        result = 5 - 3
        assert result == 2
    
        duration = time.time() - start_time
        logger.log_test_pass(test_name, duration=duration)
    except:
        duration = time.time() - start_time
        logger.log_test_fail(test_name, error="Subtraction failed", duration=duration)
        raise