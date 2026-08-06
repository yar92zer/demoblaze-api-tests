"""Разведка контракта Demoblaze API.

Бьёт по кандидатам-эндпоинтам и печатает, что реально возвращается:
метод, статус, тело ответа. Ничего не угадывает — только фиксирует факты.

    pip install requests
    python probe_demoblaze.py
"""

import base64
import json
import uuid

import requests

BASE = "https://api.demoblaze.com"
TIMEOUT = 15


def call(method, path, body=None):
    """Один вызов. Возвращает (status, распарсенное тело или сырой текст)."""
    url = f"{BASE}{path}"
    try:
        if method == "GET":
            response = requests.get(url, timeout=TIMEOUT)
        else:
            response = requests.post(url, json=body, timeout=TIMEOUT)
    except requests.RequestException as error:
        return None, f"СЕТЬ: {error}"

    try:
        return response.status_code, response.json()
    except ValueError:
        return response.status_code, response.text.strip()


def show(method, path, body, status, payload):
    print("=" * 68)
    print(f"{method} {path}  ->  {status}")
    if body is not None:
        print("  запрос:  " + json.dumps(body, ensure_ascii=False))

    if isinstance(payload, (dict, list)):
        text = json.dumps(payload, ensure_ascii=False)
    else:
        text = str(payload)

    if len(text) > 400:
        text = text[:400] + "  ...(обрезано)"
    print("  ответ:   " + text)


def try_both(path, body):
    """Сначала POST, если 404/405 — пробуем GET. Так находим верный метод."""
    status, payload = call("POST", path, body)
    if status in (404, 405):
        show("POST", path, body, status, payload)
        status, payload = call("GET", path, None)
        show("GET", path, None, status, payload)
        return "GET", status, payload

    show("POST", path, body, status, payload)
    return "POST", status, payload


def main():
    # --- каталог, без авторизации ---
    status, payload = call("GET", "/entries")
    show("GET", "/entries", None, status, payload)

    try_both("/bycat", {"cat": "phone"})
    try_both("/bycat", {"cat": "monitor"})
    try_both("/view", {"id": "1"})

    # --- регистрация и вход ---
    # Пароль на фронте кодируется в base64. Скрипт делает так же,
    # чтобы проверить, действительно ли бэкенд этого ждёт.
    username = f"probe_{uuid.uuid4().hex[:10]}"
    password = "Passw0rd!"
    encoded = base64.b64encode(password.encode()).decode()

    print("\n>>> пробуем пароль В BASE64")
    try_both("/signup", {"username": username, "password": encoded})
    _, _, login_payload = try_both("/login", {"username": username, "password": encoded})

    print("\n>>> контроль: тот же пароль ОТКРЫТЫМ текстом, другой юзер")
    plain_user = f"probe_{uuid.uuid4().hex[:10]}"
    try_both("/signup", {"username": plain_user, "password": password})
    try_both("/login", {"username": plain_user, "password": password})

    # Токен приходит строкой вида "Auth_token: <...>" — вытаскиваем хвост.
    token = None
    if isinstance(login_payload, str) and ":" in login_payload:
        token = login_payload.split(":", 1)[1].strip()
    elif isinstance(login_payload, dict):
        token = login_payload.get("Auth_token") or login_payload.get("token")

    print(f"\n>>> извлечённый токен: {token!r}")

    if not token:
        print("Токена нет — дальше корзину не проверить. Смотри ответ /login выше.")
        return

    # --- корзина ---
    item_id = str(uuid.uuid4())
    try_both(
        "/addtocart",
        {"id": item_id, "cookie": token, "prod_id": 1, "flag": True},
    )
    try_both("/viewcart", {"cookie": token, "flag": True})
    try_both("/deleteitem", {"id": item_id})
    try_both("/viewcart", {"cookie": token, "flag": True})

    # --- негатив: битый токен ---
    print("\n>>> негатив: заведомо неверный cookie")
    try_both("/viewcart", {"cookie": "definitely-not-a-token", "flag": True})


if __name__ == "__main__":
    main()
