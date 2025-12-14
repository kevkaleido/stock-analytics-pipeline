# STOCK ANALYSIS PIPELINE

A comprehensive and customizable data analytics project that extracts, analyzes, and visualizes performance metrics for stocks across S&P 500, NASDAQ, and Russell 2000 indices using Python, SQL, and Power BI.
## Overview
This project demonstrates an end-to-end data pipeline for financial analysis, covering data extraction, transformation, storage, and visualization of key stock performance indicators. The pipeline is fully customizable and can analyze any number of stocks specified.
## Tech Stack
- **Python**: Data extraction and metric calculation using yfinance and pandas
- **SQL**: Data querying and analysis
- **Power BI**: Interactive dashboard and visualization
- **Data Source**: Yahoo Finance API (2020-present)

## Key Metrics Analyzed
- Total Shareholder Return (TSR) & Annualized TSR
- Volatility & Sharpe Ratio
- Daily price movements and profit ranges
- Market capitalization and sector distribution

## Dataset
- **Default Configuration: 200 stocks** spanning three major indices:
  - 100 S&P 500 stocks (large-cap)
  - 50 NASDAQ stocks (tech-focused)
  - 50 Russell 2000 stocks (small-cap)

## Customization
- The analysis is **fully customizable** to any number of stocks. Simply modify the `tickers` list at the beginning of the Python script to add or remove stocks:
```python
  tickers = ['AAPL', 'MSFT', 'GOOGL', ...]  # Add your desired tickers here
```

* **Scalability**: The script will process as many or as few tickers as you provide
* **Runtime**: Scales linearly with the number of tickers (approximately 5-10 seconds per ticker)
* **Flexibility**: Analyze specific sectors, industries, or custom stock portfolios

## Visualizations

### Main Dashboard
![Main Dashboard](Visualizations/Imgs/01_main_dashboard.png)


### Risk Analysis
![Risk Analysis](Visualizations/Imgs/03_risk_analysis.png)



## Project Workflow
1. **Extract**: Python script downloads historical stock data and calculates financial metrics
2. **Transform**: Data cleaned and exported to Microsoft Server and CSV
3. **Load & Analyze**: SQL queries for deeper insights and aggregations
4. **Visualize**: Power BI dashboard for interactive exploration

## Features
- Customizable ticker selection - analyze any stocks you choose
- Multi-market coverage for diversified analysis
- Risk-adjusted performance metrics
- Sector and industry classification
- Scalable pipeline design
