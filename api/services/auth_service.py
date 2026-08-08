from api.services.base_service import BaseService
from config.endpoints import Endpoint


class AuthService(BaseService):
    def signup(self, username: str, password: str) -> None:
        self.requester.post(
            Endpoint.SIGNUP,
            payload={"username": username, "password": password},
        )

    def login(self, username: str, password: str) -> str:
        response = self.requester.post(
            Endpoint.LOGIN,
            payload={"username": username, "password": password},
        )
        return response.body.split(":", 1)[1].strip()
