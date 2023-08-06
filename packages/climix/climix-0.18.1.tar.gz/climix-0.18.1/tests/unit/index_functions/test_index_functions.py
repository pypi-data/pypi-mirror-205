import dask.array as da
from cf_units import Unit
from contextlib import nullcontext as does_not_raise
import numpy as np
import pytest

from climix.index_functions import index_functions as idx_func


def lazy_func_test(index_function, cubes, expected):
    if isinstance(cubes, dict):
        data = {argname: cube.lazy_data() for argname, cube in cubes.items()}
        for value in data.values():
            assert hasattr(value, "compute")
    else:
        data = cubes.lazy_data()
        assert hasattr(data, "compute")
    res = index_function.lazy_func(data, axis=0)
    assert (res == expected).all()
    expected_mask = da.ma.getmaskarray(expected)
    res_mask = da.ma.getmaskarray(res)
    assert (res_mask == expected_mask).all()
    assert res.dtype == np.float32


def call_func_test(index_function, cubes, expected):
    if isinstance(cubes, dict):
        data = {argname: cube.data for argname, cube in cubes.items()}
    else:
        data = cubes.data
    if hasattr(data, "compute"):
        raise AssertionError
    res = index_function.call_func(data, axis=0)
    assert (res == expected).all()
    expected_mask = np.ma.getmaskarray(expected)
    res_mask = np.ma.getmaskarray(res)
    assert (res_mask == expected_mask).all()
    assert res.dtype == np.float32


TEST_COUNT_LEVEL_CROSSINGS_PARAMETERS = [
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        np.array([[1, 2, 2], [2, 2, 2]]),
    ),  # ordinary np
    (
        {
            "data": (-1)
            * np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
            "units": "degree_Celsius",
        },
        {
            "data": np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        np.ma.masked_array([1, 1, 1, 1], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked np
    (
        {"data": (-1) * da.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": da.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        np.array([[1, 2, 2], [2, 2, 2]]),
    ),  # ordinary da
    (
        {
            "data": (-1)
            * da.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
            "units": "degree_Celsius",
        },
        {
            "data": da.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        np.ma.masked_array([1, 1, 1, 1], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked da
    (
        {
            "data": (-1)
            * da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [0, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {
            "data": da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 1], [0, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        np.ma.masked_array([[0, 1], [3, 1]]),
    ),  # masked da
    (
        {"data": (-1) * 275.15 * np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        pytest.raises(AssertionError),
    ),  # prepare assert error
    (
        {"data": (-1) * 275.15 * np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": 275.15 * np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        does_not_raise(),
    ),  # prepare do not raise
]

parameter_names = "f_cube_tasmin, f_cube_tasmax, f_first_threshold, expected"
fixtures = ["f_cube_tasmin", "f_cube_tasmax", "f_first_threshold"]


@pytest.mark.parametrize(
    parameter_names, TEST_COUNT_LEVEL_CROSSINGS_PARAMETERS[:5], indirect=fixtures
)
def test_count_level_crossings_call_func(
    f_cube_tasmin, f_cube_tasmax, f_first_threshold, expected
):
    index_function = idx_func.CountLevelCrossings(f_first_threshold)
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    call_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("1")


@pytest.mark.parametrize(
    parameter_names, TEST_COUNT_LEVEL_CROSSINGS_PARAMETERS[:5], indirect=fixtures
)
def test_count_level_crossings_lazy_func(
    f_cube_tasmin, f_cube_tasmax, f_first_threshold, expected
):
    index_function = idx_func.CountLevelCrossings(f_first_threshold)
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    lazy_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("1")


@pytest.mark.parametrize(
    parameter_names, TEST_COUNT_LEVEL_CROSSINGS_PARAMETERS[5:], indirect=fixtures
)
def test_count_level_crossings_prepare(
    f_cube_tasmin, f_cube_tasmax, f_first_threshold, expected
):
    index_function = idx_func.CountLevelCrossings(f_first_threshold)
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    with expected:
        index_function.prepare(cube_mapping)
        assert index_function.threshold.units == f_cube_tasmin.units


TEST_COUNT_OCCURRENCES_PARAMETERS = [
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 3, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.array([[1, 1, 1], [1, 2, 2]]),
    ),  # ordinary np
    (
        {
            "data": np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.ma.masked_array([0, 0, 1, 1], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked np
    (
        {"data": da.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 3, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.array([[1, 1, 1], [1, 2, 2]]),
    ),  # ordinary da
    (
        {
            "data": da.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.ma.masked_array([0, 0, 1, 1], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked da
    (
        {
            "data": da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [0, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 3, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.ma.masked_array([[0, 1], [2, 0]]),
    ),  # masked da
]

parameter_names = "f_cube_tas, f_first_threshold, condition, expected"
fixtures = ["f_cube_tas", "f_first_threshold"]


@pytest.mark.parametrize(
    parameter_names, TEST_COUNT_OCCURRENCES_PARAMETERS, indirect=fixtures
)
def test_count_occurences_call_func(f_cube_tas, f_first_threshold, condition, expected):
    index_function = idx_func.CountOccurrences(f_first_threshold, condition)
    call_func_test(index_function, f_cube_tas, expected)
    assert index_function.units == Unit("1")


@pytest.mark.parametrize(
    parameter_names, TEST_COUNT_OCCURRENCES_PARAMETERS, indirect=fixtures
)
def test_count_occurences_lazy_func(f_cube_tas, f_first_threshold, condition, expected):
    index_function = idx_func.CountOccurrences(f_first_threshold, condition)
    lazy_func_test(index_function, f_cube_tas, expected)
    assert index_function.units == Unit("1")


TEST_DIURNAL_TEMPERATURE_RANGE_PARAMETERS = [
    (
        {"data": (-1) * np.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        {"data": np.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        "min",
        np.array([[0, 2, 4], [6, 8, 10]]),
    ),  # ordinary np
    (
        {
            "data": 275.15 + (-1) * np.arange(12).reshape(2, 2, 3),
            "units": "K",
        },
        {
            "data": 275.15 + np.arange(12).reshape(2, 2, 3),
            "units": "K",
        },
        "max",
        np.array([[12, 14, 16], [18, 20, 22]]),
    ),  # ordinary np
    (
        {
            "data": (-1)
            * np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
            "units": "degree_Celsius",
        },
        {
            "data": np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        "min",
        np.ma.masked_array([2, 4, 6, 8], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked np
    (
        {
            "data": 275.15 + (-1) * da.arange(12).reshape(2, 2, 3),
            "units": "K",
        },
        {
            "data": 275.15 + da.arange(12).reshape(2, 2, 3),
            "units": "K",
        },
        "max",
        np.array([[12, 14, 16], [18, 20, 22]]),
    ),  # ordinary da
    (
        {
            "data": (-1)
            * da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {
            "data": da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
            ),
            "units": "degree_Celsius",
        },
        "max",
        np.ma.masked_array([[0, 18], [12, 6]]),
    ),  # masked da
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "K"},
        "max",
        pytest.raises(AssertionError),
    ),  # prepare assertion error
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "K"},
        "max",
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = "f_cube_tasmin, f_cube_tasmax, statistics, expected"
fixtures = ["f_cube_tasmin", "f_cube_tasmax"]


@pytest.mark.parametrize(
    parameter_names, TEST_DIURNAL_TEMPERATURE_RANGE_PARAMETERS[:5], indirect=fixtures
)
def test_diurnal_temperature_range_call_func(
    f_cube_tasmin, f_cube_tasmax, statistics, expected
):
    index_function = idx_func.DiurnalTemperatureRange(statistics)
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    call_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("degree_Celsius")


@pytest.mark.parametrize(
    parameter_names, TEST_DIURNAL_TEMPERATURE_RANGE_PARAMETERS[:5], indirect=fixtures
)
def test_diurnal_temperature_range_lazy_func(
    f_cube_tasmin, f_cube_tasmax, statistics, expected
):
    index_function = idx_func.DiurnalTemperatureRange(statistics)
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    lazy_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("degree_Celsius")


@pytest.mark.parametrize(
    parameter_names, TEST_DIURNAL_TEMPERATURE_RANGE_PARAMETERS[5:], indirect=fixtures
)
def test_diurnal_temperature_range_prepare(
    f_cube_tasmin, f_cube_tasmax, statistics, expected
):
    index_function = idx_func.DiurnalTemperatureRange(statistics)
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    with expected:
        index_function.prepare(cube_mapping)


TEST_EXTREME_TEMPERATURE_RANGE_PARAMETERS = [
    (
        {"data": (-1) * np.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        {"data": np.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        np.array([[48, 50, 52], [54, 56, 58]]),
    ),  # ordinary np
    (
        {
            "data": (-1)
            * np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
            "units": "degree_Celsius",
        },
        {
            "data": np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        np.ma.masked_array([2, 4, 6, 8], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked np
    (
        {
            "data": 275.15 + (-1) * da.arange(12).reshape(2, 2, 3),
            "units": "K",
        },
        {
            "data": 275.15 + da.arange(12).reshape(2, 2, 3),
            "units": "K",
        },
        np.array([[12, 14, 16], [18, 20, 22]]),
    ),  # ordinary da
    (
        {
            "data": (-1)
            * da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {
            "data": da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
            ),
            "units": "degree_Celsius",
        },
        np.ma.masked_array(data=[[0, 18], [12, 6]]),
    ),  # masked da
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "K"},
        pytest.raises(AssertionError),
    ),  # prepare assertion error
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "kg"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "kg"},
        pytest.raises(AssertionError),
    ),  # prepare assertion error
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "K"},
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = "f_cube_tasmin, f_cube_tasmax, expected"
fixtures = ["f_cube_tasmin", "f_cube_tasmax"]


@pytest.mark.parametrize(
    parameter_names, TEST_EXTREME_TEMPERATURE_RANGE_PARAMETERS[:4], indirect=fixtures
)
def test_extreme_temperature_range_call_func(f_cube_tasmin, f_cube_tasmax, expected):
    index_function = idx_func.ExtremeTemperatureRange()
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    call_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("degree_Celsius")


@pytest.mark.parametrize(
    parameter_names, TEST_EXTREME_TEMPERATURE_RANGE_PARAMETERS[:4], indirect=fixtures
)
def test_extreme_temperature_range_lazy_func(f_cube_tasmin, f_cube_tasmax, expected):
    index_function = idx_func.ExtremeTemperatureRange()
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    lazy_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("degree_Celsius")


@pytest.mark.parametrize(
    parameter_names, TEST_EXTREME_TEMPERATURE_RANGE_PARAMETERS[4:], indirect=fixtures
)
def test_extreme_temperature_range_prepare(f_cube_tasmin, f_cube_tasmax, expected):
    index_function = idx_func.ExtremeTemperatureRange()
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    with expected:
        index_function.prepare(cube_mapping)


TEST_INTERDAY_DIURNAL_TEMPERATURE_RANGE_PARAMETERS = [
    (
        {"data": (-1) * np.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        {"data": np.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        np.array([[12, 12, 12], [12, 12, 12]]),
    ),  # ordinary np
    (
        {
            "data": (-1)
            * np.ma.masked_array(
                [[1, 2, 3, 3], [5, 2, 3, 3]], mask=[[0, 0, 1, 0], [0, 0, 0, 0]]
            ).reshape(2, 1, 4),
            "units": "degree_Celsius",
        },
        {
            "data": np.ma.masked_array(
                [[1, 2, 3, 3], [1, 2, 4, 4]], mask=[[0, 0, 1, 0], [0, 0, 0, 0]]
            ).reshape(2, 1, 4),
            "units": "degree_Celsius",
        },
        np.ma.masked_array([4, 0, 1, 1], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked np
    (
        {
            "data": 275.15 + (-1) * da.arange(18).reshape(3, 2, 3),
            "units": "K",
        },
        {
            "data": 274.15 + da.ones(18).reshape(3, 2, 3),
            "units": "K",
        },
        np.array([[6, 6, 6], [6, 6, 6]]),
    ),  # ordinary da
    (
        {
            "data": (-1)
            * da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [0, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {
            "data": da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [0, 1]]],
            ),
            "units": "degree_Celsius",
        },
        np.ma.masked_array([[8, 8], [8, 8]], mask=[[1, 1], [0, 1]]),
    ),  # masked da
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "K"},
        pytest.raises(AssertionError),
    ),  # prepare assertion error
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "kg"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "kg"},
        pytest.raises(AssertionError),
    ),  # prepare assertion error
    (
        {"data": (-1) * np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": np.arange(12).reshape(2, 2, 3), "units": "K"},
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = "f_cube_tasmin, f_cube_tasmax, expected"
fixtures = ["f_cube_tasmin", "f_cube_tasmax"]


@pytest.mark.parametrize(
    parameter_names,
    TEST_INTERDAY_DIURNAL_TEMPERATURE_RANGE_PARAMETERS[:4],
    indirect=fixtures,
)
def test_interday_diurnal_temperature_range_call_func(
    f_cube_tasmin, f_cube_tasmax, expected
):
    index_function = idx_func.InterdayDiurnalTemperatureRange()
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    call_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("degree_Celsius")


@pytest.mark.parametrize(
    parameter_names,
    TEST_INTERDAY_DIURNAL_TEMPERATURE_RANGE_PARAMETERS[:4],
    indirect=fixtures,
)
def test_interday_diurnal_temperature_range_lazy_func(
    f_cube_tasmin, f_cube_tasmax, expected
):
    index_function = idx_func.InterdayDiurnalTemperatureRange()
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    lazy_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("degree_Celsius")


@pytest.mark.parametrize(
    parameter_names,
    TEST_INTERDAY_DIURNAL_TEMPERATURE_RANGE_PARAMETERS[4:],
    indirect=fixtures,
)
def test_interday_diurnal_temperature_range_prepare(
    f_cube_tasmin, f_cube_tasmax, expected
):
    index_function = idx_func.InterdayDiurnalTemperatureRange()
    cube_mapping = {"low_data": f_cube_tasmin, "high_data": f_cube_tasmax}
    with expected:
        index_function.prepare(cube_mapping)


TEST_PERCENTILE_PARAMETERS = [
    (
        {"data": np.arange(44).reshape(11, 2, 2), "units": "degree_Celsius"},
        {"data": 90, "units": "%"},
        np.array([[36, 37], [38, 39]]),
    ),  # ordinary np
    (
        {"data": da.arange(60).reshape(15, 2, 2), "units": "degree_Celsius"},
        {"data": 50, "units": "%"},
        np.array([[28, 29], [30, 31]]),
    ),  # ordinary da
    (
        {
            "data": np.ma.masked_array(
                data=[
                    [[0, 0], [0, 0]],
                    [[4, 5], [6, 7]],
                    [[8, 9], [10, 11]],
                    [[12, 13], [14, 15]],
                ],
                mask=[
                    [[0, 0], [0, 0]],
                    [[0, 0], [0, 0]],
                    [[0, 0], [0, 0]],
                    [[1, 1], [1, 1]],
                ],
            ),
            "units": "degree_Celsius",
        },
        {"data": 50, "units": "%"},
        np.ma.masked_array(data=[[4, 5], [6, 7]]),
    ),  # masked np
    (
        {
            "data": da.ma.masked_array(
                data=[
                    [[0, 1], [2, 3]],
                    [[4, 5], [6, 7]],
                    [[0, 0], [0, 0]],
                    [[12, 13], [14, 15]],
                ],
                mask=[
                    [[0, 0], [1, 0]],
                    [[0, 1], [0, 0]],
                    [[0, 0], [0, 0]],
                    [[0, 0], [0, 0]],
                ],
            ),
            "units": "degree_Celsius",
        },
        {"data": 50, "units": "%"},
        np.ma.masked_array(data=[[2, 1], [6, 5]]),
    ),  # masked da
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 50, "units": "%"},
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = "f_cube_tas, f_percentile, expected"
fixtures = ["f_cube_tas", "f_percentile"]


@pytest.mark.parametrize(
    parameter_names, TEST_PERCENTILE_PARAMETERS[:4], indirect=fixtures
)
def test_percentile_call_func(f_cube_tas, f_percentile, expected):
    index_function = idx_func.Percentile(f_percentile)
    call_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_PERCENTILE_PARAMETERS[:4], indirect=fixtures
)
def test_percentile_lazy_func(f_cube_tas, f_percentile, expected):
    index_function = idx_func.Percentile(f_percentile)
    lazy_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_PERCENTILE_PARAMETERS[4:], indirect=fixtures
)
def test_percentile_prepare(f_cube_tas, f_percentile, expected):
    index_function = idx_func.Percentile(f_percentile)
    cube_mapping = {"data": f_cube_tas}
    with expected:
        index_function.prepare(cube_mapping)
        assert index_function.units == f_cube_tas.units
        assert index_function.standard_name == f_cube_tas.standard_name


TEST_THRESHOLDED_PERCENTILE_PARAMETERS = [
    (
        {"data": np.arange(44).reshape(11, 2, 2), "units": "degree_Celsius"},
        {"data": 50, "units": "%"},
        {"data": 15, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.array([[28, 29], [30, 31]]),
    ),  # ordinary np
    (
        {"data": da.arange(60).reshape(15, 2, 2), "units": "degree_Celsius"},
        {"data": 50, "units": "%"},
        {"data": 15, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.array([[36, 37], [38, 39]]),
    ),  # ordinary da
    (
        {
            "data": np.ma.masked_array(
                data=[
                    [[0, 0], [0, 0]],
                    [[4, 5], [6, 7]],
                    [[8, 9], [10, 11]],
                    [[12, 13], [14, 15]],
                ],
                mask=[
                    [[0, 0], [0, 0]],
                    [[0, 0], [0, 0]],
                    [[0, 0], [0, 0]],
                    [[1, 1], [1, 1]],
                ],
            ),
            "units": "degree_Celsius",
        },
        {"data": 50, "units": "%"},
        {"data": 5, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.ma.masked_array(data=[[8, 9], [8, 9]]),
    ),  # masked np
    (
        {
            "data": da.ma.masked_array(
                data=[
                    [[0, 1], [2, 3]],
                    [[4, 5], [6, 7]],
                    [[0, 0], [0, 0]],
                    [[12, 13], [14, 15]],
                ],
                mask=[
                    [[0, 0], [1, 0]],
                    [[0, 1], [0, 0]],
                    [[0, 0], [0, 0]],
                    [[0, 0], [0, 0]],
                ],
            ),
            "units": "degree_Celsius",
        },
        {"data": 50, "units": "%"},
        {"data": 4, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.ma.masked_array([[12, 13], [10, 11]]),
    ),  # masked da
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 500, "units": "%"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        pytest.raises(AssertionError),
    ),  # Indexfunction assertion error
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": -50, "units": "%"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        pytest.raises(AssertionError),
    ),  # Indexfunction assertion error
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "kg"},
        {"data": 50, "units": "%"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        pytest.raises(ValueError),
    ),  # prepare assertion error
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": 50, "units": "%"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        does_not_raise(),
    ),  # prepare do not raise
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 50, "units": "%"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = "f_cube_tas, f_percentile, f_first_threshold, condition, expected"
fixtures = ["f_cube_tas", "f_percentile", "f_first_threshold"]


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_PERCENTILE_PARAMETERS[:4], indirect=fixtures
)
def test_thresholded_percentile_call_func(
    f_cube_tas, f_percentile, f_first_threshold, condition, expected
):
    index_function = idx_func.ThresholdedPercentile(
        f_first_threshold, condition, f_percentile
    )
    call_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_PERCENTILE_PARAMETERS[:4], indirect=fixtures
)
def test_thresholded_percentile_lazy_func(
    f_cube_tas, f_percentile, f_first_threshold, condition, expected
):
    index_function = idx_func.ThresholdedPercentile(
        f_first_threshold, condition, f_percentile
    )
    lazy_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_PERCENTILE_PARAMETERS[4:6], indirect=fixtures
)
def test_thresholded_percentile_index_function(
    f_cube_tas, f_percentile, f_first_threshold, condition, expected
):
    with expected:
        _ = idx_func.ThresholdedPercentile(f_first_threshold, condition, f_percentile)


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_PERCENTILE_PARAMETERS[6:], indirect=fixtures
)
def test_thresholded_percentile_prepare(
    f_cube_tas, f_percentile, f_first_threshold, condition, expected
):
    index_function = idx_func.ThresholdedPercentile(
        f_first_threshold, condition, f_percentile
    )
    cube_mapping = {"data": f_cube_tas}
    with expected:
        index_function.prepare(cube_mapping)
        assert index_function.units == f_cube_tas.units
        assert index_function.standard_name == f_cube_tas.standard_name


TEST_STATISTICS_PARAMETERS = [
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        "max",
        np.array([[6, 7, 8], [9, 10, 11]]),
    ),  # ordinary np
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        "min",
        np.array([[0, 1, 2], [3, 4, 5]]),
    ),  # ordinary np
    (
        {
            "data": np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        "max",
        np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked np
    (
        {"data": da.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        "max",
        np.array([[6, 7, 8], [9, 10, 11]]),
    ),  # ordinary da
    (
        {
            "data": (-1)
            * da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
            ),
            "units": "degree_Celsius",
        },
        "min",
        np.ma.masked_array([[0, -9], [-6, -3]]),
    ),  # masked da
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        "max",
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = "f_cube_tas, statistics, expected"
fixtures = ["f_cube_tas"]


@pytest.mark.parametrize(
    parameter_names, TEST_STATISTICS_PARAMETERS[:5], indirect=fixtures
)
def test_statistics_call_func(f_cube_tas, statistics, expected):
    index_function = idx_func.Statistics(statistics)
    call_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_STATISTICS_PARAMETERS[:5], indirect=fixtures
)
def test_statistics_lazy_func(f_cube_tas, statistics, expected):
    index_function = idx_func.Statistics(statistics)
    lazy_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_STATISTICS_PARAMETERS[5:], indirect=fixtures
)
def test_statistics_prepare(f_cube_tas, statistics, expected):
    index_function = idx_func.Statistics(statistics)
    cube_mapping = {"data": f_cube_tas}
    with expected:
        index_function.prepare(cube_mapping)
        assert index_function.units == f_cube_tas.units
        assert index_function.standard_name == f_cube_tas.standard_name


TEST_THRESHOLDED_STATISTICS_PARAMETERS = [
    (
        {"data": np.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        {"data": 15, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "min",
        np.array([[18, 19, 20], [21, 16, 17]]),
    ),  # ordinary np
    (
        {
            "data": np.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "max",
        np.ma.masked_array([1, 2, 3, 4], mask=[1, 1, 1, 0]).reshape(1, 1, 4),
    ),  # masked np
    (
        {"data": da.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        {"data": 15, "units": "degree_Celsius", "standard_name": "air_temperature"},
        "<",
        "max",
        np.array([[12, 13, 14], [9, 10, 11]]),
    ),  # ordinary da
    (
        {
            "data": da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [0, 0]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 3, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "min",
        np.ma.masked_array(data=[[8, 9], [6, 11]], mask=[[1, 0], [0, 0]]),
    ),  # masked da
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "kg"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "max",
        pytest.raises(ValueError),
    ),  # prepare assertion error
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "max",
        does_not_raise(),
    ),  # prepare do not raise
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "max",
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = "f_cube_tas, f_first_threshold, condition, statistics, expected"
fixtures = ["f_cube_tas", "f_first_threshold"]


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_STATISTICS_PARAMETERS[:4], indirect=fixtures
)
def test_thresholded_statistics_call_func(
    f_cube_tas, f_first_threshold, condition, statistics, expected
):
    index_function = idx_func.ThresholdedStatistics(
        f_first_threshold, condition, statistics
    )
    call_func_test(index_function, f_cube_tas, expected)
    assert index_function.units == Unit("days")


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_STATISTICS_PARAMETERS[:4], indirect=fixtures
)
def test_thresholded_statistics_lazy_func(
    f_cube_tas, f_first_threshold, condition, statistics, expected
):
    index_function = idx_func.ThresholdedStatistics(
        f_first_threshold, condition, statistics
    )
    lazy_func_test(index_function, f_cube_tas, expected)
    assert index_function.units == Unit("days")


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_STATISTICS_PARAMETERS[4:], indirect=fixtures
)
def test_thresholded_statistics_prepare(
    f_cube_tas, f_first_threshold, condition, statistics, expected
):
    index_function = idx_func.ThresholdedStatistics(
        f_first_threshold, condition, statistics
    )
    cube_mapping = {"data": f_cube_tas}
    with expected:
        index_function.prepare(cube_mapping)
        assert index_function.units == f_cube_tas.units
        assert index_function.standard_name == f_cube_tas.standard_name


TEST_RUNNING_STATISTICS_PARAMETERS = [
    (
        {"data": np.arange(42).reshape(7, 2, 3), "units": "degree_Celsius"},
        {"data": 5, "units": "day"},
        "sum",
        "max",
        np.array(
            [
                [
                    [0, 6, 12, 18, 24, 120, 18, 24, 30, 36],
                    [1, 7, 13, 19, 25, 125, 19, 25, 31, 37],
                    [2, 8, 14, 20, 26, 130, 20, 26, 32, 38],
                ],
                [
                    [3, 9, 15, 21, 27, 135, 21, 27, 33, 39],
                    [4, 10, 16, 22, 28, 140, 22, 28, 34, 40],
                    [5, 11, 17, 23, 29, 145, 23, 29, 35, 41],
                ],
            ]
        ),
    ),  # ordinary np
    (
        {
            "data": np.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 1], [0, 0]], [[1, 0], [0, 0]], [[1, 0], [0, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        "sum",
        "max",
        np.ma.masked_array(
            data=[[[0, 12, 8], [1, 14, 9]], [[2, 16, 10], [3, 18, 11]]],
            mask=[[[0, 1, 1], [1, 1, 0]], [[0, 0, 0], [0, 1, 1]]],
        ),
    ),  # masked np
    (
        {"data": da.arange(42).reshape(7, 2, 3), "units": "degree_Celsius"},
        {"data": 5, "units": "day"},
        "sum",
        "min",
        np.array(
            [
                [
                    [0, 6, 12, 18, 24, 60, 18, 24, 30, 36],
                    [1, 7, 13, 19, 25, 65, 19, 25, 31, 37],
                    [2, 8, 14, 20, 26, 70, 20, 26, 32, 38],
                ],
                [
                    [3, 9, 15, 21, 27, 75, 21, 27, 33, 39],
                    [4, 10, 16, 22, 28, 80, 22, 28, 34, 40],
                    [5, 11, 17, 23, 29, 85, 23, 29, 35, 41],
                ],
            ]
        ),
    ),  # ordinary da
    (
        {
            "data": da.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 1], [0, 0]], [[1, 0], [0, 0]], [[1, 0], [0, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        "sum",
        "max",
        np.ma.masked_array(
            data=[[[0, 12, 8], [1, 14, 9]], [[2, 16, 10], [3, 18, 11]]],
            mask=[[[0, 1, 1], [1, 1, 0]], [[0, 0, 0], [0, 1, 1]]],
        ),
    ),  # masked da
    (
        {
            "data": np.arange(12).reshape(3, 2, 2),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        "sum",
        "max",
        does_not_raise(),
    ),  # prepare do not raise
    (
        {
            "data": np.arange(42).reshape(7, 2, 3),
            "units": "degree_Celsius",
        },
        {"data": 5, "units": "day"},
        "sum",
        "max",
        (10,),
    ),  # pre_aggregate_shape
    (
        {
            "data": np.arange(42).reshape(7, 2, 3),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        "sum",
        "max",
        (3,),
    ),  # pre_aggregate_shape
    (
        {
            "data": np.arange(42).reshape(7, 2, 3),
            "units": "degree_Celsius",
        },
        {"data": 10, "units": "day"},
        "sum",
        "max",
        (19,),
    ),  # pre_aggregate_shape
    (
        {
            "data": np.array(
                [
                    [
                        [0, 6, 12, 18, 24, 120, 18, 24, 30, 36],
                        [1, 7, 13, 19, 25, 125, 19, 25, 31, 37],
                        [2, 8, 14, 20, 26, 130, 20, 26, 32, 38],
                    ],
                    [
                        [3, 9, 15, 21, 27, 135, 21, 27, 33, 39],
                        [4, 10, 16, 22, 28, 140, 22, 28, 34, 40],
                        [5, 11, 17, 23, 29, 145, 23, 29, 35, 41],
                    ],
                ]
            ),
            "units": "degree_Celsius",
        },
        {"data": 5, "units": "day"},
        "sum",
        "max",
        np.array(
            [[[120, 125, 130], [135, 140, 145]]],
        ),
    ),  # postprocess no-fuse np
    (
        {
            "data": np.array(
                [
                    [
                        [
                            [0, 6, 12, 18, 24, 120, 18, 24, 30, 36],
                            [1, 7, 13, 19, 25, 125, 19, 25, 31, 37],
                            [2, 8, 14, 20, 26, 130, 20, 26, 32, 38],
                        ],
                        [
                            [3, 9, 15, 21, 27, 135, 21, 27, 33, 39],
                            [4, 10, 16, 22, 28, 140, 22, 28, 34, 40],
                            [5, 11, 17, 23, 29, 145, 23, 29, 35, 41],
                        ],
                    ],
                    [
                        [
                            [10, 6, 12, 18, 24, 1201, 181, 24, 30, 36],
                            [11, 7, 13, 19, 25, 1251, 191, 25, 31, 37],
                            [12, 8, 14, 20, 26, 1301, 201, 26, 32, 38],
                        ],
                        [
                            [13, 9, 15, 21, 27, 1351, 211, 27, 33, 39],
                            [14, 10, 16, 22, 28, 1401, 221, 28, 34, 40],
                            [15, 11, 17, 23, 29, 1451, 231, 29, 35, 41],
                        ],
                    ],
                ]
            ),
            "units": "degree_Celsius",
        },
        {"data": 5, "units": "day"},
        "sum",
        "max",
        np.array(
            [
                [[120, 125, 130], [135, 140, 145]],
                [[1201, 1251, 1301], [1351, 1401, 1451]],
            ]
        ),
    ),  # postprocess fuse np
    (
        {
            "data": np.ma.masked_array(
                data=[[[0, 12, 8], [1, 14, 9]], [[2, 16, 10], [3, 18, 11]]],
                mask=[[[0, 1, 1], [1, 1, 0]], [[0, 0, 0], [0, 1, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        "sum",
        "max",
        np.ma.masked_array(data=[[12, 14], [16, 18]], mask=[[1, 1], [0, 1]]),
    ),  # postprocess masked no-fuse np
    (
        {
            "data": np.ma.masked_array(
                data=[
                    [[[0, 12, 8], [1, 14, 9]], [[7, 16, 10], [6, 18, 11]]],
                    [[[7, 16, 10], [6, 18, 11]], [[0, 12, 8], [1, 14, 9]]],
                ],
                mask=[
                    [[[0, 1, 1], [0, 0, 0]], [[0, 0, 0], [1, 1, 1]]],
                    [[[0, 1, 1], [0, 0, 0]], [[0, 0, 0], [1, 1, 1]]],
                ],
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        "sum",
        "max",
        np.ma.masked_array(
            data=[[[15, 15], [16, 18]], [[16, 18], [12, 14]]],
            mask=[[[1, 0], [0, 1]], [[1, 0], [0, 1]]],
        ),
    ),  # postprocess masked fuse np
    (
        {
            "data": da.array(
                [
                    [
                        [
                            [0, 6, 12, 18, 24, 120, 18, 24, 30, 36],
                            [1, 7, 13, 19, 25, 125, 19, 25, 31, 37],
                            [2, 8, 14, 20, 26, 130, 20, 26, 32, 38],
                        ],
                        [
                            [3, 9, 15, 21, 27, 135, 21, 27, 33, 39],
                            [4, 10, 16, 22, 28, 140, 22, 28, 34, 40],
                            [5, 11, 17, 23, 29, 145, 23, 29, 35, 41],
                        ],
                    ],
                    [
                        [
                            [40, 40, 40, 4, 5, 100, 5, 6, 7, 8],
                            [40, 40, 40, 4, 5, 100, 5, 6, 7, 8],
                            [40, 40, 40, 4, 5, 100, 5, 6, 7, 8],
                        ],
                        [
                            [3, 9, 15, 21, 27, 200, 50, 60, 70, 80],
                            [4, 10, 16, 22, 28, 200, 50, 60, 70, 80],
                            [5, 11, 17, 23, 29, 200, 50, 60, 70, 80],
                        ],
                    ],
                ]
            ),
            "units": "degree_Celsius",
        },
        {"data": 5, "units": "day"},
        "sum",
        "max",
        np.array(
            [[[170, 173, 176], [135, 140, 145]], [[186, 188, 190], [260, 260, 260]]],
        ),
    ),  # postprocess fuse da (max)
    (
        {
            "data": da.array(
                [
                    [
                        [
                            [0, 6, 12, 18, 24, 60, 18, 24, 30, 36],
                            [1, 7, 13, 19, 25, 65, 19, 25, 31, 37],
                            [2, 8, 14, 20, 26, 70, 20, 26, 32, 38],
                        ],
                        [
                            [3, 9, 15, 21, 27, 75, 21, 27, 33, 39],
                            [4, 10, 16, 22, 28, 80, 22, 28, 34, 40],
                            [5, 11, 17, 23, 29, 85, 23, 29, 35, 41],
                        ],
                    ],
                    [
                        [
                            [40, 40, 40, 4, 5, 30, 5, 6, 7, 8],
                            [40, 40, 40, 4, 5, 30, 5, 6, 7, 8],
                            [40, 40, 40, 4, 5, 30, 5, 6, 7, 8],
                        ],
                        [
                            [3, 9, 15, 21, 27, 75, 50, 60, 70, 80],
                            [4, 10, 16, 22, 28, 80, 50, 60, 70, 80],
                            [5, 11, 17, 23, 29, 85, 50, 60, 70, 80],
                        ],
                    ],
                ]
            ),
            "units": "degree_Celsius",
        },
        {"data": 5, "units": "day"},
        "sum",
        "min",
        np.array([[[60, 65, 70], [75, 80, 85]], [[30, 30, 30], [75, 80, 85]]]),
    ),  # postprocess fuse da (min)
    (
        {
            "data": np.array(
                [
                    [
                        [0, 6, 12, 18, 24, 60, 18, 24, 30, 36],
                        [1, 7, 13, 19, 25, 65, 19, 25, 31, 37],
                        [2, 8, 14, 20, 26, 70, 20, 26, 32, 38],
                    ],
                    [
                        [3, 9, 15, 21, 27, 75, 21, 27, 33, 39],
                        [4, 10, 16, 22, 28, 80, 22, 28, 34, 40],
                        [5, 11, 17, 23, 29, 85, 23, 29, 35, 41],
                    ],
                ]
            ),
            "units": "degree_Celsius",
        },
        {"data": 5, "units": "day"},
        "sum",
        "min",
        np.array([[[60, 65, 70], [75, 80, 85]]]),
    ),  # postprocess no-fuse da
    (
        {
            "data": da.ma.masked_array(
                data=[[[0, 12, 8], [1, 14, 9]], [[7, 16, 10], [5, 18, 11]]],
                mask=[[[0, 1, 1], [1, 1, 0]], [[0, 0, 0], [1, 1, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        "sum",
        "max",
        np.ma.masked_array(data=[[12, 14], [16, 18]], mask=[[1, 1], [0, 1]]),
    ),  # postprocess masked no-fuse da
    (
        {
            "data": da.ma.masked_array(
                data=[
                    [[[0, 12, 8], [1, 14, 9]], [[7, 16, 10], [6, 18, 11]]],
                    [[[7, 16, 10], [6, 18, 11]], [[0, 12, 8], [1, 14, 9]]],
                ],
                mask=[
                    [[[0, 1, 1], [0, 0, 0]], [[0, 0, 0], [1, 1, 1]]],
                    [[[0, 1, 1], [0, 0, 0]], [[0, 0, 0], [1, 1, 1]]],
                ],
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        "sum",
        "max",
        np.ma.masked_array(
            data=[[[15, 15], [16, 18]], [[16, 18], [12, 14]]],
            mask=[[[1, 0], [0, 1]], [[1, 0], [0, 1]]],
        ),
    ),  # postprocess masked fuse da
]


parameter_names = (
    "f_cube_tas, f_window_size, rolling_aggregator, overall_statistic, expected"
)
fixtures = ["f_cube_tas", "f_window_size"]


@pytest.mark.parametrize(
    parameter_names, TEST_RUNNING_STATISTICS_PARAMETERS[:4], indirect=fixtures
)
def test_running_statistics_call_func(
    f_cube_tas, f_window_size, rolling_aggregator, overall_statistic, expected
):
    index_function = idx_func.RunningStatistics(
        rolling_aggregator, f_window_size, overall_statistic
    )
    call_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_RUNNING_STATISTICS_PARAMETERS[:4], indirect=fixtures
)
def test_running_statistics_lazy_func(
    f_cube_tas, f_window_size, rolling_aggregator, overall_statistic, expected
):
    index_function = idx_func.RunningStatistics(
        rolling_aggregator, f_window_size, overall_statistic
    )
    lazy_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_RUNNING_STATISTICS_PARAMETERS[4:5], indirect=fixtures
)
def test_running_statistics_prepare(
    f_cube_tas, f_window_size, rolling_aggregator, overall_statistic, expected
):
    index_function = idx_func.RunningStatistics(
        rolling_aggregator, f_window_size, overall_statistic
    )
    cube_mapping = {"data": f_cube_tas}
    with expected:
        index_function.prepare(cube_mapping)
        assert index_function.units == f_cube_tas.units
        assert index_function.standard_name == f_cube_tas.standard_name


@pytest.mark.parametrize(
    parameter_names, TEST_RUNNING_STATISTICS_PARAMETERS[5:8], indirect=fixtures
)
def test_running_statistics_pre_aggregate_shape(
    f_cube_tas, f_window_size, rolling_aggregator, overall_statistic, expected
):
    index_function = idx_func.RunningStatistics(
        rolling_aggregator, f_window_size, overall_statistic
    )
    shape = index_function.pre_aggregate_shape()
    assert shape == expected


@pytest.mark.parametrize(
    parameter_names, TEST_RUNNING_STATISTICS_PARAMETERS[8:], indirect=fixtures
)
def test_running_statistics_post_process(
    f_cube_tas, f_window_size, rolling_aggregator, overall_statistic, expected
):
    index_function = idx_func.RunningStatistics(
        rolling_aggregator, f_window_size, overall_statistic
    )
    data = f_cube_tas.data
    if data.ndim < 4:
        shape = data.shape
        data = data.reshape((1,) + shape)
    aggregateby_cube = f_cube_tas
    cube, res = index_function.post_process(aggregateby_cube, data, None, None)
    assert cube == f_cube_tas
    assert (res == expected).all()
    expected_mask = np.ma.getmaskarray(expected)
    res_mask = np.ma.getmaskarray(res)
    assert (res_mask == expected_mask).all()


TEST_THRESHOLDED_RUNNING_STATISTICS_PARAMETERS = [
    (
        {"data": np.arange(42).reshape(7, 2, 3), "units": "degree_Celsius"},
        {"data": 5, "units": "day"},
        {"data": 10, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "sum",
        "max",
        np.array(
            [
                [
                    [0, 0, 12, 18, 24, 120, 18, 24, 30, 36],
                    [0, 0, 13, 19, 25, 125, 19, 25, 31, 37],
                    [0, 0, 14, 20, 26, 130, 20, 26, 32, 38],
                ],
                [
                    [0, 0, 15, 21, 27, 135, 21, 27, 33, 39],
                    [0, 0, 16, 22, 28, 140, 22, 28, 34, 40],
                    [0, 11, 17, 23, 29, 145, 23, 29, 35, 41],
                ],
            ],
        ),
    ),  # ordinary np
    (
        {
            "data": np.ma.masked_array(
                data=[[[0, 1], [2, 3]], [[4, 5], [6, 7]], [[8, 9], [10, 11]]],
                mask=[[[0, 1], [0, 0]], [[0, 0], [1, 0]], [[0, 0], [0, 0]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        {"data": 5, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "sum",
        "max",
        np.ma.masked_array(
            data=[[[0, 8, 8], [0, 9, 9]], [[0, 16, 10], [0, 18, 11]]],
            mask=[[[0, 0, 0], [1, 1, 0]], [[0, 1, 0], [0, 0, 0]]],
        ),
    ),  # masked np
    (
        {"data": da.arange(42).reshape(7, 2, 3), "units": "degree_Celsius"},
        {"data": 5, "units": "day"},
        {"data": 10, "units": "degree_Celsius", "standard_name": "air_temperature"},
        "<",
        "sum",
        "max",
        np.array(
            [
                [
                    [0, 6, 0, 0, 0, 6, 0, 0, 0, 0],
                    [1, 7, 0, 0, 0, 8, 0, 0, 0, 0],
                    [2, 8, 0, 0, 0, 10, 0, 0, 0, 0],
                ],
                [
                    [3, 9, 0, 0, 0, 12, 0, 0, 0, 0],
                    [4, 0, 0, 0, 0, 4, 0, 0, 0, 0],
                    [5, 0, 0, 0, 0, 5, 0, 0, 0, 0],
                ],
            ],
        ),
    ),  # ordinary da
    (
        {
            "data": da.ma.masked_array(
                data=[[[0, 1], [2, 3]], [[4, 5], [6, 7]], [[8, 9], [10, 11]]],
                mask=[[[0, 1], [0, 0]], [[0, 0], [1, 0]], [[0, 0], [0, 0]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "day"},
        {"data": 5, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "sum",
        "max",
        np.ma.masked_array(
            data=[[[0, 8, 8], [0, 9, 9]], [[0, 16, 10], [0, 18, 11]]],
            mask=[[[0, 0, 0], [1, 1, 0]], [[0, 1, 0], [0, 0, 0]]],
        ),
    ),  # masked da
]

parameter_names = (
    "f_cube_tas, f_window_size, f_first_threshold, condition, "
    + "rolling_aggregator, overall_statistic, expected"
)
fixtures = ["f_cube_tas", "f_window_size", "f_first_threshold"]


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_RUNNING_STATISTICS_PARAMETERS, indirect=fixtures
)
def test_thresholded_running_statistics_call_func(
    f_cube_tas,
    f_window_size,
    f_first_threshold,
    condition,
    rolling_aggregator,
    overall_statistic,
    expected,
):
    index_function = idx_func.ThresholdedRunningStatistics(
        f_first_threshold,
        condition,
        rolling_aggregator,
        f_window_size,
        overall_statistic,
    )
    call_func_test(index_function, f_cube_tas, expected)


@pytest.mark.parametrize(
    parameter_names, TEST_THRESHOLDED_RUNNING_STATISTICS_PARAMETERS, indirect=fixtures
)
def test_thresholded_running_statistics_lazy_func(
    f_cube_tas,
    f_window_size,
    f_first_threshold,
    condition,
    rolling_aggregator,
    overall_statistic,
    expected,
):
    index_function = idx_func.ThresholdedRunningStatistics(
        f_first_threshold,
        condition,
        rolling_aggregator,
        f_window_size,
        overall_statistic,
    )
    lazy_func_test(index_function, f_cube_tas, expected)


TEST_TEMPERATURE_SUM_PARAMETERS = [
    (
        {"data": np.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        {"data": 15, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        np.array([[12, 14, 16], [18, 21, 24]]),
    ),  # ordinary np
    (
        {
            "data": np.ma.masked_array(
                np.arange(12).reshape(3, 2, 2),
                mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]], [[1, 0], [1, 1]]],
            ),
            "units": "degree_Celsius",
        },
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        "<=",
        np.ma.masked_array([[7, 6], [6, 4]]),
    ),  # masked np
    (
        {"data": da.arange(30).reshape(5, 2, 3), "units": "degree_Celsius"},
        {"data": 15, "units": "degree_Celsius", "standard_name": "air_temperature"},
        "<",
        np.array([[27, 24, 21], [18, 16, 14]]),
    ),  # ordinary da
    (
        {
            "data": da.ma.masked_array([1, 2, 3, 4], mask=[0, 0, 1, 0]).reshape(
                1, 1, 4
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">=",
        np.ma.masked_array([0, 0, 1, 2], mask=[0, 0, 1, 0]).reshape(1, 1, 4),
    ),  # masked da
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "kg"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        pytest.raises(ValueError),
    ),  # prepare assertion error
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "kg"},
        {"data": 7, "units": "kg", "standard_name": "air_temperature"},
        ">",
        pytest.raises(RuntimeError),
    ),  # prepare assertion error
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": 7, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        does_not_raise(),
    ),  # prepare assert
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": 7, "units": "K", "standard_name": "air_temperature"},
        ">",
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = "f_cube_tas, f_first_threshold, condition, expected"
fixtures = ["f_cube_tas", "f_first_threshold"]


@pytest.mark.parametrize(
    parameter_names, TEST_TEMPERATURE_SUM_PARAMETERS[:4], indirect=fixtures
)
def test_temperature_sum_call_func(f_cube_tas, f_first_threshold, condition, expected):
    index_function = idx_func.TemperatureSum(f_first_threshold, condition)
    call_func_test(index_function, f_cube_tas, expected)
    assert index_function.units == Unit("days")


@pytest.mark.parametrize(
    parameter_names, TEST_TEMPERATURE_SUM_PARAMETERS[:4], indirect=fixtures
)
def test_temperature_sum_lazy_func(f_cube_tas, f_first_threshold, condition, expected):
    index_function = idx_func.TemperatureSum(f_first_threshold, condition)
    lazy_func_test(index_function, f_cube_tas, expected)
    assert index_function.units == Unit("days")


@pytest.mark.parametrize(
    parameter_names, TEST_TEMPERATURE_SUM_PARAMETERS[4:], indirect=fixtures
)
def test_temperature_sum_prepare(f_cube_tas, f_first_threshold, condition, expected):
    index_function = idx_func.TemperatureSum(f_first_threshold, condition)
    cube_mapping = {"data": f_cube_tas}
    with expected:
        index_function.prepare(cube_mapping)
        assert index_function.units == "degC days"
        assert index_function.standard_name == f_cube_tas.standard_name


TEST_COUNT_JOINT_OCCURRENCES_PRECIPITATION_TEMPERATURE_PARAMETERS = [
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {
            "data": np.arange(12).reshape(2, 2, 3),
            "units": "mm day-1",
            "standard_name": "lwe_precipitation_rate",
        },
        {"data": 1, "units": "mm day-1", "standard_name": "lwe_precipitation_rate"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        ">=",
        np.array([[1, 2, 2], [2, 2, 2]]),
    ),  # ordinary np
    (
        {
            "data": np.ma.masked_array(
                np.arange(8).reshape(2, 2, 2), mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]]]
            ),
            "units": "degree_Celsius",
        },
        {
            "data": 0.5
            * np.ma.masked_array(
                np.arange(8).reshape(2, 2, 2), mask=[[[0, 0], [0, 0]], [[0, 0], [0, 0]]]
            ),
            "units": "mm day-1",
            "standard_name": "lwe_precipitation_rate",
        },
        {"data": 1, "units": "mm day-1", "standard_name": "lwe_precipitation_rate"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        ">=",
        np.ma.masked_array([[0, 0], [2, 1]]),
    ),  # masked np
    (
        {"data": da.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {
            "data": da.arange(12).reshape(2, 2, 3),
            "units": "mm day-1",
            "standard_name": "lwe_precipitation_rate",
        },
        {"data": 1, "units": "mm day-1", "standard_name": "lwe_precipitation_rate"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        ">=",
        np.array([[1, 2, 2], [2, 2, 2]]),
    ),  # ordinary da
    (
        {
            "data": da.ma.masked_array(
                np.arange(8).reshape(2, 2, 2), mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]]]
            ),
            "units": "degree_Celsius",
        },
        {
            "data": 0.5
            * da.ma.masked_array(
                np.arange(8).reshape(2, 2, 2), mask=[[[0, 0], [0, 0]], [[0, 0], [0, 0]]]
            ),
            "units": "mm day-1",
            "standard_name": "lwe_precipitation_rate",
        },
        {"data": 1, "units": "mm day-1", "standard_name": "lwe_precipitation_rate"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        ">=",
        np.ma.masked_array(data=[[0, 0], [2, 1]]),
    ),  # masked da
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {
            "data": np.arange(12).reshape(2, 2, 3),
            "units": "mm day-1",
            "standard_name": "lwe_precipitation_rate",
        },
        {"data": 1, "units": "mm day-1", "standard_name": "lwe_precipitation_rate"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        ">=",
        does_not_raise(),
    ),  # add_extra_coords do not raise
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "kg"},
        {
            "data": np.arange(12).reshape(2, 2, 3),
            "units": "mm day-1",
            "standard_name": "lwe_precipitation_rate",
        },
        {"data": 1, "units": "mm day-1", "standard_name": "lwe_precipitation_rate"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        ">=",
        pytest.raises(ValueError),
    ),  # prepare assertion error
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {
            "data": np.arange(12).reshape(2, 2, 3),
            "units": "mm day-1",
            "standard_name": "lwe_precipitation_rate",
        },
        {"data": 1, "units": "mm day-1", "standard_name": "lwe_precipitation_rate"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        ">=",
        does_not_raise(),
    ),  # prepare do not raise
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "K"},
        {
            "data": np.arange(12).reshape(2, 2, 3),
            "units": "mm day-1",
            "standard_name": "lwe_precipitation_rate",
        },
        {"data": 1, "units": "mm day-1", "standard_name": "lwe_precipitation_rate"},
        {"data": 0, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        ">=",
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = (
    "f_cube_tas, f_cube_pr, f_first_threshold, f_second_threshold, condition_tas, "
    + "condition_pr, expected"
)
fixtures = ["f_cube_tas", "f_cube_pr", "f_first_threshold", "f_second_threshold"]


@pytest.mark.parametrize(
    parameter_names,
    TEST_COUNT_JOINT_OCCURRENCES_PRECIPITATION_TEMPERATURE_PARAMETERS[:4],
    indirect=fixtures,
)
def test_count_joint_occurrences_precipitation_temperature_call_func(
    f_cube_tas,
    f_cube_pr,
    f_first_threshold,
    f_second_threshold,
    condition_tas,
    condition_pr,
    expected,
):
    index_function = idx_func.CountJointOccurrencesPrecipitationTemperature(
        f_first_threshold, f_second_threshold, condition_pr, condition_tas
    )
    cube_mapping = {"temp_data": f_cube_tas, "precip_data": f_cube_pr}
    call_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("1")


@pytest.mark.parametrize(
    parameter_names,
    TEST_COUNT_JOINT_OCCURRENCES_PRECIPITATION_TEMPERATURE_PARAMETERS[:4],
    indirect=fixtures,
)
def test_count_joint_occurrences_precipitation_temperature_lazy_func(
    f_cube_tas,
    f_cube_pr,
    f_first_threshold,
    f_second_threshold,
    condition_tas,
    condition_pr,
    expected,
):
    index_function = idx_func.CountJointOccurrencesPrecipitationTemperature(
        f_first_threshold, f_second_threshold, condition_pr, condition_tas
    )
    cube_mapping = {"temp_data": f_cube_tas, "precip_data": f_cube_pr}
    lazy_func_test(index_function, cube_mapping, expected)
    assert index_function.units == Unit("1")


@pytest.mark.parametrize(
    parameter_names,
    TEST_COUNT_JOINT_OCCURRENCES_PRECIPITATION_TEMPERATURE_PARAMETERS[4:5],
    indirect=fixtures,
)
def test_count_joint_occurrences_precipitation_temperature_add_extra_coords(
    f_cube_tas,
    f_cube_pr,
    f_first_threshold,
    f_second_threshold,
    condition_tas,
    condition_pr,
    expected,
):
    index_function = idx_func.CountJointOccurrencesPrecipitationTemperature(
        f_first_threshold, f_second_threshold, condition_pr, condition_tas
    )
    cube_mapping = {"temp_data": f_cube_tas, "precip_data": f_cube_pr}
    with expected:
        index_function.add_extra_coords(cube_mapping)


@pytest.mark.parametrize(
    parameter_names,
    TEST_COUNT_JOINT_OCCURRENCES_PRECIPITATION_TEMPERATURE_PARAMETERS[5:],
    indirect=fixtures,
)
def test_count_joint_occurrences_precipitation_temperature_prepare(
    f_cube_tas,
    f_cube_pr,
    f_first_threshold,
    f_second_threshold,
    condition_tas,
    condition_pr,
    expected,
):
    index_function = idx_func.CountJointOccurrencesPrecipitationTemperature(
        f_first_threshold, f_second_threshold, condition_pr, condition_tas
    )
    cube_mapping = {"temp_data": f_cube_tas, "precip_data": f_cube_pr}
    with expected:
        index_function.prepare(cube_mapping)
        assert f_cube_tas.units == index_function.mapping["temp_data"][0][0].units
        assert f_cube_pr.units == index_function.mapping["precip_data"][0][0].units


TEST_COUNT_JOINT_OCCURRENCES_TEMPERATURE_PARAMETERS = [
    (
        {"data": np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        {"data": 6, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "<",
        np.array([[0, 0, 0], [1, 1, 1]]),
    ),  # ordinary np
    (
        {
            "data": np.ma.masked_array(
                np.arange(8).reshape(2, 2, 2), mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]]]
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        {"data": 6, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "<",
        np.ma.masked_array([[0, 0], [0, 1]]),
    ),  # masked np
    (
        {"data": da.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        {"data": 6, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "<",
        np.array([[0, 0, 0], [1, 1, 1]]),
    ),  # ordinary da
    (
        {
            "data": da.ma.masked_array(
                np.arange(8).reshape(2, 2, 2), mask=[[[0, 0], [0, 0]], [[1, 1], [0, 1]]]
            ),
            "units": "degree_Celsius",
        },
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        {"data": 6, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "<",
        np.ma.masked_array([[0, 0], [0, 1]]),
    ),  # masked da
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {
            "data": 2,
            "units": "degree_Celsius",
            "standard_name": "air_temperature",
            "long_name": "threshold",
        },
        {
            "data": 6,
            "units": "degree_Celsius",
            "standard_name": "air_temperature",
            "long_name": "threshold",
        },
        ">",
        "<",
        pytest.raises(ValueError),
    ),  # add_extra_coord assertion error
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "kg"},
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        {"data": 6, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "<",
        pytest.raises(ValueError),
    ),  # prepare assertion error
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "degree_Celsius"},
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        {"data": 6, "units": "degree_Celsius", "standard_name": "air_temperature"},
        ">",
        "<",
        does_not_raise(),
    ),  # prepare do not raise
    (
        {"data": 275.15 + np.arange(12).reshape(2, 2, 3), "units": "K"},
        {"data": 2, "units": "degree_Celsius", "standard_name": "air_temperature"},
        {"data": 6, "units": "K", "standard_name": "air_temperature"},
        ">",
        "<",
        does_not_raise(),
    ),  # prepare do not raise
]


parameter_names = (
    "f_cube_tas, f_first_threshold, f_second_threshold, condition_low, condition_high, "
    + "expected"
)
fixtures = ["f_cube_tas", "f_first_threshold", "f_second_threshold"]


@pytest.mark.parametrize(
    parameter_names,
    TEST_COUNT_JOINT_OCCURRENCES_TEMPERATURE_PARAMETERS[:4],
    indirect=fixtures,
)
def test_count_joint_occurrences_temperature_call_func(
    f_cube_tas,
    f_first_threshold,
    f_second_threshold,
    condition_low,
    condition_high,
    expected,
):
    index_function = idx_func.CountJointOccurrencesTemperature(
        f_first_threshold, f_second_threshold, condition_low, condition_high
    )
    call_func_test(index_function, f_cube_tas, expected)
    assert index_function.units == Unit("1")


@pytest.mark.parametrize(
    parameter_names,
    TEST_COUNT_JOINT_OCCURRENCES_TEMPERATURE_PARAMETERS[:4],
    indirect=fixtures,
)
def test_count_joint_occurrences_temperature_lazy_func(
    f_cube_tas,
    f_first_threshold,
    f_second_threshold,
    condition_low,
    condition_high,
    expected,
):
    index_function = idx_func.CountJointOccurrencesTemperature(
        f_first_threshold, f_second_threshold, condition_low, condition_high
    )
    lazy_func_test(index_function, f_cube_tas, expected)
    assert index_function.units == Unit("1")


@pytest.mark.parametrize(
    parameter_names,
    TEST_COUNT_JOINT_OCCURRENCES_TEMPERATURE_PARAMETERS[4:5],
    indirect=fixtures,
)
def test_count_joint_occurrences_temperature_add_extra_coords(
    f_cube_tas,
    f_first_threshold,
    f_second_threshold,
    condition_low,
    condition_high,
    expected,
):
    index_function = idx_func.CountJointOccurrencesTemperature(
        f_first_threshold, f_second_threshold, condition_low, condition_high
    )
    cube_mapping = {"data": f_cube_tas}
    with expected:
        index_function.add_extra_coords(cube_mapping)


@pytest.mark.parametrize(
    parameter_names,
    TEST_COUNT_JOINT_OCCURRENCES_TEMPERATURE_PARAMETERS[5:],
    indirect=fixtures,
)
def test_count_joint_occurrences_temperature_prepare(
    f_cube_tas,
    f_first_threshold,
    f_second_threshold,
    condition_low,
    condition_high,
    expected,
):
    index_function = idx_func.CountJointOccurrencesTemperature(
        f_first_threshold, f_second_threshold, condition_low, condition_high
    )
    cube_mapping = {"data": f_cube_tas}
    with expected:
        index_function.prepare(cube_mapping)
        assert f_cube_tas.units == index_function.mapping["data"][0][0].units
        assert f_cube_tas.units == index_function.mapping["data"][1][0].units
