from typing import Type, Union, get_origin

from lang2py._utils import issubtype

PARSABLE_TYPES = None | int | str | bool | float | list | tuple | dict


def parse(text: str, type: Type[PARSABLE_TYPES], remove_quotes=True) -> PARSABLE_TYPES:
    orig_text, text = text, text.strip()
    if issubtype(type, int):
        return int(text)
    elif issubtype(type, str):
        print("TEXT")
        if remove_quotes:
            if (
                len(orig_text) > 2
                and orig_text[0] == orig_text[-1]
                and orig_text[0] in ('"', "'")
            ):
                print()
                orig_text = orig_text[1:-1]
        return orig_text
    elif issubtype(type, bool):
        print("BOOL")
        return text.lower() == "true"
    elif issubtype(type, float):
        return float(text)
    elif issubtype(type, None):
        return (
            None if text.lower() == "none" else text
        )  # return None if the input string is "None"
    elif issubtype(type, list):
        elem_type = (
            type.__args__[0]
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else str
        )
        return list(
            parse(elem.strip(), elem_type) for elem in text.strip("[]()").split(",")
        )
    elif issubtype(type, tuple):
        elem_types = (
            type.__args__
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else (str, ...)
        )
        elems = text.strip("[]()").split(",")
        if len(elem_types) == 1 and elem_types[0] is Ellipsis:
            elem_type = str
            parsed_elems = [parse(elem.strip(), elem_type) for elem in elems]
        else:
            if len(elem_types) > len(elems):
                raise ValueError(
                    f"Expected at least {len(elem_types)} elements, but got {len(elems)}"
                )
            elif len(elem_types) < len(elems) and elem_types[-1] is not Ellipsis:
                raise ValueError(
                    f"Expected {len(elem_types)} elements, but got {len(elems)}"
                )
            parsed_elems = [
                parse(elem.strip(), elem_type)
                for elem, elem_type in zip(elems[: len(elem_types) - 1], elem_types[:-1])
            ]
            if elem_types[-1] is not Ellipsis:
                parsed_elems.append(parse(elems[-1].strip(), elem_types[-1]))
            else:
                elem_type = elem_types[-2] if len(elem_types) > 1 else str
                parsed_elems.extend(
                    [
                        parse(elem.strip(), elem_type)
                        for elem in elems[len(elem_types) - 1 :]
                    ]
                )
        return tuple(parsed_elems)
    elif issubtype(type, dict):
        key_type, value_type = (
            type.__args__
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else (str, str)
        )
        elem_dict = {}
        for kv_pair in text.strip("{}").split(","):
            k, v = kv_pair.split(":")
            elem_dict[parse(k.strip(), key_type)] = parse(v.strip(), value_type)
        return elem_dict
    elif issubtype(type, Union):
        scores = {
            bool: 0,
            int: 1,
            float: 2,
            list: 3,
            tuple: 4,
            dict: 5,
            str: 6,
        }
        args = list(type.__args__)
        args.sort(key=lambda t: scores.get(t, len(scores)))
        for sub_type in args:
            try:
                return parse(text, sub_type)
            except (ValueError, TypeError):
                pass
        raise ValueError(f"Cannot parse '{text}' as any of the types {type.__args__}")
    else:
        raise TypeError(f"Unsupported type {type}")


from random import randint, uniform


def generate_examples(type: Type[PARSABLE_TYPES], num_examples=3) -> list[str]:
    if issubtype(type, int):
        return [str(randint(-100, 100)) for _ in range(num_examples)]
    elif issubtype(type, str):
        return ["hello", "world", "python"][:num_examples]
    elif issubtype(type, bool):
        return [str(bool(randint(0, 1))).lower() for _ in range(num_examples)]
    elif issubtype(type, float):
        return [str(round(uniform(-100, 100), 2)) for _ in range(num_examples)]
    elif issubtype(type, None):
        return [None] * num_examples
    elif issubtype(type, list):
        elem_type = (
            type.__args__[0]
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else str
        )
        return [
            f"[{', '.join(generate_examples(elem_type))}]" for _ in range(num_examples)
        ]
    elif issubtype(type, tuple):
        elem_types = (
            type.__args__
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else (str,)
        )
        elem_examples = []
        for elem_type in elem_types:
            if elem_type == Ellipsis:
                elem_examples.append([elem_examples[-1][0]] * num_examples)
            else:
                elem_examples.append(generate_examples(elem_type))
        return [
            tuple(example[i] for example in elem_examples)
            for i in range(max(map(len, elem_examples)))
        ]
    elif issubtype(type, dict):
        key_type, value_type = (
            type.__args__
            if hasattr(type, "__args__") and len(type.__args__) > 0
            else (str, str)
        )
        return [
            f"{{{k}: {v}}}"
            for k, v in zip(
                generate_examples(key_type),
                generate_examples(value_type, num_examples),
            )
        ]
    elif issubtype(type, Union):
        examples = []
        for sub_type in type.__args__:
            examples += generate_examples(sub_type, num_examples)
        return examples[:num_examples]
    else:
        raise TypeError(f"Unsupported type {type}")


1
