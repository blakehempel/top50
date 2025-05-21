import datetime as dt
import numpy as np  # NumPy
import math
import dateutil.relativedelta
from dateutil.relativedelta import relativedelta
import time
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def createFactors(df):
    df = df.replace(pd.NA, np.nan)
    # dfFactors = pd.DataFrame(index=df.index)
    ''' 
    q-factor Model
    We construct  the q-factors from a triple 2-by-3-by-3 sort on size, I/A, and ROE.


    Investment Factor is investment-to-assets, I/A, as the annual change in total assets divided by 1-year-lagged total assets.
    3 GROUPS: 30% Low, 40% Middle, 30% High
    Independently, at the end of June of year t, we break all stocks into 3 I/A groups, 
    using the NYSE breakpoints for the low 30%, middle 40%, and high 30% of the 
    ranked values of I/A for the fiscal year ending in calendar year t −1.


    Profitability Factor as ROE, is income before extraordinary items divided by 1-quarter-lagged book equity.
    3 GROUPS: 30% Low, 40% Middle, 30% High
    In addition, independently, at the beginning of each month, we sort all
    stocks into 3 groups based on the NYSE breakpoints for the low 30%, middle
    40%, and high 30% of the ranked values of ROE


    Size factor, at the end of June of each year t, we use [market cap] to split stocks into 2 groups, 
    small and big. 
    2 GROUPS: 50% SMALL, 50% BIG
    The size factor, rME, is the difference (small-minus-big), each month, 
    between the simple average of the returns on the 9 small size portfolios 
    and the simple average of the returns on the 9 big size portfolios.

    Taking the intersections of the 2 size, 3 I/A, and 3 ROE groups, we form 18 portfolios.

    Monthly value-weighted portfolio returns are calculated for the current month, 
    and the portfolios are rebalanced monthly. (The ROE portfolios are rebalanced monthly 
    at the beginning of each month, and the size and I/A portfolios are rebalanced annually 
    at the end of each June.)


    '''
    # q-factor size is market cap
    '''
    Investment
    '''
    df['q-factor Investment to Assets'] = (df['Total Assets'] - df['Lagged: FQ-5 Total Assets']) / df['Lagged: FQ-5 Total Assets']

    # Set ROE to zero if Net Income is negative
    df['q-factor ROE (Income before Extraordinary / Lagged Shareholder Equity) Positive Income before Extraordinary'] = (df['Income before Discontinued Operations & Extraordinary Items'].mask(df['Income before Discontinued Operations & Extraordinary Items'].lt(0), 0)) / df['Lagged FQ-1: Total Shareholders\' Equity incl Minority Intr & Hybrid Debt']

    # df["Return on Equity: Zhang (Income before Extraordinary / Lagged Shareholder Equity) Positive Income before Extraordinary"] = df['Income before Discontinued Operations & Extraordinary Items'].apply(lambda x: x if x > 0 else 0) / df['Lagged FQ-1: Total Shareholders\' Equity incl Minority Intr & Hybrid Debt']

    '''
    VALUE
    '''
    # Sales to Price
    df['Sales to Price: Barbee Mukherji Raines (Total Revenue / MC)'] = df['Revenue from Business Activities - Total'] / df['Company Market Cap']


    # Earnings to Price: Firms with non-positive earnings are excluded.
    # 3/20/2023 setting to np.nan instead of zero
    df['Earnings to Price: Basu (Income before Extraordinary Items / MC) Positive EPS'] = (df['Income before Discontinued Operations & Extraordinary Items'].mask(df['Income before Discontinued Operations & Extraordinary Items'].lt(0), np.nan)) / df['Company Market Cap']
    df['Earnings to Price: (Income before Extraordinary Items / MC)'] = df['Operating Profit before Non-Recurring Income/Expense']/df['Company Market Cap']


    # Enterprise Multiple: Firms with non-positive earnings are excluded.
    # 3/20/2023 setting to np.nan instead of zero
    df['Operating Profit before Depreciation'] = df['Operating Profit before Non-Recurring Income/Expense'] + df['Depreciation Depletion & Amortization - Total'].fillna(0)
    df['Enterprise Multiple: Loughran and Wellman (Operating Profit before Depreciation / EV) Positive EPS'] = (df['Operating Profit before Depreciation'].mask(df['Operating Profit before Depreciation'].lt(0), np.nan)) / df['EV Merged']
    df['Enterprise Multiple (Operating Profit / EV)'] = df['Operating Profit before Depreciation']/df['EV Merged']
    # df.loc[df['EPS - Diluted - incl Extraordinary Items, Common - Total'] < 0, 'Enterprise Multiple: Loughran and Wellman (Operating Profit / EV) Positive EPS'] = 0.0
    # df = df.sort_values(['EEnterprise Multiple (Operating Profit / EV)'],ascending=False)

    '''
    Profitability
    '''
    # Set ROE to zero if Net Income is negative
    # 3/20/2023 setting to np.nan instead of zero, setting to zero calculates change in ROE is zero. Zero was sorted as best, when dROE is ranked asc and current ROE is > 0.
    # 3/20/2023 also set dROE to na-option to keep, instead of bottom (which sorted by asc = top)
    df['Return on Equity: Conventional (Net Income to Common Shares / Shareholder Equity) Positive Net Income'] = (df['Income Available to Common Shares'].mask(df['Income Available to Common Shares'].lt(0), np.nan)) / df['Total Shareholders\' Equity incl Minority Intr & Hybrid Debt']
    # df["Return on Equity: Conventional (Net Income to Common Shares / Shareholder Equity) Positive Net Income"] = df['Income Available to Common Shares'].apply(lambda x: x if x > 0 else 0) / df['Total Shareholders\' Equity incl Minority Intr & Hybrid Debt']

    df['Change in ROE: Conventional'] = df["Return on Equity: Conventional (Net Income to Common Shares / Shareholder Equity) Positive Net Income"] / (df['Lagged FQ-4: Income Available to Common Shares'] / df['Lagged FQ-4: Total Shareholders\' Equity incl Minority Intr & Hybrid Debt'])
    df['Change in ROE: Zhang'] = df['q-factor ROE (Income before Extraordinary / Lagged Shareholder Equity) Positive Income before Extraordinary'] / (df['Lagged FQ-4: Income before Discontinued Operations & Extraordinary Items'] / df['Lagged FQ-5: Total Shareholders\' Equity incl Minority Intr & Hybrid Debt'])

    df['Gross Profitability to Total Assets (Novy-Marx)'] = (df['Gross Profit - Industrials/Property - Total']) / df['Total Assets']
    df['Gross Profitability to Lagged Assets'] = (df['Gross Profit - Industrials/Property - Total']) / df['Lagged: FQ-1 Total Assets']

    # Ole
    # Operating Profit + Interest / lagged book equity
    # df['ole '] = (df['Operating Profit + Interest']) / df['Lagged FQ-1: Total Shareholders\' Equity incl Minority Intr & Hybrid Debt']

    # ola = Operating Profit + R&D / lagged book assets
    # df['ola Operating Profits-to-lagged Assets'] = (df['Operating Profit + R&D']) / df['Lagged: FQ-1 Total Assets']

    '''
    BUILD RANKS
    '''
    # Investment should be ranked Small to Big
    # ascending=False means lowest is the highest score
    df["Size Rank: q-factor Market Cap SB"] = df['Company Market Cap'].rank(ascending=False, method='max', na_option='keep', pct=True)

    # Investment should be ranked Low to High
    # ascending=False means lowest is the highest score
    df["Investment Rank: q-factor Investment to Assets LH"] = df['q-factor Investment to Assets'].rank(ascending=False, method='max', na_option='keep', pct=True)

    df["Value Rank: Sales to Price HL"] = df['Sales to Price: Barbee Mukherji Raines (Total Revenue / MC)'].rank(ascending=True, method='max', na_option='keep', pct=True)

    #df["Value Rank: Earnings to Price HL"] = df['Earnings to Price: Basu (Income before Extraordinary Items / MC) Positive EPS'].rank(ascending=True, method='max', na_option='bottom', pct=True)
    df["Value Rank: Earnings to Price HL"] = df['Earnings to Price: (Income before Extraordinary Items / MC)'].rank(ascending=True, method='max', na_option='bottom', pct=True)

    #df["Value Rank: Enterprise Multiple HL"] = df['Enterprise Multiple: Loughran and Wellman (Operating Profit before Depreciation / EV) Positive EPS'].rank(ascending=True, method='max', na_option='keep', pct=True)
    df["Value Rank: Enterprise Multiple HL"] = df['Enterprise Multiple (Operating Profit / EV)'].rank(ascending=True, method='max', na_option='keep', pct=True)



    df["Profitability Rank: q-factor ROE HL"] = df['q-factor ROE (Income before Extraordinary / Lagged Shareholder Equity) Positive Income before Extraordinary'].rank(ascending=True, method='max', na_option='keep', pct=True)
    df["Profitability Rank: ROE Conventional HL"] = df["Return on Equity: Conventional (Net Income to Common Shares / Shareholder Equity) Positive Net Income"].rank(ascending=True, method='max', na_option='keep', pct=True)
    df["Profitability Rank: dROE Conventional HL"] = df['Change in ROE: Conventional'].rank(ascending=True, method='max', na_option='keep', pct=True)
    df["Profitability Rank: dROE Zhang HL"] = df['Change in ROE: Zhang'].rank(ascending=True, method='max', na_option='keep', pct=True)
    df["Profitability Rank: Gross Profitability Novy-Marx HL"] = df['Gross Profitability to Total Assets (Novy-Marx)'].rank(ascending=True, method='max', na_option='keep', pct=True)
    df["Profitability Rank: Gross Profitability Lagged HL"] = df['Gross Profitability to Lagged Assets'].rank(ascending=True, method='max', na_option='keep', pct=True)

    df["Momentum Rank: Momentum 6Mo-2Wk HL"] = df["Momentum 6 Mo, skip 2 Weeks"].rank(ascending=True, method='max', na_option='keep', pct=True)
    df["Momentum Rank: Momentum 6Mo-1Mo HL"] = df["Momentum 6 Mo, skip 1 Month"].rank(ascending=True, method='max', na_option='keep', pct=True)
    df["Momentum Rank: Momentum 12Mo-1Mo HL"] = df["Momentum 12 Mo, skip 1 Month"].rank(ascending=True, method='max', na_option='keep', pct=True)

    # Volatility should be ranked Low to High
    df["Volatility Rank: Volatility 6Mo LT"] = df["Volatility 6Mo"].rank(ascending=False, method='max', na_option='keep', pct=True)
    df["Volatility Rank: Volatility 126D LT"] = df["Volatility 126D"].rank(ascending=False, method='max', na_option='keep', pct=True)
    df["Volatility Rank: Volatility 12Mo LT"] = df["Volatility 12Mo"].rank(ascending=False, method='max', na_option='keep', pct=True)
    df["Volatility Rank: Volatility 252D LT"] = df["Volatility 252D"].rank(ascending=False, method='max', na_option='keep', pct=True)

    # Combined Alpha Model Sector Rank Percent
    #Couldn't I just divide by 100
    df['Starmine Model Rank Pct'] = df['Combined Alpha Model Sector Rank'].rank(ascending=True, method='max', na_option='keep', pct=True)

    # df[""] = df[].rank(ascending=False, na_option='keep')
    # df[""] = df[].rank(ascending=False, na_option='keep')
    # df[""] = df[].rank(ascending=False, na_option='keep')
    return df
