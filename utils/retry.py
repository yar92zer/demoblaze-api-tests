import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from settings import RETRY_ATTEMPTS


@retry(
    retry=retry_if_exception_type(requests.RequestException),
    stop=stop_after_attempt(RETRY_ATTEMPTS),
    wait=wait_fixed(1),
)
def with_retry(func, *args, **kwargs):
    return func(*args, **kwargs)
