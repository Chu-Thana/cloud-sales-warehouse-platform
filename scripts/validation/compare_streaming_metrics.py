from __future__ import annotations

from decimal import Decimal


PAYMENT_AMOUNT_TOLERANCE = Decimal("0.01")


def compare_streaming_metrics(
    athena_metrics: dict[str, str],
    redshift_metrics: dict[str, str],
) -> None:
    errors: list[str] = []

    athena_row_count = int(
        athena_metrics["row_count"]
    )
    redshift_row_count = int(
        redshift_metrics["row_count"]
    )

    if athena_row_count != redshift_row_count:
        errors.append(
            "row_count mismatch: "
            f"Athena={athena_row_count}, "
            f"Redshift={redshift_row_count}"
        )

    athena_distinct_event_count = int(
        athena_metrics["distinct_event_count"]
    )
    redshift_distinct_event_count = int(
        redshift_metrics["distinct_event_count"]
    )

    if (
        athena_distinct_event_count
        != redshift_distinct_event_count
    ):
        errors.append(
            "distinct_event_count mismatch: "
            f"Athena={athena_distinct_event_count}, "
            f"Redshift={redshift_distinct_event_count}"
        )

    athena_total_payment_amount = Decimal(
        athena_metrics["total_payment_amount"]
    )
    redshift_total_payment_amount = Decimal(
        redshift_metrics["total_payment_amount"]
    )

    payment_amount_difference = abs(
        athena_total_payment_amount
        - redshift_total_payment_amount
    )

    if (
        payment_amount_difference
        > PAYMENT_AMOUNT_TOLERANCE
    ):
        errors.append(
            "total_payment_amount mismatch: "
            f"Athena={athena_total_payment_amount}, "
            f"Redshift={redshift_total_payment_amount}, "
            f"difference={payment_amount_difference}"
        )

    if errors:
        raise ValueError(
            "Streaming cross-layer validation failed:\n"
            + "\n".join(errors)
        )

    print(
        "Streaming cross-layer validation: PASS"
    )