from dockerode_api_proxy_client.utils.datatype import is_array


dict_ = {}
list_ = []


def test_true_when_list() -> None:
    assert is_array(list_) == True


def test_false_when_int() -> None:
    assert is_array(1337) == False


def test_false_when_string() -> None:
    assert is_array("hello world") == False


def test_false_when_dict() -> None:
    assert is_array(dict_) == False
