import ast
import random
from types import NoneType
from typing import Type, Union, get_origin

from lang2py._utils import issubtype

TYPES = NoneType | int | str | bool | float | list | tuple | dict


def parse(text: str) -> TYPES:
    return ast.literal_eval(text)


from random import randint, uniform


def generate_examples(type: Type[TYPES], num_examples=3) -> list[TYPES]:

    if issubtype(type, int):
        return [randint(-100, 100) for _ in range(num_examples)]
    elif issubtype(type, str):
        return ((num_examples // 3 + 1) * ["hello", "world", "python"])[:num_examples]
    elif issubtype(type, bool):
        return [bool(randint(0, 1)) for _ in range(num_examples)]
    elif issubtype(type, float):
        return [round(uniform(-100, 100), 2) for _ in range(num_examples)]
    elif issubtype(type, None):
        return [None] * num_examples
    elif issubtype(type, list):
        elem_type = (
            type.__args__[0]
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else TYPES
        )
        examples = []
        for _ in range(num_examples):
            num_entries = randint(0, 5)
            entires = generate_examples(elem_type, num_examples=num_entries)
            examples.append(entires)
        return examples
    elif issubtype(type, tuple):
        elem_types = (
            type.__args__
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else (TYPES, ...)
        )
        examples = []
        for _ in range(num_examples):
            entires = []
            for i, elem_type in enumerate(elem_types):
                if elem_type == Ellipsis:
                    if i != len(elem_types) - 1:
                        raise ValueError(
                            "Ellipsis can only be used as the last element of a tuple"
                        )
                    num_entries = randint(0, 5)
                    if _ in range(num_entries):
                        entires.append(
                            (generate_examples(elem_types[-2], num_examples=1)[0])
                        )
                else:
                    entires.append((generate_examples(elem_type, num_examples=1)[0]))
            examples.append(tuple(entires))
        return examples
    elif issubtype(type, dict):
        key_type, value_type = (
            type.__args__
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else (str, TYPES)
        )
        examples = []
        for _ in range(num_examples):
            num_entries = randint(1, 5)
            keys = generate_examples(key_type, num_examples=num_entries)
            values = generate_examples(value_type, num_examples=num_entries)
            entires = dict(zip(keys, values))
            examples.append(entires)
        return examples
    elif issubtype(type, Union):
        examples = []
        sub_types = random.choices(type.__args__, k=num_examples)
        for sub_type in sub_types:
            examples.append(generate_examples(sub_type, num_examples=1)[0])
        return examples
    else:
        raise TypeError(f"Unsupported type {type}")
