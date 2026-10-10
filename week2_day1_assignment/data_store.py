
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PAYMENT_FILE = DATA_DIR / "payments.json"
INVOICE_FILE = DATA_DIR / "invoices.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path):
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, list):
            raise ValueError(f"{path.name} must contain a JSON list")

        return data

    except FileNotFoundError:
        return []

    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path.name}: {exc}"
        ) from exc


def save_json(path, data):
    with path.open("w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)


def load_payments():
    return load_json(PAYMENT_FILE)


def save_payments(payments):
    save_json(PAYMENT_FILE, payments)


def load_invoices():
    return load_json(INVOICE_FILE)
