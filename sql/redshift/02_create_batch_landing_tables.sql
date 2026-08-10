CREATE TABLE IF NOT EXISTS landing.vendor_payments_streaming_events (
    fiscal_year                 INTEGER,
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);


CREATE TABLE IF NOT EXISTS landing.spending_by_department (
    fiscal_year                 INTEGER,
    organization_group          VARCHAR(256),
    department                  VARCHAR(256),
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);


CREATE TABLE IF NOT EXISTS landing.spending_by_supplier_top_n (
    supplier_name               VARCHAR(512),
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);


CREATE TABLE IF NOT EXISTS landing.fund_category_summary (
    fiscal_year                 INTEGER,
    fund_type                   VARCHAR(256),
    fund_category               VARCHAR(256),
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);


CREATE TABLE IF NOT EXISTS landing.pending_by_department (
    fiscal_year                 INTEGER,
    department                  VARCHAR(256),
    total_vouchers_paid         DECIMAL(20, 2),
    total_vouchers_pending      DECIMAL(20, 2),
    total_encumbrance_balance   DECIMAL(20, 2),
    total_pending_retainage     DECIMAL(20, 2),
    record_count                BIGINT,
    unique_suppliers            BIGINT,
    negative_paid_records       BIGINT,
    large_paid_1m_records       BIGINT,
    missing_po_date_records     BIGINT
);