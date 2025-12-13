# Stock Metrics Yearly Analysis Documentation

## Overview

This Python script analyzes historical stock data for 200 tickers across S&P 500, NASDAQ, and Russell 2000 indices from 2020 to 2025. It calculates year-specific financial performance metrics to enable detailed temporal analysis and year-over-year comparisons.

---

## Purpose and Output

**Purpose**: Provides year-by-year performance metrics for detailed temporal analysis.

**Output**: 6 rows per stock (one for each year: 2020-2025), totaling approximately 1,200 rows.

**Key Advantage**: Enables tracking of performance changes across time and identification of trends in specific years.

---

## Data Sources

### Tickers (Customizable)

The script is customizable and can analyze any number of stocks. The default configuration includes 200 tickers:

- **100 from S&P 500**: Large-cap companies like AAPL, MSFT, NVDA, GOOGL, AMZN
- **50 from NASDAQ**: Tech and growth stocks like ABNB, DDOG, CRWD, PANW
- **50 from Russell 2000**: Small-cap stocks like SAIA, GTLS, PLNT, RYAN


Simply modify the `tickers` list at the beginning of the script to add more tickers:

**Important Notes:**
- Ticker symbols must be valid Yahoo Finance tickers
- International stocks should use the correct Yahoo Finance format (e.g., "0700.HK" for Tencent)
- The script will process as many or as few tickers as you provide
- Runtime scales linearly with the number of tickers (approximately 5-10 seconds per ticker)

### Data Provider
- **Source**: Yahoo Finance via yfinance library
- **Date Range**: January 1, 2020 to present (customizable)
- **Data Retrieved**: Daily closing prices, dividend history, company information

---

## Metrics Calculated (Per Year)

| Metric | Description | Formula/Method |
|--------|-------------|----------------|
| **Annual TSR** | Total Shareholder Return for the year | `((last_close - first_close) + yearly_dividends) / first_close` |
| **Annualized Volatility** | Risk measure (standard deviation of returns) | `daily_volatility × √252` |
| **Sharpe Ratio** | Return per unit of risk | `annual_tsr / annualized_volatility` |
| **Max Daily Profit** | Highest single-day percentage gain | `daily_return.max()` |
| **Min Daily Profit** | Lowest single-day percentage loss | `daily_return.min()` |
| **Market Cap** | Company valuation at year-end | `outstanding_shares × last_close` |

### Additional Fields

- **Ticker**: Stock symbol
- **Year**: The specific year (2020-2025)
- **CompanyName**: Full company name
- **Sector**: Business sector classification
- **Industry**: Specific industry sub-category
- **Complete_Year**: Boolean flag indicating whether the year has finished
- **MaxDP_Date**: Date when maximum daily profit occurred
- **MinDP_Date**: Date when minimum daily profit occurred
- **LastUpdated**: Timestamp of data generation

---

## Understanding the Key Metrics

### Total Shareholder Return (TSR)

Measures complete investment performance by combining capital appreciation and dividend income:

```
TSR = (Price Gain + Dividends) / Initial Price
```

**Why Include Dividends?**  
Dividends represent cash returned to shareholders. Excluding them would understate true investor returns, especially for dividend-paying stocks like utilities and consumer staples.

**Example**:
- Stock starts at $100, ends at $110
- Pays $5 in dividends during the year
- TSR = ((110 - 100) + 5) / 100 = 15%

### Volatility Metrics

**Daily Volatility**: Standard deviation of daily percentage returns  
**Annualized Volatility**: `daily_volatility × √252` (252 = typical trading days per year)

**Interpretation**:
- High volatility (>30%): Higher risk, larger price swings (common in tech stocks)
- Medium volatility (15-30%): Moderate price fluctuations
- Low volatility (<15%): More stable, predictable returns (utilities, consumer staples)

### Sharpe Ratio

Measures risk-adjusted returns (return earned per unit of risk taken):

```
Sharpe Ratio = Annual TSR / Annualized Volatility
```

**Interpretation**:
- Sharpe < 1.0: Returns don't justify the risk taken
- Sharpe ≥ 1.0: Returns adequately compensate for risk
- Sharpe > 2.0: Excellent risk-adjusted returns

**Example**:
- Stock A: 20% return, 40% volatility → Sharpe = 0.5 (poor)
- Stock B: 20% return, 15% volatility → Sharpe = 1.33 (good)

### Market Capitalization

Approximates company valuation using:
```
Market Cap = Outstanding Shares × Year-End Stock Price
```

This provides a snapshot of company size at the end of each year.

---

## Script Workflow

### 1. Data Download
For each of the 200 tickers:
- Downloads daily stock data from 2020-01-01 to present
- Retrieves company information (sector, industry, name)
- Extracts dividend history and outstanding shares

### 2. Year-by-Year Processing
For each year (2020-2025):
- Filters data to include only the current year
- Skips if insufficient data (fewer than 2 trading days)
- Extracts closing prices for calculations

### 3. Metric Calculation
Computes all financial metrics for the specific year:
- Identifies first and last closing prices
- Sums dividends paid during the year
- Calculates daily returns and volatility
- Determines max/min daily profits and their dates
- Computes TSR, Sharpe ratio, and market cap

### 4. Data Assembly
Creates a DataFrame row for each year-ticker combination with all calculated metrics.

### 5. Export
Concatenates all rows and exports to:
- Microsoft SQL Server database
- Timestamped CSV file

---

## Data Export

### Microsoft SQL Server

**Configuration**:
```python
server = r'KEVIN\SQLEXPRESS'
database = 'stock_metrics'
driver = 'ODBC Driver 17 for SQL Server'
table_name = 'stock_metrics_yearly'
```

**Connection Method**: SQLAlchemy with pyodbc  
**Load Strategy**: `if_exists='replace'` (overwrites existing table)

**Finding Your ODBC Driver**:
1. Press `Windows + R`
2. Type `odbcad32` and press Enter
3. Go to "Drivers" tab
4. Look for `ODBC Driver 17 for SQL Server`

**Common Issue**: Using `SQL Server` driver can cause "invalid precision value" errors. Always use `ODBC Driver 17 for SQL Server`.

### CSV Files

**Filename Format**: `stock_metrics_yearly_YYYYMMDD_HHMMSS.csv`  
**Location**: Current working directory  
**Index**: Not included in export

---

## Error Handling

The script includes robust safeguards:

- **Empty Data Check**: Skips years with empty or insufficient data
- **Zero Volatility**: Checks before calculating Sharpe ratio to avoid division by zero
- **Missing Shares**: Handles stocks without outstanding shares data

---

## Use Cases

### When to Use This Analysis

✓ **Year-over-Year Performance Comparison**: Track how individual stocks performed each year  
✓ **Trend Identification**: Spot patterns like improving Sharpe ratios or increasing volatility  
✓ **Event Analysis**: Examine impact of specific events in particular years (e.g., 2020 pandemic impact)  
✓ **SQL Time-Series Queries**: Filter and aggregate by year in database queries  
✓ **Historical Context**: Understand how stocks behaved in different market conditions


## Technical Notes


### Performance Considerations

- **Sequential Processing**: Downloads data one ticker at a time
- **Progress Tracking**: Prints status for each ticker and year
- **Expected Runtime**: 
  - ~5-10 seconds per ticker
  - Default 200 tickers: 15-30 minutes
- **Data Volume**: Approximately 6 rows per ticker (one per year)

### Dependencies

```python
yfinance        # Stock data retrieval from Yahoo Finance
pandas          # Data manipulation and DataFrame operations
sqlalchemy      # Database connectivity and SQL operations
pyodbc          # ODBC database driver for SQL Server
datetime        # Timestamp generation
```

### Installation

```bash
pip install yfinance pandas sqlalchemy pyodbc
```

---


## Limitations and Considerations

1. **Incomplete 2025 Data**: Since 2025 is ongoing, metrics for this year are partial and will change
2. **Market Cap Approximation**: Uses outstanding shares × price; actual market cap may differ slightly
3. **Dividend Timing**: Assumes dividends are received when paid (doesn't account for ex-dividend dates)
4. **Delisted Stocks**: Historical data may be incomplete for stocks that were delisted
5. **Trading Days**: Assumes 252 trading days per year for annualization (actual may vary)

---


## Conclusion

This script provides granular, time-dimensioned analysis of stock performance across multiple years. The year-by-year approach enables sophisticated temporal analysis, making it ideal for understanding how individual stocks evolve over time and how they respond to changing market conditions.