SELECT
    'spending_by_fiscal_year' AS dataset_name,
    COUNT(*) AS row_count,
    SUM(record_count) AS source_record_count,
    SUM(CAST(total_vouchers_paid AS DECIMAL(20, 2))) AS total_vouchers_paid,
    SUM(CAST(total_vouchers_pending AS DECIMAL(20, 2))) AS total_vouchers_pending
FROM vendor_payments_analytics.mart_spending_by_fiscal_year

UNION ALL

SELECT
    'spending_by_supplier_top_n' AS dataset_name,
    COUNT(*) AS row_count,
    SUM(record_count) AS source_record_count,
    SUM(CAST(total_vouchers_paid AS DECIMAL(20, 2))) AS total_vouchers_paid,
    SUM(CAST(total_vouchers_pending AS DECIMAL(20, 2))) AS total_vouchers_pending
FROM vendor_payments_analytics.mart_spending_by_supplier_top_n

UNION ALL

SELECT
    'pending_by_department' AS dataset_name,
    COUNT(*) AS row_count,
    SUM(record_count) AS source_record_count,
    SUM(CAST(total_vouchers_paid AS DECIMAL(20, 2))) AS total_vouchers_paid,
    SUM(CAST(total_vouchers_pending AS DECIMAL(20, 2))) AS total_vouchers_pending
FROM vendor_payments_analytics.mart_pending_by_department;