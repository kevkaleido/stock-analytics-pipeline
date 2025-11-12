#This script downloads historical stock data(2020 till 2025) for 200 tickers (S&P 500, NASDAQ, 
# and Russell 2000), calculates key financial metrics including total shareholder return,
#  volatility, and Sharpe ratio, then exports the results to a CSV file.

import yfinance as yf
import os
import pandas as pd

tickers = tickers = [
    # S&P 500 (100 tickers)
    "AAPL", "MSFT", "NVDA", "GOOGL", "AMZN", "META", "TSLA", "BRK.B", "LLY", "V",
    "JPM", "WMT", "XOM", "UNH", "MA", "PG", "JNJ", "HD", "COST", "ABBV",
    "NFLX", "CRM", "BAC", "MRK", "CVX", "KO", "AMD", "AVGO", "PEP", "TMO",
    "ADBE", "MCD", "CSCO", "ACN", "LIN", "ABT", "WFC", "DHR", "INTU", "ORCL",
    "TXN", "VZ", "PM", "NEE", "IBM", "CMCSA", "DIS", "RTX", "AMGN", "HON",
    "SPGI", "GE", "LOW", "UNP", "QCOM", "CAT", "PFE", "AXP", "NKE", "MS",
    "NOW", "COP", "UPS", "BA", "T", "GS", "ELV", "BLK", "SYK", "BKNG",
    "ADP", "GILD", "LMT", "MDLZ", "ADI", "PLD", "MMC", "VRTX", "SCHW", "REGN",
    "TJX", "CVS", "AMT", "BMY", "CI", "DE", "SO", "MU", "ETN", "ISRG",
    "CB", "FI", "BSX", "BDX", "PGR", "EOG", "C", "DUK", "SLB", "ZTS",
    
    # NASDAQ (50 tickers)
    "ABNB", "DDOG", "ZS", "CRWD", "PANW", "MELI", "TEAM", "DXCM", "WDAY", "FTNT",
    "BIIB", "MRVL", "SNPS", "CDNS", "MNST", "KLAC", "LRCX", "CTAS", "MAR", "PAYX",
    "AZN", "IDXX", "ORLY", "FAST", "PCAR", "VRSK", "CHTR", "ODFL", "ILMN", "AEP",
    "EA", "CPRT", "XEL", "ROST", "KDP", "CSGP", "ANSS", "MCHP", "GEHC", "TTD",
    "ON", "FANG", "BKR", "EXC", "CCEP", "DKNG", "ZM", "KHC", "MRNA", "CEG",
    
    # Russell 2000 (50 tickers)
    "SAIA", "GTLS", "PLNT", "RYAN", "FN", "STEP", "HQY", "CDAY", "SITM", "EXLS",
    "CALM", "UFPI", "CRVL", "IBOC", "EXPO", "SKYW", "PRIM", "CVCO", "APAM", "ENSG",
    "IBP", "CEIX", "AMR", "TNET", "MATX", "HRI", "SHOO", "NGVT", "ATKR", "PTEN",
    "ADMA", "INSM", "OMCL", "ALKS", "GBCI", "CATY", "SFNC", "FBP", "WAFD", "WTFC",
    "ABCB", "UMBF", "FFIN", "ONB", "HWC", "BANR", "SBCF", "CVBF", "BUSE", "NYCB"
]
data =[]                 
for ticker in tickers:
    print(f'downloading {ticker}')
    stock = yf.download(ticker, start='2020-01-01') #gets stocks from 2020
    print(f'getting {ticker} stock info')
    symbol = ticker                                        #defines a variable holding ticker string as symbol                        
    ticker_object = yf.Ticker(symbol)                      #creates a ticker object which holds all data for a specified stock whose ticker is assigned to symbol
    info = ticker_object.info                              #this calls the info property of the ticker object
    sector = info.get('sector')                            #extracts the value associated with the key 'sector' from the info dictionary
    industry = info.get('industry')                        #extracts the value associated with industry, usually more specific industry sub category
    company_name = info.get('longName')                    #extracts the the name of the company that owns the stock
    market_cap = info.get('marketCap')                     #extracts the market cap
    dividend_history = ticker_object.dividends             #this extracts the dividend history of the stock
    print(f'Calculating metrics for {ticker} stock')
    closing_prices = stock['Close']
    if closing_prices.empty or len(closing_prices) == 0:
        continue
    last_close = closing_prices.iloc[-1] 
    first_close = closing_prices.iloc[0]
    total_dividends = dividend_history.sum()/first_close   #calculates the sum of dividend history
    tsr = ((last_close - first_close) + total_dividends) / first_close #total stakeholder return
    daily_return = closing_prices.pct_change() 
    daily_volatility = daily_return.std()
    num_of_trading_days =len(stock)

#annualized volatility is the square root of trading days (252) multiplied by daily volatility    
    annualized_volatility = daily_volatility * (252**0.5)
    
#annualized return: (1 + total return) ** (yearly trading days/ no of trading days in dataframe) - 1
    annualized_tsr = (1 + tsr)**(252/num_of_trading_days)-1

#Sharpe ratio measures the return earned per unit of risk(volatility)
#if the sharpe ratio is less than 1.0, the stocks return is low compared to its risk
    sharpe_ratio = annualized_tsr/annualized_volatility

#the average daily movement is often more intuitive than volatility, it is the average of the difference in daily prices
    daily_dollar_change = closing_prices.diff().abs().mean()

    max_daily_profit = daily_return.max()
    min_daily_profit = daily_return.min()
    print('Creating Dataframe')
    
#create a dataframe    
    new_data=pd.DataFrame({'CompanyName': company_name,
                         'TotalStakeholderReturn': tsr,
                         'Annual_TSR': annualized_tsr,
                         'AnnualVolatility': annualized_volatility,
                         'TradingDays' : num_of_trading_days, 
                         'SharpeRatio': sharpe_ratio,
                         'DailyDollarChange': daily_dollar_change,
                         'MaxDailyProfit': max_daily_profit,
                         'MinDailyProfit': min_daily_profit,
                         'MarketCap': market_cap,
                         'Sector': sector,
                         'industry': industry})
#append the dataframes to the empty list
    data.append(new_data)

#concatenate all dataframes in the list    
    final_data = pd.concat(data)
print('Process complete')

final_data.to_csv('stocks.csv')
current_directory =os.getcwd()
print(f'data saved successfully to {current_directory}')

