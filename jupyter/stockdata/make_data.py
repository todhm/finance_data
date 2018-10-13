import pandas as pd
from koreabank.bank_handler import BankHandler


if __name__ == "__main__":
    bh = BankHandler()
    data = bh.get_daily_stats('19950103', '20181001', '060Y001', '010300000')
    df = pd.DataFrame(data)
    df.to_csv("interests_data.csv")
