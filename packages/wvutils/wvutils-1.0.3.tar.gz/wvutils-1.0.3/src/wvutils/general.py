"""General utilities for working with Python.

This module provides general utilities for working with Python.
"""
from __future__ import annotations

import copy
import gc
import io
import logging
import platform
import sys
from typing import TYPE_CHECKING

from wvutils.path import resolve_path

if TYPE_CHECKING:
    from collections.abc import Generator, Sequence
    from typing import Any

    from wvutils.type_aliases import FilePath

__all__ = [
    "chunker",
    "count_lines_in_file",
    "dedupe_list",
    "dupe_in_list",
    "gc_set_threshold",
    "is_iolike",
    "is_iterable",
    "rename_key",
    "sort_dict_by_key",
    "sys_set_recursion_limit",
    "unnest_key",
]

logger: logging.Logger = logging.getLogger(__name__)


def is_iolike(potential_io: Any) -> bool:
    """Check if an object is IO-like.

    Args:
        potential_io (Any): Object to check.

    Returns:
        bool: True if the object is IO-like, otherwise False.
    """
    if isinstance(potential_io, io.IOBase):
        return True
    if all(
        hasattr(potential_io, attr)
        for attr in ("write", "seek", "close", "__enter__", "__exit__")
    ):
        return True
    return False


def _count_generator(
    bytes_io: io.BufferedReader,
    buffer_size: int = 1024 * 1024,
) -> Generator[bytes, None, None]:
    reader = bytes_io.raw.read
    chunk_b = reader(buffer_size)
    while chunk_b:
        yield chunk_b
        chunk_b = reader(buffer_size)


def count_lines_in_file(file_path: FilePath) -> int:
    """Count the number of lines in a file.

    Note:
        All files have at least 1 line (# of lines = # of newlines + 1).

    Args:
        file_path (FilePath): Path of the file to count lines in.

    Returns:
        int: Total number of lines in the file.
    """
    file_path = resolve_path(file_path)
    line_count = 1
    with open(file_path, mode="rb") as rbf:
        for buffer in _count_generator(rbf):
            line_count += buffer.count(b"\n")
    return line_count


def sys_set_recursion_limit() -> None:
    """Raise recursion limit to allow for more recurse."""
    sys.setrecursionlimit(10000)
    logger.debug("Adjusted Python recursion to allow more recurse")


def gc_set_threshold() -> None:
    """Reduce Number of GC Runs to Improve Performance

    Note:
        Only applies to CPython.
    """
    if platform.python_implementation() == "CPython":
        # allocs, g1, g2 = gc.get_threshold()
        gc.set_threshold(50_000, 500, 1000)
        logger.debug("Adjusted Python allocations to reduce GC runs")


def chunker(seq: Sequence[Any], n: int) -> Generator[Sequence[Any], None, None]:
    """Iterate a sequence in size `n` chunks.

    Args:
        seq (Sequence[Any]): Sequence of values.
        n (int): Number of values per chunk.

    Yields:
        Sequence[Any]: Chunk of values with length <= n.

    Raises:
        ValueError: If `n` is 0 or negative.
    """
    if n <= 0:
        raise ValueError(f"n must be greater than 0, got {n}")
    for i in range(0, len(seq), n):
        yield seq[i : i + n]


def is_iterable(obj: Any) -> bool:
    """Check if an object is iterable.

    Args:
        obj (Any): Object to check.

    Returns:
        bool: Whether the object is iterable.
    """
    try:
        iter(obj)
        return True
    except TypeError:
        return False


def rename_key(
    obj: dict,
    src_key: str,
    dest_key: str,
    in_place: bool = False,
) -> dict | None:
    """Rename a dictionary key.

    Todo:
        * Add support for nested keys.
        * Add support for renaming multiple keys at once.
        * Add support for non-string (built-in) key types.

        All of the following are True:

        ```python
        isinstance(True, bool)
        isinstance(True, int)
        1 == True
        1 in {1: "a"}
        True in {1: "a"}
        1 in {True: "a"}
        True in {True: "a"}
        1 in {1: "a", True: "b"}
        True in {1: "a", True: "b"}
        ```

    Args:
        obj (dict): Reference to the dictionary to modify.
        src (str): Name of the key to rename.
        dest (str): Name of the key to change to.
        in_place (bool, optional): Perform in-place using the provided reference. Defaults to False.

    Returns:
        dict | None: Copy of the dictionary if in_place is False, otherwise None.
    """
    if in_place:
        if src_key in obj:
            obj[dest_key] = obj.pop(src_key)
        return None
    else:
        obj_copy = copy.deepcopy(obj)
        rename_key(obj_copy, src_key, dest_key, in_place=True)
        return obj_copy


def unnest_key(obj: dict, *keys: str) -> Any | None:
    """Fetch a value from a deeply nested dictionary.

    Args:
        obj (dict): Dictionary to recursively iterate.
        *keys (str): Ordered keys to fetch.

    Returns:
        Any | None: The result of the provided keys, or None if any key is not found.
    """
    found = obj
    for key in keys:
        # TODO: Finish adding a parameter to allow for missing keys.
        # try:
        #     if key in found:
        #         found = found[key]
        #     else:
        #         return None
        # except ValueError:
        #     return None
        if key in found:
            found = found[key]
        else:
            return None
    return found


def sort_dict_by_key(
    obj: dict,
    reverse: bool = False,
    deep_copy: bool = False,
) -> dict | None:
    """Sort a dictionary by key.

    Args:
        obj (dict): Dictionary to sort.
        reverse (bool, optional): Sort in reverse order. Defaults to False.
        deep_copy (bool, optional): Return a deep copy of the dictionary. Defaults to False.

    Returns:
        dict | None: Dictionary sorted by key. If `in_place` is True, None is returned.

    Raises:
        ValueError: If the dictionary keys are not of the same type.
    """
    key_types = {type(k) for k in obj.keys()}
    if len(key_types) > 1:
        error_msg = "Dictionary keys must be of the same type, got ["
        for key_type in key_types:
            error_msg += f"{key_type}, "
        error_msg = error_msg[:-2] + "]"
        raise ValueError(error_msg)
    if deep_copy:
        return sort_dict_by_key(
            copy.deepcopy(obj), reverse=reverse, deep_copy=False, in_place=False
        )
    sorted_keys = sorted(obj, reverse=reverse)
    return {k: obj[k] for k in sorted_keys}


def dedupe_list(values: list[Any], raise_on_dupe: bool = False) -> list[Any]:
    """Remove duplicate values from a list.

    Example:

    ```python
    dedupe_list([1, 2, 3, 1, 2, 3])
    # [1, 2, 3]
    ```

    Args:
        values (list[Any]): List of values to dedupe.
        raise_on_dupe (bool, optional): Raise an error if a duplicate is found. Defaults to False.

    Returns:
        list[Any]: List of unique values.

    Raises:
        ValueError: If a duplicate is found and `raise_on_dupe` is True.
    """
    deduped = []
    for value in values:
        if value not in deduped:
            deduped.append(value)
        elif raise_on_dupe:
            raise ValueError(f"Duplicate value found: {value}")
    return deduped


def dupe_in_list(values: list[Any]) -> bool:
    """Check if a list has duplicate values.

    Args:
        values (list[Any]): List of values to check.

    Returns:
        bool: Whether the list has duplicate values.
    """
    try:
        dedupe_list(values, raise_on_dupe=True)
        return False
    except ValueError:
        return True


def invert_dict_of_str(
    obj: dict[Any, str],
    deep_copy: bool = False,
    raise_on_dupe: bool = False,
) -> dict:
    """Invert a dictionary of strings.

    Note:
        The value of the last key with a given value will be used.

    Example:

    ```python
    invert_dict_of_str({"a": "b", "c": "d"})
    # {"b": "a", "d": "c"}
    ```

    Args:
        obj (dict[Any, str]): Dictionary to invert.
        deep_copy (bool, optional): Return a deep copy of the dictionary. Defaults to False.
        raise_on_dupe (bool, optional): Raise an error if a duplicate is found. Defaults to False.

    Returns:
        dict: Inverted dictionary.

    Raises:
        ValueError: If a duplicate is found and `raise_on_dupe` is True.
    """
    if deep_copy:
        return invert_dict_of_str(copy.deepcopy(obj), deep_copy=False)
    inverted_obj = {}
    for k in obj:
        if obj[k] not in inverted_obj:
            inverted_obj[obj[k]] = k
        elif raise_on_dupe:
            raise ValueError(f"Duplicate value of found for key {k!r}: {obj[k]!r}")
    return {obj[k]: k for k in obj}


# Messing around here
# class AdvancedDict(dict):
#     """A dictionary with advanced features.
#
#     Args:
#         *args (Any, optional): Positional arguments to pass to the parent class.
#         **kwargs (Any, optional): Keyword arguments to pass to the parent class.
#     """
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#
#     def _capitalize_keys(self, obj: dict, in_place: bool = False) -> dict | None:
#         """Capitalize the keys of the dictionary.
#
#         Args:
#             obj (dict): Dictionary to capitalize.
#             in_place (bool, optional): Perform in-place using the provided reference. Defaults to False.
#
#         Returns:
#             dict | None: Copy of the dictionary if in_place is False, otherwise None.
#         """
#         if in_place:
#             for key in list(obj.keys()):
#                 if isinstance(obj[key], dict):
#                     self._capitalize_keys(obj[key], in_place=True)
#                 obj[key.capitalize()] = obj.pop(key)
#             return None
#         else:
#             obj_copy = copy.deepcopy(obj)
#             self._capitalize_keys(obj_copy, in_place=True)
#             return obj_copy
#
#     def capitalize_keys(self, in_place: bool = False) -> dict | None:
#         """Capitalize the keys of the dictionary.
#
#         Args:
#             in_place (bool, optional): Perform in-place using the provided reference. Defaults to False.
#
#         Returns:
#             dict | None: Copy of the dictionary if in_place is False, otherwise None.
#         """
#         return self._capitalize_keys(self, in_place=in_place)
