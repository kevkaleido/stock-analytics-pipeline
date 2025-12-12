## Query 1: Predictable High-Performing Stocks

**Purpose:** Find stocks with strong risk-adjusted returns (Sharpe > 1) and consistent performance.

**Key Metrics:**

- **Coefficient of Variation (CV):** Lower values = more predictable returns
- **Sharpe Ratio:** Risk-adjusted return measure (>1 is good)
- **Standard Deviation of Sharpe:** Measures consistency of risk-adjusted performance

**Query Logic:**

- Groups stocks by ticker and sector
- Calculates average and range of Sharpe ratios
- Computes CV to measure return predictability
- Filters for average Sharpe Ratio > 1
- Orders by CV (ascending) and average returns (descending)

**Use Case:** Conservative investors seeking steady, predictable growth with proven risk-adjusted returns.

---

## Query 2: Top Annual Performers

**Purpose:** Identify the 5 best-performing stocks each year.

**Query Logic:**

- Ranks stocks by Annual TSR within each year using window functions
- Returns top 5 performers per year
- Formats returns as percentages for readability

**Use Case:** Understanding historical winners, identifying momentum patterns, and analyzing sector leadership trends.

---

## Query 3: High Returns with Moderate Risk

**Purpose:** Find stocks balancing strong returns with manageable risk.

**Filter Criteria:**

- Average Sharpe Ratio > 1
- Sorted by highest Sharpe Ratio

**Output Includes:**

- Average return, volatility, and Sharpe ratio
- Sector classification

**Use Case:** Growth-oriented investors seeking favorable risk/reward profiles without excessive volatility.

---

## Query 4: Stock Stability Analysis

**Purpose:** Categorize stocks by risk level based on volatility.

**Risk Categories:**

- **Low Risk:** Volatility < 0.2
- **Medium Risk:** Volatility 0.2-0.4
- **High Risk:** Volatility > 0.4

**Output Includes:**

- Average volatility and Sharpe ratio
- Automated risk categorization

**Use Case:** Portfolio construction based on risk tolerance; identifying stable stocks for conservative allocations.

---

## Query 5: Best Risk-Adjusted Performers

**Purpose:** Identify top 20 stocks with optimal risk-adjusted returns.

**Ranking Criteria:**

- Ordered by average Sharpe Ratio (descending)
- Includes return and volatility metrics

**Use Case:** Finding efficient investments that maximize return per unit of risk taken.

---

## Query 6: Consistent Winners

**Purpose:** Find reliable stocks with positive returns in most years (minimum 4 positive years).

**Key Metrics:**

- Percentage of positive return years
- Total positive years count
- Average TSR across all years

**Filter:**

- Must have at least 4 years with positive returns

**Use Case:** Long-term buy-and-hold strategies focusing on consistency and reliability over time.

---

## Query 7: Sector Performance Over Time

**Purpose:** Analyze which sectors deliver the best returns annually.

**Output:**

- Average returns by sector per year
- Number of stocks per sector
- Sorted by most recent year first, then by returns

**Use Case:** Sector rotation strategies, diversification planning, and identifying cyclical patterns in different industries.

---

## Query 8: Sector Risk-Return Profile

**Purpose:** Comprehensive sector analysis including recent vs historical performance.

**Key Metrics:**

- **Recent_AvgAnnual_TSR:** Performance from 2023 onwards
- **Overall_AvgAnnual_TSR:** All-time average performance
- **TSR_Consistency:** Standard deviation showing year-to-year variability (higher = more unpredictable)
- **YearsCovered:** Data completeness
- **NoOfStocks:** Average number of stocks per year in sector

**Use Case:** Comparing sector momentum, identifying stable vs volatile sectors, assessing sector diversification.

---

## Query 9: Stock vs Sector Comparison

**Purpose:** Determine if individual stocks outperform their sector peers.

**Key Metrics:**

- **AvgAnnualReturnYearly:** Sector average for that year
- **ReturnVsSector:** How much stock beat/lagged sector (positive = outperformance)
- **AvgSharpeYearly:** Sector average Sharpe ratio
- **RiskReturnVsSector:** Risk-adjusted outperformance vs sector

**Query Logic:**

- Uses window functions to calculate sector averages
- Computes differences for each stock vs its sector
- Sorted by year and outperformance

**Use Case:** Identifying sector leaders, finding stocks that consistently beat their peers, sector-relative performance analysis.

---

## Query 10: Quality Score System

**Purpose:** Create a composite metric (0-100 scale) that combines returns and risk-adjusted performance.

**Methodology:**

### Step 1: MinMax CTE

- Calculates the highest and lowest values for returns, Sharpe ratio, and volatility per year
- Establishes year-specific ranges for normalization

### Step 2: Scores CTE

- Normalizes each metric to 0-100 scale within each year
- **AnnualScore:** Return normalized (higher = better)
- **SharpeScore:** Risk-adjusted return normalized (higher = better)
- **VolatilityScore:** Volatility inverted (lower volatility = higher score)

### Step 3: QualityScore CTE

- Calculates weighted composite score
- **Default weights:** 80% AnnualScore + 20% SharpeScore
- Joins normalized scores with stock details

### Step 4: Final Aggregation

- **RecentQualityScore:** Average for years 2023+
- **OverallQualityScore:** All-time average
- **Filter:** Requires minimum 3 years of data
- **Sorted by:** Recent quality score (descending)

**Important Note:** The query avoids using both SharpeScore and separate VolatilityScore to prevent double-counting volatility's impact. Since Sharpe ratio already incorporates volatility (return/risk), adding volatility separately would be redundant unless building an ultra-conservative portfolio.

**Weight Customization:**

- **Growth-focused:** Increase AnnualScore weight (e.g., 90% / 10%)
- **Risk-averse:** Use 50% / 50% or include VolatilityScore separately
- **Balanced:** Current 80% / 20% split

**Use Case:** Holistic stock evaluation, comparing performance across different market conditions, identifying high-quality investments with recent momentum.


## Metrics Glossary
Sharpe Ratio: >1 = good, >2 = excellent, >3 = exceptional

CV (Coefficient of Variation): Lower = more predictable returns

TSR_Consistency: Standard deviation of annual returns (higher = more volatile)

Quality Score: 0-100 composite metric (higher = better overall quality)

ReturnVsSector: Positive values indicate outperformance vs sector peers