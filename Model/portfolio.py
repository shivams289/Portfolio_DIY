
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import seaborn as sns
import copy
import streamlit as st
from .model_inputs import InputVariables


class PortFolio:
    def __init__(self, data, asset_weights = {}):
        self.nav = data
        self.weights = asset_weights
        print("Weights In Portfolio Class:", self.weights)
        print("Columns in Nav data:",self.nav.columns)
        self.cur_units = {x:[] for x in self.weights.keys()}
        self.funds_portfolio_value = {x:[] for x in self.weights.keys()}
        self.fund_vals = [x+'_value' for x in self.weights.keys()]
        self.fund_units = [x+'_units' for x in self.weights.keys()]
        self.fund_abv = [x for x in self.weights.keys()]

        
    def portfolio_creator(self, lumpsum_investment=1000):
        rebalancing = [np.nan for _ in range(len(self.nav))]
        weights = self.weights
        # print('len', len(self.funds_portfolio_value['fund1']))
        cur_units = copy.deepcopy(self.cur_units)  # dict.copy() wouldnt work becuase the dictionary contains references to arrays
        funds_portfolio_value = copy.deepcopy(self.funds_portfolio_value)
        @st.cache_data()
        def PC(weights, cur_units, funds_portfolio_value):
            for fund in weights.keys():
                for i in range(len(self.nav)):
                    if i == 0:
                        cur_units[fund].append(
                            lumpsum_investment * weights[fund] / self.nav[fund][i]
                        )
                        funds_portfolio_value[fund].append(
                            cur_units[fund][i] * self.nav[fund][i]
                        )

                    else:
                        cur_units[fund].append(cur_units[fund][i - 1])
                        funds_portfolio_value[fund].append(
                            cur_units[fund][i] * self.nav[fund][i]
                        )
            return cur_units, funds_portfolio_value
        cur_units, funds_portfolio_value = PC(weights, cur_units, funds_portfolio_value)
        funds_portfolio_value = pd.DataFrame(funds_portfolio_value)
        cur_units = pd.DataFrame(cur_units)

        funds_portfolio_value = funds_portfolio_value.add_suffix("_value")
        cur_units = cur_units.add_suffix("_units")

        funds_portfolio_value[
            "Portfolio"] = funds_portfolio_value.sum(axis=1)
        # print(f'funds_port_val_shape:{funds_portfolio_value.shape}')
        portfolio_BAH = pd.concat(
            [self.nav, cur_units, funds_portfolio_value], axis=1
        )
        # print(f'portfolio_shape:{portfolio_automated.shape}, reabalancing shape{len(rebalancing)}')
        portfolio_BAH["rebalanced"] = rebalancing

        return portfolio_BAH
    
    def portfolio_rebalancer(self, signal = {}):

        self.portfolio_automated = self.portfolio_creator()
        print(f"In Portfolio Rebalancer Function")
        fund_wts = list(self.weights.values())
        
        for i in range(1, len(self.portfolio_automated)):
            self.portfolio_automated.loc[
                i, self.fund_units
            ] = self.portfolio_automated.loc[i - 1, self.fund_units]
            self.portfolio_automated.loc[i, self.fund_vals] = (
                self.portfolio_automated.loc[i, self.fund_units].values
                * self.portfolio_automated.loc[i, self.fund_abv].values
            )

            if ((self.nav.dates.iloc[i].date() in signal.keys()) and signal[self.nav.dates.iloc[i].date()]):
                self.portfolio_automated.loc[i, "rebalanced"] = 1
                # print('portfolio_weights_before_rebalancing',self.portfolio_automated.loc[i, self.fund_vals]/self.portfolio_automated.loc[i, self.fund_vals].sum())
                fund_navs = self.portfolio_automated.loc[i,
                                                        self.fund_abv].values
                curr_port_val = self.portfolio_automated.loc[
                    i, self.fund_vals
                ].sum()
                self.portfolio_automated.loc[i, self.fund_units] = [
                    curr_port_val * x / y for x, y in zip(fund_wts, fund_navs)
                ]
                self.portfolio_automated.loc[i, self.fund_vals] = (
                    self.portfolio_automated.loc[i, self.fund_units].values
                    * self.portfolio_automated.loc[i, self.fund_abv].values
                )
                # print('portfolio_weights_after_rebalancing',self.portfolio_automated.loc[i, self.fund_vals]/self.portfolio_automated.loc[i, self.fund_vals].sum())
        self.portfolio_automated[
            "Portfolio_rebalanced"
        ] = self.portfolio_automated[self.fund_vals].sum(axis=1)

        return self.portfolio_automated

