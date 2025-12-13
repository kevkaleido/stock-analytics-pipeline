# This script downloads historical stock data (2020-2025) for 200 tickers (S&P 500, NASDAQ, and Russell 2000). 
# It calculates time-dimensioned, year-specific financial metrics (TSR, Volatility, Sharpe Ratio, and Market Cap) 
# for each individual year (2020 through 2025). This results in granular data, providing 6 rows per stock, 
# which is essential for detailed year-over-year performance analysis.
# Results are exported to a Microsoft SQL Server database and a timestamped CSV file.


import yfinance as yf
import os
import pandas as pd
import os
import pyodbc
import pandas
from sqlalchemy import create_engine

from datetime import datetime





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
    stock = yf.download(ticker, start='2020-01-01')        #gets stocks from 2020
    print(f'getting {ticker} info')
    symbol = ticker                                        #defines a variable holding ticker string as symbol                        
    ticker_object = yf.Ticker(symbol)                      #creates a ticker object which holds all data for a specified stock whose ticker is assigned to symbol
    info = ticker_object.info                              #this calls the info property of the ticker object
    sector = info.get('sector')                            #extracts the value associated with the key 'sector' from the info dictionary
    industry = info.get('industry')                        #extracts the value associated with industry, usually more specific industry sub category
    company_name = info.get('longName')                    #extracts the the name of the company that owns the stock
    dividend_history = ticker_object.dividends             #this extracts the dividend history of the stock
    outstanding_shares = info.get('sharesOutstanding')      #gets current share
    for year in range(2020, 2026):                  #for each year
        year_data = stock[stock.index.year==year]   #process only the current year in loop, and get only that year's data
        if year_data.empty or len(year_data)<2:     
            continue
        print(f'Calculating {year} {ticker} metrics for {company_name}')
        closing_prices = year_data['Close'].squeeze()        #adding .squeeze() so I will always get scaler values from standard deviations and the likes, instead of series, will need to add an index to dataframe because If using all scalar values, you must pass an index
        if closing_prices.empty or len(closing_prices) == 0:   #an if condition to avoid any error that would stop the entire loop, if a stock close series is empty, ignore and move to another  
            continue
        last_close = closing_prices.iloc[-1] 
        first_close = closing_prices.iloc[0]

        yearly_dividends = dividend_history[dividend_history.index.year == year].sum()   #calculates the sum of yearly dividend history
        annual_tsr = ((last_close - first_close) + yearly_dividends) / first_close #this now becomes annual total shareholder return since we are calculating by year_data
        daily_return = closing_prices.pct_change() 
        daily_volatility = daily_return.std()                   #high volatility means more risk
        
 
    #annualized volatility is the square root of trading days (252) multiplied by daily volatility    
        annualized_volatility = daily_volatility * (252**0.5)

     
    #get market cap approximation using outstanding shares
        if outstanding_shares:
            market_cap = outstanding_shares * last_close
        else:
            market_cap = None

    #Sharpe ratio measures the return earned per unit of risk(volatility)
    #if the sharpe ratio is less than 1.0, the stocks return is low compared to its risk
        if annualized_volatility.squeeze() !=0:           #adding squeeze gets a scaler value
            sharpe_ratio = annual_tsr/annualized_volatility 
        else:
            sharpe_ratio =None
        

    #get max and min profit per year includind days it happened
        max_daily_profit = daily_return.max()
        max_daily_profit_date = daily_return.idxmax()        #get the index where daily return is max
        min_daily_profit = daily_return.min()
        min_daily_profit_date = daily_return.idxmin()        #get the index where daily return in minimum

    #check if current year in loop is less than current year, if it is, then true, year is complete, otherwise, false, year is not complete
        is_complete = (year < datetime.now().year)


    #create a dataframe 
        print(f'Creating Dataframe for {year} {company_name} {ticker} stock for ')   
        new_data=pd.DataFrame({'Ticker': ticker,
                               'Year': year,
                            'CompanyName': company_name,
                            'Annual_TSR': annual_tsr,
                            'AnnualVolatility': annualized_volatility, 
                            'SharpeRatio': sharpe_ratio,
                            'MaxDailyProfit': max_daily_profit,
                            'MaxDP_Date': max_daily_profit_date,
                            'MinDailyProfit': min_daily_profit,
                            'MinDP_Date': min_daily_profit_date,
                            'MarketCap': market_cap,
                            'Sector': sector,
                            'industry': industry,
                            'Complete_Year': is_complete,
                            'LastUpdated': datetime.now()}, index=[0])
        


    #append the dataframes to the formally empty list
        data.append(new_data)

    #concatenate all dataframes in the list    
        final_data = pd.concat(data)
        
final_data

#saving to microsoft server
server = r'KEVIN\SQLEXPRESS'         #creates a variable with my servername   
database = 'stock_metrics'           #the name of the database I want my dataframe in, assigned to a variable

#create connection string 
#after importing pyodbc and from sqlalchemy, importing create_engine-- these are language tranlators to write to sql server
connection_str = f'mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+Sql+Server&trusted_connection=yes'
engine = create_engine(connection_str)     
print('Inserting Data into Sql Server')
final_data.to_sql('stock_metrics_yearly', engine, if_exists= 'replace', index=False) #load to Sql Server

print(f'{len(final_data)} rows of stock data added to MS server')


#saving the data as csv with timestamps
directory = os.getcwd()
timestamp = datetime.now()
timestamp = timestamp.strftime('%Y%m%d_%H%M%S')    #format timestamp to string 
filename = f'stock_metrics_yearly{timestamp}.csv'
final_data.to_csv(filename, index=False)
print(f'{len(final_data)} rows of stock data saved successfully to {directory}')



