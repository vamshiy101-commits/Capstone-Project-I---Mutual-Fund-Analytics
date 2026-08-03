-- =========================================
-- Mutual Fund ETL Project
-- SQLite Star Schema
-- =========================================

-- =========================================
-- Dimension Table : Fund
-- =========================================

CREATE TABLE dim_fund (
    fund_id INTEGER PRIMARY KEY AUTOINCREMENT,
    amfi_code INTEGER UNIQUE NOT NULL,
    scheme_name TEXT NOT NULL,
    fund_house TEXT,
    category TEXT,
    sub_category TEXT,
    plan TEXT,
    risk_grade TEXT
);

-- =========================================
-- Dimension Table : Date
-- =========================================

CREATE TABLE dim_date (
    date_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_date DATE UNIQUE NOT NULL,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    quarter INTEGER
);

-- =========================================
-- Fact Table : NAV
-- =========================================

CREATE TABLE fact_nav (
    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    date_id INTEGER,
    nav_value REAL,

    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);


-- =========================================
-- Fact Table : Performance
-- =========================================

CREATE TABLE fact_performance (
    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    return_1yr_pct REAL,
    return_3yr_pct REAL,
    return_5yr_pct REAL,
    benchmark_3yr_pct REAL,
    alpha REAL,
    beta REAL,
    sharpe_ratio REAL,
    sortino_ratio REAL,
    std_dev_ann_pct REAL,
    max_drawdown_pct REAL,

    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id)
);


-- =========================================
-- Fact Table : AUM
-- =========================================

CREATE TABLE fact_aum (
    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    aum_crore REAL,
    expense_ratio_pct REAL,
    morningstar_rating INTEGER,

    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id)
);




-- =========================================
-- Fact Table : Transactions
-- =========================================

CREATE TABLE fact_transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fund_id INTEGER,
    transaction_date DATE,
    transaction_type TEXT,
    amount REAL,
    units REAL,
    state TEXT,
    kyc_status TEXT,

    FOREIGN KEY (fund_id) REFERENCES dim_fund(fund_id)
);