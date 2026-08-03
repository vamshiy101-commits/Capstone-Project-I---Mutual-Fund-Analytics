-- =========================================
-- Mutual Fund ETL Project
-- Analytical SQL Queries
-- =========================================

------------------------------------------------------------
-- 1. Top 5 Funds by AUM
------------------------------------------------------------
SELECT
    d.scheme_name,
    d.fund_house,
    a.amfi_code,
    a.aum_crore
FROM fact_aum a
JOIN dim_fund d
ON a.amfi_code = d.amfi_code
ORDER BY a.aum_crore DESC
LIMIT 5;


------------------------------------------------------------
-- 2. Average NAV per Month
------------------------------------------------------------
SELECT
    strftime('%Y-%m', date) AS month,
    ROUND(AVG(nav), 2) AS average_nav
FROM fact_nav
GROUP BY month
ORDER BY month;


------------------------------------------------------------
-- 3. SIP Year-wise Investment (YoY)
------------------------------------------------------------
SELECT
    strftime('%Y', transaction_date) AS year,
    SUM(amount_inr) AS total_sip_amount
FROM fact_transactions
WHERE transaction_type = 'SIP'
GROUP BY year
ORDER BY year;


------------------------------------------------------------
-- 4. Transactions by State
------------------------------------------------------------
SELECT
    state,
    COUNT(*) AS total_transactions
FROM fact_transactions
GROUP BY state
ORDER BY total_transactions DESC;


------------------------------------------------------------
-- 5. Funds with Expense Ratio Less Than 1%
------------------------------------------------------------
SELECT
    d.scheme_name,
    a.amfi_code,
    a.expense_ratio_pct
FROM fact_aum a
JOIN dim_fund d
ON a.amfi_code = d.amfi_code
WHERE a.expense_ratio_pct < 1
ORDER BY a.expense_ratio_pct;


------------------------------------------------------------
-- 6. Top 5 Funds by 5-Year Return
------------------------------------------------------------
SELECT
    scheme_name,
    fund_house,
    return_5yr_pct
FROM fact_performance
ORDER BY return_5yr_pct DESC
LIMIT 5;


------------------------------------------------------------
-- 7. Average Expense Ratio
------------------------------------------------------------
SELECT
    ROUND(AVG(expense_ratio_pct), 2) AS average_expense_ratio
FROM fact_aum;


------------------------------------------------------------
-- 8. Morningstar Rating Distribution
------------------------------------------------------------
SELECT
    morningstar_rating,
    COUNT(*) AS total_funds
FROM fact_aum
GROUP BY morningstar_rating
ORDER BY morningstar_rating DESC;


------------------------------------------------------------
-- 9. Total NAV Records
------------------------------------------------------------
SELECT
    COUNT(*) AS total_nav_records
FROM fact_nav;


------------------------------------------------------------
-- 10. Average Transaction Amount by Transaction Type
------------------------------------------------------------
SELECT
    transaction_type,
    ROUND(AVG(amount_inr), 2) AS average_transaction_amount
FROM fact_transactions
GROUP BY transaction_type
ORDER BY average_transaction_amount DESC;