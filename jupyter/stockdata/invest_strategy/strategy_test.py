import json
import unittest
from invest_strategy.invest_strategy_handler import InvestStrategyHandler
import pandas as pd

class StrategyTest(unittest.TestCase):

    def setUp(self):
        self.df = pd.read_csv('test_interest.csv', index_col=0)
        self.ish = InvestStrategyHandler()

    def test_interest_strategy(self):
        result = self.ish.find_expected_interest(
            self.df, self.df.index[0], self.df.index[-1]
        )
        self.assertTrue(str(result).isdigit())




if __name__ == "__main__":
    unittest.main()
