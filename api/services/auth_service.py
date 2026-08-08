from api.services.base_service import BaseService
from config.endpoints import Endpoint
from utils.assertions import assert_no_error


class AuthService(BaseService):
    def signup(self, username: str, password: str) -> None:
        response = self.requester.post(
            Endpoint.SIGNUP,
            payload={"username": username, "password": password},
        )
        assert_no_error(response.body)

    def login(self, username: str, password: str) -> str:
        response = self.requester.post(
            Endpoint.LOGIN,
            payload={"username": username, "password": password},
        )
        body = response.body
        if not isinstance(body, str) or ":" not in body:
            raise AssertionError(
                f"Ожидали строку вида 'Auth_token: <...>', получили: {body!r}"
            )
        return body.split(":", 1)[1].strip()
