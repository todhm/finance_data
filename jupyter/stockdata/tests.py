import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import unittest

from utils.utiltest import TestUtils
from koreabank.bankdatatest import BankDataTest
if __name__ == "__main__":
    unittest.main()
