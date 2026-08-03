import sqlite3
import pandas as pd

conn = sqlite3.connect("bluestock_mf.db")

queries = [
    ("Top 5 Funds by AUM", """
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
    """),

    ("Average NAV per Month", """
        SELECT
            strftime('%Y-%m', date) AS month,
            ROUND(AVG(nav),2) AS average_nav
        FROM fact_nav
        GROUP BY month
        ORDER BY month;
    """),

    ("SIP Year-wise Investment", """
        SELECT
            strftime('%Y', transaction_date) AS year,
            SUM(amount_inr) AS total_sip_amount
        FROM fact_transactions
        WHERE transaction_type='SIP'
        GROUP BY year
        ORDER BY year;
    """),

    ("Transactions by State", """
        SELECT
            state,
            COUNT(*) AS total_transactions
        FROM fact_transactions
        GROUP BY state
        ORDER BY total_transactions DESC;
    """),

    ("Funds with Expense Ratio < 1%", """
        SELECT
            d.scheme_name,
            a.expense_ratio_pct
        FROM fact_aum a
        JOIN dim_fund d
        ON a.amfi_code=d.amfi_code
        WHERE a.expense_ratio_pct<1
        ORDER BY a.expense_ratio_pct;
    """),

    ("Top 5 Funds by 5-Year Return", """
        SELECT
            scheme_name,
            return_5yr_pct
        FROM fact_performance
        ORDER BY return_5yr_pct DESC
        LIMIT 5;
    """),

    ("Average Expense Ratio", """
        SELECT
            ROUND(AVG(expense_ratio_pct),2) AS average_expense_ratio
        FROM fact_aum;
    """),

    ("Morningstar Rating Distribution", """
        SELECT
            morningstar_rating,
            COUNT(*) AS total_funds
        FROM fact_aum
        GROUP BY morningstar_rating;
    """),

    ("Total NAV Records", """
        SELECT COUNT(*) AS total_nav_records
        FROM fact_nav;
    """),

    ("Average Transaction Amount", """
        SELECT
            transaction_type,
            ROUND(AVG(amount_inr),2) AS average_amount
        FROM fact_transactions
        GROUP BY transaction_type;
    """)
]

for title, query in queries:
    print("\n" + "="*70)
    print(title)
    print("="*70)
    df = pd.read_sql_query(query, conn)
    print(df)

conn.close()