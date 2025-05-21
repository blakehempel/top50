
import pandas as pd
import datetime as dt
import numpy as np  # NumPy
import math
import dateutil.relativedelta
from dateutil.relativedelta import relativedelta
import time
import seaborn as sns
import matplotlib.pyplot as plt

'''
SET VARIABLES
'''
global_startYear = 2000
global_startMonth = 1
global_endYear = 2022
global_endMonth = 11

quarterlyAnalysis = False
sectorNeutralize = False
displayPeriodResults = False

oneMillion = 1000000.0

startIndexValue_SPXTR = 0
currentIndexValue_SPXTR = 0
forwardPortfolioValue_SPXTR = 0
currentPortfolioValue_top50 = 0

forwardIndexValue_SPXTR = 0.0
forwardPortfolioValue_top50 = 0.0

forwardReturn_SPXTR = 0.0
forwardReturn_top50 = 0.0

periodReturn_SPXTR = 0.0
periodReturn_top50 = 0.0

totalReturn_SPXTR = 0.0
totalReturn_top50 = 0.0

maxValue_SPXTR = 0
maxValue_top50 = 0

maxDrawDown_SPXTR = 0
maxDrawDown_top50 = 0

parameterNarrative = ""
rebalanceDragInBPS = 0

portfolioPeriodReturns = []
sp500TRPeriodReturns = []

portfolioSize = 50
currentPortfolioHoldings = []
marketHedge = False
riskOffModifier = 0
marketMomentum = True
marketRiskOff = False
usePriorPeriodBestFit = False


def setVariables():
    global global_startYear, global_startMonth, global_endYear, global_endMonth
    global quarterlyAnalysis, sectorNeutralize, displayPeriodResults, oneMillion
    global forwardPortfolioValue_SPXTR, forwardReturn_SPXTR, periodReturn_SPXTR, totalReturn_SPXTR, maxValue_SPXTR, maxDrawDown_SPXTR, forwardIndexValue_SPXTR, startIndexValue_SPXTR, currentIndexValue_SPXTR
    global currentPortfolioValue_top50, forwardReturn_top50, periodReturn_top50, totalReturn_top50, maxValue_top50, maxDrawDown_top50, forwardPortfolioValue_top50
    global parameterNarrative, portfolioPeriodReturns, sp500TRPeriodReturns, rebalanceDragInBPS, marketHedge,marketMomentum

    #global_startYear = 2000
    #global_startMonth = 2
    #global_endYear = 2022
    #global_endMonth = 11

    quarterlyAnalysis = False
    sectorNeutralize = False
    displayPeriodResults = False

    oneMillion = 1000000.0

    startIndexValue_SPXTR = oneMillion
    currentIndexValue_SPXTR = oneMillion
    forwardPortfolioValue_SPXTR = oneMillion
    currentPortfolioValue_top50 = oneMillion

    forwardIndexValue_SPXTR = 0.0
    forwardPortfolioValue_top50 = 0.0

    forwardReturn_SPXTR = 0.0
    forwardReturn_top50 = 0.0

    periodReturn_SPXTR = 0.0
    periodReturn_top50 = 0.0

    totalReturn_SPXTR = 0.0
    totalReturn_top50 = 0.0

    maxValue_SPXTR = oneMillion
    maxValue_top50 = oneMillion

    maxDrawDown_SPXTR = oneMillion
    maxDrawDown_top50 = oneMillion

    parameterNarrative = ""
    rebalanceDragInBPS = 10
    #Bloomberg Model Drag is 35.25 bps per rebalance
    portfolioPeriodReturns = []
    sp500TRPeriodReturns = []
    marketHedge = False


def start():
    global global_startYear, global_startMonth, global_endYear, global_endMonth
    global quarterlyAnalysis, sectorNeutralize, displayPeriodResults
    global portfolioPeriodReturns, sp500TRPeriodReturns, portfolioSize

    '''
    '''
    testSectorNeutralize = True
    ifTestMonthly = False
    ifTestQuarterly = True

    if ifTestQuarterly and testSectorNeutralize:
        #Alpha Test
        setVariables()
        portfolioPeriodReturns = []
        displayPeriodResults = False
        quarterlyAnalysis = True
        sectorNeutralize = True
        dfPerformance = BackTestLoop()

        df = pd.DataFrame(sp500TRPeriodReturns)
        print("\nS&P 500 TR Period Returns")
        print(df.describe())

        df = pd.DataFrame(portfolioPeriodReturns)
        print("\nPortfolio Alpha Period Returns")
        print(df.describe())

        # loading lineplot
        #sns.lineplot(data=dfPerformance, x='Date', y='Portfolio Value')
        #plt.yscale('log')
        #plt.yscale('linear')
        #plt.xticks(plt.xticks()[0], dfPerformance.Date.dt.date, rotation=90)
        
        
        
        
        
        
        plt.show()
        #dfPerformance.to_csv("PortfolioValues.csv")

        pass

    if ifTestQuarterly and testSectorNeutralize is False:
        #Bravo Test
        setVariables()
        portfolioPeriodReturns = []
        displayPeriodResults = True
        quarterlyAnalysis = True
        sectorNeutralize = False
        dfPerformance = BackTestLoop()

        df = pd.DataFrame(sp500TRPeriodReturns)
        print("\nS&P 500 TR Period Returns")
        print(df.describe())

        df = pd.DataFrame(portfolioPeriodReturns)
        print("\nPortfolio Bravo Period Returns")
        print(df.describe())

        # Plotting the DataFrame
        #dfPerformance.plot()
        #plt.show()
        #pass
        
        # loading lineplot
        #sns.set_theme(style="whitegrid")
        sns.lineplot(data=dfPerformance, dashes=False)
        #plt.ticklabel_format(style='plain', axis='y')
        #sns.lineplot(data=dfPerformance, palette="tab10", linewidth=2, dashes=False)
        #plt.yscale('log')
        plt.yscale('linear')
        # plt.xticks(plt.xticks()[0], dfPerformance.Date.dt.date, rotation=90)
        
        # Get the current axes
        ax = plt.gca()
        
        # Format y-axis tick labels with commas
        import matplotlib.ticker as mtick
        ax.yaxis.set_major_formatter(mtick.StrMethodFormatter('{x:,.0f}'))
        plt.ylabel('Portfolo Value')
        
        # Rotate x-axis labels
        #ax.set_xticklabels(ax.get_xticklabels(), rotation=60, ha='right')
        # Adjust tick density
        #ax.set_xticks(ax.get_xticks()[::3])  # Show every other tick
        

        plt.show()
        # dfPerformance.to_csv("PortfolioValues.csv")
        pass

    if ifTestMonthly and testSectorNeutralize:
        #Charlie Test
        setVariables()
        portfolioPeriodReturns = []
        displayPeriodResults = False
        quarterlyAnalysis = False
        global_endMonth = 12
        sectorNeutralize = True
        dfPerformance = BackTestLoop()

        df = pd.DataFrame(sp500TRPeriodReturns)
        print("\nS&P 500 TR Period Returns")
        print(df.describe())

        df = pd.DataFrame(portfolioPeriodReturns)
        print("\nPortfolio Charlie Period Returns")
        print(df.describe())

        # loading lineplot
        sns.lineplot(data=dfPerformance)
        plt.yscale('log')
        # plt.xticks(plt.xticks()[0], dfPerformance.Date.dt.date, rotation=90)
        plt.show()
        # dfPerformance.to_csv("PortfolioValues.csv")
        pass

    if ifTestMonthly and testSectorNeutralize is False:
        #Delta Test
        setVariables()
        portfolioPeriodReturns = []
        displayPeriodResults = True
        quarterlyAnalysis = False
        global_endMonth = 12
        sectorNeutralize = False
        dfPerformance = BackTestLoop()

        df = pd.DataFrame(sp500TRPeriodReturns)
        print("\nS&P 500 TR Period Returns")
        print(df.describe())

        df = pd.DataFrame(portfolioPeriodReturns)
        print("\nPortfolio Delta Period Returns")
        print(df.describe())
        # loading lineplot
        sns.lineplot(data=dfPerformance)
        #plt.yscale('log')
        # plt.xticks(plt.xticks()[0], dfPerformance.Date.dt.date, rotation=90)
        plt.show()
        # dfPerformance.to_csv("PortfolioValues.csv")


def applyFactorModel(df):
    global parameterNarrative,marketHedge,marketRiskOff
    """
    df["Size Rank: q-factor Market Cap SB"]

    df["Investment Rank: q-factor Investment to Assets LH"]

    df["Value Rank: Sales to Price HL"]
    df["Value Rank: Earnings to Price HL"]
    df["Value Rank: Enterprise Multiple HL"]

    df["Profitability Rank: q-factor ROE HL"]
    df["Profitability Rank: ROE Conventional HL"]
    df["Profitability Rank: dROE Conventional HL"]
    df["Profitability Rank: dROE Zhang HL"]
    df["Profitability Rank: Gross Profitability Novy-Marx HL"]
    df["Profitability Rank: Gross Profitability Lagged HL"]

    df["Momentum Rank: Momentum 6Mo-2Wk HL"]
    df["Momentum Rank: Momentum 6Mo-1Mo HL"]
    df["Momentum Rank: Momentum 12Mo-1Mo HL"]

    df["Volatility Rank: Volatility 6Mo LT"]
    df["Volatility Rank: Volatility 126D LT"]
    df["Volatility Rank: Volatility 12Mo LT"]
    df["Volatility Rank: Volatility 252D LT"]
    
    df['Starmine Model Rank Pct']

    """

    '''
    Cain 2020
    Qual: ROIC
    Val: EBIT/EV
    Vol: 100Day
    Mom: 6M Lookback 1M Skip
        
    Bloomberg 2022
    Qual: ROE
    Val: Sales to Price
    Vol: 6 Month/126 Day
    Mom: 6M - 2Wk
    '''

    #Expected Investment Growth is calculated from the log of Tobin’s q; cash flow measured by Cop; Change in Return on Equity measured by dRoe.
    #The simplified Q ratio is the equity market value divided by equity book value.
    #df['simplified Q'] = df['Company Market Cap'] / (df['Total Shareholders\' Equity incl Minority Intr & Hybrid Debt'].mask(df['Total Shareholders\' Equity incl Minority Intr & Hybrid Debt'].lt(0), np.nan))
    #df['simplified Q'] = df['Company Market Cap'] / df['Total Shareholders\' Equity incl Minority Intr & Hybrid Debt']
    #df['Rank: log q'] = np.log10(df['simplified Q']).rank(ascending=True, method='max', na_option='keep', pct=True)
    #df["Rank: Cash Flow Cop"] = np.nan
    #df["Profitability Rank: dROE Zhang HL"]
    #df['Rank: simplified Expected Growth'] = (df['Rank: log q'] + df["Profitability Rank: dROE Zhang HL"]) / 2



    '''Bloomberg Factors'''
    bloombergModel = False #'Bloomberg Top 50 Portfolio 2022 - Equal Weight Investment, Profitability, Low Volatility, Momentum'
    improvedBloombergModel = False #"Revised Bloomberg Factors - Equal Weight Investment, Profitability, Low Volatility, Momentum"

    '''Warren Buffett Factors'''
    warrenBuffett = False #'Buffett Factors, Equal Weight - Value, Profitability, Low Volatility'
    buffettPedersen = False #'Buffett Factors, Pedersen Weight - Value (.34), Profitability (.49), Low Volatility (.17)'
    modernBuffett = False #'Revised Buffett Factors - Equal Weight Investment, Profitability, Low Volatility'
    modernBuffett_PedersenWeights = False #'Revised Buffett Factors, Pedersen Weight - Value (.34), Profitability (.49), Low Volatility (.17)'
    revisedBuffet_elimiateHighBeta_AddMomentum = False #'Revised Buffett, eliminate High Beta quintile, add 0.1 wMom'

    '''Hempel Models'''
    overloadMomentum = False # Overweight Momentum, the most powerful factor & Exclude 10% Most Volatile.
    overloadMomentum_addVolatilityFilter = False # Add Volatility to Hempel Model 1
    
    equalWeight_3factor = False # Sector Refinitiv Alpha Factor + Investment + Low Volatility
    equalWeight_4factor_volatilityFilter = False
    
    starmineModel = False # Refinitiv Starmine Alpha Model
    starmineModel_qinvestment = False # Refinitiv Starmine Alpha Model with qFactor Investment Weighting
    starmineModel_qinvestment_momentum = False # Refinitiv Starmine Alpha Model with qFactor Investment Weighting and Momentum Weighting
    starmineModel_qinvestment_momentum_volatility = False # Refinitiv Starmine Alpha Model with qFactor Investment Weighting and Momentum Weighting and Volatility Weighting

    hempelWeatlh_top50 = False # Hempel Wealth Top 50 
    hempelWealth_top50_lowVolatility = False # Hempel Wealth Top 50 Low Vol
    onlyremoveHighestVolatility = True
    riskOffExperiment = False



    if bloombergModel:
        parameterNarrative = 'Bloomberg Top 50 Portfolio 2022 - Equal Weight Investment, Profitability, Low Volatility, Momentum'
        #Description: Equal Weight Value, profitability, Momentum, Volatility
        df['Factor Total Score'] = df["Value Rank: Sales to Price HL"] \
                                   + df["Profitability Rank: ROE Conventional HL"] \
                                   +df["Momentum Rank: Momentum 6Mo-2Wk HL"] \
                                   +df["Volatility Rank: Volatility 126D LT"]
        pass
    elif improvedBloombergModel:
        parameterNarrative = "Revised Bloomberg Factors - Equal Weight Investment, Profitability, Low Volatility, Momentum"
        df['Factor Total Score'] = df["Investment Rank: q-factor Investment to Assets LH"] \
                                   + df["Profitability Rank: ROE Conventional HL"] \
                                   + df["Volatility Rank: Volatility 126D LT"] \
                                   + df["Momentum Rank: Momentum 6Mo-2Wk HL"]
        pass


    elif warrenBuffett:
        parameterNarrative = "Buffett Factors, Equal Weight - Value, Profitability, Low Volatility"
        df['Factor Total Score'] = df["Value Rank: Sales to Price HL"] \
                                   + df["Profitability Rank: ROE Conventional HL"] \
                                   + df["Volatility Rank: Volatility 126D LT"]
        pass
    elif buffettPedersen:
        parameterNarrative = "Buffett Factors, Pedersen Weight - Value (.34), Profitability (.49), Low Volatility (.17)"
        valueLoading = 0.34
        profitabilityLoading = 0.49
        volatilityLoading = 0.17
        df['Factor Total Score'] = (valueLoading * df["Value Rank: Sales to Price HL"]) \
                                   + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) \
                                   + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"])
        pass
    elif modernBuffett:
        parameterNarrative = "Revised Buffett Factors - Equal Weight Investment, Profitability, Low Volatility"
        df['Factor Total Score'] = df["Investment Rank: q-factor Investment to Assets LH"] \
                                   + df["Profitability Rank: ROE Conventional HL"] \
                                   + df["Volatility Rank: Volatility 126D LT"]
        pass
    elif modernBuffett_PedersenWeights:
        parameterNarrative = "Revised Buffett Factors - Equal Weight Investment, Profitability, Low Volatility"
        valueLoading = 0.34
        profitabilityLoading = 0.49
        volatilityLoading = 0.17
        df['Factor Total Score'] = df["Investment Rank: q-factor Investment to Assets LH"] \
                                   + df["Profitability Rank: ROE Conventional HL"] \
                                   + df["Volatility Rank: Volatility 126D LT"]
        pass
    elif revisedBuffet_elimiateHighBeta_AddMomentum:
        df1 = df[df['Volatility Rank: Volatility 126D LT'] > 0.20]
        df = df1.copy()
        parameterNarrative = "Hempel Model 0.3: Revised Buffett, eliminate High Beta quintile, add 0.1 wMom"
        valueLoading = 0
        investmentLoading = 1
        profitabilityLoading = 1
        volatilityLoading = 1
        momentumLoading = 0.1
        loading = "Factor Loadings are wValue:" + str(valueLoading) + " wInvest:" + str(investmentLoading) + " wProfit:" + str(profitabilityLoading) + " wVol:" + str(volatilityLoading) + " HMom:" + str(momentumLoading)
        parameterNarrative = parameterNarrative + "\n" + loading
        df['Factor Total Score'] = (valueLoading * df["Value Rank: Sales to Price HL"]) \
                                   + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) \
                                   + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) \
                                   + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) \
                                   + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"])
        pass


    elif overloadMomentum:
        parameterNarrative = "Hempel Model 0.1: 2Val.2Qual.1Inv.0Vol.4Mom, Exclude 10% Most Volatile."
        #Description: 2xValue, 2xProfitability, 1xInvestment, 0xVolatility, 4xMomentum, Exclude 10% Most Volatile (No factor load on Volatility)
        df1 = df[df['Volatility Rank: Volatility 126D LT'] > 0.10]
        df = df1.copy()
        valueLoading = 2
        profitabilityLoading = 2
        investmentLoading = 1
        momentumLoading = 4
        df['Factor Total Score'] = (valueLoading * df["Value Rank: Sales to Price HL"]) + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"])
        pass
    elif overloadMomentum_addVolatilityFilter:
        parameterNarrative = "Hempel Model 0.2: 2Val.2Qual.1Inv.1Vol.4Mom, Exclude 10% Most Volatile."
        # Description: 2xValue, 2xProfitability, 1xInvestment, 1xVolatility, 4xMomentum, Exclude 10% Most Volatile.
        df1 = df[df['Volatility Rank: Volatility 126D LT'] > 0.10]
        df = df1.copy()
        valueLoading = 2
        profitabilityLoading = 2
        investmentLoading = 1
        volatilityLoading = 0.25
        momentumLoading = 4
        df['Factor Total Score'] = (valueLoading * df["Value Rank: Sales to Price HL"]) + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"])
        pass
    
    elif equalWeight_3factor:
        parameterNarrative = "Hempel Model 0.3: Sector Alpha + Investment + Low Volatility"
        df['Factor Total Score'] = df["Investment Rank: q-factor Investment to Assets LH"] \
                                   + df["Starmine Model Rank Pct"] \
                                   + df["Volatility Rank: Volatility 126D LT"]
        pass
    elif equalWeight_4factor_volatilityFilter:
        df1 = df[df['Volatility Rank: Volatility 126D LT'] > 0.10]
        df = df1.copy()
        loading = "Limit Vol Bottom 90% | "
        parameterNarrative = "Hempel Model 0.4: Sector Alpha + Investment + Profit + Momentum"
        alphaLoading = 0.25
        investmentLoading = 0.25
        profitabilityLoading = 0.25
        momentumLoading = 0.25
        df['Factor Total Score'] = (alphaLoading * df['Starmine Model Rank Pct']) \
                                   + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) \
                                   + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) \
                                   + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"])
        pass
    

    elif starmineModel:
        parameterNarrative = "Alpha Model, Sector Neutral"
        df['Factor Total Score'] = df['Starmine Model Rank Pct']
        pass
    elif starmineModel_qinvestment:
        investmentLoading = 0.5
        parameterNarrative = "Alpha Model, Sector Neutral with wInv of " + str(investmentLoading)
        df['Factor Total Score'] = df['Starmine Model Rank Pct'] + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"])
        pass
    elif starmineModel_qinvestment_momentum:
        investmentLoading = 0.5
        momentumLoading = 0.25
        #+ " with volLoading of "+str(volatilityLoading) \
        parameterNarrative = "Alpha Model, Sector Neutral with wInv of " + str(investmentLoading) + " and wMom of " + str(momentumLoading)
        df['Factor Total Score'] = df['Starmine Model Rank Pct'] + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"])
        pass
    elif starmineModel_qinvestment_momentum_volatility:
        investmentLoading = 0.333333
        momentumLoading = 0.166667
        volatilityLoading = 0.5
        """
        STILL TESTING THE VOLATILITY WEIGHT
        """
        # + " with volLoading of "+str(volatilityLoading) \
        parameterNarrative = "Sector Alpha Model with wIinv of " + str(investmentLoading) + " and wMom of " + str(momentumLoading)+ " with wVol of "+str(volatilityLoading)
        df['Factor Total Score'] = df['Starmine Model Rank Pct'] + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"])
        pass
    
    elif hempelWeatlh_top50:
        #Hempel Wealth Top 50
        loading = ""
        parameterNarrative = "Hempel Wealth Top 50"
        alphaLoading = 1
        valueLoading = 0
        investmentLoading = 0.333
        profitabilityLoading = 0.333
        volatilityLoading = 0.333
        momentumLoading = 0
        loading = loading + "Factor Loadings are"+" wAlpha:" +str(alphaLoading) +" wValue:" +str(valueLoading) + " wInvest:"+str(investmentLoading) + " wProfit:"+str(profitabilityLoading) + " wVol:"+str(volatilityLoading) + " wHMom:"+str(momentumLoading)
        parameterNarrative = parameterNarrative+"\n"+loading
        df['Factor Total Score'] = (alphaLoading * df['Starmine Model Rank Pct'])\
                                   + (valueLoading * df["Value Rank: Sales to Price HL"]) \
                                   + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) \
                                   + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) \
                                   + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) \
                                   + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"])

        pass
    elif hempelWealth_top50_lowVolatility:
        # Hempel Wealth Top 50 Low Vol
        loading = ""
        parameterNarrative = "Hempel Wealth Top 50 Low Vol"
        alphaLoading = 1
        valueLoading = 0
        investmentLoading = 1
        profitabilityLoading = 1
        volatilityLoading = 1
        momentumLoading = 0
        loading = loading + "Factor Loadings are"+" wAlpha:" +str(alphaLoading) +" wValue:" +str(valueLoading) + " wInvest:"+str(investmentLoading) + " wProfit:"+str(profitabilityLoading) + " wVol:"+str(volatilityLoading) + " wHMom:"+str(momentumLoading)
        parameterNarrative = parameterNarrative+"\n"+loading
        df['Factor Total Score'] = (alphaLoading * df['Starmine Model Rank Pct'])\
                                   + (valueLoading * df["Value Rank: Sales to Price HL"]) \
                                   + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) \
                                   + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) \
                                   + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) \
                                   + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"])

        pass
    
    elif onlyremoveHighestVolatility:
        loading = ""
        # df1 = df[df['Profitability Rank: ROE Conventional HL'] > 0.10]
        # df = df1.copy()
        # loading = "Limit Qual Best 90% | "

        # df1 = df[df['Value Rank: Sales to Price HL'] > 0.10]
        # df = df1.copy()
        # loading = "Limit Value Best 90% | "

        # df1 = df[df['Momentum Rank: Momentum 12Mo-1Mo HL'] > 0.10]
        # df = df1.copy()
        # loading = "Limit Momentum Best 90% | "

        #df1 = df[df['Volatility Rank: Volatility 126D LT'] > 0.10]
        #df = df1.copy()
        #loading = "Limit Vol Bottom 90% | "

        df1 = df[df['Volatility Rank: Volatility 126D LT'] < 0.90]
        df = df1.copy()
        loading = "Remove 10% Lowest Vol | "



        parameterNarrative = "HempelModel_v13 "
        alphaLoading = 0.25
        valueLoading = 0
        investmentLoading = 0.25
        profitabilityLoading = 0.25
        volatilityLoading = -0.25
        shortMomentumLoading = 1
        longMomentumLoading = 0.25
        sizeLoading = 0
        if marketRiskOff:
            parameterNarrative = "SETTING RISK OFF " + parameterNarrative
            # print("SETTING RISK OFF.")
            alphaLoading = 1
            valueLoading = 0
            investmentLoading = 0
            profitabilityLoading = 1
            volatilityLoading = 1
            shortMomentumLoading = 1
            longMomentumLoading = 0
            sizeLoading = 0
            pass

        loading = loading + "Factor Loadings are" + " wAlpha:" + str(alphaLoading) + " wValue:" + str(valueLoading) + " wInvest:" + str(investmentLoading) + " wProfit:" + str(profitabilityLoading) + " wVol:" + str(volatilityLoading) + " wHMom:" + str(shortMomentumLoading) + "/" + str(longMomentumLoading)
        parameterNarrative = parameterNarrative + "\n" + loading
        df['Factor Total Score'] = (alphaLoading * df['Starmine Model Rank Pct']) \
                                   + (valueLoading * df["Value Rank: Sales to Price HL"]) \
                                   + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) \
                                   + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) \
                                   + (shortMomentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) \
                                   + (longMomentumLoading * df["Momentum Rank: Momentum 12Mo-1Mo HL"]) \
                                   + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"]) \
                                   + (sizeLoading * df["Size Rank: q-factor Market Cap SB"])
        pass

    elif riskOffExperiment:
        loading = ""
        #df1 = df[df['Profitability Rank: ROE Conventional HL'] > 0.10]
        #df = df1.copy()
        #loading = "Limit Qual Best 90% | "

        #df1 = df[df['Value Rank: Sales to Price HL'] > 0.10]
        #df = df1.copy()
        #loading = "Limit Value Best 90% | "

        #df1 = df[df['Momentum Rank: Momentum 12Mo-1Mo HL'] > 0.10]
        #df = df1.copy()
        #loading = "Limit Momentum Best 90% | "

        df1 = df[df['Volatility Rank: Volatility 126D LT'] > 0.10]
        df = df1.copy()
        loading = "Limit Vol Bottom 90% | "

        parameterNarrative = "HempelModel_v13 "
        alphaLoading = 1
        valueLoading = 0
        investmentLoading = 0
        profitabilityLoading = 1
        volatilityLoading = -0.25
        shortMomentumLoading = 1
        longMomentumLoading = 0
        sizeLoading = 0.25
        if marketRiskOff:
            parameterNarrative = "SETTING RISK OFF " + parameterNarrative
            #print("SETTING RISK OFF.")
            alphaLoading = 1
            valueLoading = 0
            investmentLoading = 0
            profitabilityLoading = 1
            volatilityLoading = 1
            shortMomentumLoading = 1
            longMomentumLoading = 0
            sizeLoading = 0
            pass

        loading = loading + "Factor Loadings are"+" wAlpha:" +str(alphaLoading) +" wValue:" +str(valueLoading) + " wInvest:"+str(investmentLoading) + " wProfit:"+str(profitabilityLoading) + " wVol:"+str(volatilityLoading) + " wHMom:"+str(shortMomentumLoading)+"/"+str(longMomentumLoading)
        parameterNarrative = parameterNarrative+"\n"+loading
        df['Factor Total Score'] = (alphaLoading * df['Starmine Model Rank Pct'])\
                                   + (valueLoading * df["Value Rank: Sales to Price HL"]) \
                                   + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) \
                                   + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) \
                                   + (shortMomentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) \
                                   + (longMomentumLoading * df["Momentum Rank: Momentum 12Mo-1Mo HL"]) \
                                   + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"]) \
                                   + (sizeLoading * df["Size Rank: q-factor Market Cap SB"])
        pass
    else:
        parameterNarrative = "Large Cap"
        df['Factor Total Score'] = -1 * df["Size Rank: q-factor Market Cap SB"]
        pass

    # ascending=False means lowest is the highest score
    df['Factor Total Percentile'] = df['Factor Total Score'].rank(ascending=False, na_option='keep', pct=True)
    df['Rank in Group'] = df.groupby(['TRBC Economic Sector / GICS Sector Code'])['Factor Total Percentile'].rank(ascending=False, method='max', na_option='keep')
    df['Inverse Rank in Group'] = df.groupby(['TRBC Economic Sector / GICS Sector Code'])['Factor Total Percentile'].rank(ascending=True, method='max', na_option='keep')
    df['Count in Group'] = df.groupby('TRBC Economic Sector / GICS Sector Code')['TRBC Economic Sector / GICS Sector Code'].transform('count')
    df['Percentile in Group'] = df['Inverse Rank in Group'] / df['Count in Group']
    return df


def BackTestLoop():
    global global_startYear, global_startMonth, global_endYear, global_endMonth
    global quarterlyAnalysis, sectorNeutralize, displayPeriodResults, oneMillion
    global forwardPortfolioValue_SPXTR, forwardReturn_SPXTR, periodReturn_SPXTR, totalReturn_SPXTR, maxValue_SPXTR, maxDrawDown_SPXTR, forwardIndexValue_SPXTR, startIndexValue_SPXTR, currentIndexValue_SPXTR
    global currentPortfolioValue_top50, forwardReturn_top50, periodReturn_top50, totalReturn_top50, maxValue_top50, maxDrawDown_top50, forwardPortfolioValue_top50
    global parameterNarrative, portfolioPeriodReturns, sp500TRPeriodReturns, portfolioSize, currentPortfolioHoldings, marketHedge,marketMomentum, priorMonthEnd_String, usePriorPeriodBestFit,marketRiskOff,riskOffModifier
    df_spxtr = pd.read_csv('SXPTR_monthly.csv', index_col='Calc Date', parse_dates=True)
    df_spxtr = df_spxtr.sort_index(ascending=True)
    df_spxtr['SMA15'] = df_spxtr['Price Close'].rolling(15).mean()


    startYear = global_startYear
    endYear = global_endYear

    if quarterlyAnalysis:
        if displayPeriodResults:
            print("Starting BackTestLoop. Preforming Quarterly Analysis")
        analysisFrequency = 3
        #global_startMonth=1
        #global_endMonth=10
    else:
        if displayPeriodResults:
            print("Starting BackTestLoop. Preforming Monthly Analysis")
        analysisFrequency = 1
        #global_startMonth = 1
        #global_endMonth = 12

    df = pd.DataFrame()
    listPerformance = []
    priorPeriod_bestCombo1M = []
    priorPeriod_bestCombo3M = []
    firstPass = True

    for year in range(startYear, endYear + 1):
        loopStartMonth = 2
        loopEndMonth = 12
        '''SET Calendar Conditions'''
        if year == startYear:
            loopStartMonth = global_startMonth
        if year == endYear:
            loopEndMonth = global_endMonth

        for month in range(loopStartMonth, loopEndMonth + 1, analysisFrequency):

            firstOfTheMonth = dt.datetime(year, month, 1)
            analysisDate_String = dt.datetime.strftime(firstOfTheMonth, '%Y-%m-%d')
            priorMonthEnd = firstOfTheMonth + relativedelta(days=-1)
            priorMonthEnd_String = dt.datetime.strftime(priorMonthEnd, '%Y-%m-%d')
            priorMonthEnd_1MoAgo = firstOfTheMonth + relativedelta(months=-1)
            priorMonthEnd_1MoAgo = priorMonthEnd_1MoAgo + relativedelta(days=-1)
            priorMonthEnd_1MoAgo_String = dt.datetime.strftime(priorMonthEnd_1MoAgo, '%Y-%m-%d')
            priorMonthEnd_3MoAgo = firstOfTheMonth + relativedelta(months=-3)
            priorMonthEnd_3MoAgo = priorMonthEnd_3MoAgo + relativedelta(days=-1)
            priorMonthEnd_3MoAgo_String = dt.datetime.strftime(priorMonthEnd_3MoAgo, '%Y-%m-%d')
            #Future
            priorMonthEnd_1MoForward = firstOfTheMonth + relativedelta(months=1)
            priorMonthEnd_1MoForward = priorMonthEnd_1MoForward + relativedelta(days=-1)
            priorMonthEnd_1MoForward_String = dt.datetime.strftime(priorMonthEnd_1MoForward, '%Y-%m-%d')
            priorMonthEnd_3MoForward = firstOfTheMonth + relativedelta(months=3)
            priorMonthEnd_3MoForward = priorMonthEnd_3MoForward + relativedelta(days=-1)
            priorMonthEnd_3MoForward_String = dt.datetime.strftime(priorMonthEnd_3MoForward, '%Y-%m-%d')

            if displayPeriodResults:
                print("\nRunning "+analysisDate_String)
            forwardDate_String = ''


            '''GET TOP 50 Portfolio'''
            df = pd.read_csv('./data/Factor_' + priorMonthEnd_String + '.csv', index_col='RICs')
            #df.to_csv('./data/Factor_' + priorMonthEnd_String + '.csv', index=True)
            df = df[~df.index.duplicated(keep='first')]
            df = createFactors(df)
            df = applyFactorModel(df)
            #df.to_csv('./parameters/Parameters_' + priorMonthEnd_String + '.csv', index=True)

            # ascending=False means lowest is the highest score
            #if firstPass is False and usePriorPeriodBestFit is True:

            if usePriorPeriodBestFit is True:
                print('Getting BestFit '+priorMonthEnd_String)
                parameterNarrative = 'priorPeriod_bestCombo3M' + parameterNarrative
                dfPast = pd.read_csv('./data/Factor_' + priorMonthEnd_3MoAgo_String + '.csv', index_col='RICs')
                dfPast = dfPast[~dfPast.index.duplicated(keep='first')]
                dfPast = createFactors(dfPast)
                priorPeriod_bestCombo1M, priorPeriod_bestCombo3M = determineFactorBestFit(dfPast)
                if quarterlyAnalysis:
                    df = applyFactorBestFit(df, priorPeriod_bestCombo3M)
                else:
                    df = applyFactorBestFit(df, priorPeriod_bestCombo3M)

            '''SPX TR'''
            currentIndexValue_SPXTR = df_spxtr.loc[priorMonthEnd_String, 'Price Close']
            SPXTR_SMA15 = df_spxtr.loc[priorMonthEnd_String, 'SMA15']

            if marketMomentum:
                if currentIndexValue_SPXTR < SPXTR_SMA15:
                    """RISK OFF. Reset Factor Parameters"""
                    marketRiskOff = True
                    marketHedge = True
                    df = applyFactorModel(df)
                    marketRiskOff = False
                    #marketHedge = False
                    pass
                else:
                    """RISK ON"""
                    marketHedge = False
                    pass

            if sectorNeutralize:
                #dfSave = df.sort_values(['Percentile in Group'], ascending=True).copy()
                df = df.sort_values(['Percentile in Group'], ascending=True).head(portfolioSize)
                #df = df.sort_values(['Percentile in Group'], ascending=False).head(portfolioSize)
            else:
                #dfSave = df.sort_values(['Factor Total Percentile'], ascending=True).copy()
                df = df.sort_values(['Factor Total Percentile'], ascending=True).head(portfolioSize)
                #df = df.sort_values(['Percentile in Group'], ascending=False).head(portfolioSize)
                #print(df[['Factor Total Score']].head())

            if firstPass:
                listPerformance.append([priorMonthEnd_String, oneMillion, oneMillion])
                #print("First Pass "+priorMonthEnd_String + " SPXTR="+str(currentIndexValue_SPXTR))
                startIndexValue_SPXTR = currentIndexValue_SPXTR
                currentPortfolioHoldings = df.index.values.tolist()
                if displayPeriodResults:
                    print("Buying " + str(len(currentPortfolioHoldings)) + " securities: "+ str(currentPortfolioHoldings))
                firstPass = False
            else:
                newPortfolioHoldings = df.index.values.tolist()
                if displayPeriodResults:
                    difference = list(set(currentPortfolioHoldings) - set(newPortfolioHoldings))
                    print("Selling " + str(len(difference)) + " securities:" + str(difference))
                    difference = list(set(newPortfolioHoldings) - set(currentPortfolioHoldings))
                    print("Buying " + str(len(difference)) + " securities:" + str(difference))
                currentPortfolioHoldings = newPortfolioHoldings

            if displayPeriodResults:
                print("Portfolio size " + str(len(currentPortfolioHoldings)) + ": " + str(currentPortfolioHoldings))

            '''CALC Forward Returns'''
            if quarterlyAnalysis:
                forwardDate = priorMonthEnd_3MoForward
                forwardDate_String = priorMonthEnd_3MoForward_String
                #S&P 500
                forwardIndexValue_SPXTR = df_spxtr.loc[priorMonthEnd_3MoForward_String, 'Price Close']
                forwardReturn_SPXTR = 100 * (forwardIndexValue_SPXTR - currentIndexValue_SPXTR) / currentIndexValue_SPXTR
                forwardPortfolioValue_SPXTR = (forwardIndexValue_SPXTR / startIndexValue_SPXTR) * oneMillion

                # Top 50 Portfolio
                forwardReturn_top50 = df["3 Month Forward Return"].mean()
                forwardReturn_top50 = forwardReturn_top50 - (rebalanceDragInBPS / 100)
                if marketHedge:
                    # Hedge Portfolio
                    print("Hedge Portfolio: PreHedge {0:,.2f}".format(forwardReturn_top50) + "% Market {0:,.2f}".format(forwardReturn_SPXTR)+"%")
                    #forwardReturn_top50 = forwardReturn_top50 - forwardReturn_SPXTR
                    forwardReturn_top50 = forwardReturn_top50 * riskOffModifier
                    parameterNarrative = "Hedged " + parameterNarrative
                forwardPortfolioValue_top50 = (1 + forwardReturn_top50 / 100) * currentPortfolioValue_top50


            else:
                forwardDate = priorMonthEnd_1MoForward
                forwardDate_String = priorMonthEnd_1MoForward_String
                #S&P 500
                forwardIndexValue_SPXTR = df_spxtr.loc[priorMonthEnd_1MoForward_String, 'Price Close']
                forwardReturn_SPXTR = 100 * (forwardIndexValue_SPXTR - currentIndexValue_SPXTR) / currentIndexValue_SPXTR
                forwardPortfolioValue_SPXTR = (forwardIndexValue_SPXTR / startIndexValue_SPXTR) * oneMillion

                # Top 50 Portfolio
                forwardReturn_top50 = df["1 Month Forward Return"].mean()
                forwardReturn_top50 = forwardReturn_top50 - (rebalanceDragInBPS / 100)
                if marketHedge:

                    # Hedge Portfolio
                    print("Hedge Portfolio: PreHedge {0:,.2f}".format(forwardReturn_top50)+" Market {0:,.2f}".format(forwardReturn_SPXTR))
                    # forwardReturn_top50 = forwardReturn_top50 - forwardReturn_SPXTR
                    forwardReturn_top50 = forwardReturn_top50 * riskOffModifier
                    parameterNarrative = "Hedged " + parameterNarrative
                forwardPortfolioValue_top50 = (1 + forwardReturn_top50 / 100) * currentPortfolioValue_top50


            if displayPeriodResults:
                #print("TESTING: priorMonthEnd_String is " + priorMonthEnd_String + " forwardDate_String is "+forwardDate_String)
                print(parameterNarrative)
                pass


            totalReturn_SPXTR = 100 * (forwardIndexValue_SPXTR - startIndexValue_SPXTR) / startIndexValue_SPXTR
            totalReturn_top50 = 100 * (forwardPortfolioValue_top50 - oneMillion) / oneMillion

            '''set max value'''
            if forwardPortfolioValue_SPXTR > maxValue_SPXTR:
                maxValue_SPXTR = forwardPortfolioValue_SPXTR
            if forwardPortfolioValue_top50 > maxValue_top50:
                maxValue_top50 = forwardPortfolioValue_top50

            '''set max drawdown          '''
            currentDrawdown = (forwardPortfolioValue_SPXTR - maxValue_SPXTR) / maxValue_SPXTR
            if currentDrawdown < maxDrawDown_SPXTR:
                maxDrawDown_SPXTR = currentDrawdown

            if displayPeriodResults:
                print("Results as of "+forwardDate_String+"\n" +
                    "  SPXTR: " + " Portfolio Value $" + "{0:,.2f}".format(forwardPortfolioValue_SPXTR)
                      + " Period {0:,.2f}".format(forwardReturn_SPXTR) + "%" + " Total Return {0:,.2f}".format(totalReturn_SPXTR) + "%"
                      + " Period Drawdown {0:,.2f}".format(currentDrawdown * 100) + "%")

            currentDrawdown = (forwardPortfolioValue_top50 - maxValue_top50) / maxValue_top50
            if currentDrawdown < maxDrawDown_top50:
                maxDrawDown_top50 = currentDrawdown

            if displayPeriodResults:
                print("  Top50: " + " Portfolio Value $" + "{0:,.2f}".format(forwardPortfolioValue_top50)
                      + " Period {0:,.2f}".format(forwardReturn_top50) + "%" + " Total Return {0:,.2f}".format(totalReturn_top50) + "%"
                      + " Period Drawdown {0:,.2f}".format(currentDrawdown * 100) + "%")

            portfolioPeriodReturns.append(forwardReturn_top50)
            sp500TRPeriodReturns.append(forwardReturn_SPXTR)
            listPerformance.append([forwardDate_String,forwardPortfolioValue_top50, forwardPortfolioValue_SPXTR])

            #currentIndexValue_SPXTR = forwardIndexValue_SPXTR
            currentPortfolioValue_top50 = forwardPortfolioValue_top50
            #rebalanceFrequency = forwardDate_String


        #END OF MONTH LOOP
    #END OF YEAR LOOP
    if quarterlyAnalysis:
        rebalanceFrequency = " Quarterly Rebalanced"
    else:
        rebalanceFrequency = " Monthly Rebalanced"
    if sectorNeutralize:
        rebalanceFrequency = rebalanceFrequency+", Sector Neutralized"

    if displayPeriodResults:
        print("\n")
    print("\nSUMMARY:")
    print("\nModel: " + parameterNarrative)
    print(rebalanceFrequency+", Rebalance cost " + "{0:,.2f}".format(rebalanceDragInBPS / 100) + "%" + ", Portfolio size of " + str(portfolioSize))
    deltaDate = relativedelta(forwardDate, dt.datetime(global_startYear, global_startMonth, 1))
    deltaYears = (1 + deltaDate.months + deltaDate.years * 12)/12
    #print("deltaYears " +str(deltaYears))
    cagrPortfolio = (((forwardPortfolioValue_top50 / oneMillion) ** (1/deltaYears)) - 1)*100
    cagrSPXTR = (((forwardPortfolioValue_SPXTR / oneMillion) ** (1 / deltaYears)) - 1) * 100
    print(" Portfolio Value $" + "{0:,.0f}".format(forwardPortfolioValue_top50)+ " vs. S&P500 $" + "{0:,.0f}".format(forwardPortfolioValue_SPXTR))
    print(" Compound Annual Growth Rate (CAGR) is " + "{0:,.1f}".format(cagrPortfolio)+"% vs. S&P500 " + "{0:,.1f}".format(cagrSPXTR)+"%")
    print(" Total Return {0:,.0f}".format(totalReturn_top50) + "% vs. S&P500 {0:,.0f}".format(totalReturn_SPXTR) + "%")
    print(" Max Drawdown {0:,.0f}".format(maxDrawDown_top50 * 100) + "% vs. S&P500 {0:,.0f}".format(maxDrawDown_SPXTR * 100) + "%")
    print(" Time Period: " + str(global_startYear) + "-"+str(global_startMonth) + "-1 to " + forwardDate_String)

    #df.to_csv("BacktestResults.csv")
    dfPerformance=pd.DataFrame(listPerformance, columns=['Date', 'Top50', 'SPXTR'])
    dfPerformance.set_index('Date', inplace=True)

    #listSave = [strMetrics, strTimePeriod, top50TotalReturn, top50MaxDrawdown * 100]
    #dfSave = pd.DataFrame(listSave)
    # dfSave.columns["TimePeriod","Factors","Results","MaxDrawdown"]
    #dfSave.to_csv("BacktestResults.csv")
    return dfPerformance


def BackTestLoopwithHoldingPeriods():
    global global_startYear, global_startMonth, global_endYear, global_endMonth
    global quarterlyAnalysis, sectorNeutralize, displayPeriodResults, oneMillion
    global forwardPortfolioValue_SPXTR, forwardReturn_SPXTR, periodReturn_SPXTR, totalReturn_SPXTR, maxValue_SPXTR, maxDrawDown_SPXTR, forwardIndexValue_SPXTR, startIndexValue_SPXTR, currentIndexValue_SPXTR
    global currentPortfolioValue_top50, forwardReturn_top50, periodReturn_top50, totalReturn_top50, maxValue_top50, maxDrawDown_top50, forwardPortfolioValue_top50
    global parameterNarrative, portfolioPeriodReturns, sp500TRPeriodReturns, portfolioSize, currentPortfolioHoldings, marketHedge,marketMomentum, priorMonthEnd_String, usePriorPeriodBestFit,marketRiskOff,riskOffModifier
    df_spxtr = pd.read_csv('SXPTR_monthly.csv', index_col='Calc Date', parse_dates=True)
    df_spxtr = df_spxtr.sort_index(ascending=True)
    df_spxtr['SMA15'] = df_spxtr['Price Close'].rolling(15).mean()


    startYear = global_startYear
    endYear = global_endYear

    if quarterlyAnalysis:
        if displayPeriodResults:
            print("Starting BackTestLoop. Preforming Quarterly Analysis")
        analysisFrequency = 3
        #global_startMonth=1
        #global_endMonth=10
    else:
        if displayPeriodResults:
            print("Starting BackTestLoop. Preforming Monthly Analysis")
        analysisFrequency = 1
        #global_startMonth = 1
        #global_endMonth = 12

    df = pd.DataFrame()
    listPerformance = []
    priorPeriod_bestCombo1M = []
    priorPeriod_bestCombo3M = []
    firstPass = True

    for year in range(startYear, endYear + 1):
        loopStartMonth = 2
        loopEndMonth = 12
        '''SET Calendar Conditions'''
        if year == startYear:
            loopStartMonth = global_startMonth
        if year == endYear:
            loopEndMonth = global_endMonth

        for month in range(loopStartMonth, loopEndMonth + 1, analysisFrequency):

            firstOfTheMonth = dt.datetime(year, month, 1)
            analysisDate_String = dt.datetime.strftime(firstOfTheMonth, '%Y-%m-%d')
            priorMonthEnd = firstOfTheMonth + relativedelta(days=-1)
            priorMonthEnd_String = dt.datetime.strftime(priorMonthEnd, '%Y-%m-%d')
            priorMonthEnd_1MoAgo = firstOfTheMonth + relativedelta(months=-1)
            priorMonthEnd_1MoAgo = priorMonthEnd_1MoAgo + relativedelta(days=-1)
            priorMonthEnd_1MoAgo_String = dt.datetime.strftime(priorMonthEnd_1MoAgo, '%Y-%m-%d')
            priorMonthEnd_3MoAgo = firstOfTheMonth + relativedelta(months=-3)
            priorMonthEnd_3MoAgo = priorMonthEnd_3MoAgo + relativedelta(days=-1)
            priorMonthEnd_3MoAgo_String = dt.datetime.strftime(priorMonthEnd_3MoAgo, '%Y-%m-%d')
            #Future
            priorMonthEnd_1MoForward = firstOfTheMonth + relativedelta(months=1)
            priorMonthEnd_1MoForward = priorMonthEnd_1MoForward + relativedelta(days=-1)
            priorMonthEnd_1MoForward_String = dt.datetime.strftime(priorMonthEnd_1MoForward, '%Y-%m-%d')
            priorMonthEnd_3MoForward = firstOfTheMonth + relativedelta(months=3)
            priorMonthEnd_3MoForward = priorMonthEnd_3MoForward + relativedelta(days=-1)
            priorMonthEnd_3MoForward_String = dt.datetime.strftime(priorMonthEnd_3MoForward, '%Y-%m-%d')

            if displayPeriodResults:
                print("\nRunning "+analysisDate_String)
            forwardDate_String = ''


            '''GET TOP 50 Portfolio'''
            df = pd.read_csv('./data/Factor_' + priorMonthEnd_String + '.csv', index_col='RICs')
            #df.to_csv('./data/Factor_' + priorMonthEnd_String + '.csv', index=True)
            df = df[~df.index.duplicated(keep='first')]
            df = createFactors(df)
            df = applyFactorModel(df)
            #df.to_csv('./parameters/Parameters_' + priorMonthEnd_String + '.csv', index=True)

            # ascending=False means lowest is the highest score
            #if firstPass is False and usePriorPeriodBestFit is True:

            if usePriorPeriodBestFit is True:
                print('Getting BestFit '+priorMonthEnd_String)
                parameterNarrative = 'priorPeriod_bestCombo3M' + parameterNarrative
                dfPast = pd.read_csv('./data/Factor_' + priorMonthEnd_3MoAgo_String + '.csv', index_col='RICs')
                dfPast = dfPast[~dfPast.index.duplicated(keep='first')]
                dfPast = createFactors(dfPast)
                priorPeriod_bestCombo1M, priorPeriod_bestCombo3M = determineFactorBestFit(dfPast)
                if quarterlyAnalysis:
                    df = applyFactorBestFit(df, priorPeriod_bestCombo3M)
                else:
                    df = applyFactorBestFit(df, priorPeriod_bestCombo3M)

            '''SPX TR'''
            currentIndexValue_SPXTR = df_spxtr.loc[priorMonthEnd_String, 'Price Close']
            SPXTR_SMA15 = df_spxtr.loc[priorMonthEnd_String, 'SMA15']

            if marketMomentum:
                if currentIndexValue_SPXTR < SPXTR_SMA15:
                    """RISK OFF. Reset Factor Parameters"""
                    marketRiskOff = True
                    marketHedge = True
                    df = applyFactorModel(df)
                    marketRiskOff = False
                    #marketHedge = False
                    pass
                else:
                    """RISK ON"""
                    marketHedge = False
                    pass

            if sectorNeutralize:
                #dfSave = df.sort_values(['Percentile in Group'], ascending=True).copy()
                df = df.sort_values(['Percentile in Group'], ascending=True).head(portfolioSize)
                #df = df.sort_values(['Percentile in Group'], ascending=False).head(portfolioSize)
            else:
                #dfSave = df.sort_values(['Factor Total Percentile'], ascending=True).copy()
                df = df.sort_values(['Factor Total Percentile'], ascending=True).head(portfolioSize)
                #df = df.sort_values(['Percentile in Group'], ascending=False).head(portfolioSize)
                #print(df[['Factor Total Score']].head())

            if firstPass:
                listPerformance.append([priorMonthEnd_String, oneMillion, oneMillion])
                #print("First Pass "+priorMonthEnd_String + " SPXTR="+str(currentIndexValue_SPXTR))
                startIndexValue_SPXTR = currentIndexValue_SPXTR
                currentPortfolioHoldings = df.index.values.tolist()
                if displayPeriodResults:
                    print("Buying " + str(len(currentPortfolioHoldings)) + " securities: "+ str(currentPortfolioHoldings))
                firstPass = False
            else:
                newPortfolioHoldings = df.index.values.tolist()
                if displayPeriodResults:
                    difference = list(set(currentPortfolioHoldings) - set(newPortfolioHoldings))
                    print("Selling " + str(len(difference)) + " securities:" + str(difference))
                    difference = list(set(newPortfolioHoldings) - set(currentPortfolioHoldings))
                    print("Buying " + str(len(difference)) + " securities:" + str(difference))
                currentPortfolioHoldings = newPortfolioHoldings

            if displayPeriodResults:
                print("Portfolio size " + str(len(currentPortfolioHoldings)) + ": " + str(currentPortfolioHoldings))

            '''CALC Forward Returns'''
            if quarterlyAnalysis:
                forwardDate = priorMonthEnd_3MoForward
                forwardDate_String = priorMonthEnd_3MoForward_String
                #S&P 500
                forwardIndexValue_SPXTR = df_spxtr.loc[priorMonthEnd_3MoForward_String, 'Price Close']
                forwardReturn_SPXTR = 100 * (forwardIndexValue_SPXTR - currentIndexValue_SPXTR) / currentIndexValue_SPXTR
                forwardPortfolioValue_SPXTR = (forwardIndexValue_SPXTR / startIndexValue_SPXTR) * oneMillion

                # Top 50 Portfolio
                forwardReturn_top50 = df["3 Month Forward Return"].mean()
                forwardReturn_top50 = forwardReturn_top50 - (rebalanceDragInBPS / 100)
                if marketHedge:
                    # Hedge Portfolio
                    print("Hedge Portfolio: PreHedge {0:,.2f}".format(forwardReturn_top50) + "% Market {0:,.2f}".format(forwardReturn_SPXTR)+"%")
                    #forwardReturn_top50 = forwardReturn_top50 - forwardReturn_SPXTR
                    forwardReturn_top50 = forwardReturn_top50 * riskOffModifier
                    parameterNarrative = "Hedged " + parameterNarrative
                forwardPortfolioValue_top50 = (1 + forwardReturn_top50 / 100) * currentPortfolioValue_top50


            else:
                forwardDate = priorMonthEnd_1MoForward
                forwardDate_String = priorMonthEnd_1MoForward_String
                #S&P 500
                forwardIndexValue_SPXTR = df_spxtr.loc[priorMonthEnd_1MoForward_String, 'Price Close']
                forwardReturn_SPXTR = 100 * (forwardIndexValue_SPXTR - currentIndexValue_SPXTR) / currentIndexValue_SPXTR
                forwardPortfolioValue_SPXTR = (forwardIndexValue_SPXTR / startIndexValue_SPXTR) * oneMillion

                # Top 50 Portfolio
                forwardReturn_top50 = df["1 Month Forward Return"].mean()
                forwardReturn_top50 = forwardReturn_top50 - (rebalanceDragInBPS / 100)
                if marketHedge:

                    # Hedge Portfolio
                    print("Hedge Portfolio: PreHedge {0:,.2f}".format(forwardReturn_top50)+" Market {0:,.2f}".format(forwardReturn_SPXTR))
                    # forwardReturn_top50 = forwardReturn_top50 - forwardReturn_SPXTR
                    forwardReturn_top50 = forwardReturn_top50 * riskOffModifier
                    parameterNarrative = "Hedged " + parameterNarrative
                forwardPortfolioValue_top50 = (1 + forwardReturn_top50 / 100) * currentPortfolioValue_top50


            if displayPeriodResults:
                #print("TESTING: priorMonthEnd_String is " + priorMonthEnd_String + " forwardDate_String is "+forwardDate_String)
                print(parameterNarrative)
                pass


            totalReturn_SPXTR = 100 * (forwardIndexValue_SPXTR - startIndexValue_SPXTR) / startIndexValue_SPXTR
            totalReturn_top50 = 100 * (forwardPortfolioValue_top50 - oneMillion) / oneMillion

            '''set max value'''
            if forwardPortfolioValue_SPXTR > maxValue_SPXTR:
                maxValue_SPXTR = forwardPortfolioValue_SPXTR
            if forwardPortfolioValue_top50 > maxValue_top50:
                maxValue_top50 = forwardPortfolioValue_top50

            '''set max drawdown          '''
            currentDrawdown = (forwardPortfolioValue_SPXTR - maxValue_SPXTR) / maxValue_SPXTR
            if currentDrawdown < maxDrawDown_SPXTR:
                maxDrawDown_SPXTR = currentDrawdown

            if displayPeriodResults:
                print("Results as of "+forwardDate_String+"\n" +
                    "  SPXTR: " + " Portfolio Value $" + "{0:,.2f}".format(forwardPortfolioValue_SPXTR)
                      + " Period {0:,.2f}".format(forwardReturn_SPXTR) + "%" + " Total Return {0:,.2f}".format(totalReturn_SPXTR) + "%"
                      + " Period Drawdown {0:,.2f}".format(currentDrawdown * 100) + "%")

            currentDrawdown = (forwardPortfolioValue_top50 - maxValue_top50) / maxValue_top50
            if currentDrawdown < maxDrawDown_top50:
                maxDrawDown_top50 = currentDrawdown

            if displayPeriodResults:
                print("  Top50: " + " Portfolio Value $" + "{0:,.2f}".format(forwardPortfolioValue_top50)
                      + " Period {0:,.2f}".format(forwardReturn_top50) + "%" + " Total Return {0:,.2f}".format(totalReturn_top50) + "%"
                      + " Period Drawdown {0:,.2f}".format(currentDrawdown * 100) + "%")

            portfolioPeriodReturns.append(forwardReturn_top50)
            sp500TRPeriodReturns.append(forwardReturn_SPXTR)
            listPerformance.append([forwardDate_String,forwardPortfolioValue_top50, forwardPortfolioValue_SPXTR])

            #currentIndexValue_SPXTR = forwardIndexValue_SPXTR
            currentPortfolioValue_top50 = forwardPortfolioValue_top50
            #rebalanceFrequency = forwardDate_String


        #END OF MONTH LOOP
    #END OF YEAR LOOP
    if quarterlyAnalysis:
        rebalanceFrequency = " Quarterly Rebalanced"
    else:
        rebalanceFrequency = " Monthly Rebalanced"
    if sectorNeutralize:
        rebalanceFrequency = rebalanceFrequency+", Sector Neutralized"

    if displayPeriodResults:
        print("\n")
    print("\nSUMMARY:")
    print("\nModel: " + parameterNarrative)
    print(rebalanceFrequency+", Rebalance cost " + "{0:,.2f}".format(rebalanceDragInBPS / 100) + "%" + ", Portfolio size of " + str(portfolioSize))
    deltaDate = relativedelta(forwardDate, dt.datetime(global_startYear, global_startMonth, 1))
    deltaYears = (1 + deltaDate.months + deltaDate.years * 12)/12
    #print("deltaYears " +str(deltaYears))
    cagrPortfolio = (((forwardPortfolioValue_top50 / oneMillion) ** (1/deltaYears)) - 1)*100
    cagrSPXTR = (((forwardPortfolioValue_SPXTR / oneMillion) ** (1 / deltaYears)) - 1) * 100
    print(" Portfolio Value $" + "{0:,.0f}".format(forwardPortfolioValue_top50)+ " vs. S&P500 $" + "{0:,.0f}".format(forwardPortfolioValue_SPXTR))
    print(" Compound Annual Growth Rate (CAGR) is " + "{0:,.1f}".format(cagrPortfolio)+"% vs. S&P500 " + "{0:,.1f}".format(cagrSPXTR)+"%")
    print(" Total Return {0:,.0f}".format(totalReturn_top50) + "% vs. S&P500 {0:,.0f}".format(totalReturn_SPXTR) + "%")
    print(" Max Drawdown {0:,.0f}".format(maxDrawDown_top50 * 100) + "% vs. S&P500 {0:,.0f}".format(maxDrawDown_SPXTR * 100) + "%")
    print(" Time Period: " + str(global_startYear) + "-"+str(global_startMonth) + "-1 to " + forwardDate_String)

    #df.to_csv("BacktestResults.csv")
    dfPerformance=pd.DataFrame(listPerformance, columns=['Date', 'Top50', 'SPXTR'])
    dfPerformance.set_index('Date', inplace=True)

    #listSave = [strMetrics, strTimePeriod, top50TotalReturn, top50MaxDrawdown * 100]
    #dfSave = pd.DataFrame(listSave)
    # dfSave.columns["TimePeriod","Factors","Results","MaxDrawdown"]
    #dfSave.to_csv("BacktestResults.csv")
    return dfPerformance


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


def determineFactorBestFitvsMarket(df, spx3MoReturn):
    pass


def determineFactorBestFit(df):
    '''

    df1 = df[df['Volatility Rank: Volatility 126D LT'] > 0.10]
    df = df1.copy()
    loading = "Remove 10% Most Vol | "
    # print(df.shape[0])
    df1 = df[df['Value Rank: Sales to Price HL'] > 0.10]
    df = df1.copy()
    loading = "Remove 10% Least Value | "
    df1 = df[df["Profitability Rank: q-factor ROE HL"] > 0.10]
    df = df1.copy()
    loading = "Remove 10% Least Profit | "
    '''

    bestCombo3M = []
    bestCombo1M = []
    best3Mo = -100
    best1Mo = -100
    counter = 0
    loops = 100
    while counter < loops:
        counter += 1
        #print("Run "+str(counter))
        '''
        df["Size Rank: q-factor Market Cap SB"]
    
        df["Investment Rank: q-factor Investment to Assets LH"]
    
        df["Value Rank: Sales to Price HL"]
        Significant at the 95% confidence level across all 3 holding periods.
        
        df["Value Rank: Earnings to Price HL"]
        Very Significant (t-test ≥ 3) more than 99% confident at 1- and 6-month period. 
        Epq1 = One Month Holding Period 0.98% average monthly return with 5.08 t-statistic
        Epq6 = Six Month Holding Period 0.65% average monthly return with 3.69 t-statistic


        df["Value Rank: Enterprise Multiple HL"]
        Very Significant (t-test ≥ 3) more than 99% confident at 1-month period.
        Emq1 = One Month Holding Period 0.81% average monthly return with 3.67 t-statistic

    
        df["Profitability Rank: q-factor ROE HL"]
        Very Significant (t-test ≥ 3) more than 99% confident at 1-month period.
        Roe1 = One Month Holding Period 0.69% average monthly return with 3.07 t-statistic
        
        df["Profitability Rank: ROE Conventional HL"]
        
        df["Profitability Rank: dROE Conventional HL"]
        Not Rated
        
        df["Profitability Rank: dROE Zhang HL"]
        Very Significant (t-test ≥ 3) more than 99% confident at 1- and 6-month period.
        dRoe1 = One Month Holding Period 0.76% average monthly return with 5.43 t-statistic
        dRoe6 = Six Month Holding Period 0.39% average monthly return with 3.28 t-statistic


        df["Profitability Rank: Gross Profitability Novy-Marx HL"]
        Significant at the 95% confidence level
        
        df["Profitability Rank: Gross Profitability Lagged HL"]
        Very Significant (t-test ≥ 3) more than 99% confident at 1-month period.
        Glaq1 = One Month Holding Period 0.51% average monthly return with 3.40 t-statistic

        df["Momentum Rank: Momentum 6Mo-2Wk HL"]
        df["Momentum Rank: Momentum 6Mo-1Mo HL"]
        df["Momentum Rank: Momentum 12Mo-1Mo HL"]
    
        df["Volatility Rank: Volatility 6Mo LT"]
        df["Volatility Rank: Volatility 126D LT"]
        df["Volatility Rank: Volatility 12Mo LT"]
        df["Volatility Rank: Volatility 252D LT"]
        
        df['Starmine Model Rank Pct']
    
        '''
        factors = ['Invest',
                   'valS/P',
                   'valE/P',
                   'valEM',
                   'prof_roeQ',
                   'prof_roeC',
                   'prof_deltaC',
                   'prof_deltaQ',
                   'GrossProfit',
                   'GrossPrfLag',
                   'Mom6m-2w',
                   'Mom6m-1m',
                   'Mom12m-1m',
                   'Vol6m',
                   'Vol126d',
                   'Vol12m',
                   'Vol252d',
                   'Alpha']
        '''
        Model: priorPeriod_bestCombo3M
 Monthly Rebalanced, Rebalance cost 0.00%, Portfolio size of 50
 Portfolio Value $16,298,696 vs. S&P500 $6,484,439
 Compound Annual Growth Rate (CAGR) is 15.0% vs. S&P500 9.8%
 Total Return 1,530% vs. S&P500 548%
 Max Drawdown -38% vs. S&P500 -51%
 Time Period: 2003-1-1 to 2022-12-31
 
        v01 = getRandomLoading()
        v02 = 0
        v03 = getRandomLoading()
        v04 = getRandomLoading()
        v05 = getRandomLoading()
        v06 = 0
        v07 = 0
        v08 = getRandomLoading()
        v09 = 0
        v10 = getRandomLoading()
        v11 = getRandomLoading()
        v12 = 0
        v13 = getRandomLoading()
        v14 = getRandomLoading()
        v15 = 0
        v16 = 0
        v17 = 0
        v18 = getRandomLoading()
        '''
        v01 = getRandomLoading() #Investment
        v02 = 0
        v03 = 0 #Earnings to Price Very Significant (t-test ≥ 3) more than 99% confident at 1- and 6-month period.
        v04 = 0
        v05 = 0 # zhang ROE Very Significant (t-test ≥ 3) more than 99% confident at 1-month period.
        v06 = 0
        v07 = 0
        v08 = getRandomLoading() #delta ROE zhang Very Significant (t-test ≥ 3) more than 99% confident at 1- and 6-month period.
        v09 = 0
        v10 = 0 #lagged Gross Profit Very Significant (t-test ≥ 3) more than 99% confident at 1-month period
        v11 = getRandomLoading() #Momentum 6Mo-2Wk
        v12 = 0
        v13 = 0 #Momentum Rank: Momentum 12Mo-1Mo
        v14 = getRandomLoading() #Volatility Rank: Volatility 6Mo
        v15 = 0
        v16 = 0 #Volatility Rank: Volatility 12Mo
        v17 = 0
        v18 = 0 #Starmine Model

        factorCombo=[v01,v02,v03,v04,v05,v06,v07,v08,v09,v10,v11,v12,v13,v14,v15,v16,v17,v18]
        df['Factor Total Score'] = (v01 * df["Investment Rank: q-factor Investment to Assets LH"]) \
                                   + (v02 * df["Value Rank: Sales to Price HL"]) \
                                   + (v03 * df["Value Rank: Earnings to Price HL"]) \
                                   + (v04 * df["Value Rank: Enterprise Multiple HL"]) \
                                   + (v05 * df["Profitability Rank: q-factor ROE HL"]) \
                                   + (v06 * df["Profitability Rank: ROE Conventional HL"]) \
                                   + (v07 * df["Profitability Rank: dROE Conventional HL"]) \
                                   + (v08 * df["Profitability Rank: dROE Zhang HL"]) \
                                   + (v09 * df["Profitability Rank: Gross Profitability Novy-Marx HL"]) \
                                   + (v10 * df["Profitability Rank: Gross Profitability Lagged HL"]) \
                                   + (v11 * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) \
                                   + (v12 * df["Momentum Rank: Momentum 6Mo-1Mo HL"]) \
                                   + (v13 * df["Momentum Rank: Momentum 12Mo-1Mo HL"]) \
                                   + (v14 * df["Volatility Rank: Volatility 6Mo LT"]) \
                                   + (v15 * df["Volatility Rank: Volatility 126D LT"]) \
                                   + (v16 * df["Volatility Rank: Volatility 12Mo LT"]) \
                                   + (v17 * df["Volatility Rank: Volatility 252D LT"]) \
                                   + (v18 * df['Starmine Model Rank Pct'])
        # ascending=False means lowest is the highest score
        df['Factor Total Percentile'] = df['Factor Total Score'].rank(ascending=False, na_option='keep', pct=True)
        df['Rank in Group'] = df.groupby(['TRBC Economic Sector / GICS Sector Code'])['Factor Total Percentile'].rank(ascending=False, method='max', na_option='keep')
        df['Inverse Rank in Group'] = df.groupby(['TRBC Economic Sector / GICS Sector Code'])['Factor Total Percentile'].rank(ascending=True, method='max', na_option='keep')
        df['Count in Group'] = df.groupby('TRBC Economic Sector / GICS Sector Code')['TRBC Economic Sector / GICS Sector Code'].transform('count')
        df['Percentile in Group'] = df['Inverse Rank in Group'] / df['Count in Group']

        dfSave = df.sort_values(['Factor Total Percentile'], ascending=True).copy()
        dfSave = dfSave.sort_values(['Factor Total Percentile'], ascending=True).head(portfolioSize)

        forwardReturn_top50_3Mo = dfSave["3 Month Forward Return"].mean()
        if forwardReturn_top50_3Mo > best3Mo:
            #print("Run " + str(counter)+". Setting best3Mo")
            best3Mo=forwardReturn_top50_3Mo
            bestCombo3M=factorCombo

        forwardReturn_top50_1Mo = dfSave["1 Month Forward Return"].mean()
        if forwardReturn_top50_1Mo > best1Mo:
            #print("Run " + str(counter)+". Setting best1Mo")
            best1Mo = forwardReturn_top50_1Mo
            bestCombo1M = factorCombo


    #print()

    #counter = 1
    for (a, b) in zip(factors, bestCombo3M):
    #    print(counter)
        print("Factor: ", a, " Weight: ", b)
    #    counter = counter+1
    #    pass
    print("BEST 3 Month Factor return {0:,.2f}".format(best3Mo) + "%")
    #print()

    #for (a, b) in zip(factors, bestCombo1M):
    #    print("Factor: ", a, " Weight: ", b)
    #    pass
    # print("BEST 1 Month Factor return {0:,.2f}".format(best1Mo) + "%")

    return bestCombo1M, bestCombo3M


def applyFactorBestFit(df, bestFit):
    v01, v02, v03, v04, v05, v06, v07, v08, v09, v10, v11, v12, v13, v14, v15, v16, v17, v18 = [bestFit[i] for i in (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)]
    df['Factor Total Score'] = (v01 * df["Investment Rank: q-factor Investment to Assets LH"]) \
                               + (v02 * df["Value Rank: Sales to Price HL"]) \
                               + (v03 * df["Value Rank: Earnings to Price HL"]) \
                               + (v04 * df["Value Rank: Enterprise Multiple HL"]) \
                               + (v05 * df["Profitability Rank: q-factor ROE HL"]) \
                               + (v06 * df["Profitability Rank: ROE Conventional HL"]) \
                               + (v07 * df["Profitability Rank: dROE Conventional HL"]) \
                               + (v08 * df["Profitability Rank: dROE Zhang HL"]) \
                               + (v09 * df["Profitability Rank: Gross Profitability Novy-Marx HL"]) \
                               + (v10 * df["Profitability Rank: Gross Profitability Lagged HL"]) \
                               + (v11 * df["Momentum Rank: Momentum 6Mo-2Wk HL"]) \
                               + (v12 * df["Momentum Rank: Momentum 6Mo-1Mo HL"]) \
                               + (v13 * df["Momentum Rank: Momentum 12Mo-1Mo HL"]) \
                               + (v14 * df["Volatility Rank: Volatility 6Mo LT"]) \
                               + (v15 * df["Volatility Rank: Volatility 126D LT"]) \
                               + (v16 * df["Volatility Rank: Volatility 12Mo LT"]) \
                               + (v17 * df["Volatility Rank: Volatility 252D LT"]) \
                               + (v18 * df['Starmine Model Rank Pct'])
    # ascending=False means lowest is the highest score
    df['Factor Total Percentile'] = df['Factor Total Score'].rank(ascending=False, na_option='keep', pct=True)
    df['Rank in Group'] = df.groupby(['TRBC Economic Sector / GICS Sector Code'])['Factor Total Percentile'].rank(ascending=False, method='max', na_option='keep')
    df['Inverse Rank in Group'] = df.groupby(['TRBC Economic Sector / GICS Sector Code'])['Factor Total Percentile'].rank(ascending=True, method='max', na_option='keep')
    df['Count in Group'] = df.groupby('TRBC Economic Sector / GICS Sector Code')['TRBC Economic Sector / GICS Sector Code'].transform('count')
    df['Percentile in Group'] = df['Inverse Rank in Group'] / df['Count in Group']
    return df


def getRandomLoading():
    from numpy import random
    #a = 4
    #b = 2
    #c = 1
    a = 2
    b = 1
    c = 0
    x = round(((random.randint(a + 1) / b) - c), 2)
    return x


if __name__ == '__main__':
    from platform import python_version
    print("Running Python version " + python_version())
    print('EikonBacktestEngine.py - Starting Project Top 50')
    start()


    #priorMonthEnd_String='2015-12-31'
    #df = pd.read_csv('./data/Factor_' + priorMonthEnd_String + '.csv', index_col='RICs')
    #df = createFactors(df)
    #determineFactorBestFit(df)

