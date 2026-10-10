import json
from pathlib import Path
from collections import defaultdict

# Dynamically resolve the JSON file relative to this script.
# This script lives in day3_cra, while the data file is inside the day3_cra/data folder.
current_dir = Path(__file__).resolve().parent
data_file = current_dir / "data" / "invoices.json"

# Load JSON data
with open(data_file, "r", encoding="utf-8") as file:
    invoices = json.load(file)


# -------------------------------------------------------------------------
# Exercise 1: Totals of the amount by vendor (using enumerate for indexing)
# -------------------------------------------------------------------------
vendor_totals = {}

for index, invoice in enumerate(invoices):
    vendor = invoice["vendor"]
    amount = invoice["amount"]
    vendor_totals[vendor] = vendor_totals.get(vendor, 0.0) + amount

print("==========================================")
print("  EXERCISE 1: AMOUNT TOTALS BY VENDOR     ")
print("==========================================")
for vendor, total in vendor_totals.items():
    print(f"Vendor: {vendor:<16} | Total: ${total:.2f}")


# -------------------------------------------------------------------------
# Exercise 2: Track indices to filter and print duplicate vendors alone
# -------------------------------------------------------------------------
# Map each vendor to all row indices where it was encountered
vendor_index_map = defaultdict(list)

for index, invoice in enumerate(invoices):
    vendor_name = invoice["vendor"]
    vendor_index_map[vendor_name].append(index)

print("\n==========================================")
print("  EXERCISE 2: DUPLICATE VENDORS ALONE     ")
print("==========================================")
for vendor, indices in vendor_index_map.items():
    # A vendor is duplicate if it appears at more than 1 index position
    if len(indices) > 1:
        print(f"\n[DUPLICATE] Vendor: '{vendor}'")
        print(f"Total Occurrences: {len(indices)} at index positions {indices}")
        for idx in indices:
            inv = invoices[idx]
            print(f"  -> Index [{idx}] | ID: {inv['invoice_id']} | Amount: ${inv['amount']:.2f}")