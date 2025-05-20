# Hempel Top 50 Quantamental Investment Models

**Hempel Top 50** is a python framework for analyzing investment factor data and quantitative approaches. Designed to accelerate development of quantitative trading strategies and risk management solutions. It was created and maintained by quantitative developers at Hempel Wealth Management LLC, an investment advisory firm that has ceased operations. If you are seeking investment advice, I recommened talking to a CFP professional. 

This codebase has been made public for posterity's sake, for this research was possible because I stood on the shoulders of giants.

## Results
Developed two proprietary quantamental investment models, "Hempel Wealth Top 50" and "Hempel Wealth Top 50 Low Volatility". Both models had a higher annual return than the S&P 500 with lower volatility and a lower max drawdown over a period of 20+ years.

### Model: Hempel Top 50

Time period: 2000-1-1 to 2022-12-31; Quarterly Rebalanced; portfolio of the 50 best stocks from the S&P 500; Max Drawdown -35.3% vs. S&P500 -45.8%

![Top50](hempelwealthtop50_2000_2022.png)

### Model: Hempel Top 50 Low Volatility

Time period: 2000-1-1 to 2022-12-31; Quarterly Rebalanced; portfolio of the 50 best stocks from the S&P 500; Max Drawdown -35.2% vs. S&P500 -45.8%

![Top50](hempelwealthtop50lowvol_2000_2022.png)

## Disclaimer

The results are hypothetical and are NOT an indicator of future results and do NOT represent returns that an investor actually attained. Indexes are unmanaged, do not reflect management or trading fees, and one cannot invest directly in an index. 
Source: Refinitiv, Hempel Wealth Management LLC


## Bloomberg MVP
This was initially designed to validate [Bloomberg's MVP Index](https://www.bloomberg.com/professional/products/indices/quote/BMVP:IND). Bloomberg's research has since been used to launch an ETF, [Invesco Bloomberg MVP Multi-factor ETF](https://www.invesco.com/us/financial-products/etfs/product-detail?audienceType=investor&ticker=bmvp), ticker BMVP. The investment strategy " is constructed to track the performance of US large cap companies that exhibit strong fundamental characteristics for Momentum (M), Value (V), Volatility (V), and Profitability (P) utilizing a factor model developed by Bloomberg Intelligence."

![Bloomberg MVP](twitter_gina_martin_adams_introducing_mpv_portfolio.jpg)
Source: [Gina Martin Adams](https://twitter.com/GinaMartinAdams/status/1598431923294150656)

## Warren Buffett & Berkshire Hathaway
 It can also be used to confirm Warren Buffet's historical investment outperformance described in terms of investment factors. Berkshire Hathaway has had a significant outperformance in investment returns that can NOT be explained using traditional Farma-French factors [Beta, Size, and Value]. However, this unexplained outperformance disappears when controlling for Low Volatility and Profitability factors. In short, Buffett’s returns appear to be neither luck nor magic, but, rather, reward for the use of Low Volatility, Value, and Profitable stocks.

Source: [Buffett’s Alpha - Pedersen 2013](https://www.nber.org/papers/w19681)

Model: 
100% Berkshire Hathaway Class A Stock
Historically, Warren Buffet’s investment approach can be described as a 1.6x leveraged portfolio using Value, Quality, Low Volatility Factors. Again over the same time frame from Jan. 1, 2000, to Dec. 31, 2022, Buffet more than double the cumulative return of the S&P 500.

![Berkshire Hathaway](brk_a.png)

## Factor History 

Formal academic models have explained individual stock performance since the 1960s. In the research since, over 500 factors have been documented that explain individual stock outperformance, that can be organized into the following categories: 

Size, Value, Investment, Momentum, Expected Growth, Profitability / Quality, High Beta & Low Volatility

![Factor Explosion](man_AAB_factors_fig1.jpg)
As published in top academic journals through to the end of December 2018. Reproduction of a chart of Harvey and Liu (2019).

### Traditional Factors
**Volatility:** While high beta historically was associated with higher absolute returns, the low volatility stocks have delivered higher risk-adjusted returns. Many investors, such as individuals, pension funds and mutual funds, are constrained in the leverage that they can take, and therefore must overweight riskier securities instead, creating a Low volatility anomaly.

**Small Size:** One of the oldest and most persuasive arguments in the stock market is that small stocks outperform large stocks. However, recent research to suggest that “There Is No Size Effect”

**Value:** the most famous factor, is the tendency for relatively cheap stocks to outperform relatively expensive stocks over time. Recent academic research suggests the value factor can be eliminated since it can be better explained using other factors

### Modern Factors
**Momentum** is the tendency for past price performance to continue in the near future. However, the q-factor model has found that the Momentum factor can be explained by a combination of Profitability and Expected Growth.

**Profitability** is the observation that investing in highly profitable stocks tend to significantly outperform companies of lower profitability.

**Investment** is the observation that firms that are more conservative in asset growth have higher future returns. 

**Expected Growth** is a combination of the firm’s valuation, cash flow, and profitability.


## Requirements

* LSEG Workstation, formerly Refinitiv
* Python 3.10 or greater
* Access to PIP package manager

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/your-repo.git
cd your-repo

# (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Poetry if you don't have it
pip install poetry

# Install dependencies
poetry install
```

## Usage

```bash
poetry run python main.py
```

Describe how to use your project, with code examples if possible.


## Authors and Acknowledgment



## License

This project is licensed under the [GPL](LICENSE).