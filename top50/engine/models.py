



class Models():
    
    def __init__(self):
       pass

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




        setBloombergModel = False
        setModernBloomberg = False

        setWarrenBuffett = False
        setBuffettPedersen = False
        setModernBuffett = False

        setHempelModel_v1 = False
        setHempelModel_v2 = False
        setHempelModel_v3 = False
        setHempelModel_v4 = False
        setHempelModel_v5 = False
        setHempelModel_v6 = False
        setHempelModel_v7 = False
        setHempelModel_v8 = False
        setHempelModel_v9 = False
        setHempelModel_v10 = False
        setHempelModel_v11 = False
        setHempelModel_v12 = False
        setHempelModel_v13 = True
        setHempelModel_v14 = False
        setHempelModel_v15 = False




        if setBloombergModel:
            parameterNarrative = 'Bloomberg Top 50 Portfolio 2022 - Equal Weight Investment, Profitability, Low Volatility, Momentum'
            #Description: Equal Weight Value, profitability, Momentum, Volatility
            df['Factor Total Score'] = df["Value Rank: Sales to Price HL"] \
                                    + df["Profitability Rank: ROE Conventional HL"] \
                                    +df["Momentum Rank: Momentum 6Mo-2Wk HL"] \
                                    +df["Volatility Rank: Volatility 126D LT"]
            pass
        elif setModernBloomberg:
            parameterNarrative = "Revised Bloomberg Factors - Equal Weight Investment, Profitability, Low Volatility, Momentum"
            df['Factor Total Score'] = df["Investment Rank: q-factor Investment to Assets LH"] \
                                    + df["Profitability Rank: ROE Conventional HL"] \
                                    + df["Volatility Rank: Volatility 126D LT"] \
                                    + df["Momentum Rank: Momentum 6Mo-2Wk HL"]
            pass

        elif setWarrenBuffett:
            parameterNarrative = "Buffett Factors, Equal Weight - Value, Profitability, Low Volatility"
            df['Factor Total Score'] = df["Value Rank: Sales to Price HL"] \
                                    + df["Profitability Rank: ROE Conventional HL"] \
                                    + df["Volatility Rank: Volatility 126D LT"]
            pass
        elif setBuffettPedersen:
            parameterNarrative = "Buffett Factors, Pedersen Weight - Value (.34), Profitability (.49), Low Volatility (.17)"
            valueLoading = 0.34
            profitabilityLoading = 0.49
            volatilityLoading = 0.17
            df['Factor Total Score'] = (valueLoading * df["Value Rank: Sales to Price HL"]) \
                                    + (profitabilityLoading * df["Profitability Rank: ROE Conventional HL"]) \
                                    + (volatilityLoading * df["Volatility Rank: Volatility 126D LT"])
            pass
        elif setModernBuffett:
            parameterNarrative = "Revised Buffett Factors - Equal Weight Investment, Profitability, Low Volatility"
            df['Factor Total Score'] = df["Investment Rank: q-factor Investment to Assets LH"] \
                                    + df["Profitability Rank: ROE Conventional HL"] \
                                    + df["Volatility Rank: Volatility 126D LT"]
            pass

        elif setHempelModel_v1:
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
        elif setHempelModel_v2:
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
        elif setHempelModel_v3:
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
        elif setHempelModel_v4:
            parameterNarrative = "Hempel Model 0.4: Sector Alpha + Investment + Low Volatility"
            df['Factor Total Score'] = df["Investment Rank: q-factor Investment to Assets LH"] \
                                    + df["Starmine Model Rank Pct"] \
                                    + df["Volatility Rank: Volatility 126D LT"]
            pass
        elif setHempelModel_v5:
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
        elif setHempelModel_v6:
            pass
        elif setHempelModel_v7:
            parameterNarrative = "Alpha Model, Sector Neutral"
            df['Factor Total Score'] = df['Starmine Model Rank Pct']
            pass
        elif setHempelModel_v8:
            investmentLoading = 0.5
            parameterNarrative = "Alpha Model, Sector Neutral with wInv of " + str(investmentLoading)
            df['Factor Total Score'] = df['Starmine Model Rank Pct'] + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"])
            pass
        elif setHempelModel_v9:
            investmentLoading = 0.5
            momentumLoading = 0.25
            #+ " with volLoading of "+str(volatilityLoading) \
            parameterNarrative = "Alpha Model, Sector Neutral with wInv of " + str(investmentLoading) + " and wMom of " + str(momentumLoading)
            df['Factor Total Score'] = df['Starmine Model Rank Pct'] + (investmentLoading * df["Investment Rank: q-factor Investment to Assets LH"]) + (momentumLoading * df["Momentum Rank: Momentum 6Mo-2Wk HL"])
            pass
        elif setHempelModel_v10:
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
        elif setHempelModel_v11:
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
        elif setHempelModel_v12:
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
        elif setHempelModel_v13:
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

        elif setHempelModel_v14:
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
        