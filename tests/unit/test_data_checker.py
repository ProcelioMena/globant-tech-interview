from processors.data_checker import DataChecker


def test_data_checker_check(data_checker_input_check, data_checker_output_check):
    """Test data_checker_check."""
    checker = DataChecker('test')
    schema = {"col1": int, "col2": int, "col3": str}
    actual = checker.check(data_checker_input_check, schema)
    expected = data_checker_output_check
    assert actual.equals(expected)
