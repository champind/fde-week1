
import json
from pathlib import Path
from collections import defaultdict

BASE_DIR = Path(__file__).resolve().parent
INVOICE_FILE = BASE_DIR / "data" / "invoices.json"
PAYMENT_FILE = BASE_DIR / "data" / "payments.json"


def load_json(path):
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"{path.name} must contain a JSON list")

        return data

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {path}")
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path.name}: {exc}"
        ) from exc


invoices = load_json(INVOICE_FILE)
payments = load_json(PAYMENT_FILE)

# 1. Normalize in place using indexes.
print("\n--- 1. NORMALIZATION ---")

invalid_indexes = []

for i in range(len(invoices)):
    invoice = invoices[i]

    invoice["vendor"] = invoice["vendor"].strip().title()
    invoice["status"] = invoice["status"].upper()

    if invoice["amount"] is None:
        invalid_indexes.append(i)
        print(
            f"Missing amount at index {i}: "
            f"{invoice['invoice_id']}"
        )

# Exclude missing amounts from all later calculations.
valid_invoices = [
    invoice
    for i, invoice in enumerate(invoices)
    if i not in invalid_indexes
]

# 2. Find exact duplicates by comparing every field.
print("\n--- 2. EXACT DUPLICATES ---")

seen = {}
exact_dupes = defaultdict(list)
unique_invoices = []

for i, invoice in enumerate(valid_invoices):
    # A sorted tuple makes a stable key from every field.
    key = tuple(sorted(invoice.items()))

    if key in seen:
        original_index = seen[key]
        exact_dupes[key].append(i)
    else:
        seen[key] = i
        exact_dupes[key] = [i]
        unique_invoices.append(invoice)

exact_dupes = {
    key: indexes
    for key, indexes in exact_dupes.items()
    if len(indexes) > 1
}

for key, indexes in exact_dupes.items():
    print(f"Duplicate row indexes: {indexes}")

print("Invoices remaining:", len(unique_invoices))

# 3. Find suspected duplicates without removing them.
print("\n--- 3. SUSPECTED DUPLICATES ---")

suspected_pairs = []

for i in range(len(unique_invoices)):
    for j in range(i + 1, len(unique_invoices)):
        first = unique_invoices[i]
        second = unique_invoices[j]

        same_details = (
            first["vendor"] == second["vendor"]
            and first["amount"] == second["amount"]
            and first["date"] == second["date"]
        )

        different_ids = (
            first["invoice_id"] != second["invoice_id"]
        )

        if same_details and different_ids:
            pair = (first["invoice_id"], second["invoice_id"])
            suspected_pairs.append(pair)
            print(f"({pair[0]} ~ {pair[1]})")

# 4. Match credit notes to positive invoices.
print("\n--- 4. CREDIT NOTES ---")

cancelled_indexes = set()
used_positive_indexes = set()

for negative_index, negative in enumerate(unique_invoices):
    if negative["amount"] >= 0:
        continue

    partner_found = False

    for positive_index, positive in enumerate(unique_invoices):
        if positive["amount"] <= 0:
            continue

        if positive_index in used_positive_indexes:
            continue

        same_vendor = (
            negative["vendor"] == positive["vendor"]
        )

        same_absolute_amount = (
            abs(negative["amount"]) == positive["amount"]
        )

        if same_vendor and same_absolute_amount:
            cancelled_indexes.add(negative_index)
            cancelled_indexes.add(positive_index)
            used_positive_indexes.add(positive_index)

            print(
                f"{negative_index} <-> {positive_index}: "
                f"{negative['invoice_id']} <-> "
                f"{positive['invoice_id']}"
            )

            partner_found = True
            break

    if not partner_found:
        print(
            f"No credit-note partner for "
            f"{negative['invoice_id']} "
            f"(index {negative_index})"
        )

for i in cancelled_indexes:
    unique_invoices[i]["status"] = "CANCELLED"

# Remaining invoices are used for totals and reconciliation.
eligible_invoices = [
    invoice
    for i, invoice in enumerate(unique_invoices)
    if i not in cancelled_indexes
]

# 5. Reconcile payments with eligible invoices.
print("\n--- 5. PAYMENT RECONCILIATION ---")

payment_totals = defaultdict(float)

for payment in payments:
    payment_totals[payment["invoice_id"]] += payment["paid"]

invoice_by_id = {
    invoice["invoice_id"]: invoice
    for invoice in eligible_invoices
}

for invoice_id, invoice in invoice_by_id.items():
    paid = payment_totals[invoice_id]
    amount = invoice["amount"]
    balance = amount - paid

    print(
        f"{invoice_id} | Vendor: {invoice['vendor']} | "
        f"Amount: {amount:.2f} | Paid: {paid:.2f} | "
        f"Balance: {balance:.2f}"
    )

# Payments with no matching eligible invoice.
for invoice_id, paid in payment_totals.items():
    if invoice_id not in invoice_by_id:
        print(
            f"UNMATCHED PAYMENT: {invoice_id} | "
            f"Paid: {paid:.2f}"
        )

total_amount = sum(
    invoice["amount"] for invoice in eligible_invoices
)

total_paid = sum(
    payment_totals[invoice["invoice_id"]]
    for invoice in eligible_invoices
)

print(f"\nTotal eligible invoice amount: {total_amount:.2f}")
print(f"Total matched payments: {total_paid:.2f}")
print(f"Outstanding balance: {total_amount - total_paid:.2f}")
