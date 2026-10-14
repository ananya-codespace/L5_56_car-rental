
"""Car rental system for the static code analysis lab."""

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


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Add a car to the fleet and return its details."""
    if not plate:
        return None

    if features is None:
        features = []

    fleet[plate] = {
        "model": model,
        "rate": daily_rate,
        "available": True,
        "features": features,
    }
    return fleet[plate]


def register_customer(name, licence, phone):
    """Register a customer using a parameterized SQL query."""
    conn.execute(
        "INSERT INTO customers VALUES (?, ?, ?)",
        (name, licence, phone),
    )


def find_customer(name):
    """Return customer records matching the supplied name."""
    query = "SELECT * FROM customers WHERE name = ?"
    return conn.execute(query, (name,)).fetchall()


def rent_car(plate, customer, start, end):
    """Book an available car and return the total rental cost."""
    if not find_customer(customer):
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
            "code": booking_code(),
            "plate": plate,
            "customer": customer,
            "days": days,
            "cost": cost,
        }
    )
    return cost


def return_car(plate, km_driven):
    """Mark a car as available and calculate any extra-distance charge."""
    if plate not in fleet:
        return None

    fleet[plate]["available"] = True
    if km_driven > 300:
        return (km_driven - 300) * 5
    return 0


def booking_code():
    """Generate a booking code using a secure random generator."""
    return "BK-" + str(secrets.randbelow(90000) + 10000)


def licence_hash(licence):
    """Return the SHA-256 digest of a licence string."""
    return hashlib.sha256(licence.encode("utf-8")).hexdigest()


def apply_promo(rule, amount):
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


def is_valid_plate(plate):
    """Check whether a number plate matches the expected format."""
    return bool(
        re.fullmatch(r"[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}", plate)
    )


def write_receipt(booking):
    """Create a receipt file and return its path."""
    file_descriptor, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(
        file_descriptor, "w", encoding="utf-8"
    ) as receipt:
        receipt.write(
            f"Booking {booking['code']}: {booking['plate']} "
            f"for {booking['days']} days = Rs.{booking['cost']}\n"
        )
    return path


def admin_login(user, password):
    """Authenticate an administrator using configured environment values."""
    expected_user = os.environ.get("CAR_RENTAL_ADMIN_USER")
    expected_password = os.environ.get("CAR_RENTAL_ADMIN_PASSWORD")

    if not expected_user or not expected_password:
        return False

    return (
        user == expected_user
        and secrets.compare_digest(password, expected_password)
    )


def available_cars():
    """Return the number plates of all currently available cars."""
    return [
        plate
        for plate, details in fleet.items()
        if details["available"]
    ]


def main():
    """Run the car rental demonstration."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)
    add_car("KA03EF9999", "Nexon", -500)

    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")

    print(
        "Rent Swift:",
        rent_car("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"),
    )
    print("Extra km charge:", return_car("KA01AB1234", 420))
    print("Return unknown car:", return_car("XX00XX0000", 50))
    print("Promo price:", apply_promo("amount = amount * 0.9", 4500))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))
    print(
        "Admin:",
        admin_login(
            "admin",
            os.environ.get("CAR_RENTAL_ADMIN_PASSWORD", ""),
        ),
    )
    print("Available:", available_cars())
    print("Receipt saved to:", write_receipt(bookings[0]))


if __name__ == "__main__":
    main()
