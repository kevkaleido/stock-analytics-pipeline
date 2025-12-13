--1. Predictable High-Performing Stocks
SELECT
	Ticker,
	CompanyName,
	AVG(SharpeRatio) as AvgSharpeRatio,
	STDEV(SharpeRatio) as StdSharpeRatio,  -- volatility of stock sharperatio, higher means riskier
	MIN(SharpeRatio) as MinSharpeRatio,
	MAX(SharpeRatio) as MaxsharpeRatio,
	Sector,
	--Coefficient of Variation(CV) -- measures volatility relative to average return,
	--lower CV means predictable and steadier while higher CV means more volatile and riskier
	STDEV(Annual_TSR) / AVG(Annual_TSR) as CV_Returns,
	AVG(Annual_TSR) as Avg_TSR
FROM stock_metrics_yearly
GROUP BY Ticker, CompanyName, Sector
HAVING AVG(SharpeRatio) > 1  
ORDER BY CV_Returns, Avg_TSR desc



--2. Which stocks gave the best returns each year
--Top stocks by annualTSR per year
SELECT 
	Year,
	Ticker,
	CompanyName,
	concat(round(Annual_TSR, 2) * 100, '%') as Annual_TSR,
	Sector
FROM (
	SELECT 
		*,
		ROW_NUMBER() OVER(PARTITION BY YEAR ORDER BY Annual_TSR DESC) as Rank
	FROM stock_metrics_yearly)sub
WHERE Rank < 6



--3. Best risk-adjusted performers
SELECT TOP 20
	Ticker,
	CompanyName,
	AVG(Annual_TSR) as AvgReturn,
	AVG(AnnualVolatility) as AvgVolatility,
	AVG(SharpeRatio) as AvgSharpe,
	Sector
FROM stock_metrics_yearly
GROUP BY Ticker, CompanyName, Sector
ORDER BY AvgSharpe DESC



--4. Which stocks are most/least stable?
SELECT 
	Ticker,
	CompanyName,
	ROUND(AVG(AnnualVolatility), 2) as AvgVolatility,
	ROUND(AVG(SharpeRatio), 2) as AvgSharpe,
CASE
	WHEN AVG(AnnualVolatility) < 0.2 THEN 'Low Risk'
	WHEN AVG(AnnualVolatility) < 0.4 THEN 'Medium Risk'
ELSE 'High Risk' END as RiskCategory,
	Sector
FROM stock_metrics_yearly
GROUP BY Ticker,CompanyName, Sector
ORDER BY AvgVolatility 




--5. Stocks with positive returns in most years, at least with four positive years
SELECT
	ticker,
	CompanyName,
	Sector,
	AVG(Annual_TSR) as Avg_TSR,
	COUNT(*)  as TotalYear,
	SUM(CASE WHEN Annual_TSR > 0 THEN 1 ELSE 0 END) as PositiveYears,
	ROUND(CAST(SUM(CASE WHEN Annual_TSR > 0 THEN 1  ELSE 0 END) AS FLOAT) / COUNT(*) * 100, 2) as PercOfPositiveReturns
FROM stock_metrics_yearly
GROUP BY ticker, CompanyName, Sector
HAVING SUM(CASE WHEN Annual_TSR > 0 THEN 1 ELSE 0 END) > 3
ORDER BY  PercOfPositiveReturns DESC



--Sector Analysis

--6 Which sectors perform best over time?
-- Average returns by sector per year
SELECT 
	Sector,
	Year,
	ROUND(AVG(Annual_TSR) * 100, 2)  as AvgReturn,
	COUNT(*) aS StockCount
FROM stock_metrics_yearly
GROUP BY Year, Sector
ORDER BY Year DESC, AvgReturn DESC


--7. Sector Risk-Return Profile
SELECT
    Sector,
    AVG(CASE WHEN year >= 2023 THEN Annual_TSR END) as Recent_AvgAnnual_TSR,
    AVG(Annual_TSR) as Overall_AvgAnnual_TSR,
    AVG(SharpeRatio) as AvgSharpeRatio,
	-- TSR_consistency measures how much a stock's returns vary year-to-year.
    STDEV(Annual_TSR) as TSR_Consistency, --yearly swings, higher means more unpredicatable
    COUNT(DISTINCT year) as YearsCovered,
    COUNT(*) / COUNT(DISTINCT year) as NoOfStocks
FROM stock_metrics_yearly
GROUP BY Sector
ORDER BY AvgSharpeRatio DESC



--8. Is stock beating its sector?
-- Sector averages and comparisons
SELECT 
	Sector,
	Ticker,
	CompanyName,
	Year,
	ROUND(AVG(Annual_TSR) OVER(PARTITION BY Sector, Year), 2) as AvgAnnualReturnYearly,
	ROUND(Annual_TSR - AVG(Annual_TSR) OVER(PARTITION BY Sector, Year), 2) as ReturnVsSector,
	ROUND(AVG(SharpeRatio) OVER(PARTITION BY Sector, Year), 2) as AvgSharpeYearly,
	ROUND(SharpeRatio - AVG(SharpeRatio) OVER(PARTITION BY Sector, Year), 2) as RiskReturnVsSector
FROM stock_metrics_yearly
ORDER BY Year DESC, ReturnVsSector DESC



--9. Quality score: this calculates the quality of a stock considering the annual return,
--volatility and risk adjusted return(sharperatio)
WITH MinMax as (
SELECT 
	Year,
	MAX(Annual_TSR) as MaxAnnual_TSR,
	MIN(Annual_TSR) as MinAnnual_TSR,
	MAX(SharpeRatio) as MaxSharpe,
	MIN(SharpeRatio) as MinSharpe,
	MAX(AnnualVolatility) as MaxVolatility,
	MIN(AnnualVolatility) as MinVolatilty
FROM stock_metrics_yearly
GROUP BY Year
)

,

Scores as (
SELECT 
	s.Year,
	s.Ticker,
	ROUND((s.Annual_TSR - m.MinAnnual_TSR) / (m.MaxAnnual_TSR - m.MinAnnual_TSR) * 100, 2) as AnnualScore,
	ROUND((s.SharpeRatio - m.MinSharpe) / (m.MaxSharpe - m.MinSharpe) * 100, 2) as SharpeScore,
	ROUND((m.MaxVolatility - s.AnnualVolatility) / (m.MaxVolatility - m.MaxVolatility), 2) as VolatiltyScore
	FROM stock_metrics_yearly s
INNER JOIN MinMax m
ON s.Year = m.Year)
,

QualityScore as (
SELECT 
	sm.Ticker,
	sm.CompanyName,
	sm.Sector,
	sm.Industry,
	sm.Year,
	--adjust number based on what you prioritize in a stock
	--both numbers must always be equal to 1)
	(s.AnnualScore * 0.8) + (s.SharpeScore * 0.2) as QualityScore
FROM stock_metrics_yearly sm 
INNER JOIN scores s
ON sm.ticker = s.ticker AND sm.year = s.year)

--note:
--I realized that including both SharpeScore (30%) AND VolatilityScore (30%) separately to AnnualScore (40%) means I am essentially double-counting volatility's impact.
-- so I used just AnnualScore(50%) and SharpeScore(50%) since Sharpe already tells me if returns justify the risk. Adding volatility separately becomes redundant.
--unless I am building a low risk portfolio where I am extra cautious about volatility, then i can use all three

--aggregating quality score by year
SELECT 
	Ticker,
	CompanyName,
	Sector,
	Industry,
	COUNT(*) as NoOfYears,
	ROUND(AVG(CASE WHEN Year > '2022' THEN QualityScore END), 2) as RecentQualityScore,
	ROUND(AVG(QualityScore),2) as OverallQualityScore
FROM QualityScore
GROUP BY Ticker,CompanyName,Sector,Industry
HAVING COUNT(*) > 2 --where stock has up to 3 years data
ORDER BY RecentQualityScore DESC

