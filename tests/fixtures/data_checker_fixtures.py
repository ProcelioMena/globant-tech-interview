from pandas import DataFrame
from pytest import fixture


@fixture
def data_checker_input_check() -> DataFrame:
    return DataFrame(
        {
            "col1": ["1", "2", "3"],
            "col2": [4, None, 6],
            "col3": ["7", "8", "9"],
        }
    )


@fixture
def data_checker_output_check() -> DataFrame:
    return DataFrame(
        {
            "col1": [1, 3],
            "col2": [4, 6],
            "col3": ["7", "9"],
        }
    )
