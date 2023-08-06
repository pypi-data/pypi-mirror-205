from dockerode_api_proxy_client.utils.formatting import (
    snake_case_keys,
    camel_case_keys,
    define_dict,
)


camel_dict = {"exposedPort": "tcp/8080"}
snake_dict = {"exposed_port": "tcp/8080"}
undefined_dict = {"defined": 1, "undefined": None}
defined_dict = {"defined": 1}
empty_dict = {}


def test_camel_to_snake():
    assert snake_case_keys(camel_dict) == snake_dict


def test_snake_to_camel_to_snake():
    assert snake_case_keys(camel_case_keys(snake_dict)) == snake_dict


def test_snake_to_camel():
    assert camel_case_keys(snake_dict) == camel_dict


def test_camel_to_snake_to_camel():
    assert camel_case_keys(snake_case_keys(camel_dict)) == camel_dict


def test_undefined_values():
    assert define_dict(undefined_dict) == defined_dict


def test_handle_empty_dict():
    assert define_dict(empty_dict) == empty_dict
