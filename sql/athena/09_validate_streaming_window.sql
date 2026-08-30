SELECT
  COUNT(*) AS row_count,
  COUNT(DISTINCT event_id) AS distinct_event_count,
  SUM(CAST(payment_amount AS DOUBLE)) AS total_payment_amount
FROM vendor_payments_analytics.vendor_payments_streaming_events;