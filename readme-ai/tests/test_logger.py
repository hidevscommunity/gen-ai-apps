"""Unit tests for the custom logger module."""

__package__ = "readmeai"

import logging
import unittest
from io import StringIO

from readmeai import logger


class LoggerTestCase(unittest.TestCase):
    """Unit tests for the custom logger module.

    Parameters
    ----------
    unittest
        TestCase class from the unittest module.
    """

    def setUp(self):
        self.logger_name = __name__
        self.logger = logger.Logger(__name__)
        self.log_output = StringIO()
        self.logger._configure_logger()

        handler = logging.StreamHandler(self.log_output)
        logging.getLogger(self.logger_name).addHandler(handler)

    def tearDown(self):
        logging.getLogger(self.logger_name).handlers.clear()
        self.log_output.close()

    def test_logger_level(self):
        logger = self.logger.Logger(__name__, level=logging.WARNING)
        self.assertEqual(logger.logger.level, logging.WARNING)

    def assertLogOutputContains(self, expected_output):
        log_output = self.log_output.getvalue()
        self.assertIn(expected_output, log_output)

    def test_logging_methods(self):
        msg = "Test log message"

        self.logger.info(msg)
        self.assertLogOutputContains(msg)

        self.logger.debug(msg)
        self.assertLogOutputContains(msg)

        self.logger.warning(msg)
        self.assertLogOutputContains(msg)

        self.logger.error(msg)
        self.assertLogOutputContains(msg)

        self.logger.critical(msg)
        self.assertLogOutputContains(msg)


if __name__ == "__main__":
    unittest.main()
