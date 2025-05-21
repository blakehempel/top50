
## Known Issues
# Under Armor changed FY time period and broke FQ reporting during that time
# missing sector IDs for some securites/months which breaks sector Rank
# Need to create industry momentum
# need to incorporate Consecutive Increase in Earnings
# Need to incorporate expected growth
# incorporate relative strength https://www.oldschoolvalue.com/book-reviews/what-works-on-wall-street/#:~:text=Perhaps%20one%20of%20the%20best,to%20turn%20%2410%2C000%20into%20%2455%2C002%2C724.
# ROE With Negative Stockholder Equity https://www.nasdaq.com/articles/how-calculate-roe-negative-stockholder-equity-2016-03-19

##COMPELTED
# DONE - EV daily time series data does not exist for Jan 2000. [Use reported EV (TR.F.EV)]
# DONE - Master Price File uses TR.PriceClose exclusively. Some older unlisted stocks only have data for TR.CLOSEPRICE. Therefore volatility is blank [use only CLOSEPRICE]
# DONE - Need to pull industry ID
# DONE - need to incorporate Investment Factor
# DONE - Even worse, a positive ROE when stockholder equity is negative and earnings are negative - SET TO ZERO IS ROE is negative
#Deferred - soln create master SECTOR tracker with as of date? - Inconsistent solution


## q-factor model
'''
described by the sensitivities of its returns
to 4 factors: the market excess return (MKT),
the difference between the return on a portfolio of small size stocks
and the return on a portfolio of big size stocks (rME),
the difference between the return on a portfolio of low investment stocks
and the return on a portfolio of high investment stocks (rI/A),
and the difference between the return on a portfolio of high profitability (return on equity, ROE) stocks
and the return on a portfolio of low profitability stocks (rROE)


From January 1972 to December 2012, the size factor earns an average return of 0.31% per month (t = 2.12);
the investment factor 0.45% (t = 4.95);
and the ROE factor 0.58% (t = 4.81).

The investment factor has a high correlation of 0.69 with HML,
and the ROE factor has a high correlation of 0.50 with the Carhart (1997) momentum factor (up-minus-down, UMD).
The alphas of HML and UMD in the q-factor model are small and insignificant,
but the alphas of the investment and ROE factors in the Carhart model
(that augments the Fama-French model with UMD) are large and significant.
As such, HML and UMD might be noisy versions of the q-factors.


In particular, the q-factor model outperforms the Fama-French and Carhart models in capturing momentum.
The high-minus-low earnings momentum decile has a Fama-French alpha of 0.55% per month
and a Carhart alpha of 0.34%, both of which are significant.



Intuitively, investment predicts returns because given expected cash flows,
high costs of capital imply low net present values of new capital and low
investment, and low costs of capital imply high net present values of new
capital and high investment. ROE predicts returns because high expected ROE
relative to low investment must imply high discount rates. The high discount
rates are necessary to offset the high expected ROE to induce low net present
values of new capital and low investment. If the discount rates were not high
enough, firms would instead observe high net present values of new capital
and invest more. Conversely, low expected ROE relative to high investment
must imply low discount rates. If the discount rates were not low enough to
counteract the low expected ROE, firms would instead observe low net present
values of new capital and invest less




This equation predicts that, all else equal, high investment stocks should earn
lower expected returns than low investment stocks earn, and that, all else equal,
high expected profitability stocks should earn higher expected returns than low
expected profitability stocks earn.

Intuitively, all else equal, firms that have
experienced large positive shocks to earnings tend to be more profitable than
firms that have experienced large negative shocks to earnings.




Factor construction

We measure investment-to-assets, I/A,
as the annual change in total assets (Compustat annual item AT) divided by 1-year-lagged total assets.

We measure profitability as ROE, which is income before extraordinary items (Compustat
quarterly item IBQ) divided by 1-quarter-lagged book equity.9

We construct the q-factors from a triple 2-by-3-by-3 sort on size, I/A, and ROE.

Because both the investment and earnings effects in the data are stronger in small firms
than in big firms (e.g., Bernard and Thomas 1990; Fama and French 2008),
we control for size when constructing the investment and ROE factors.

Sorting jointly with size is also standard in constructing the value factor, HML, and
the momentum factor, UMD. HML is from a double 2-by-3 sort on size and
book-to-market, and UMD is from a double 2-by-3 sort on size and prior 2–12
month returns.

Finally, sorting on investment and ROE independently helps orthogonalize the 2 new factors.


'''

import eikon as ek
import pandas as pd
import datetime as dt
import numpy as np  # NumPy
import math
import dateutil.relativedelta
from dateutil.relativedelta import relativedelta
import time

'''  IMPORTS & CONSTANTS'''
from top50.engine import utilities
import top50.engine.createfactors as cf


ek.set_app_key(utilities.APP_KEY)
#ek.set_app_key('DEFAULT_CODE_BOOK_APP_KEY')

'''
SET VARIABLES
'''
global_startYear = 2000
global_startMonth = 1
global_endYear = 2022
global_endMonth = 12

lastRun = dt.datetime.now()
lastSuccessfulRunYear = 0
lastSuccessfulRunMonth = 0

df_Historical_SPX_Components = pd.DataFrame()
df_SecurityMaster = pd.DataFrame()

df_PriceHistory_v4 = pd.DataFrame()
df_PriceHistoryPivot_v4 = pd.DataFrame()

df_PriceClose = pd.DataFrame()
ignoreSuccessfulRun = False


def MasterLoop(bool_getFundamentalDataFromRefinitiv, bool_buildFactorDataFromFundamental):
    print("Starting MasterLoop with bool_getFundamentalDataFromRefinitiv=" + str(bool_getFundamentalDataFromRefinitiv) + " & bool_buildFactorDataFromFundamental=" + str(bool_buildFactorDataFromFundamental))
    defineGlobalVariables()
    reverseCalendarOrder = False

    global global_startYear, global_startMonth, global_endYear, global_endMonth
    global df_Historical_SPX_Components, df_SecurityMaster, df_PriceHistory_v4
    global lastSuccessfulRunYear, lastSuccessfulRunMonth
    global lastRun, ignoreSuccessfulRun


    if ignoreSuccessfulRun and reverseCalendarOrder is False:
        lastSuccessfulRunYear = 2000
        lastSuccessfulRunMonth = 0

    if reverseCalendarOrder:
        loopStartYear = global_endYear
        loopEndYear = global_startYear
        stepDirection = -1
        loopAdjustment = stepDirection
        print("getFundamentalData: running in reverse calendar order with the following parameters: loopStartYear=" + str(loopStartYear))
    else:
        loopStartYear = global_startYear
        loopEndYear = global_endYear
        stepDirection = 1
        loopAdjustment = stepDirection
        print("getFundamentalData: running in calendar order with the following parameters: loopStartYear=" + str(loopStartYear))

    #loopCount = 0
    for year in range(loopStartYear, loopEndYear + loopAdjustment, stepDirection):
        if reverseCalendarOrder:
            loopStartMonth = 12
            loopEndMonth = 1
            '''Reverse Calendar'''
            if year == loopStartYear:
                loopStartMonth = global_endMonth
                print('Reverse Calendar: Setting loopStartMonth = ' + str(loopStartMonth) + ' for ' + str(year))
            if year == loopEndYear:
                loopEndMonth = global_startMonth
                print('Reverse Calendar: Setting loopEndMonth = ' + str(loopEndMonth) + ' for ' + str(year))
        else:
            loopStartMonth = 1
            loopEndMonth = 12
            '''SET Calendar Conditions'''
            if year == loopStartYear:
                loopStartMonth = global_startMonth
            if year == loopEndYear:
                loopEndMonth = global_endMonth

        for month in range(loopStartMonth, loopEndMonth + loopAdjustment, stepDirection):
            firstOfTheMonth = dt.datetime(year, month, 1)
            analysisDate_String = dt.datetime.strftime(firstOfTheMonth, '%Y-%m-%d')

            '''
            SKIP MONTHS ALREADY CALCULATED
            '''
            if reverseCalendarOrder:
                if (year > lastSuccessfulRunYear) or (year == lastSuccessfulRunYear and month >= lastSuccessfulRunMonth):
                    print("Skipping " + analysisDate_String)
                    continue
                else:
                    print("\nProcessing " + analysisDate_String + " at " + dt.datetime.strftime(dt.datetime.now(), "%H:%M:%S"))
            else:
                if (year < lastSuccessfulRunYear) or (year == lastSuccessfulRunYear and month <= lastSuccessfulRunMonth):
                    print("Reverse Calendar: Skipping " + analysisDate_String)
                    continue
                else:
                    print("\nReverse Calendar: Processing " + analysisDate_String + " at " + dt.datetime.strftime(dt.datetime.now(), "%H:%M:%S"))

            priorMonthEnd = firstOfTheMonth + relativedelta(days=-1)
            priorMonthEnd_String = dt.datetime.strftime(priorMonthEnd, '%Y-%m-%d')

            if bool_getFundamentalDataFromRefinitiv:
                '''
                GET FUNDAMENTAL DATA
                '''
                df = getFundamentalDataFromRefinitiv(firstOfTheMonth)
                df.to_csv('./data/FundamentalData_' + priorMonthEnd_String + '.csv', index=True)
                #df.to_excel('./data/FundamentalData_' + priorMonthEnd_String + '.xlsx', sheet_name=priorMonthEnd_String)

            if bool_buildFactorDataFromFundamental:
                '''
                BUILD FACTOR DATA
                '''
                if bool_getFundamentalDataFromRefinitiv is False:
                    #pick up stored data
                    df = pd.read_csv('./data/FundamentalData_' + priorMonthEnd_String + '.csv', index_col='RICs')
                df = cf.createFactors(df)
                df.to_csv('./data/Factor_' + priorMonthEnd_String + '.csv', index=True)

            print(" Completed with " + analysisDate_String)
            # UPDATE SETTINGS FILE
            lastSuccessfulRunYear = year
            lastSuccessfulRunMonth = month
            update_Utility_Settings()
            # END OF
            #return
        #MONTH FOR LOOP COMPLETE
    #YEAR FOR LOOP COMPLETE
    print("MasterLoop is complete")


def getFundamentalDataFromRefinitiv(firstOfTheMonth):
    global df_Historical_SPX_Components
    #firstOfTheMonth = dt.datetime(2000, 1, 1)
    # SET DATES
    priorMonthEnd = firstOfTheMonth + relativedelta(days=-1)
    priorMonthEnd_String = dt.datetime.strftime(priorMonthEnd, '%Y-%m-%d')
    priorMonthEnd_2WkAgo = priorMonthEnd + relativedelta(weeks=-2)
    priorMonthEnd_2WkAgo_String = dt.datetime.strftime(priorMonthEnd_2WkAgo, '%Y-%m-%d')
    priorMonthEnd_1MoAgo = firstOfTheMonth + relativedelta(months=-1)
    priorMonthEnd_1MoAgo_String = dt.datetime.strftime(priorMonthEnd_1MoAgo, '%Y-%m-%d')
    priorMonthEnd_6MoAgo = firstOfTheMonth + relativedelta(months=-6)
    priorMonthEnd_6MoAgo_String = dt.datetime.strftime(priorMonthEnd_6MoAgo, '%Y-%m-%d')
    priorMonthEnd_12MoAgo = firstOfTheMonth + relativedelta(months=-12)
    priorMonthEnd_12MoAgo_String = dt.datetime.strftime(priorMonthEnd_12MoAgo, '%Y-%m-%d')
    priorMonthEnd_1MoForward = firstOfTheMonth + relativedelta(months=1)
    priorMonthEnd_1MoForward = priorMonthEnd_1MoForward + relativedelta(days=-1)
    priorMonthEnd_1MoForward_String = dt.datetime.strftime(priorMonthEnd_1MoForward, '%Y-%m-%d')
    priorMonthEnd_3MoForward = firstOfTheMonth + relativedelta(months=3)
    priorMonthEnd_3MoForward = priorMonthEnd_3MoForward + relativedelta(days=-1)
    priorMonthEnd_3MoForward_String = dt.datetime.strftime(priorMonthEnd_3MoForward, '%Y-%m-%d')

    print(" starting getFundamentalData for " + priorMonthEnd_String)

    currentRow = df_Historical_SPX_Components.loc[df_Historical_SPX_Components['Dates'] == firstOfTheMonth]
    spx_list = (currentRow.iloc[0, 1])
    df_currentSPX = pd.DataFrame(spx_list)
    df_currentSPX.rename(columns={df_currentSPX.columns[0]: "RICs"}, inplace=True)
    df_currentSPX.set_index(["RICs"], inplace=True)
    df_currentSPX = pd.merge(df_currentSPX, df_SecurityMaster, how="left", left_index=True, right_index=True)

    '''
    GET FUNDAMENTAL DATA
    '''
    df = getEikonEarningsData_Wrapper(spx_list, priorMonthEnd_String)
    df = pd.merge(df_currentSPX, df, how="left", left_index=True, right_index=True)

    '''
    GET SUPPLEMENTAL DATA
    '''
    print(" starting GET SUPPLEMENTAL DATA for " + priorMonthEnd_String)
    if True:
        size_requested = len(spx_list)
        '''
        Retrieving Data - Price Momentum
        '''
        dataFields = [
            'TR.TotalReturn(SDate=' + priorMonthEnd_6MoAgo_String + ',EDate=' + priorMonthEnd_2WkAgo_String + ')'
            , 'TR.TotalReturn(SDate=' + priorMonthEnd_6MoAgo_String + ',EDate=' + priorMonthEnd_1MoAgo_String + ')'
            , 'TR.TotalReturn(SDate=' + priorMonthEnd_12MoAgo_String + ',EDate=' + priorMonthEnd_1MoAgo_String + ')']
        dfMomentum = getEikonAPI(spx_list, dataFields)
        if size_requested != dfMomentum.shape[0]:
            print(dfMomentum)
            print(dfMomentum.shape)
            raise Exception("results Size is Different")
        dfMomentum.columns = ["Instrument", "Momentum 6 Mo, skip 2 Weeks", "Momentum 6 Mo, skip 1 Month", "Momentum 12 Mo, skip 1 Month"]
        dfMomentum.set_index(["Instrument"], inplace=True)
        df = pd.merge(df, dfMomentum, how="left", left_index=True, right_index=True)
        '''
        Retrieving Data - Earnings Momentum
        '''

        # TODO

        '''
        Retrieving Data - Volatility
        '''
        df['Volatility 126D'] = np.nan
        for security in spx_list:
            volatilityValue = getLocal_Volatility_byNumOf_DaysOrMonths(security, priorMonthEnd, 126, True)
            df.loc[security, 'Volatility 126D'] = volatilityValue
            # print("Volatility for " + security + " is "+str(volatilityValue))
        df['Volatility 252D'] = np.nan
        for security in spx_list:
            volatilityValue = getLocal_Volatility_byNumOf_DaysOrMonths(security, priorMonthEnd, 252, True)
            df.loc[security, 'Volatility 252D'] = volatilityValue
            # print("Volatility for " + security + " is "+str(volatilityValue))
        df['Volatility 6Mo'] = np.nan
        for security in spx_list:
            volatilityValue = getLocal_Volatility_byNumOf_DaysOrMonths(security, priorMonthEnd, 6, False)
            df.loc[security, 'Volatility 6Mo'] = volatilityValue
            # print("Volatility for " + security + " is "+str(volatilityValue))
        df['Volatility 12Mo'] = np.nan
        for security in spx_list:
            volatilityValue = getLocal_Volatility_byNumOf_DaysOrMonths(security, priorMonthEnd, 12, False)
            df.loc[security, 'Volatility 12Mo'] = volatilityValue
            # print("Volatility for " + security + " is "+str(volatilityValue))

        '''
        Retrieving Data - GICS Sector Code & Industry Code
        '''
        tempDate = firstOfTheMonth
        while tempDate.weekday() >= 5:
            tempDate = tempDate + relativedelta(days=1)
            # print(tempDate.strftime('%A'))
        tempDate_String = dt.datetime.strftime(tempDate, '%Y-%m-%d')
        dfGICS = pd.DataFrame()
        innerLoopCount = 0
        isSuccess = False
        while not isSuccess:
            dataFields = [
                'TR.CombinedAlphaSectorRank(SDate=' + tempDate_String + ').trbcsector',
                'TR.CombinedAlphaIndustryRank(SDate=' + tempDate_String + ').trbcindustry',
                'TR.CombinedAlphaSectorRank(SDate=' + tempDate_String + ').date',
                'TR.CombinedAlphaSectorRank(SDate=' + tempDate_String + ')',
                'TR.CombinedAlphaIndustryRank(SDate=' + tempDate_String + ')']
            results = getEikonAPI(spx_list, dataFields)
            if size_requested != results.shape[0]:
                raise Exception("results Size is Different")
            results.columns = ["Instrument", "TRBC Economic Sector / GICS Sector Code",
                               "TRBC Industry Group / GICS Industry Code", "TRBC / GICS Code Date",
                               "Combined Alpha Model Sector Rank", "Combined Alpha Model Industry Rank"]
            results.set_index(["Instrument"], inplace=True)
            numberOfNaN = results["TRBC Economic Sector / GICS Sector Code"].isna().sum()
            if numberOfNaN < (size_requested / 2):
                isSuccess = True
                dfGICS = results.copy()
            else:
                '''excessive NaN'''
                tempDate = tempDate + relativedelta(days=1)
                tempDate_String = dt.datetime.strftime(tempDate, '%Y-%m-%d')
                time.sleep(1)
                if innerLoopCount < 10:
                    print("Excessive NaN Returned querying GICS: Trying " + tempDate_String)
                else:
                    print("Can Not find GICS Sector Code!")
                    raise Exception("Can Not find GICS Sector Code!")
            innerLoopCount = innerLoopCount + 1

        dfGICS = dfGICS.reset_index()
        dfGICS.set_index(["Instrument"], inplace=True)
        df = pd.merge(df, dfGICS, how="left", left_index=True, right_index=True)
        '''
        Individual Performance
        '''
        dataFields = [
            'TR.TotalReturn(SDate=' + priorMonthEnd_String + ',EDate=' + priorMonthEnd_1MoForward_String + ')'
            , 'TR.TotalReturn(SDate=' + priorMonthEnd_String + ',EDate=' + priorMonthEnd_3MoForward_String + ')']

        df_PortfolioReturns = getEikonAPI(spx_list, dataFields)
        if size_requested != df_PortfolioReturns.shape[0]:
            raise Exception("results Size is Different")
        df_PortfolioReturns.columns = ["Instrument", "1 Month Forward Return", "3 Month Forward Return"]
        df_PortfolioReturns['Return From EOD'] = priorMonthEnd_String
        df_PortfolioReturns = df_PortfolioReturns[
            ["Instrument", 'Return From EOD', "1 Month Forward Return", "3 Month Forward Return"]]
        df_PortfolioReturns.set_index(["Instrument"], inplace=True)
        df = pd.merge(df, df_PortfolioReturns, how="left", left_index=True, right_index=True)

    '''
    Use Existing Factor Data
    '''
    if False:
        try:
            df_performance = pd.read_csv('zMarketData_' + priorMonthEnd_String + '.csv')
            df_performance = df_performance[
                ["RICs", "Momentum 6 Mo, skip 2 Weeks", "Momentum 6 Mo, skip 1 Month", "Volatility 6Mo",
                 "TRBC Economic Sector / GICS Sector Code", "Return From EOD", "1 Month Forward Return",
                 "3 Month Forward Return"]]
            df_performance.columns = ["Instrument", "Momentum 6 Mo, skip 2 Weeks", "Momentum 6 Mo, skip 1 Month",
                                      "Volatility 6Mo", "TRBC Economic Sector / GICS Sector Code", "Return From EOD",
                                      "1 Month Forward Return", "3 Month Forward Return"]
            df_performance.set_index(['Instrument'], inplace=True)
            print("Printing performance")
            print(df_performance)

            df = pd.merge(df, df_performance, how="left", left_index=True, right_index=True)
            # df.to_excel('aaa.xlsx')
        except FileNotFoundError as err:
            print(err)
            print("Existing file not found for 'zMarketData_" + priorMonthEnd_String + ".csv Requesting data from EIKON")
            useExistingData=False

    df.index.name = 'RICs'
    return df


def getEikonEarningsData_Wrapper(spx_list, analysisDate_String):
    global lastRun
    currentTime = dt.datetime.now()
    delta = currentTime - lastRun
    if delta.total_seconds() < 1.0:
        sleepTime = 1.0
        # delta.total_seconds()
        time.sleep(sleepTime)
    isSuccess = False
    while not isSuccess:
        try:
            results = getEikonEarningsData(spx_list, analysisDate_String)
            return results
        except ek.EikonError as err:
            if err.code == 400:
                print("Exception 400 occurred: " + str(err.message))
                time.sleep(5)
            elif err.code == 408:
                print("Exception 408 (HTTP TimeoutException) occurred: " + str(err.message))
                time.sleep(5)
            else:
                print("Printing df causing error:")
                print(results)
                raise Exception(f'Eikon error {err.code}\n{err.args}\n{err.message}')


#Does not use wrapper for Eikon get_data, therefore currently needs custom wrapper
def getEikonEarningsData(spx_list, analysisDate_String):
    print(" starting getEikonEarningsData for " + analysisDate_String)
    '''
    Market Cap & EV
    '''
    df_market, err = ek.get_data(instruments=spx_list,
                                 fields=['TR.EV', 'TR.F.EV(Period=FQ0)', 'TR.CompanyMarketCap'],
                                 parameters={'SDate': analysisDate_String,
                                             'Scale': '6'})
    df_market.set_index(['Instrument'], inplace=True)
    df_market['Enterprise Value (Daily Time Series)'] = df_market['Enterprise Value (Daily Time Series)'].astype(np.float64)
    df_market['Enterprise Value'] = df_market['Enterprise Value'].astype(np.float64)
    df_market['EV Merged'] = df_market['Enterprise Value (Daily Time Series)']
    df_market['EV Merged'] = df_market['EV Merged'].fillna(df_market['Enterprise Value'])
    # df = pd.merge(df, df_market, left_index=True, right_index=True)
    df = df_market

    time.sleep(0.25)
    df_earningsRelease, err = ek.get_data(instruments=spx_list,
                                          fields=[
                                              'TR.F.TotShHoldEq.periodenddate',
                                              'TR.F.OriginalAnnouncementDate',
                                              'TR.F.OPPROFBEFNONRECURINCEXPN',  # Enterprise Multiple
                                              'TR.F.DEPRDEPLAMORTTOT',  # Enterprise Multiple
                                              'TR.F.TOTREVENUE',  # Sales to Price
                                              'TR.F.INCAVAILTOCOMSHR',  # Net Income to Common Shares - Conventional ROE
                                              'TR.F.TotShHoldEq',  # Shareholder Equity - ROE (Conventional & Zhang)
                                              'TR.F.GROSSPROFINDPROPTOT',
                                              # Gross Profits Novy-Marx & Gross Profits lagged
                                              'TR.F.TOTASSETS',  # Gross Profits - Novy-Marx
                                              'TR.F.INCBEFDISCOPSEXORDITEMS',
                                              # Income before Extraordinay Items - Earnings to Price & ROE Zhang
                                              'TR.F.EPSDILINCLEXORDITEMSCOMTOT'
                                              # Firms with non-positive earnings are excluded.
                                          ],
                                          parameters={'SDate': analysisDate_String,
                                                      'Period': 'FQ0',
                                                      'Scale': '6'})
    df_earningsRelease.set_index(['Instrument'], inplace=True)
    df = pd.merge(df, df_earningsRelease, left_index=True, right_index=True)

    time.sleep(0.25)
    df_lagged, err = ek.get_data(spx_list, ['TR.F.TOTASSETS(SDate=' + analysisDate_String + ',Period=FQ-1,Scale=6)',
                                            'TR.F.TOTASSETS(SDate=' + analysisDate_String + ',Period=FQ-5,Scale=6)',
                                            'TR.F.TotShHoldEq(SDate=' + analysisDate_String + ',Period=FQ-1,Scale=6)',
                                            'TR.F.TotShHoldEq(SDate=' + analysisDate_String + ',Period=FQ-4,Scale=6)',
                                            'TR.F.TotShHoldEq(SDate=' + analysisDate_String + ',Period=FQ-5,Scale=6)',
                                            'TR.F.INCBEFDISCOPSEXORDITEMS(SDate=' + analysisDate_String + ',Period=FQ-4,Scale=6)',
                                            'TR.F.INCAVAILTOCOMSHR(SDate=' + analysisDate_String + ',Period=FQ-4,Scale=6)'])
    df_lagged.columns = ["Instrument",
                         "Lagged: FQ-1 Total Assets",  # gross profit lagged
                         "Lagged: FQ-5 Total Assets",  # gross profit lagged
                         "Lagged FQ-1: Total Shareholders\' Equity incl Minority Intr & Hybrid Debt",  # ROE zhang
                         "Lagged FQ-4: Total Shareholders\' Equity incl Minority Intr & Hybrid Debt",  # delta ROE
                         "Lagged FQ-5: Total Shareholders\' Equity incl Minority Intr & Hybrid Debt",  # delta ROE
                         "Lagged FQ-4: Income before Discontinued Operations & Extraordinary Items",  # delta ROE
                         "Lagged FQ-4: Income Available to Common Shares"]  # delta ROE
    df_lagged.set_index(['Instrument'], inplace=True)
    df = pd.merge(df, df_lagged, left_index=True, right_index=True)

    # df.to_excel('aaa.xlsx')
    print(" Complete getEikonEarningsData for " + analysisDate_String)
    # print(df)
    return df


# Normal Wrapper for get_Data calls
def getEikonAPI(securityList, dataFields):
    global lastRun
    currentTime = dt.datetime.now()
    delta = currentTime - lastRun
    if delta.total_seconds() < 0.5:
        sleepTime = 0.5
        # delta.total_seconds()
        time.sleep(sleepTime)
    isSuccess = False
    while not isSuccess:
        try:
            lastRun = dt.datetime.now()
            results, err = ek.get_data(securityList, dataFields)
            return results
        except ek.EikonError as err:
            if err.code == 400:
                print("Exception 400 occurred: " + str(err.message))
                time.sleep(5)
            elif err.code == 408:
                print("Exception 408 (HTTP TimeoutException) occurred: " + str(err.message))
                time.sleep(5)
            else:
                print("Printing df causing error:")
                print(results)
                raise Exception(f'Eikon error {err.code}\n{err.args}\n{err.message}')


def read_Historical_ConstituentsFromCSV():
    global df_Historical_SPX_Components
    df_Historical_SPX_Components = pd.read_csv("Historical_SPX_Constituents_sinceJan2000wIndex.csv", converters={
        "Index Constituents": lambda x: x.strip("[]").replace("\'", "").split(", ")})
    df_Historical_SPX_Components.rename(columns={df_Historical_SPX_Components.columns[0]: "Dates"}, inplace=True)
    df_Historical_SPX_Components['Dates'] = df_Historical_SPX_Components['Dates'].astype(str).apply(
        lambda _: dt.datetime.strptime(_, '%Y-%m-%d'))
    df_Historical_SPX_Components = df_Historical_SPX_Components.iloc[::-1]
    # print(df_Historical_SPX_Components)
    # print(df_Historical_SPX_Components)
    print(" Loaded read_Historical_Constituents")
    return df_Historical_SPX_Components


def get_Historical_ConstituentsFromRefinitiv():
    global df_Historical_SPX_Components

    ic, err = ek.get_data('.SPX', ['TR.IndexConstituentRIC'])
    lj, err = ek.get_data('.SPX',
                          ['TR.IndexJLConstituentChangeDate',
                           'TR.IndexJLConstituentRIC.change',
                           'TR.IndexJLConstituentRIC'],
                          {'SDate': '0D', 'EDate': '-276M', 'IC': 'B'})
    lj['Date'] = pd.to_datetime(lj['Date']).dt.date
    lj.sort_values(['Date', 'Change'], ascending=False, inplace=True)
    dates = [dt.date(2000, 1, 1)]
    i = 0
    while (dates[0] + dateutil.relativedelta.relativedelta(months=+i + 1)) < dt.date.today():
        dates.append(dates[0] + dateutil.relativedelta.relativedelta(months=+i + 1))
        i = i + 1
    dates.append(dt.date.today())
    df_Historical_SPX_Components = pd.DataFrame(index=dates, columns=['Index Constituents'])
    ic_list = ic['Constituent RIC'].tolist()
    for i in range(len(dates)):
        print(str(dates[len(dates) - i - 1]))
        df_Historical_SPX_Components.at[dates[len(dates) - i - 1], 'Index Constituents'] = ic_list[:]
        for j in lj.index:
            if lj['Date'].loc[j] <= dates[len(dates) - i - 1]:
                if lj['Date'].loc[j] > dates[len(dates) - i - 2]:
                    if lj['Change'].loc[j] == 'Joiner':
                        print('Removing ' + lj['Constituent RIC'].loc[j])
                        ic_list.remove(lj['Constituent RIC'].loc[j])
                    elif lj['Change'].loc[j] == 'Leaver':
                        print('Adding ' + lj['Constituent RIC'].loc[j])
                        ic_list.append(lj['Constituent RIC'].loc[j])
                else:
                    break
    # Observe the result
    # df_Historical_SPX_Components

    # df.to_excel("Historical_SPX_Constituents_sinceJan2000.xlsx")
    # df_Historical_SPX_Components.to_csv('alpha.csv',index=True)

    # Reverse rows using iloc() Function
    df_Historical_SPX_Components = df_Historical_SPX_Components.iloc[::-1]
    print(df_Historical_SPX_Components)


def readSecurityMasterFileCSV():
    global df_SecurityMaster
    df_SecurityMaster = pd.read_csv("SecurityMaster.csv")
    #print(df_SecurityMaster)
    df_SecurityMaster = df_SecurityMaster.sort_values(['RICs'], ascending=True)
    #print(df_SecurityMaster)
    df_SecurityMaster.set_index(["RICs"], inplace=True)
    #print(df_SecurityMaster)
    print(" Loaded SecurityMaster.csv")
    # print(df_SecurityMaster)
    return df_SecurityMaster


def buildPriceHistoryVersion4():
    print("RUNNING buildPriceHistoryVersion4")
    global df_SecurityMaster, df_PriceHistory_v4, lastRun
    readSecurityMasterFileCSV()
    df_PriceHistory_v4 = pd.DataFrame()
    rics_list = df_SecurityMaster.index.values.tolist()
    #isin_list = df_SecurityMaster['ISIN'].tolist()
    counter = 0
    for ric in rics_list:
        counter = counter + 1
        isSuccess = False
        innerCount = 0
        df = pd.DataFrame()
        while not isSuccess:
            innerCount = innerCount + 1
            if innerCount > 5:
                raise Exception('EXCESSIVE LOOPING')
            try:
                #edate = '2023-02-28'
                currentTime = dt.datetime.now()
                delta = currentTime - lastRun
                print(" Loop " + str(counter) + ". " + str(round(delta.total_seconds(), 1)) + " sec delay. Getting price history for " + str(ric))
                if delta.total_seconds() < 0.5:
                    sleepTime = 0.5 - delta.total_seconds()
                    delta.total_seconds()
                    time.sleep(sleepTime)
                lastRun = dt.datetime.now()
                dataFields = ['TR.CLOSEPRICE(SDate=1999-1-1,EDate=2023-02-28,Adjusted=1,CALCMETHOD=CLOSE,FILL=NONE).date',
                              'TR.CLOSEPRICE(SDate=1999-1-1,EDate=2023-02-28,Adjusted=1,CALCMETHOD=CLOSE,FILL=NONE)']
                # dataFields = ['TR.PriceClose(SDate=1999-1-1,EDate=2023-02-28).date',
                #              'TR.PriceClose(SDate=1999-1-1,EDate=2023-02-28)']
                df, err = ek.get_data("'" + ric + "'", dataFields)
                runPriceClose = False
                if len(df.index) == 1:
                    df = df.dropna()
                if df.empty:
                    print("Empty Dataframe Returned for " + ric + " via TR.CLOSEPRICE trying alternate")
                    dataFields = ['TR.PriceClose(SDate=1999-1-1,EDate=2023-02-28).date',
                                  'TR.PriceClose(SDate=1999-1-1,EDate=2023-02-28)']
                    df, err = ek.get_data("'" + ric + "'", dataFields)
                    if len(df.index) == 1:
                        df = df.dropna()
                    if df.empty:
                        print("Empty Dataframe Returned for " + ric + " via TR.PriceClose. Break loop.")
                        break
                        # raise Exception("Empty Dataframe Returned for " + rics)
                    #TODO testing
                    global df_PriceClose
                    df_PriceClose = pd.concat([df_PriceClose, df], verify_integrity=True)
                isSuccess = True
                # df.columns = ["RICs", "Price Close Date", "Price Close", "Close Price Date", "Close Price"]
                df.columns = ["RICs", "Close Price Date", "Close Price"]
                df = df.dropna(subset=['Close Price'])
                df = df.drop_duplicates(subset=["RICs", "Close Price Date"], keep='last')
                df.set_index(["RICs", "Close Price Date"], inplace=True)
                ####
                print(df.head(5))
                #print(df.info())
            except ek.EikonError as err:
                if err.code == 400:
                    print("Exception occurred: " + str(err.code) + "\n" + str(err.message))
                    time.sleep(5)
                    print("Error Sleep complete... resuming hopefully!")
                elif err.code == 408:
                    print("Exception 408 (HTTP TimeoutException) occurred: " + str(err.message))
                    time.sleep(5)
                else:
                    print(df)
                    time.sleep(1)
                    raise Exception(f'Eikon error {err.code}\n{err.args}\n{err.message}')
        # end of while loop
        try:
            df_PriceHistory_v4 = pd.concat([df_PriceHistory_v4, df], verify_integrity=True)
        except Exception as e:
            print(e)
            print("verify_integrity failed. Saving df and continuing")
            df.to_csv('failed_ric_'+ric+'.csv')
            print("Saving df_PriceHistory_v4")
            df_PriceHistory_v4.to_csv("PriceHistoryVersion4_RawDataFile" + str(counter) + ".csv")
            raise Exception(e)
        #if counter % 100 == 0:
            #print("Loop " + str(counter) + " is complete. Saving progress...")
            #df_PriceHistory_v4.to_csv("PriceHistoryVersion4_RawDataFile" + str(counter) + ".csv")
            #print("BREAK!!")
            #return
    # end of for loop
    print("LOOP COMPLETE saving PriceHistoryVersion4_RawDataFile.csv")
    df_PriceHistory_v4.to_csv("PriceHistoryVersion4_RawDataFile.csv")

    '''
    OPTION 1: 
    KEEP ONLY Close Price AND Date FIELDS SINCE IT APPEARS MORE COMPLETE
    '''
    # cleanPriceHistory_v3()

    '''
    OPTION 2:
    COMBINE BOTH DATASETS AND DROP nan
    OUTER JOIN BOTH DATE COLUMNS, OUTER-JOIN BOTH CLOSE COLUMNS
    REMOVE NA

    '''
    print("*** Job Complete - buildPriceHistoryVersion2 *** ")
    return df_PriceHistory_v4


def createPivotTable_v4():
    global df_PriceHistoryPivot_v4, df_PriceHistory_v4
    print("Creating Pivot")
    df_PriceHistoryPivot_v4 = df_PriceHistory_v4.copy()
    df_PriceHistoryPivot_v4 = df_PriceHistoryPivot_v4.reset_index()
    df_PriceHistoryPivot_v4['Close Price Date'] = pd.to_datetime(df_PriceHistoryPivot_v4['Close Price Date'])
    #print(df_PriceHistoryPivot_v4.info())
    df_PriceHistoryPivot_v4 = df_PriceHistoryPivot_v4.pivot(index='Close Price Date', columns='RICs', values='Close Price')
    print(" Created PriceHistory Pivot Table Version 4")
    return df_PriceHistoryPivot_v4


def readPriceHistory_v4_Cleaned():
    global df_PriceHistory_v4
    df_PriceHistory_v4 = pd.read_csv("PriceHistoryVersion4_CleanDataFile.csv")
    print(" Loaded PriceHistoryVersion4_CleanDataFile.csv")
    df_PriceHistory_v4.set_index(["RICs", "Close Price Date"], inplace=True)
    df_PriceHistory_v4['Close Price'] = df_PriceHistory_v4['Close Price'].astype(float)
    print('CleanedDataFile Loaded')
    return df_PriceHistory_v4


def readPriceHistory_v4_Raw():
    global df_PriceHistory_v4
    df_PriceHistory_v4 = pd.read_csv("PriceHistoryVersion4_RawDataFile.csv")
    print(" Loaded PriceHistoryVersion4_RawDataFile.csv")
    df_PriceHistory_v4.set_index(["RICs", "Close Price Date"], inplace=True)
    df_PriceHistory_v4['Close Price'] = df_PriceHistory_v4['Close Price'].astype(float)
    print('RawDataFile Loaded')
    return df_PriceHistory_v4


def cleanPriceHistory_v4():
    global df_PriceHistory_v4
    # clean data
    df_PriceHistory_v4 = df_PriceHistory_v4.reset_index()
    # df_PriceHistory_v2['Merged Close'] = df_PriceHistory_v2['Close Price']
    # df_PriceHistory_v2['Merged Close Date'] = df_PriceHistory_v2['Close Price Date']
    # df_PriceHistory_v2['Merged Close']=df_PriceHistory_v2['Merged Close'].fillna(df_PriceHistory_v2['Price Close'])
    # df_PriceHistory_v2['Merged Close Date']=df_PriceHistory_v2['Merged Close Date'].fillna(df_PriceHistory_v2['Price Close Date'])

    #following commented code was needed prior to buildPriceHistoryVersion4
    #df_PriceHistory_v4['Close Price'] = df_PriceHistory_v4['Close Price'].fillna(df_PriceHistory_v4['Price Close'])
    #df_PriceHistory_v4['Close Price Date'] = df_PriceHistory_v4['Close Price Date'].fillna(df_PriceHistory_v4['Price Close Date'])

    #df_PriceHistory_v4 = df_PriceHistory_v4.drop('Price Close', axis='columns')
    #df_PriceHistory_v4 = df_PriceHistory_v4.drop('Price Close Date', axis='columns')

    df_PriceHistory_v4 = df_PriceHistory_v4[df_PriceHistory_v4['Close Price Date'].notna()]
    df_PriceHistory_v4 = df_PriceHistory_v4[df_PriceHistory_v4['Close Price'].notna()]
    df_PriceHistory_v4 = df_PriceHistory_v4.drop_duplicates(subset=["RICs", "Close Price Date"], keep='last')
    df_PriceHistory_v4.set_index(["RICs", "Close Price Date"], inplace=True)
    print("clean data COMPLETE saving PriceHistoryVersion4_CleanDataFile.csv")
    df_PriceHistory_v4.to_csv("PriceHistoryVersion4_CleanDataFile.csv")


def getLocal_Volatility_byNumOf_DaysOrMonths(securityRIC, analysisEndDate, numberOfPeriods, dayTrue_monthFalse):
    global df_PriceHistoryPivot_v4, df_SecurityMaster
    originalAnalysisDate = analysisEndDate
    tryCount = 0
    isSuccess = False
    #isin = df_SecurityMaster.loc[securityRIC, 'ISIN']
    while not isSuccess:
        try:
            tryCount = tryCount + 1
            df = df_PriceHistoryPivot_v4[securityRIC].copy()
            df = df.dropna()
            df.index = pd.to_datetime(df.index).tz_localize(None)
            df = df.reset_index()
            df.columns = ['Close Price Date', 'Close Price']
            df['pct_change'] = df['Close Price'].pct_change()
            # Use -1 for descending and +1 for ascending dates
            df['log_change'] = np.log(df['Close Price'] / df['Close Price'].shift(1))
            #TODO save the calculated values
            #print(df)
            '''Need to save the calculated values.'''
            if dayTrue_monthFalse:
                df_lastXperiods = df[(df['Close Price Date'] <= analysisEndDate)].tail(numberOfPeriods)
            else:
                start_date = analysisEndDate + relativedelta(months=-numberOfPeriods)
                mask = (df['Close Price Date'] > start_date) & (df['Close Price Date'] <= analysisEndDate)
                df_lastXperiods = df.loc[mask]
            df_lastXperiods = df_lastXperiods.dropna()
            volatility = np.nan
            if df_lastXperiods.empty:
                return np.nan
            else:
                volatility = df_lastXperiods['log_change'].std() * math.sqrt(252)  # annualized volatilities
                volatility = round(volatility, 4)
                isSuccess = True
                return volatility
        except KeyError as keyerr:
            if tryCount > 7:
                print("Volatility: KeyError on " + securityRIC + " " + dt.datetime.strftime(originalAnalysisDate, '%Y-%m-%d'))
                # raise Exception(keyerr)
                return np.nan
            else:
                '''Market was closed at EOM. Try day before'''
                analysisEndDate = analysisEndDate + relativedelta(days=-1)
        except TypeError as typeerr:
            print("Volatility: TypeError on " + securityRIC + " " + dt.datetime.strftime(originalAnalysisDate, '%Y-%m-%d') + " " + str(typeerr))
            return np.nan
        except Exception as err:
            print("Exception on " + securityRIC + " " + dt.datetime.strftime(analysisEndDate, '%Y-%m-%d'))
            raise Exception(err)
    return np.nan


def defineGlobalVariables():
    print("Setting Global Variables")
    global lastSuccessfulRunYear, lastSuccessfulRunMonth
    utilities.read_Settings()
    lastSuccessfulRunYear = int(utilities.df_Settings.loc['lastSuccessfulRunYear', 'Value'])
    lastSuccessfulRunMonth = int(utilities.df_Settings.loc['lastSuccessfulRunMonth', 'Value'])
    print(" SETTINGS FILE: Last Successful Run " + str(lastSuccessfulRunMonth) + "/" + str(
        lastSuccessfulRunYear))

    global df_Historical_SPX_Components
    df_Historical_SPX_Components = read_Historical_ConstituentsFromCSV()

    global df_SecurityMaster
    df_SecurityMaster = readSecurityMasterFileCSV()

    global df_PriceHistory_v4
    df_PriceHistory_v4 = readPriceHistory_v4_Cleaned()

    global df_PriceHistoryPivot_v4
    df_PriceHistoryPivot_v4 = createPivotTable_v4()
    print("Global Variables Complete")


def update_Utility_Settings():
    utilities.df_Settings.loc['lastSuccessfulRunYear', 'Value'] = lastSuccessfulRunYear
    utilities.df_Settings.loc['lastSuccessfulRunMonth', 'Value'] = lastSuccessfulRunMonth
    utilities.write_Settings()


def start():
    print('Starting EikonDataLoader')
    global ignoreSuccessfulRun
    ignoreSuccessfulRun = False

    requestFundamentalDataFromRefinitiv = True
    bool_buildFactorData = True
    MasterLoop(requestFundamentalDataFromRefinitiv, bool_buildFactorData)


    print('End of EikonDataLoader')



