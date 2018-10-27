import sys

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from mock import Mock
except ImportError:
    if sys.version_info < (3, 0, 0):
        print("[-] The mock module is needed to create mock objects,"
              "\ninstall it from https://pypi.org/project/mock/"
              "\nor run `pip install mock`.")
        raise
    else:
        sys.exit("""
                    The mock module is needed to create mock objects,
                    install it from https://pypi.org/project/mock/    
                    or run `pip install mock`.
                """)

from config_logger import SameLevelFilter, LessEqualLevelFilter


class FiltersTest(unittest.TestCase):
    def test_same_level_filter_equal(self):
        # Given
        mock_log_record = Mock(levelno=10)
        # When
        level_filter = SameLevelFilter(level=10)
        # Then
        self.assertTrue(level_filter.filter(mock_log_record))

    def test_same_level_filter_not_equal(self):
        # Given
        mock_log_record = Mock(levelno=5)
        # When
        level_filter = SameLevelFilter(level=10)
        # Then
        self.assertFalse(level_filter.filter(mock_log_record))

    def test_less_equal_level_filter_equal(self):
        # Given
        mock_log_record = Mock(levelno=10)
        # When
        level_filter = LessEqualLevelFilter(level=10)
        # Then
        self.assertTrue(level_filter.filter(mock_log_record))

    def test_less_equal_level_filter_less(self):
        # Given
        mock_log_record = Mock(levelno=5)
        # When
        level_filter = LessEqualLevelFilter(level=10)
        # Then
        self.assertTrue(level_filter.filter(mock_log_record))

    def test_less_equal_level_filter_more(self):
        # Given
        mock_log_record = Mock(levelno=15)
        # When
        level_filter = LessEqualLevelFilter(level=10)
        # Then
        self.assertFalse(level_filter.filter(mock_log_record))
