from typing import Any


def assert_no_error(body: Any) -> None:
    if isinstance(body, dict) and "errorMessage" in body:
        raise AssertionError(f"API вернул ошибку: {body['errorMessage']}")


def assert_status_code(response, expected: int = 200) -> None:
    assert response.status == expected, (
        f"Ожидали {expected}, получили {response.status}, Тело: {response.body}"
    )
