import pandas as pd
import datetime
import streamlit as st
class Base:
    def __init__(self, indices_path = 'Data/n50_nn50_smallcap_midcap_indices.xlsx', smallcap_path='Data/all_smallcap_jan31.xlsx', midcap_path = 'Data/all_midcap_jan31.xlsx', start = '04/01/1997', end = '01/19/2023'):
        self.start_dt = start
        self.end_dt = end
        self.indices = pd.read_excel(indices_path) #Contains NIFTY50, NIFTY NEXT50, NIFTY SMALLCAP 250, NIFTY MIDCAP 150 & S&P500
        print("Loading indices data.....\n",self.indices)

        self.indices = self.data_preprocessing(self.indices)
        
        indices_names = {"NIFTY 50":"N50", "NIFTY NEXT 50":"NN50", "Nifty Midcap 150 - TRI":"MIDCAP150", "Nifty Smallcap 250 - TRI":"SMALLCAP250", "GOLD":"GOLD", "Aditya Birla SL Corp Bond Fund(G)":"DEBT", "SNP500":"SNP500"}
        self.indices.rename(columns = indices_names, inplace =True)

    def get_assets_nav(self, asset_names = []):
        asset_names.append("dates")
        nav = self.indices[asset_names].dropna(axis = 0)
        nav.sort_values(by = 'dates', inplace =True)
        return nav
    
    def get_end_date(self, data):
        return data.dates.iloc[-1].date()
    
    def get_start_date(self, data):
        return data.dates.iloc[0].date()

    
    # start, end date format id mm/dd/yy
    def preprocess_dates(self, data):
        date_col = list(
            set(data.columns[data.columns.str.contains("ate")].values)
        )
        if 'dates' not in data.columns:
            data.rename(columns={date_col[0]: "dates"}, inplace=True)

        dates = pd.DataFrame()
        dates["dates"] = list(
            set(pd.date_range(start=self.start_dt, end=self.end_dt, freq="B")))
        dates.sort_values(
            by="dates", inplace=True
        )  # business/trading dates in this range
        dates.dates = pd.to_datetime(dates.dates, infer_datetime_format=True)

        data.dates = pd.to_datetime(
            data.dates, infer_datetime_format=True)
        data.sort_values(by="dates", inplace=True)
        data = pd.merge(dates, data, on="dates", how="left")
        data.sort_values(by="dates", inplace=True)

        return data

    def preprocess_missing(self, data):
        for col in data.columns:
            if col != "dates":
                data[col] = data[col].ffill().add(
                    data[col].bfill()).div(2)
                
        return data

    def data_preprocessing(self, data):
        data = self.preprocess_dates(data)
        print("After Preprocessing......\n",data)
        data = self.preprocess_missing(data)
        return data
    
    def scale_data(self, data):
        cols = data.columns[~data.columns.str.contains('ate')].values
        data[cols] = (
            data[cols]
            / data[cols].iloc[0]
            * 1000
        )

        return data
    def convert_csv(self, data):
        return data.to_csv(index = False).encode('utf-8')





    
