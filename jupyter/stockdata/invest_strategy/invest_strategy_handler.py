import pandas as pd
import numpy as np


class InvestStrategyHandler(object):

    def find_expected_interest(self, df, start_date, end_date, date_shift=0):
        start_money = 0
        value_col = list(df.columns)
        value_col.remove('interest_rate')
        df['interest_rate'] = df['interest_rate'].pct_change()
        dataMap = {val: 0 for val in value_col}
        for idx, row in df.iterrows():
            if idx >= start_date and idx <= end_date:
                row_dict = row.to_dict()
                if not np.isnan(row_dict['interest_rate']):
                    if row_dict['interest_rate'] < 0:
                        for key in value_col:
                            if not np.isnan(row_dict[key]) :
                                dataMap[key] += 1
                                start_money -= row_dict[key]
                    else:
                        for key in value_col:
                            if not np.isnan(row_dict[key]) and dataMap[key] >= 1:
                                dataMap[key] -= 1
                                start_money += row_dict[key]
            if idx > end_date:
                for key in value_col:
                    if not np.isnan(row_dict[key]) and dataMap[key] >= 1:
                        dataMap[key] -= 1
                        start_money += row_dict[key]
                break
        print(dataMap)

        return start_money
