import uuid

from faker import Faker

fake = Faker()
DEFAULT_PASSWORD = "Passw0rd!"


def unique_username() -> str:
    return f"qa_{uuid.uuid4().hex[:12]}"


def order_data() -> dict[str, str]:
    return {
        "name": fake.name(),
        "contact": fake.country(),
        "city": fake.city(),
        "card": fake.credit_card_number(),
        "month": str(fake.random_int(1, 12)),
        "year": str(fake.random_int(2027, 2035)),
    }
