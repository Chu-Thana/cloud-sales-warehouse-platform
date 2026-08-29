TRUNCATE TABLE landing.vendor_payments_streaming_events;

COPY landing.vendor_payments_streaming_events
FROM '${STREAMING_CURATED_S3_URI}'
IAM_ROLE default
FORMAT AS CSV
IGNOREHEADER 1
QUOTE AS '"'
REGION 'ap-southeast-1'
ACCEPTINVCHARS
TRUNCATECOLUMNS;