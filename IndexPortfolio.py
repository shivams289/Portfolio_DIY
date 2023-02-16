
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from dateutil.relativedelta import relativedelta
from Model.base import Base
from Model.portfolio import PortFolio
from Model.rebalancing_signal import RebalanceSignal
from Model.metrics import Metrics
M = Metrics()
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
with st.form("My form1"):
    st.subheader("Enter the TimeFrame of Backtest")
    col10, col11, col12 = st.columns(3)
    with col10:
        start_date = st.date_input("Start Date", value = start_dt, min_value= start_dt, max_value=end_dt)
    with col11:
        end_date = st.date_input("End Date", value = end_dt,min_value= start_date, max_value=end_dt)

    with col12:
        delta = relativedelta(months=0)
        rebalance = st.selectbox("Rebalancing", options = ['NO', 'Annual', 'Semi-Annual', 'Quaterly', 'Monthly'], index = 0)
        if rebalance == 'Annual':
            delta = relativedelta(months=12)
        if rebalance == 'Semi-Annual':
            delta = relativedelta(months=6)
        if rebalance == 'Quaterly':
            delta = relativedelta(months=3)
        if rebalance == 'Monthly':
            delta = relativedelta(months=1)

    submitted = st.form_submit_button("Submit")
    if submitted:
        st.write("Creating Portfolio For You.....")

print("User Entered Start and End Dates:",start_date, end_date, "\n")
rebalancing_date = start_date+delta
print("rebalancing_date: ", rebalancing_date)


assets_nav = assets_nav.loc[(assets_nav.dates.dt.date >= start_date) & (assets_nav.dates.dt.date <= end_date) ]
assets_nav.reset_index(inplace=True, drop=True)
print("Final Dates With Which Portfolio Will be created",assets_nav.dates.iloc[0], assets_nav.dates.iloc[-1], "\n")

P = PortFolio(assets_nav, asset_weights)

R = RebalanceSignal(start=rebalancing_date, end=end_date)
if rebalance == "NO":
    portfolio = P.portfolio_creator()
else:
    if rebalance == 'Annual':
        portfolio = P.portfolio_rebalancer(R.create_annual_signal())

    if rebalance == 'Semi-Annual':
        portfolio = P.portfolio_rebalancer(R.create_semi_annual_signal())
    if rebalance == 'Monthly':
        portfolio = P.portfolio_rebalancer(R.create_monthly_signal())

    if rebalance == 'Quaterly':
        portfolio = P.portfolio_rebalancer(R.create_semi_annual_signal())

print("final BAH Portfolio", portfolio['Portfolio'])

st.subheader(
    """ ## Select To Show Performance
                        """
)

rolling_calc_cols_assets = list(set(assets_nav.columns) - set(['dates']))

chart_options = list(set(assets_nav.columns) - set(['dates']))
portfolio[chart_options] = B.scale_data(portfolio[chart_options])
chart_options.append('Portfolio')
rolling_calc_cols_assets.append('Portfolio')
if rebalance != "NO":
    chart_options.append('Portfolio_rebalanced')
    rolling_calc_cols_assets.append('Portfolio_rebalanced')

selected_options = st.multiselect(
    'PortfolioVs',
    chart_options, 'Portfolio')

st.line_chart(portfolio, x='dates', y=selected_options)
selected_options_with_date = selected_options.copy()
selected_options_with_date.append('dates')
st.download_button(label="Download Selected Data", data = B.convert_csv(portfolio[selected_options_with_date]), file_name="customportfolios.csv", mime='text/csv')
st.write('----------------------------------------------------------------------------------------------------------')
st.subheader("METRICS")
st.table(M.drawdown(portfolio[selected_options]))
st.write('----------------------------------------------------------------------------------------------------------')
st.subheader('Rolling Return Chart')
y = st.number_input("Year", value=3, min_value=1, max_value=100)
rollin,avg = M.rolling(portfolio, portfolio_name = rolling_calc_cols_assets, n=y)
st.line_chart(rollin, x='dates', y=rolling_calc_cols_assets)
st.download_button(label="Download Rolling", data = B.convert_csv(rollin), file_name="customrolling.csv", mime='text/csv')
st.write('----------------------------------------------------------------------------------------------------------')
st.subheader("Rolling Return Aggregate Metrics")
st.table(avg)
st.download_button(label="Download Average", data = B.convert_csv(avg), file_name="customavg.csv", mime='text/csv')
st.write('----------------------------------------------------------------------------------------------------------')
st.subheader("CAGR Returns")
cagr = M.cagr(portfolio, cols = rolling_calc_cols_assets)
st.table(cagr)

st.download_button(label="Download CAGR", data = B.convert_csv(cagr), file_name="customcagr.csv", mime='text/csv')