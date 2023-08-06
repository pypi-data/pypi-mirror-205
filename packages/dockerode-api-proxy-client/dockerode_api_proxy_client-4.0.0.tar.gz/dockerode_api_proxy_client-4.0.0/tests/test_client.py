from dockerode_api_proxy_client.client import ApiProxyClient


def test_create_client():
    client = ApiProxyClient(host="http://fake-url.com")
    assert client != None
