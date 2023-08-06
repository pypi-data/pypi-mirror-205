from dockerode_api_proxy_client.utils.get_authentication_header import (
    extend_headers,
get_authentication_header
)


empty_headers = {}
existing_headers = {"Accept": "application/json"}

auth_headers = {"Authorization": "Bearer <token_here/>"}
extra_headers = {"Content-Type": "application/json"}


def test_extend_empty_header_object():
    expected = {"Content-Type": "application/json"}
    assert extend_headers(empty_headers, extra_headers) == expected


def test_extend_header_object():
    expected = {"Authorization": "Bearer <token_here/>", "Accept": "application/json"}
    assert extend_headers(existing_headers, auth_headers) == expected


def test_get_authorization_header():
    authenticated_headers = get_authentication_header("jwt_secret")
    assert "Authorization" in authenticated_headers

