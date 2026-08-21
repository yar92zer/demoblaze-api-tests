from typing import Any


def assert_no_error(body: Any) -> None:
    if isinstance(body, dict) and "errorMessage" in body:
        raise AssertionError(f"API вернул ошибку: {body['errorMessage']}")


def assert_status_code(response, expected: int = 200) -> None:
    # У стенда любой успешный вызов приходит с 200, поэтому другой код
    # означает недоступность стенда, а не бизнес-ошибку.
    assert response.status_code == expected, (
        f"Стенд ответил {response.status_code}, ожидали {expected}. "
        f"Тело: {response.text}"
    )
