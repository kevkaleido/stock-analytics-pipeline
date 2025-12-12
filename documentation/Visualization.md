# Stock Performance Analysis Dashboard Documentation

## Executive Dashboard

### 1. TSR Trends Over Time - Line Chart
This visualization displays Total Shareholder Return (TSR) trends from 2020 to 2025 for the top 10 performing stocks based on average Sharpe Ratio, which means that it focuses on stocks with best risk-adjusted returns.

This visualization enables users to:
- Identify which top-performing stocks maintained consistent year-over-year growth vs. those with dramatic swings between years
- Observe market-wide events such as the 2022 market correction where most stocks reached their lowest TSR levels
- Compare annual performance trajectories and recovery patterns post-correction

### 2. Risk vs Return by Sector - Scatter Chart
This visualization displays the relationship between risk (annual volatility) and return (Annual TSR) across different market sectors, with bubble size representing market capitalization.

- **X-axis (Volatility):** Represents risk - higher values = more unstable returns
- **Y-axis (TSR):** Represents reward - higher values = better returns
- **Classic risk-return framework:** Upper-left quadrant = high return/low risk (ideal), lower-right = high risk/low return (unfavorable)

The visualization enables users to:
- Identify sectors with favorable risk-return profiles (high TSR, low volatility)
- Spot outlier companies with exceptional performance or unusual risk levels
- Compare sector clustering patterns to understand industry-specific risk characteristics
- Assess whether larger companies (bigger bubbles) offer more stable returns
- Discover undervalued sectors offering strong returns without excessive volatility
- Evaluate diversification opportunities by selecting sectors from different risk zones

**Key observations from the chart:**
- Most companies cluster in the 20-60% volatility range with 0-200% TSR
- Sectors appear to overlap significantly, suggesting company-specific factors matter more than sector alone

### 3. Card Visuals
This displays high-level summary statistics for quick performance overview of the entire stock portfolio.

---

## Sector And Industry Dashboard

### 1. Sum of MarketCap by Sector - Treemap
This visualization displays the distribution of total market capitalization across different sectors, showing relative size and sector composition of the analyzed stock universe.

This visualization enables users to:
- Identify which sectors dominate by total market capitalization
- Compare relative size of sectors and industries
- Spot diversification opportunities in underrepresented sectors
- Drill down from sector to industry to individual stocks

### 2. Best Risk Adjusted Return by Sector - Bar Chart
This displays the median Sharpe Ratio (risk-adjusted return) for each sector, ranked from highest to lowest, to identify which sectors deliver the best returns relative to their risk. I used median sharperatio because it is less affected by outliers than average sharperatio.

This visualization enables users to:
- Identify sectors with best risk-adjusted returns (Utilities, Technology, Industrials lead)
- Compare sector efficiency in generating returns relative to risk
- Make sector allocation decisions based on risk-adjusted performance
- Spot sectors with poor risk-return tradeoffs

### 3. Best Return by Sector - Horizontal Bar Chart
Displays average Total Shareholder Return (TSR) by sector, ranked from highest to lowest, to identify which sectors generated the strongest overall returns.

This visualization enables users to:
- Identify highest-returning sectors (Technology, Basic Materials, Consumer Cyclical lead)
- Compare raw return performance across sectors
- Make growth-focused investment decisions
- Spot underperforming sectors (Real Estate trails significantly)

### 4. Top 5 and Bottom 5 Performers - Table Visuals
Displays the best and worst performing stocks with detailed metrics, enabling quick identification of extreme performers and their characteristics.

This visualization enables users to:
- Identify specific stocks with exceptional or poor performance
- Compare risk metrics (volatility, Sharpe) between top and bottom performers
- Find specific tickers for further investigation

---

## Risk Analysis Dashboard

### 1. Volatility Trend Over Time - Line Chart
This visualization displays the annual volatility trends for the top 10 stocks (by market capitalization) over a multi-year period, enabling analysis of risk patterns and stability overtime on the largest, most influential companies.

This visualization enables users to:
- Identify stocks with consistent low volatility vs. those with fluctuating risk levels
- Observe market-wide volatility events
- Compare year-over-year volatility trends and normalization patterns
- Assess current risk environment for major stocks
- Spot which large-cap stocks maintain stability vs. those with persistent volatility

### 2. Worst Single-Day Loss vs Annual Return by Sector - Scatter Chart
Displays the relationship between worst single-day loss and annual return across sectors, revealing which sectors offer strong returns despite extreme drawdown events.

This visualization enables users to:
- Identify stocks/sectors with strong annual returns despite severe single-day losses
- Assess downside risk tolerance requirements for different return levels
- Compare sector clustering to understand industry-specific risk characteristics
- Spot outliers with exceptional returns and manageable worst-day losses
- Evaluate whether accepting larger single-day losses correlates with higher annual returns
- Make risk management decisions based on worst-case scenarios

### 3. Volatility Range Within Each Sector - Stacked Bar Chart
Displays the minimum, median, and maximum annual volatility within each sector, revealing the range and distribution of risk levels across different industries.

This visualization enables users to:
- Compare volatility ranges across different sectors
- Identify sectors with tight volatility clustering (consistent risk) vs. wide spreads (diverse risk profiles)
- Assess typical sector volatility through median values
- Find sectors with low minimum volatility for conservative investors

### 4. Yearly Risk Adjusted Returns by Sector - Matrix Table
Displays median Sharpe Ratio (risk-adjusted return) for each sector across multiple years (2020-2025), with color-coded heatmap to quickly identify best and worst performing sectors by year.

This visualization enables users to:
- Compare sector performance year-over-year
- Identify sectors with consistent positive Sharpe Ratios across time
- Spot temporal patterns
- Find sectors with persistent strength or weakness
- Assess overall sector quality through Total column

---

## Individual Stock Dive Dashboard

### 1. Stock Details - Table Visual
Displays detailed performance metrics for individual stocks, including company name, year, returns, volatility, risk-adjusted returns, and market capitalization.

This visualization enables users to:
- Look up detailed metrics for specific stocks
- Compare individual stock performance within filtered sectors
- Identify stocks with specific risk-return characteristics
- Analyze company size (market cap) relative to performance
- Drill down from sector-level insights to individual stock details
- Export or reference specific stock data for further analysis

#### Interactivity Features
- Click company names to potentially drill through to more details
- Use slicers to filter by sector, ticker, or year
- Sort by any column header (TSR, volatility, Sharpe, market cap)
- Cross-filters with other report visualizations
- Scroll through multiple rows of stock data
- Dynamic updates based on slicer selections

### 2. Yearly Performance Over Time - Combo Chart
Combo chart (column chart with line overlay) that displays the relationship between average annual TSR (bars) and median Sharpe Ratio (line) over time, showing how returns and risk-adjusted performance evolved.

This visualization enables users to:
- Track how overall market returns changed year-over-year
- Assess whether returns were accompanied by good risk-adjusted performance
- Identify years with strong absolute returns but poor risk efficiency (high bars, low line)
- Spot market recovery patterns
- Compare current performance levels to historical patterns
- Understand the relationship between raw returns and risk-adjusted returns over time