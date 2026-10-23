import argparse
import csv
import sys
from decimal import Decimal, InvalidOperation
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CSV = BASE_DIR.parent / "homework_invoices.csv"
REQUIRED_COLUMNS = ("invoice_id", "vendor", "amount", "status")


def validate_csv(path: Path) -> list[str]:
    errors = []

    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames

        if headers is None:
            return ["CSV file is empty or has no header row"]

        missing_columns = [
            column for column in REQUIRED_COLUMNS if column not in headers
        ]
        if missing_columns:
            return [
                "Missing required columns: " + ", ".join(missing_columns)
            ]

        if len(headers) != len(set(headers)):
            return ["CSV header contains duplicate column names"]

        for row_number, row in enumerate(reader, start=2):
            if None in row:
                errors.append(f"Row {row_number}: contains extra columns")

            for column in REQUIRED_COLUMNS:
                value = row.get(column)
                if value is None or not value.strip():
                    errors.append(
                        f"Row {row_number}: {column} is required"
                    )

            amount = row.get("amount")
            if amount is not None and amount.strip():
                try:
                    parsed_amount = Decimal(amount)
                    if not parsed_amount.is_finite():
                        raise InvalidOperation
                except InvalidOperation:
                    errors.append(
                        f"Row {row_number}: amount must be a finite number"
                    )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate an invoice CSV file."
    )
    parser.add_argument(
        "csv_file",
        nargs="?",
        type=Path,
        default=DEFAULT_CSV,
        help=f"CSV file to validate (default: {DEFAULT_CSV})",
    )
    args = parser.parse_args()

    try:
        errors = validate_csv(args.csv_file)
    except (OSError, csv.Error) as exc:
        print(
            f"Unable to read or parse {args.csv_file}: {exc}",
            file=sys.stderr,
        )
        return 2

    if errors:
        for error in errors:
            print(error)
        print(f"CSV validation failed with {len(errors)} error(s).")
        return 1

    print(f"CSV validation passed: {args.csv_file}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
