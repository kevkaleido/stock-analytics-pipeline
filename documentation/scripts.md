
## Overview

This documentation covers two Python scripts designed to analyze historical stock data for 200 tickers across S&P 500, NASDAQ, and Russell 2000 indices from 2020 to 2025. Both scripts calculate financial performance metrics but differ in their temporal granularity.

---

## Script 1: Yearly Granular Analysis

**Purpose**: Provides year-by-year performance metrics for detailed temporal analysis.

**Output**: 6 rows per stock (one for each year: 2020-2025), totaling approximately 1,200 rows.

### Key Features

- **Temporal Granularity**: Calculates metrics separately for each year
- **Year-over-Year Comparison**: Enables tracking of performance changes across time
- **Market Cap Approximation**: Calculates market cap using outstanding shares × year-end price

### Metrics Calculated (Per Year)

|Metric|Description|Formula/Method|
|---|---|---|
|**Annual TSR**|Total Shareholder Return for the year|`((last_close - first_close) + yearly_dividends) / first_close`|
|**Annualized Volatility**|Risk measure (standard deviation of returns)|`daily_volatility × √252`|
|**Sharpe Ratio**|Return per unit of risk|`annual_tsr / annualized_volatility`|
|**Max Daily Profit**|Highest single-day percentage gain|`daily_return.max()`|
|**Min Daily Profit**|Lowest single-day percentage loss|`daily_return.min()`|
|**Market Cap**|Company valuation|`outstanding_shares × last_close`|

### Additional Fields

- **Complete_Year**: Boolean flag indicating whether the year is finished
- **MaxDP_Date / MinDP_Date**: Dates when max/min daily profits occurred
- **LastUpdated**: Timestamp of data generation
- **Sector & Industry**: Company classification

---

## Script 2: Aggregated Long-Term Analysis

**Purpose**: Provides a single, comprehensive performance summary over the entire 2020-2025 period.

**Output**: 1 row per stock, totaling approximately 200 rows.

### Key Features

- **Long-Term Perspective**: Single metric representing entire 5-year period
- **Maximum Drawdown**: Captures worst peak-to-trough decline
- **Direct Market Cap**: Uses current market cap from yfinance API

### Metrics Calculated (Entire Period)

|Metric|Description|Formula/Method|
|---|---|---|
|**Total Shareholder Return (TSR)**|Overall return including dividends|`((last_close - first_close) + total_dividends) / first_close`|
|**Annualized TSR**|Period average return|`(1 + tsr)^(252/num_trading_days) - 1`|
|**Annualized Volatility**|Overall risk measure|`daily_volatility × √252`|
|**Sharpe Ratio**|Risk-adjusted return|`annualized_tsr / annualized_volatility`|
|**Maximum Drawdown**|Largest peak-to-trough decline|`min((cumulative_return - running_max) / running_max)`|
|**Max/Min Daily Profit**|Best and worst single-day returns|`daily_return.max()` / `daily_return.min()`|

### Understanding Maximum Drawdown

Maximum drawdown measures the worst loss an investor would have experienced buying at the peak and selling at the trough:

```
Example: -50% max drawdown = stock lost half its value at some point
```

**Calculation Process**:

1. Calculate cumulative returns: `(1 + daily_return).cumprod()`
2. Track running maximum: `cumulative_return.cummax()`
3. Calculate drawdown at each point: `(cumulative_return - running_max) / running_max`
4. Find the minimum (worst) value

---

## Common Elements

### Data Sources

- **Tickers**: 200 stocks total
    - 100 from S&P 500
    - 50 from NASDAQ
    - 50 from Russell 2000
- **Date Range**: January 1, 2020 to present
- **Data Provider**: Yahoo Finance (yfinance library)

### Core Calculations

#### Total Shareholder Return (TSR)

Measures complete investment performance by combining capital appreciation and dividend income:

```
TSR = (Price Gain + Dividends) / Initial Price
```

**Why Include Dividends?**  
Dividends represent cash returned to shareholders. Excluding them would understate true investor returns, especially for dividend-paying stocks.

#### Volatility Metrics

**Daily Volatility**: Standard deviation of daily percentage returns  
**Annualized Volatility**: `daily_volatility × √252` (252 = typical trading days per year)

**Interpretation**:

- High volatility = Higher risk, larger price swings
- Low volatility = More stable, predictable returns

#### Sharpe Ratio

Measures risk-adjusted returns (return per unit of risk):

```
Sharpe Ratio = Return / Volatility
```

**Interpretation**:

- Sharpe < 1.0: Returns don't justify the risk
- Sharpe ≥ 1.0: Returns adequately compensate for risk
- Sharpe > 2.0: Excellent risk-adjusted returns

---

## Data Export

### Microsoft SQL Server

**Configuration**:

```python
server = r'KEVIN\SQLEXPRESS'
database = 'stock_metrics'
driver = 'ODBC Driver 17 for SQL Server'
```

**Tables**:

- Yearly Script: `stock_metrics_yearly`
- Aggregated Script: `stock_metrics`

**Method**: Bulk load using SQLAlchemy's `to_sql()` with `if_exists='replace'`

### CSV Files

Both scripts export timestamped CSV files:

- Yearly: `stock_metrics_yearly_YYYYMMDD_HHMMSS.csv`
- Aggregated: `stock_metrics_YYYYMMDD_HHMMSS.csv`

---

## Technical Notes

### ODBC Driver Resolution

Finding the correct SQL Server driver name:

1. Press `Windows + R`
2. Type `odbcad32`
3. Go to "Drivers" tab
4. Look for `ODBC Driver 17 for SQL Server`

**Common Issue**: Using `SQL Server` driver can cause "invalid precision value" errors. Use `ODBC Driver 17 for SQL Server` instead.

### Error Handling

Both scripts include safeguards:

- Skip stocks with insufficient data (`len(closing_prices) < 2`)
- Handle empty dividend histories
- Check for zero volatility before calculating Sharpe ratio
- Validate yearly data availability before processing

### Performance Considerations

- Downloads data sequentially (not parallelized)
- Prints progress for each ticker and year
- Expected runtime: 15-30 minutes depending on network speed

---

## Use Cases

### When to Use Yearly Granular Analysis

- Year-over-year performance comparison
- Identifying trends and patterns across years
- Analyzing impact of specific events in particular years
- Building time-series models
- SQL queries with WHERE clauses filtering by year

### When to Use Aggregated Analysis

- Quick overview of long-term performance
- Screening stocks based on 5-year metrics
- Portfolio optimization using historical risk/return profiles
- Identifying maximum loss potential (drawdown analysis)
- Simple ranking and comparison across all stocks

---

## Dependencies

```python
yfinance        # Stock data retrieval
pandas          # Data manipulation
sqlalchemy      # Database connectivity
pyodbc          # ODBC database driver
datetime        # Timestamp generation
```
