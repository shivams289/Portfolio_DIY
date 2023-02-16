import pandas as pd
import numpy as np
import streamlit as st
from dateutil.relativedelta import relativedelta
class Metrics:
    def __init__(self):
        pass
    def drawdown(self, filter):
        cols = filter.columns[~filter.columns.str.contains('ate')].values
        filter = filter[cols]
        filter = pd.DataFrame((filter.cummax() - filter).div(filter.cummax()).max()*100, columns=[
                              'MaxDrawdown_%']).reset_index().sort_values(by=['MaxDrawdown_%'], ascending=True)
        # Least drawdown is ranked 0
        return filter
    def cagr(self, data, cols = 'Portfolio'):
        res = ((data[cols].iloc[-1]/data[cols].iloc[0])**(1/(data.shape[0]/262))-1)*100
        print("CAGR",res)
        res = res.reset_index()
        res.columns = ["NAME", "CAGR_%"]

        return res
    
    def rolling(self, data, portfolio_name = 'Accumulator',  n=7):
        rel = relativedelta(months=12*n)
        location = data.loc[data.dates >= data.dates.iloc[0]+rel].index[0] #finding the index after n-years from starting portfolio date 
        print(location, 'location')
        rolling = ((data[portfolio_name]/data[portfolio_name].shift(location))**(1/n) - 1)*100
        rolling['dates'] = data.dates
        cols = rolling.columns[~rolling.columns.str.contains('ate')].values
        avg = rolling[cols].mean().reset_index()
        mini = rolling[cols].min().reset_index()
        mini.columns = ["NAME", str(n)+"_YEAR_ROLLING_MIN_%" ]
        avg.columns = ["NAME", str(n)+"_YEAR_ROLLING_AVG_%"]
        res = pd.merge(avg, mini, on ="NAME", how="left")
        return rolling, res


    
