
"""Car rental system used for the static code analysis lab."""

import hashlib
import os
import re
import secrets
import sqlite3
import tempfile
from datetime import datetime

# Global rental state
fleet = {}
bookings = []
conn = sqlite3.connect(":memory:")
conn.execute(
    "CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)"
)


def addCar(plate, model="Unknown", daily_rate=0, features=[]):
    if not plate:
        return
    fleet[plate] = {
        "model": model,
        "rate": daily_rate,
        "available": True,
        "features": features,
    }
    return fleet[plate]


def registerCustomer(name, licence, phone):
    conn.execute(
        "INSERT INTO customers VALUES (?, ?, ?)",
        (name, licence, phone),
    )


def findCustomer(name):
    query = "SELECT * FROM customers WHERE name = ?"
    return conn.execute(query, (name,)).fetchall()


def rentCar(plate, customer, start, end):
    if not findCustomer(customer):
        raise ValueError("Customer not registered")

    if plate not in fleet:
        raise ValueError("Car not found")

    days = (
        datetime.strptime(end, "%Y-%m-%d")
        - datetime.strptime(start, "%Y-%m-%d")
    ).days

    if days <= 0:
        raise ValueError("End date must be after start date")

    if fleet[plate]["rate"] < 0:
        raise ValueError("Daily rental rate cannot be negative")

    if not fleet[plate]["available"]:
        raise ValueError("Car is not available")

    cost = days * fleet[plate]["rate"]
    fleet[plate]["available"] = False
    bookings.append(
        {
            "code": bookingCode(),
            "plate": plate,
            "customer": customer,
            "days": days,
            "cost": cost,
        }
    )
    return cost


def returnCar(plate, km_driven):
    if plate not in fleet:
        return None

    fleet[plate]["available"] = True
    if km_driven > 300:
        return (km_driven - 300) * 5
    return 0


def bookingCode():
    return "BK-" + str(secrets.randbelow(90000) + 10000)


def licenceHash(licence):
    return hashlib.sha256(licence.encode("utf-8")).hexdigest()


def applyPromo(rule, amount):
    """Apply a supported percentage multiplier without executing code."""
    match = re.fullmatch(
        r"\s*amount\s*=\s*amount\s*\*\s*(\d+(?:\.\d+)?)\s*",
        rule,
    )
    if not match:
        raise ValueError("Unsupported promo rule")

    multiplier = float(match.group(1))
    if not 0 <= multiplier <= 1:
        raise ValueError("Promo multiplier must be between 0 and 1")

    return amount * multiplier


def isValidPlate(plate):
    return bool(re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", plate))


def writeReceipt(booking):
    file_descriptor, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(file_descriptor, "w", encoding="utf-8") as receipt:
        receipt.write(
            f"Booking {booking['code']}: {booking['plate']} "
            f"for {booking['days']} days = Rs.{booking['cost']}\n"
        )
    return path


def adminLogin(user, password):
    expected_user = os.environ.get("CAR_RENTAL_ADMIN_USER")
    expected_password = os.environ.get("CAR_RENTAL_ADMIN_PASSWORD")

    if not expected_user or not expected_password:
        return False

    return (
        user == expected_user
        and secrets.compare_digest(password, expected_password)
    )


def availableCars():
    result = []
    for plate in fleet:
        if fleet[plate]["available"]:
            result.append(plate)
    return result


def main():
    addCar("KA01AB1234", "Swift", 1500)
    addCar("KA02CD5678", "Innova", 3000)
    addCar("KA03EF9999", "Nexon", -500)

    registerCustomer("Ravi", "DL-0420110012345", "9845012345")
    registerCustomer("Meera", "DL-0420110099999", "9845099999")

    print("Rent Swift:", rentCar("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"))

    print("Extra km charge:", returnCar("KA01AB1234", 420))
    print("Return unknown car:", returnCar("XX00XX0000", 50))
    print("Promo price:", applyPromo("amount = amount * 0.9", 4500))
    print("Plate valid?", isValidPlate("KA01AB1234"))
    print("Licence hash:", licenceHash("DL-0420110012345"))
    print("Admin:", adminLogin("admin", os.environ.get("CAR_RENTAL_ADMIN_PASSWORD", "")))
    print("Available:", availableCars())
    print("Receipt saved to:", writeReceipt(bookings[0]))


if __name__ == "__main__":
    main()
