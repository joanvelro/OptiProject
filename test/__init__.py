import os
import sys
import logging

from opti_suite import add_stderr_logger

sys.path.append('src')

TEST_DATA_PATH = os.path.join(os.path.dirname(__file__), 'data')

REPORTS_PATH = os.path.join(os.path.dirname(__file__), 'reports/')


def get_test_path(filename):
    return os.path.join(TEST_DATA_PATH, filename)


# Adding logger only to test executions because there must not be any handler on a library.
# DEBUG, INFO, WARNING, ERROR, CRITICAL
add_stderr_logger(level=logging.INFO)
