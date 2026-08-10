-- ============================================================
-- Mutual Fund Analytics - Analytical SQL Queries
-- ============================================================


-- Query 1: Top 5 Fund Houses by Latest AUM
-- Purpose: Identify the five largest fund houses by latest AUM.

SELECT
    fund_house,
    date,
    aum_crore,
    num_schemes
FROM aum_by_fund_house
WHERE date = (
    SELECT MAX(date)
    FROM aum_by_fund_house
)
ORDER BY aum_crore DESC
LIMIT 5;


-- ============================================================


-- Query 2: Average NAV Per Month
-- Purpose: Calculate the average NAV across all schemes for each month.

SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 2) AS average_nav
FROM nav_history
GROUP BY strftime('%Y-%m', date)
ORDER BY month;


-- ============================================================


-- Query 3: SIP Year-over-Year Growth
-- Purpose: Calculate yearly SIP totals and YoY growth.

WITH yearly_sip AS (
    SELECT
        strftime('%Y', transaction_date) AS year,
        SUM(amount_inr) AS total_sip
    FROM investor_transactions
    WHERE transaction_type = 'SIP'
    GROUP BY strftime('%Y', transaction_date)
)

SELECT
    year,
    ROUND(total_sip, 2) AS total_sip_inr,
    ROUND(
        (total_sip - LAG(total_sip) OVER (ORDER BY year))
        * 100.0
        / LAG(total_sip) OVER (ORDER BY year),
        2
    ) AS yoy_growth_pct
FROM yearly_sip
ORDER BY year;


-- ============================================================


-- Query 4: Transactions by State
-- Purpose: Compare transaction volume and transaction value by state.

SELECT
    state,
    COUNT(*) AS total_transactions,
    ROUND(SUM(amount_inr), 2) AS total_amount_inr
FROM investor_transactions
GROUP BY state
ORDER BY total_transactions DESC;


-- ============================================================


-- Query 5: Schemes with Expense Ratio Below 1%
-- Purpose: Identify schemes with relatively low expense ratios.

SELECT
    scheme_name,
    fund_house,
    expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct ASC;


-- ============================================================
-- Queries 6-10 will be added after verifying the actual
-- scheme_performance table columns.
-- ============================================================