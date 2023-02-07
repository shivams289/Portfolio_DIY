
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import datetime as dt
from dateutil.relativedelta import relativedelta
from Model.base import Base
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
minimum_dates = []
def get_epoch(date_string):
    return (date_string - dt.datetime(1970,1,1)).dt.total_seconds()


if n50 !=0:
    minimum_dates.append(B.get_min_start_date(asset_name = "N50"))
if nn50 !=0:
    minimum_dates.append(B.get_min_start_date(asset_name = "NN50"))

if midcap !=0:
    minimum_dates.append(B.get_min_start_date(asset_name = "MIDCAP150"))

if smallcap !=0:
    minimum_dates.append(B.get_min_start_date(asset_name = "SMALLCAP250"))

if gold_alloc !=0:
    minimum_dates.append(B.get_min_start_date(asset_name = "GOLD"))

if debt_alloc !=0 :
    minimum_dates.append(B.get_min_start_date(asset_name = "DEBT"))

if snp500 !=0 :
    minimum_dates.append(B.get_min_start_date(asset_name = "SNP500"))

start_date = min(minimum_dates)
end_date = B.get_end_date()

st.subheader("Enter the TimeFrame of Backtest")
start_date = st.date_input("What Should be the Start Date portfolio", min_value= '')
end_date = st.date_input("What Should be the End Date")
