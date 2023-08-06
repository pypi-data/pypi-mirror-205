from typing import Any, List, Optional, Union


def is_array(data: Optional[Union[Any, List[Any]]] = None) -> bool:
    if data is not None and (isinstance(data, list)):
        return True
    return False
