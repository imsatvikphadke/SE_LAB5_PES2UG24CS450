import json
import sqlite3
from datetime import datetime

conn = sqlite3.connect(":memory:")
stock = {}
prescriptions = []


def setup_database():
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS patients "
        "(id TEXT, name TEXT, allergy TEXT)"
    )
    cursor.execute(
        "INSERT INTO patients VALUES ('P1', 'Kavya', 'penicillin')"
    )
    cursor.execute(
        "INSERT INTO patients VALUES ('P2', 'Arjun', 'none')"
    )
    cursor.execute(
        "INSERT INTO patients VALUES ('P3', 'Meena', 'ibuprofen')"
    )
    conn.commit()


def find_patient(name):
    cursor = conn.cursor()
    query = "SELECT id, allergy FROM patients WHERE name = ?"
    return cursor.execute(query, (name,)).fetchall()


def add_stock(drug, units, expiry, batch_log=None):
    if units < 0:
        raise ValueError("Stock units cannot be negative.")

    if batch_log is None:
        batch_log = []

    current_units = stock.get(drug, {}).get("units", 0)
    stock[drug] = {
        "units": current_units + units,
        "expiry": expiry,
    }
    batch_log.append((drug, units))
    return len(batch_log)


def dispense(patient_name, drug, units):
    patients = find_patient(patient_name)
    if not patients or units <= 0:
        return False

    patient_id, allergy = patients[0]

    if allergy.casefold() not in {"", "none"}:
        if allergy.casefold() == drug.casefold():
            print("Allergy warning for", patient_name)
            return False

    stock_drug = next(
        (name for name in stock if name.casefold() == drug.casefold()),
        None,
    )

    if stock_drug is None or stock[stock_drug]["units"] < units:
        return False

    stock[stock_drug]["units"] -= units
    prescriptions.append(
        {
            "patient": patient_id,
            "drug": stock_drug,
            "units": units,
            "time": datetime.now().isoformat(timespec="seconds"),
        }
    )
    return True


def expiring_soon(days=30):
    soon = []

    for drug, details in stock.items():
        expiry = datetime.strptime(details["expiry"], "%Y-%m-%d")
        if (expiry - datetime.now()).days < days:
            soon.append(drug)

    return soon


def export_prescriptions(file="prescriptions.json"):
    with open(file, "w", encoding="utf-8") as prescription_file:
        json.dump(prescriptions, prescription_file, indent=2)


def load_stock(file="stock.json"):
    try:
        with open(file, "r", encoding="utf-8") as stock_file:
            loaded_stock = json.load(stock_file)
    except FileNotFoundError:
        return
    except json.JSONDecodeError as error:
        print(f"Error: Invalid stock JSON: {error}")
        return
    except OSError as error:
        print(f"Error reading stock file: {error}")
        return

    if not isinstance(loaded_stock, dict):
        print("Error: Stock data must be a JSON object.")
        return

    stock.clear()
    stock.update(loaded_stock)


def print_stock():
    print("Pharmacy Stock")

    for drug, details in stock.items():
        print(
            drug,
            "->",
            details["units"],
            "units, expires",
            details["expiry"],
        )


def main():
    setup_database()
    load_stock()

    add_stock("Paracetamol", 100, "2027-03-01")
    add_stock("Amoxicillin", 40, "2027-12-31")
    add_stock("Penicillin", 50, "2027-01-15")
    add_stock("Ibuprofen", 15, "2026-11-30")

    print("Arjun gets Amoxicillin:", dispense("Arjun", "Amoxicillin", 30))
    print("Kavya gets Penicillin:", dispense("Kavya", "Penicillin", 10))
    print("Meena gets ibuprofen:", dispense("Meena", "ibuprofen", 2))
    print("Unknown patient:", dispense("Ghost", "Paracetamol", 5))

    name = input("Patient name to look up (Enter for Arjun): ") or "Arjun"
    print("Lookup result:", find_patient(name))
    print("Expiring within 30 days:", expiring_soon())

    export_prescriptions()
    print_stock()


if __name__ == "__main__":
    main()
