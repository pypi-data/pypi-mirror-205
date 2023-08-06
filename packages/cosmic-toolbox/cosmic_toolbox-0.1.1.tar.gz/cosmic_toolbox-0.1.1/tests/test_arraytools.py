import numpy as np
import pytest
from cosmic_toolbox.arraytools import arr2rec, rec2arr, dict2rec, rec2dict, arr_to_rec


@pytest.fixture
def example_array():
    return np.array([[1, 2], [3, 4], [5, 6]])


@pytest.fixture
def example_names():
    return ["col1", "col2"]


@pytest.fixture
def example_dict():
    return {"col1": [1, 2, 3], "col2": [4, 5, 6]}


@pytest.fixture
def example_dtype():
    return np.dtype([("col1", int), ("col2", int)])


def compare_dict(dict1, dict2):
    return np.all([dict1[key] == dict2[key] for key in dict1.keys() if key in dict2])


def test_arr2rec(example_array, example_names):
    expected = np.rec.array([(1, 2), (3, 4), (5, 6)], names=example_names)
    assert np.array_equal(arr2rec(example_array, example_names), expected)


def test_rec2arr(example_array, example_names):
    rec_array = np.rec.array([(1, 2), (3, 4), (5, 6)], names=example_names)
    expected = np.array([[1, 2], [3, 4], [5, 6]])
    assert np.array_equal(rec2arr(rec_array), expected)


def test_dict2rec(example_dict):
    expected = np.rec.array([(1, 4), (2, 5), (3, 6)], names=["col1", "col2"])
    assert np.array_equal(dict2rec(example_dict), expected)


def test_rec2dict(example_dtype):
    rec_array = np.rec.array([(1, 4), (2, 5), (3, 6)], dtype=example_dtype)
    expected = {"col1": np.array([1, 2, 3]), "col2": np.array([4, 5, 6])}
    predicted = rec2dict(rec_array)
    assert compare_dict(expected, predicted)


def test_arr_to_rec(example_array, example_dtype):
    expected = np.rec.array([(1, 2), (3, 4), (5, 6)], dtype=example_dtype)
    assert np.array_equal(arr_to_rec(example_array, example_dtype), expected)
