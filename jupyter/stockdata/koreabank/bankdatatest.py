import json
import unittest
from utils.data_utils import *
from koreabank.bank_handler import BankHandler


class BankDataTest(unittest.TestCase):
    def setUp(self):
        self.bh = BankHandler()

    def test_bank_data_properly(self):
        data = self.bh.get_daily_stats(
            '20160103', '20181001', '060Y001', '010300000')
        self.assertTrue(len(data['회사채(3년,AA-)']) > 500)
        self.assertTrue(len(data['date']) > 500)


if __name__ == "__main__":
    unittest.main()
