SELECT
    scheme_name,
    aum_cr
FROM fund_master
ORDER BY aum_cr DESC
LIMIT 5;

SELECT
    strftime('%Y-%m', date) AS Month,
    ROUND(AVG(nav),2) AS Average_NAV
FROM nav_history
GROUP BY Month
ORDER BY Month;

SELECT
    strftime('%Y', transaction_date) AS Year,
    ROUND(SUM(amount),2) AS SIP_Amount
FROM investor_transactions
WHERE transaction_type='SIP'
GROUP BY Year;

SELECT
    state,
    COUNT(*) AS Total_Transactions
FROM investor_transactions
GROUP BY state
ORDER BY Total_Transactions DESC;

SELECT
    scheme_name,
    expense_ratio_pct
FROM scheme_performance
WHERE expense_ratio_pct < 1
ORDER BY expense_ratio_pct;

SELECT
    scheme_name,
    return_3yr_pct
FROM scheme_performance
ORDER BY return_3yr_pct DESC
LIMIT 10;

SELECT
    fund_house,
    COUNT(*) AS Total_Funds
FROM fund_master
GROUP BY fund_house
ORDER BY Total_Funds DESC;

SELECT
    category,
    ROUND(AVG(expense_ratio_pct),2) AS Avg_Expense
FROM scheme_performance
GROUP BY category;

SELECT
    investor_id,
    amount,
    transaction_type
FROM investor_transactions
ORDER BY amount DESC
LIMIT 10;

SELECT
    ROUND(AVG(return_5yr_pct),2) AS Average_5Y_Return
FROM scheme_performance;