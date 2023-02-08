
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
def get_epoch(date_string):
    return (date_string - dt.datetime(1970,1,1)).dt.total_seconds()

if n50 !=0:
    assets.append("N50")
if nn50 !=0:
    assets.append("NN50")

if midcap !=0:
    assets.append("MIDCAP150")

if smallcap !=0:
    assets.append("SMALLCAP250")

if gold_alloc !=0:
    assets.append("GOLD")

if debt_alloc !=0 :
    assets.append("DEBT")

if snp500 !=0 :
    assets.append("SNP500")

assets_nav = B.get_assets_nav(assets)
start_dt = B.get_start_date(assets_nav)
end_dt = B.get_end_date(assets_nav)
print(start_dt, end_dt)

st.subheader("Enter the TimeFrame of Backtest")
start_date = st.date_input("What Should be the Start Date portfolio", value = start_dt, min_value= start_dt)
end_date = st.date_input("What Should be the End Date", value = end_dt,min_value= start_date, max_value=end_dt)

print("User Entered Start and End Dates:",start_date, end_date)

assets_nav = assets_nav.loc[(assets_nav.dates.dt.date >= start_date) & (assets_nav.dates.dt.date <= end_date) ]
print("Final Dates With Which Portfolio Will be created",assets_nav.dates.iloc[0], assets_nav.dates.iloc[-1])

P = PortFolio(assets_nav)

