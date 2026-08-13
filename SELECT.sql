SELECT
    scheme_name,
    fund_house,
    morningstar_rating,
    risk_grade,
    return_3yr_pct
FROM scheme_performance
WHERE morningstar_rating IS NOT NULL
ORDER BY
    morningstar_rating DESC,
    return_3yr_pct DESC
LIMIT 10;