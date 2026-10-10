import json
from pathlib import Path

# Resolve the invoice JSON file relative to this script.
current_dir = Path(__file__).resolve().parent
invoices_file = current_dir / "data" / "invoices.json"

with open(invoices_file, "r", encoding="utf-8") as file:
    invoices = json.load(file)

# Sort invoices by amount in descending order
sorted_by_amount = sorted(invoices, key=lambda invoice: invoice["amount"], reverse=True)

print("==========================================")
print("     EXERCISE: SORT INVOICES BY AMOUNT     ")
print("==========================================")
for invoice in sorted_by_amount:
    print(f"{invoice['invoice_id']:<10} | {invoice['vendor']:<16} | ${invoice['amount']:.2f}")

# Also show vendor names sorted alphabetically
sorted_vendors = sorted({invoice["vendor"] for invoice in invoices})
print("\n==========================================")
print("     VENDORS IN ALPHABETICAL ORDER         ")
print("==========================================")
for vendor in sorted_vendors:
    print(vendor)
