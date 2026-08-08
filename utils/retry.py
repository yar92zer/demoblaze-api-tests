from tenacity import retry, stop_after_attempt, wait_fixed
from config.settings import RETRY_ATTEMPTS


@retry(stop=stop_after_attempt(RETRY_ATTEMPTS), wait=wait_fixed(1))
def with_retry(func, *args, **kwargs):
    return func(*args, **kwargs)
