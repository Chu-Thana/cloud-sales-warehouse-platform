SELECT
    'spending_by_fiscal_year' AS dataset_name,
    COUNT(*) AS row_count,
    SUM(record_count) AS source_record_count,
    SUM(total_vouchers_paid) AS total_vouchers_paid,
    SUM(total_vouchers_pending) AS total_vouchers_pending
FROM landing.spending_by_fiscal_year

UNION ALL

SELECT
    'spending_by_supplier_top_n' AS dataset_name,
    COUNT(*) AS row_count,
    SUM(record_count) AS source_record_count,
    SUM(total_vouchers_paid) AS total_vouchers_paid,
    SUM(total_vouchers_pending) AS total_vouchers_pending
FROM landing.spending_by_supplier_top_n

UNION ALL

SELECT
    'pending_by_department' AS dataset_name,
    COUNT(*) AS row_count,
    SUM(record_count) AS source_record_count,
    SUM(total_vouchers_paid) AS total_vouchers_paid,
    SUM(total_vouchers_pending) AS total_vouchers_pending
FROM landing.pending_by_department;