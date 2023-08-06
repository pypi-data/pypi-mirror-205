import ast
from lang2py import parse, generate_examples


for t in (
    int,
    str,
    bool,
    float,
    None,
    list,
    tuple,
    dict,
    int | str,
    int | str | bool | float,
    list[int],
    list[int | str | bool | float],
    tuple[tuple],
    dict[str, int],
    dict[str, int | str | bool | list[float, tuple]],
):

    examples = generate_examples(t, num_examples=3)
    examples_repr = [repr(e) for e in examples]
    parsed = [parse(repr(s)) for s in examples_repr]

    print("input:", t)
    print("examples:", examples)
    print("examples_repr:", examples_repr)
    print("parsed:", parsed)
    print(32 * "=")
