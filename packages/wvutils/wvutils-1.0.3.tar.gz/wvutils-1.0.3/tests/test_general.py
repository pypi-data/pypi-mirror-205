import gc
import io
import sys

import pytest

from tests.fixtures import temp_file
from wvutils.general import (
    chunker,
    count_lines_in_file,
    dedupe_list,
    dupe_in_list,
    gc_set_threshold,
    invert_dict_of_str,
    is_iolike,
    is_iterable,
    rename_key,
    sort_dict_by_key,
    sys_set_recursion_limit,
    unnest_key,
)


class IOLike:
    def __init__(self):
        pass

    def read(self):
        pass

    def write(self):
        pass

    def seek(self):
        pass

    def close(self):
        pass

    def __enter__(self):
        pass

    def __exit__(self):
        pass


class NonIOLike:
    pass


class CustomIterable:
    def __init__(self, data: list):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index >= len(self.data):
            raise StopIteration
        result = self.data[self.index]
        self.index += 1
        return result


@pytest.mark.parametrize(
    "potential_io,expected",
    [
        (io.StringIO(), True),
        (io.BytesIO(), True),
        (IOLike(), True),
        (NonIOLike(), False),
    ],
)
def test_is_iolike(potential_io, expected):
    assert is_iolike(potential_io) is expected


@pytest.mark.parametrize(
    "file_contents,expected",
    [
        ("", 1),
        ("First line", 1),
        ("First line\n", 2),
        ("First line\nSecond line", 2),
        ("First line\nSecond line\n", 3),
        ("First line\nSecond line\nThird line", 3),
        ("First line\nSecond line\nThird line\n", 4),
        ("First line\r\n", 2),
        ("First line\r\nSecond line", 2),
        ("First line\r\nSecond line\r\n", 3),
        ("First line\r\nSecond line\r\nThird line", 3),
        ("First line\r\nSecond line\r\nThird line\r\n", 4),
    ],
)
def test_file_with_newline_at_end(temp_file, file_contents, expected):
    temp_file.write("First line\nSecond line\nThird line\n".encode("utf-8"))
    temp_file.seek(0)
    assert count_lines_in_file(temp_file.name) == 4


def test_sys_set_recursion_limit():
    prev_limit = sys.getrecursionlimit()
    sys_set_recursion_limit()
    assert sys.getrecursionlimit() == 10000
    sys.setrecursionlimit(prev_limit)


def test_gc_set_threshold():
    prev_threshold = gc.get_threshold()
    gc_set_threshold()
    assert gc.get_threshold() == (50000, 500, 1000)
    gc.set_threshold(*prev_threshold)


@pytest.mark.parametrize(
    "seq,n,expected",
    [
        ([], 2, []),
        ([1, 2, 3], 4, [[1, 2, 3]]),
        ([1, 2, 3], 3, [[1, 2, 3]]),
        ([1, 2, 3, 4, 5], 2, [[1, 2], [3, 4], [5]]),
    ],
)
def test_chunker(seq, n, expected):
    assert list(chunker(seq, n)) == expected


@pytest.mark.parametrize("seq, n", [([1, 2, 3], 0), ([1, 2, 3], -1)])
def test_chunker_raises_for_invalid_n(seq, n):
    with pytest.raises(ValueError, match=r"n must be greater than 0, got .+"):
        list(chunker(seq, n))


@pytest.mark.parametrize(
    "obj,expected",
    [
        (None, False),
        (1, False),
        (1.0, False),
        (True, False),
        ("test", True),
        ([1, 2, 3], True),
        ((1, 2, 3), True),
        ({1, 2, 3}, True),
        (frozenset({1, 2, 3}), True),
        ({"a": 1, "b": 2}, True),
        (iter([1, 2, 3]), True),
        (CustomIterable([1, 2, 3]), True),
    ],
)
def test_is_iterable(obj, expected):
    assert is_iterable(obj) is expected


RENAME_KEY_TEST_VALUES = [
    1,
    "test_str",
    True,
    3.14,
    [1, 2, 3],
    {"nested_key": "nested_value"},
    {1, 2, 3},
    frozenset([1, 2, 3]),
    (1, 2, 3),
]


@pytest.mark.parametrize("value", RENAME_KEY_TEST_VALUES)
def test_rename_key(value):
    obj = {"old_key": value}
    obj_copy = rename_key(obj, "old_key", "new_key")
    assert obj_copy == {"new_key": value}
    assert obj == {"old_key": value}
    assert obj is not obj_copy


@pytest.mark.parametrize("value", RENAME_KEY_TEST_VALUES)
def test_rename_key_in_place(value):
    obj = {"old_key": value}
    rename_key(obj, "old_key", "new_key", in_place=True)
    assert obj == {"new_key": value}


@pytest.mark.parametrize("value", RENAME_KEY_TEST_VALUES)
def test_rename_key_missing_src_key(value):
    obj = {"old_key": value}
    obj_copy = rename_key(obj, "missing_key", "new_key")
    assert obj_copy == {"old_key": value}
    assert obj == {"old_key": value}
    assert obj is not obj_copy


@pytest.mark.parametrize("value", RENAME_KEY_TEST_VALUES)
def test_rename_key_missing_src_key_in_place(value):
    obj = {"old_key": value}
    rename_key(obj, "missing_key", "new_key", in_place=True)
    assert obj == {"old_key": value}


def test_rename_key_existing_dest_key():
    obj = {"a": 1, "b": 2}
    obj_copy = rename_key(obj, "a", "b")
    assert obj_copy == {"b": 1}
    assert obj == {"a": 1, "b": 2}
    assert obj is not obj_copy


def test_rename_key_existing_dest_key_in_place():
    obj = {"a": 1, "b": 2}
    rename_key(obj, "a", "b", in_place=True)
    assert obj == {"b": 1}


def test_rename_key_empty_dict():
    obj = {}
    obj_copy = rename_key(obj, "old_key", "new_key")
    assert obj_copy == {}
    assert obj == {}
    assert obj is not obj_copy


def test_rename_key_empty_dict_in_place():
    obj = {}
    rename_key(obj, "old_key", "new_key", in_place=True)
    assert obj == {}


def test_rename_key_src_key_equals_dest_key():
    obj = {"a": 1, "b": 2}
    obj_copy = rename_key(obj, "key", "key")
    assert obj_copy == {"a": 1, "b": 2}
    assert obj == {"a": 1, "b": 2}
    assert obj is not obj_copy


def test_rename_key_src_key_equals_dest_key_in_place():
    obj = {"a": 1, "b": 2}
    rename_key(obj, "key", "key", in_place=True)
    assert obj == {"a": 1, "b": 2}


@pytest.mark.parametrize(
    "obj,keys,expected",
    [
        ({"a": 1, "b": 2, "c": 3}, ("a",), 1),
        ({"a": 1, "b": 2, "c": 3}, ("b",), 2),
        ({"a": 1, "b": 2, "c": 3}, ("c",), 3),
        ({"a": {"b": {"c": 1}}}, ("a",), {"b": {"c": 1}}),
        ({"a": {"b": {"c": 1}}}, ("a", "b"), {"c": 1}),
        ({"a": {"b": {"c": 1}}}, ("a", "b", "c"), 1),
        # TODO: Add parameter for allowing missing keys.
        # ({"a": {"b": {"c": 1}}}, ("a", "b", "c", "d"), None),
        ({"a": {"b": {"c": 1}}}, ("a", "b", "d"), None),
        ({"a": {"b": {"c": 1}}}, ("a", "d"), None),
        ({"a": {"b": {"c": 1}}}, ("d",), None),
        ({}, ("a",), None),
        ({}, ("a", "b"), None),
        ({}, ("a", "b", "c"), None),
        # ({}, (), ),
    ],
)
def test_unnest_key(obj, keys, expected):
    assert unnest_key(obj, *keys) == expected


@pytest.mark.parametrize("deep_copy", [False, False])
@pytest.mark.parametrize(
    "obj,reverse,expected",
    [
        (
            {"foo": 0, "bar": 1, "baz": 2, "FOO": 3, "BAR": 4, "BAZ": 5},
            False,
            {"BAR": 4, "BAZ": 5, "FOO": 3, "bar": 1, "baz": 2, "foo": 0},
        ),
        (
            {3: "foo", 1: "bar", 2: "baz", 0: "FOO", 4: "BAR", 5: "BAZ"},
            False,
            {0: "FOO", 1: "bar", 2: "baz", 3: "foo", 4: "BAR", 5: "BAZ"},
        ),
        (
            {"foo": 0, "bar": 1, "baz": 2, "FOO": 3, "BAR": 4, "BAZ": 5},
            True,
            {"foo": 0, "bar": 1, "baz": 2, "FOO": 3, "BAR": 4, "BAZ": 5},
        ),
        (
            {3: "foo", 1: "bar", 2: "baz", 0: "FOO", 4: "BAR", 5: "BAZ"},
            True,
            {5: "BAZ", 4: "BAR", 3: "foo", 2: "baz", 1: "bar", 0: "FOO"},
        ),
        ({}, False, {}),
        ({}, True, {}),
    ],
)
def test_sort_dict_by_key(deep_copy, obj, reverse, expected):
    if deep_copy:
        actual = sort_dict_by_key(obj, reverse=reverse, deep_copy=True)
        assert actual == expected
        assert obj is not actual
    else:
        actual = sort_dict_by_key(obj, reverse=reverse)
        assert actual == expected


@pytest.mark.parametrize("reverse", [False, False])
@pytest.mark.parametrize("deep_copy", [False, False])
def test_sort_dict_by_key_raises_if_keys_not_same_type(reverse, deep_copy):
    with pytest.raises(
        ValueError, match=r"Dictionary keys must be of the same type, got \[.+\]"
    ):
        sort_dict_by_key({"a": None, 1: None}, reverse=reverse, deep_copy=deep_copy)


@pytest.mark.parametrize(
    "values,expected",
    [
        ([1, 2, 3], [1, 2, 3]),
        ([1, 2, 1], [1, 2]),
        ([1, 2, 1, 2], [1, 2]),
        (["a", "b", "c"], ["a", "b", "c"]),
        (["a", "b", "a"], ["a", "b"]),
        (["a", "b", "a", "b"], ["a", "b"]),
        ([[1, 2], [3, 4]], [[1, 2], [3, 4]]),
        ([[1, 2], [3, 4], [1, 2]], [[1, 2], [3, 4]]),
        ([[1, 2], [3, 4], [1, 2], [3, 4]], [[1, 2], [3, 4]]),
        ([], []),
    ],
)
def test_dedupe_list(values, expected):
    assert dedupe_list(values) == expected


@pytest.mark.parametrize(
    "values",
    [
        [1, 2, 1],
        [1, 2, 1, 2],
        ["a", "b", "a"],
        ["a", "b", "a", "b"],
        [[1, 2], [3, 4], [1, 2]],
        [[1, 2], [3, 4], [1, 2], [3, 4]],
    ],
)
def test_dedupe_list_raises_on_dupe_with_raise_on_dupe(values):
    with pytest.raises(ValueError, match=r"Duplicate value found: .+"):
        dedupe_list(values, raise_on_dupe=True)


@pytest.mark.parametrize(
    "values,expected",
    [
        ([1, 2, 3], False),
        ([1, 2, 1], True),
        ([1, 2, 1, 2], True),
        (["a", "b", "c"], False),
        (["a", "b", "a"], True),
        (["a", "b", "a", "b"], True),
        ([[1, 2], [3, 4]], False),
        ([[1, 2], [3, 4], [1, 2]], True),
        ([[1, 2], [3, 4], [1, 2], [3, 4]], True),
        ([], False),
    ],
)
def test_dupe_in_list(values, expected):
    assert dupe_in_list(values) == expected


@pytest.mark.parametrize(
    "obj,expected",
    [
        ({"a": "foo", "b": "bar", "c": "baz"}, {"foo": "a", "bar": "b", "baz": "c"}),
        ({"a": "foo", "b": "bar", "c": "foo"}, {"foo": "c", "bar": "b"}),
        ({"a": "foo", "b": "bar", "c": "foo", "d": "bar"}, {"foo": "c", "bar": "d"}),
        ({}, {}),
    ],
)
def test_invert_dict_of_str(obj, expected):
    assert invert_dict_of_str(obj) == expected


@pytest.mark.parametrize(
    "obj",
    [
        {"a": "foo", "b": "foo"},
        {"a": "foo", "b": "bar", "c": "foo", "d": "bar"},
    ],
)
def test_invert_dict_of_str_raises_on_dupe_with_raise_on_dupe(obj):
    with pytest.raises(ValueError, match=r"Duplicate value of found for key .+: .+"):
        invert_dict_of_str(obj, raise_on_dupe=True)
