import os
import pandas as pd
import datetime as dt
import numpy as np  # NumPy
import math
import dateutil.relativedelta
from dateutil.relativedelta import relativedelta
import time
import seaborn as sns
import matplotlib.pyplot as plt

class ResearchEngineParameters():
    """
    researchEngineParameters is a class that represents a strategy.
    """

    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters
        print(f"ResearchEngineParameters {name} initialized with parameters: \n{parameters}")


class ResearchEngine():
    initialized = False
    """
    ResearchEngine is a class that simulates the execution of historical factor strategies. 
    """

    '''
    SET DEFAULT VARIABLES
    '''
    startYear = 2000
    startMonth = 1
    endYear = 2022
    endMonth = 11

    quarterlyAnalysis = True
    analysisFrequency = 3
    sectorNeutralize = True
    displayInterPeriodResults = False

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

    df_portfolio = pd.DataFrame()
    df_spxtr = pd.DataFrame()


    def __init__(self, researchEngineParameters = None ):

        self.config = ResearchEngine.read_configuration()
        if self.config is None:
            exit(1)

        self.startYear = bool(self.config.loc['start_year'].values[0])
        self.startMonth = bool(self.config.loc['start_month'].values[0])
        self.endMonth = bool(self.config.loc['end_month'].values[0])
        self.endYear = bool(self.config.loc['end_year'].values[0])    
        self.quarterlyAnalysis = bool(self.config.loc['quarterlyAnalysis'].values[0])
        if self.quarterlyAnalysis:
            self.analysisFrequency = 3
        else:
            self.analysisFrequency = 1
        self.sectorNeutralize = bool(self.config.loc['sectorNeutralize'].values[0])
        self.rebalanceDragInBPS = self.config.loc['rebalanceDragInBPS'].values[0]
        print("ResearchEngine initialized with configuration.csv\n", self.config,"\n")
        self.results = None
        

    @staticmethod
    def read_configuration():
        """
        Reads the configuration.csv file into a Pandas DataFrame.
        """
        import pandas as pd
        import os
    
        current_directory = os.getcwd()
        config_path = os.path.join('top50', 'configuration.csv')  # or specify a full path if needed
        full_path = os.path.join(current_directory, config_path)
    
        try:
            df = pd.read_csv(full_path)
            df = df.set_index('parameters')
            #print("Configuration loaded successfully:")
            #print(df)
            return df
        except FileNotFoundError:
            print(f"Error: The file '{full_path}' was not found.")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
       
    def run(self):
        print("Running ResearchEngine.")
        startYear = self.startYear
        startMonth = self.startMonth
        endMonth = self.endMonth
        endYear = self.endYear

        rebalanceDragInBPS = self.rebalanceDragInBPS
        analysisFrequency = self.analysisFrequency
        displayPeriodResults = self.displayPeriodResults
        sectorNeutralize = self.sectorNeutralize
        quarterlyAnalysis = self.quarterlyAnalysis
        oneMillion = self.oneMillion

 
        global forwardPortfolioValue_SPXTR, forwardReturn_SPXTR, periodReturn_SPXTR, totalReturn_SPXTR, maxValue_SPXTR, maxDrawDown_SPXTR, forwardIndexValue_SPXTR, startIndexValue_SPXTR, currentIndexValue_SPXTR
        global currentPortfolioValue_top50, forwardReturn_top50, periodReturn_top50, totalReturn_top50, maxValue_top50, maxDrawDown_top50, forwardPortfolioValue_top50
        global parameterNarrative, portfolioPeriodReturns, sp500TRPeriodReturns, portfolioSize, currentPortfolioHoldings, marketHedge, marketMomentum, priorMonthEnd_String, usePriorPeriodBestFit,marketRiskOff, riskOffModifier
        
        ''' GET SXP Total Return Data'''
        current_directory = os.getcwd()
        config_path = os.path.join('top50', 'data', 'SXPTR_monthly.csv')  # or specify a full path if needed
        full_path = os.path.join(current_directory, config_path)
        df_spxtr = pd.read_csv(full_path, index_col='Calc Date', parse_dates=True)
        df_spxtr = df_spxtr.sort_index(ascending=True)
        df_spxtr['SMA15'] = df_spxtr['Price Close'].rolling(15).mean()
        print("Full S&P 500 TR data has been loaded.\n", df_spxtr.head(5))
        
        
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
                loopStartMonth = startMonth
            if year == endYear:
                loopEndMonth = endMonth

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


                '''GET FACTOR DATA'''
                current_directory = os.getcwd()
                config_path = os.path.join('top50', 'data','factor', 'Factor_' + priorMonthEnd_String + '.csv')  # or specify a full path if needed
                full_path = os.path.join(current_directory, config_path)
                df = pd.read_csv(full_path, index_col='RICs')
                df = df[~df.index.duplicated(keep='first')]
                
                print('Factor data loaded for ' + priorMonthEnd_String)
                print(df.head(5))
                exit(0)
                
                #df = createFactors(df)
                df = setFactorParameters(df)
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
                        df = setFactorParameters(df)
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
        deltaDate = relativedelta(forwardDate, dt.datetime(startYear, startMonth, 1))
        deltaYears = (1 + deltaDate.months + deltaDate.years * 12)/12
        #print("deltaYears " +str(deltaYears))
        cagrPortfolio = (((forwardPortfolioValue_top50 / oneMillion) ** (1/deltaYears)) - 1)*100
        cagrSPXTR = (((forwardPortfolioValue_SPXTR / oneMillion) ** (1 / deltaYears)) - 1) * 100
        print(" Portfolio Value $" + "{0:,.0f}".format(forwardPortfolioValue_top50)+ " vs. S&P500 $" + "{0:,.0f}".format(forwardPortfolioValue_SPXTR))
        print(" Compound Annual Growth Rate (CAGR) is " + "{0:,.1f}".format(cagrPortfolio)+"% vs. S&P500 " + "{0:,.1f}".format(cagrSPXTR)+"%")
        print(" Total Return {0:,.0f}".format(totalReturn_top50) + "% vs. S&P500 {0:,.0f}".format(totalReturn_SPXTR) + "%")
        print(" Max Drawdown {0:,.0f}".format(maxDrawDown_top50 * 100) + "% vs. S&P500 {0:,.0f}".format(maxDrawDown_SPXTR * 100) + "%")
        print(" Time Period: " + str(startYear) + "-"+str(startMonth) + "-1 to " + forwardDate_String)

        #df.to_csv("BacktestResults.csv")
        dfPerformance=pd.DataFrame(listPerformance, columns=['Date', 'Top50', 'SPXTR'])
        dfPerformance.set_index('Date', inplace=True)

        #listSave = [strMetrics, strTimePeriod, top50TotalReturn, top50MaxDrawdown * 100]
        #dfSave = pd.DataFrame(listSave)
        # dfSave.columns["TimePeriod","Factors","Results","MaxDrawdown"]
        #dfSave.to_csv("BacktestResults.csv")
        return dfPerformance



if __name__ == "__main__":
    rse = ResearchEngine()
    rse.setFactors()
    rse.run()
