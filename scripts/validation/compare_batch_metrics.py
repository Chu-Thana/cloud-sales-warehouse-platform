from __future__ import annotations

from decimal import Decimal


ROUNDING_TOLERANCE_PER_ROW = Decimal("0.005")


def compare_batch_metrics(
    athena_results: list[dict[str, str]],
    redshift_results: list[dict[str, str]],
) -> None:
    athena_by_dataset = {
        row["dataset_name"]: row
        for row in athena_results
    }

    redshift_by_dataset = {
        row["dataset_name"]: row
        for row in redshift_results
    }

    if athena_by_dataset.keys() != redshift_by_dataset.keys():
        raise ValueError(
            "Batch validation dataset names do not match."
        )

    errors: list[str] = []

    for dataset_name in athena_by_dataset:
        athena = athena_by_dataset[dataset_name]
        redshift = redshift_by_dataset[dataset_name]

        athena_row_count = int(
            athena["row_count"]
        )
        redshift_row_count = int(
            redshift["row_count"]
        )

        if athena_row_count != redshift_row_count:
            errors.append(
                f"{dataset_name} row_count mismatch: "
                f"Athena={athena_row_count}, "
                f"Redshift={redshift_row_count}"
            )

        athena_source_count = int(
            athena["source_record_count"]
        )
        redshift_source_count = int(
            redshift["source_record_count"]
        )

        if athena_source_count != redshift_source_count:
            errors.append(
                f"{dataset_name} source_record_count mismatch: "
                f"Athena={athena_source_count}, "
                f"Redshift={redshift_source_count}"
            )

        monetary_tolerance = (
            Decimal(str(athena_row_count))
            * ROUNDING_TOLERANCE_PER_ROW
        )

        for metric_name in (
            "total_vouchers_paid",
            "total_vouchers_pending",
        ):
            athena_value = Decimal(
                athena[metric_name]
            )
            redshift_value = Decimal(
                redshift[metric_name]
            )

            difference = abs(
                athena_value - redshift_value
            )

            if difference > monetary_tolerance:
                errors.append(
                    f"{dataset_name} {metric_name} mismatch: "
                    f"Athena={athena_value}, "
                    f"Redshift={redshift_value}, "
                    f"difference={difference}, "
                    f"tolerance={monetary_tolerance}"
                )

    if errors:
        raise ValueError(
            "Batch cross-layer validation failed:\n"
            + "\n".join(errors)
        )

    print(
        "Batch cross-layer validation: PASS"
    )