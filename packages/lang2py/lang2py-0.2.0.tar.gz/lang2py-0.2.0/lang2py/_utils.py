from types import NoneType, UnionType
from typing import Union, get_origin


def issubtype(subtype, basetype):
    subtype = None if subtype is NoneType else subtype
    basetype = None if basetype is NoneType else basetype
    if basetype is None:
        return subtype is None
    if basetype is Ellipsis:
        return True
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
