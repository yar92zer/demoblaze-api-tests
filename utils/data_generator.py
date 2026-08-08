import uuid


def unique_username() -> str:
    return f"qa_{uuid.uuid4().hex[:12]}"


DEFAULT_PASSWORD = "Passw0rd!"
