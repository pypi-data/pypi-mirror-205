import re
from typing import TypeVar, Dict, Any

T = TypeVar("T")


def snake_case_keys(dictionary: Dict[str, T]) -> Dict[str, T]:
    snake_case_dict = dict()
    for (k, v) in dictionary.items():
        new_key = re.sub("[A-Z]", lambda letter: f"_{str.lower(letter[0])}", k)
        snake_case_dict[new_key] = v
    return snake_case_dict


def camel_case_keys(dictionary: Dict[str, T]) -> Dict[str, T]:
    camel_case_dict = dict()
    for (k, v) in dictionary.items():
        new_key = re.sub("(_[a-z])", lambda letter: str.upper(letter[0][1]), k)
        camel_case_dict[new_key] = v
    return camel_case_dict


def define_dict(dictionary: Dict[str, Any]) -> Dict[str, Any]:
    defined = dict(list(filter(lambda entry: entry[1] is not None, dictionary.items())))
    return defined
