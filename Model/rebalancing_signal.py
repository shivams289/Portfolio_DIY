import pandas as pd
import datetime as dt
import streamlit as st
class RebalanceSignal:
    def __init__(self, start = dt.date(2010, 1, 1), end = dt.date(2022, 4, 1)):
        #Let's create business dates in the range of of our portfolio data
        self.month = start.month
        start=str(start)
        end=str(end)
        self.dates = pd.DataFrame()
        self.dates["dates"] = list(set(pd.date_range(start=start, end=end, freq="B")))
        self.dates.sort_values(by="dates", inplace=True)  # business/trading dates in this range
        self.dates.dates = pd.to_datetime(self.dates.dates, infer_datetime_format=True)
        self.dates.sort_values(by="dates", inplace=True)  # business/trading dates in this range
        self.dates.reset_index(drop=True, inplace=True)


    def create_annual_signal(self):
        month = self.month
        month1 =  month-1
        if month1 == 0:
            month1 = 12
        rebalancing_signal_dic = {}
        for i in range(1, len(self.dates)):
            if ((self.dates.dates[i].month == month) and (self.dates.dates[i - 1].month == month1)):
                d = self.dates.dates.iloc[i].date()
                rebalancing_signal_dic[self.dates.dates.iloc[i].date()] = 1

        print("Rebalancing dates",rebalancing_signal_dic)

        return rebalancing_signal_dic

    def create_semi_annual_signal(self):
        month = self.month
        month1 =  month-1
        if month1 == 0:
            month1 = 12
        month2 = self.month+6
        if month2>12 :
            month2 = month2-12
        month3 = month2-1
        if month3 == 0:
            month3 = 12
        rebalancing_signal_dic = {}
        for i in range(1, len(self.dates)):
            if ((self.dates.dates[i].month == month) and (self.dates.dates[i - 1].month == month1)) or ((self.dates.dates[i].month == month2) and (self.dates.dates[i - 1].month == month3)):
                d = self.dates.dates.iloc[i].date()
                rebalancing_signal_dic[self.dates.dates.iloc[i].date()] = 1

        print("Rebalancing dates",rebalancing_signal_dic)


        return rebalancing_signal_dic

    def create_quaterly_signal(self):
        rebalancing_signal_dic = {}
        for i in range(1, len(self.dates)):
            if ((self.dates.dates[i].month == 4) and (self.dates.dates[i - 1].month == 3)):
                d = self.dates.dates.iloc[i].date()
                rebalancing_signal_dic[self.dates.dates.iloc[i].date()] = 1

        print("Rebalancing dates",rebalancing_signal_dic)

        return rebalancing_signal_dic

    def create_monthly_signal(self):
        rebalancing_signal_dic = {}
        for i in range(1, len(self.dates)):
            if (self.dates.dates[i].month != self.dates.dates[i - 1].month):
                d = self.dates.dates.iloc[i].date()
                rebalancing_signal_dic[self.dates.dates.iloc[i].date()] = 1

        print("Rebalancing dates",rebalancing_signal_dic)


        return rebalancing_signal_dic
    
# R = RebalanceSignal().create_monthly_signal()
# print(R)

