import pandas as pd
import datetime
class Base:
    def __init__(self, indices_path = 'Data/n50_nn50_smallcap_midcap_indices.xlsx', smallcap_path='Data/all_smallcap_jan31.xlsx', midcap_path = 'Data/all_midcap_jan31.xlsx', start = '04/01/1997', end = '02/06/2023', gold_path = "", debt_path = ""):
        self.start_dt = start
        self.end_dt = end
        self.indices = pd.read_excel(indices_path) #Contains NIFTY50, NIFTY NEXT50, NIFTY SMALLCAP 250, NIFTY MIDCAP 150 & S&P500
        self.gold = pd.read_excel(gold_path)
        self.debt = pd.read_excel(debt_path)

        self.indices = self.data_preprocessing(self.indices)
        self.gold = self.data_preprocessing(self.gold)
        self.gold.columns = ['dates', 'GOLD']
        self.debt = self.data_preprocessing(self.debt)
        self.debt.columns = ['dates', 'DEBT']
        
        self.indices_name = {'GOLD':'GOLD', 'DEBT':'DEBT', 'INTEQ':'SNP500', 'DOMEQ':[]}


    def get_min_start_date(self, asset_name = ""):
        if asset_name == "GOLD":
            start = self.gold.dropna().dates.head(1).dt.date()
        if asset_name == "DEBT":
            start = self.debt.dropna().dates.head(1).dt.date()

        if asset_name == "SNP500":
            start = self.indices['dates', 'SNP500'].dropna().dates.head(1).dt.date()

        if asset_name == "NIFTY50":
            start = self.indices['dates', 'SNP500'].dropna().dates.head(1).dt.date()

        if asset_name == "NIFTY_SMALLCAP_250":
            start = self.indices['dates', 'NIFTY_SMALLCAP_250'].dropna().dates.head(1).dt.date()
        if asset_name == "NIFTY_NEXT_50":
            start = self.indices['dates', 'NIFTY_NEXT_50'].dropna().dates.head(1).dt.date()

        if asset_name == "NIFTY_MIDCAP_150":
            start = self.indices['dates', 'NIFTY_MIDCAP_150'].dropna().dates.head(1).dt.date()
            

        return start.strftime("%m/%d/%Y")
    
    def get_end_date(self):
        return self.end_dt

    
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

    def preprocess_missing(self, data):
        for col in data.columns:
            if col != "dates":
                data[col] = data[col].ffill().add(
                    data[col].bfill()).div(2)

    def data_preprocessing(self, data):
        data = self.preprocess_dates(data)
        data = self.preprocess_missing(data)
        return data

    def load_indices_data(self):
        self.indices_data = {}  
        print("------Loading Indices Data------") 
        for asset in self.asset_weights.keys():
            if self.asset_weights[asset] != 0:
                if asset not in self.indices_data.keys():
                    self.indices_data[asset] = pd.read_excel(self.paths[asset])

        print("-------Indices data Loaded----------------")

        return self.indices_data

        



        

    def print_weights(self):
        print(self.asset_weights)


    
