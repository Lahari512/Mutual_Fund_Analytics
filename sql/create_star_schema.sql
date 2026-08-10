-- ==========================================
-- MUTUAL FUND ANALYTICS STAR SCHEMA
-- ==========================================

-- =========================
-- Dimension Table : Fund
-- =========================
CREATE TABLE dim_fund (

    fund_id INTEGER PRIMARY KEY AUTOINCREMENT,

    amfi_code INTEGER UNIQUE NOT NULL,

    scheme_name TEXT,

    fund_house TEXT,

    category TEXT,

    sub_category TEXT,

    plan_type TEXT,

    option_type TEXT,

    risk_grade TEXT
);

-- =========================
-- Dimension Table : Date
-- =========================
CREATE TABLE dim_date (

    date_id INTEGER PRIMARY KEY AUTOINCREMENT,

    full_date DATE UNIQUE,

    day INTEGER,

    month INTEGER,

    month_name TEXT,

    quarter INTEGER,

    year INTEGER
);

-- =========================
-- Fact Table : NAV
-- =========================
CREATE TABLE fact_nav (

    nav_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_id INTEGER,

    date_id INTEGER,

    nav REAL,

    FOREIGN KEY (fund_id)
        REFERENCES dim_fund(fund_id),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);

-- =========================
-- Fact Table : Transactions
-- =========================
CREATE TABLE fact_transactions (

    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_id INTEGER,

    date_id INTEGER,

    investor_id INTEGER,

    transaction_type TEXT,

    amount REAL,

    units REAL,

    FOREIGN KEY (fund_id)
        REFERENCES dim_fund(fund_id),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);

-- =========================
-- Fact Table : Performance
-- =========================
CREATE TABLE fact_performance (

    performance_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_id INTEGER,

    return_1yr REAL,

    return_3yr REAL,

    return_5yr REAL,

    expense_ratio REAL,

    benchmark_return REAL,

    FOREIGN KEY (fund_id)
        REFERENCES dim_fund(fund_id)
);

-- =========================
-- Fact Table : AUM
-- =========================
CREATE TABLE fact_aum (

    aum_id INTEGER PRIMARY KEY AUTOINCREMENT,

    fund_id INTEGER,

    date_id INTEGER,

    aum_cr REAL,

    FOREIGN KEY (fund_id)
        REFERENCES dim_fund(fund_id),

    FOREIGN KEY (date_id)
        REFERENCES dim_date(date_id)
);