from itertools import count
from typing import Iterable


def get_first_available_name(base_name: str, names: Iterable[str]) -> str:
    """
    Finds the first available name by incrementally adding numbers from 1 and
    onwards until it is not in given names.

    :param base_name: The base of the name, which will have numbers
                      incrementally added to
    :type base_name: str
    :param names: Iterable of names that will be checked to see if generated
                  name is in or not
    :type names: Iterable[str]
    :return: New unique name, using the base name and a number, which is not
             in given names iterator
    :rtype: str
    """
    for i in count(0, 1):
        name = f"{base_name} {i if i > 0 else ''}".rstrip()
        if name not in names:
            return name
