import pytest
from utils.encoders import decode_token


@pytest.mark.smoke
@pytest.mark.auth
def test_login_returns_token(authenticated_user):
    assert authenticated_user["token"]

@pytest.mark.auth
@pytest.mark.regression
def test_token_contains_username(authenticated_user):
    decoded = decode_token(authenticated_user["token"])
    assert authenticated_user["username"] in decoded