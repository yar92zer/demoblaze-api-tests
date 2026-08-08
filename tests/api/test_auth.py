import pytest
import base64


@pytest.mark.smoke
@pytest.mark.auth
def test_login_returns_token(authenticated_user):
    assert authenticated_user["token"]

@pytest.mark.auth
@pytest.mark.regression
def test_token_contains_username(authenticated_user):
    decoded = base64.b64decode(authenticated_user["token"]).decode()
    assert authenticated_user["username"] in decoded