-- Workflow 2: 7-day moving average of copay revenue per clinic with DENSE_RANK()
WITH daily_revenue AS (
    SELECT 
        clinic_id,
        DATE(created_at) AS transaction_date,
        SUM(copay_amount) AS daily_total
    FROM appointments
    GROUP BY clinic_id, DATE(created_at)
),
moving_averages AS (
    SELECT 
        clinic_id,
        transaction_date,
        daily_total,
        AVG(daily_total) OVER (
            PARTITION BY clinic_id 
            ORDER BY transaction_date 
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ) AS moving_avg_7d
    FROM daily_revenue
)
SELECT 
    clinic_id,
    transaction_date,
    daily_total,
    ROUND(moving_avg_7d, 2) AS moving_avg_7d,
    DENSE_RANK() OVER (PARTITION BY transaction_date ORDER BY moving_avg_7d DESC) AS rank_by_revenue
FROM moving_averages
ORDER BY transaction_date DESC, rank_by_revenue ASC;
