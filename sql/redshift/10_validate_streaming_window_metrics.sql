SELECT
    COUNT(*) AS row_count,
    COUNT(DISTINCT event_id) AS distinct_event_count,
    SUM(CAST(payment_amount AS DOUBLE PRECISION)) AS total_payment_amount
FROM landing.vendor_payments_streaming_events
WHERE window_id = '${STREAMING_WINDOW_ID}';