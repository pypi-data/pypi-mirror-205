from types import UnionType
from typing import Union, get_origin


def issubtype(subtype, basetype):
    if subtype == basetype:
        return True
    if get_origin(subtype) == basetype:
        return True
    try:
        if basetype != int and issubclass(subtype, basetype):
            return True
    except TypeError:
        pass
    if basetype is Union and get_origin(subtype) == UnionType:
        return True
    return False
