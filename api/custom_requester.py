from dataclasses import dataclass
from typing import Any

import allure
import requests

from config.endpoints import Endpoint
from config.settings import BASE_URL, TIMEOUT
from utils.assertions import assert_status_code


@dataclass
class ApiResponse:
    status: int
    body: Any
    raw: requests.Response


class CustomRequester:
    def __init__(self, base_url: str = BASE_URL, timeout: int = TIMEOUT):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _url(self, endpoint: Endpoint) -> str:
        return f"{self.base_url}{endpoint}"

    @staticmethod
    def _parse(response) -> Any:
        try:
            return response.json()
        except ValueError:
            return response.text.strip()

    def _log_to_allure(self, response, payload: dict | None = None) -> None:
        allure.attach(
            f"{response.request.method} {response.url}",
            name="Request",
            attachment_type=allure.attachment_type.TEXT,
        )
        if payload is not None:
            allure.attach(
                str(payload),
                name="Payload",
                attachment_type=allure.attachment_type.TEXT,
            )
        allure.attach(
            response.text,
            name="Response",
            attachment_type=allure.attachment_type.TEXT,
        )

    def get(self, endpoint: Endpoint) -> ApiResponse:
        response = self.session.get(self._url(endpoint), timeout=self.timeout)
        self._log_to_allure(response)
        assert_status_code(response)
        return ApiResponse(
            status=response.status_code,
            body=self._parse(response),
            raw=response,
        )

    def post(self, endpoint: Endpoint, payload: dict | None = None) -> ApiResponse:
        response = self.session.post(self._url(endpoint), json=payload, timeout=self.timeout)
        self._log_to_allure(response, payload)
        assert_status_code(response)
        return ApiResponse(
            status=response.status_code,
            body=self._parse(response),
            raw=response,
        )
