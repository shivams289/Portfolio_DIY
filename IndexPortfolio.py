
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from dateutil.relativedelta import relativedelta
from Model.base import Base
from Model.portfolio import PortFolio
B = Base()
st.title('Create Your Own Index Portfolio')
st.write('------------------------------------------------------------------------------------------------------')
st.header('Using Which Assets You Want to Create your Own POrtfolio?')
col1, col2, col3, col4 = st.columns(4)
with col1:
    gold = st.checkbox("GOLD")

with col2:
    domeq = st.checkbox("DOMESTIC EQUITY")

with col3:
    inteq= st.checkbox("INTERNATIONAL EQUITY")

with col4:
    debt = st.checkbox("DEBT")

with st.form("my_form"):
    st.header('Percentage Allocation')
    col1, col2, col3, col4= st.columns(4)
    col5, col6, col7= st.columns(3)
    if domeq:
        with col1:
            n50 = st.number_input("NIFTY 50", min_value=0, max_value=100)

        with col2:
            nn50 = st.number_input("NIFTY NEXT 50", min_value=0, max_value=100)

        with col3:
            smallcap = st.number_input("NIFTY SMALLCAP 250", min_value=0, max_value=100)

        with col4:
            midcap = st.number_input("NIFTY MIDCAP 150", min_value=0, max_value=100)

    else:
        n50, smallcap, midcap, nn50 = 0,0,0,0

    if inteq:
        with col5:
            snp500 = st.number_input("S&P 500", min_value=0, max_value=100)
    else:
        snp500 = 0

    if debt:
        with col6:
            debt_alloc = st.number_input("DEBT", min_value=0, max_value=100)

    else:
        debt_alloc = 0
            

    if gold:
        with col7:
            gold_alloc = st.number_input("GOLD", min_value=0, max_value=100)

    else:
        gold_alloc = 0


    submitted = st.form_submit_button("Submit")
    if submitted:
        if n50+nn50+smallcap+midcap+debt_alloc+gold_alloc+snp500 != 100:

            st.write("Please Check Weights!")

        else:
            st.write("Portfolio Weights Initialised.......")
assets = []
asset_weights = {}
def get_epoch(date_string):
    return (date_string - dt.datetime(1970,1,1)).dt.total_seconds()

if n50 !=0:
    assets.append("N50")
    asset_weights["N50"] = n50/100
if nn50 !=0:
    assets.append("NN50")
    asset_weights["NN50"] = nn50/100

if midcap !=0:
    assets.append("MIDCAP150")
    asset_weights["MIDCAP150"] = midcap/100

if smallcap !=0:
    assets.append("SMALLCAP250")
    asset_weights["SMALLCAP250"] = smallcap/100

if gold_alloc !=0:
    assets.append("GOLD")
    asset_weights["GOLD"] = gold_alloc/100

if debt_alloc !=0 :
    assets.append("DEBT")
    asset_weights["DEBT"] = debt_alloc/100

if snp500 !=0 :
    assets.append("SNP500")
    asset_weights["SNP500"] = snp500/100

assets_nav = B.get_assets_nav(assets)
start_dt = B.get_start_date(assets_nav)
end_dt = B.get_end_date(assets_nav)
print(start_dt, end_dt)

st.subheader("Enter the TimeFrame of Backtest")
col10, col11 = st.columns(2)
with col10:
    start_date = st.date_input("Start Date", value = start_dt, min_value= start_dt)
with col11:
    end_date = st.date_input("End Date", value = end_dt,min_value= start_date, max_value=end_dt)

print("User Entered Start and End Dates:",start_date, end_date, "\n")

assets_nav = assets_nav.loc[(assets_nav.dates.dt.date >= start_date) & (assets_nav.dates.dt.date <= end_date) ]
assets_nav.reset_index(inplace=True, drop=True)
print("Final Dates With Which Portfolio Will be created",assets_nav.dates.iloc[0], assets_nav.dates.iloc[-1], "\n")

P = PortFolio(assets_nav, asset_weights)
portfolio = P.portfolio_creator()

print("final BAH Portfolio", portfolio['Portfolio'])

st.subheader(
    """ ## Select To Show Performance
                        """
)

chart_options = list(set(assets_nav.columns) - set(['dates']))
portfolio[chart_options] = B.scale_data(portfolio[chart_options])
chart_options.append('Portfolio')
selected_options = st.multiselect(
    'PortfolioVs',
    chart_options, 'Portfolio')

st.line_chart(portfolio, x='dates', y=selected_options)

