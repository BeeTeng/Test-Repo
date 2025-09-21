import pytest
import pandas as pd
from src.code_executor import execute_code

@pytest.fixture
def sample_dataframe():
    """
    Provides a sample DataFrame for testing.
    """
    return pd.DataFrame({
        'A': [1, 2, 3],
        'B': [4, 5, 6]
    })

def test_execute_code_success(sample_dataframe):
    """
    Tests that execute_code successfully runs a script and captures its output.
    """
    code = "print(df.shape)"
    output = execute_code(code, sample_dataframe)
    assert output.strip() == "(3, 2)"

def test_execute_code_with_error(sample_dataframe):
    """
    Tests that execute_code captures errors from the executed script.
    """
    code = "print(df['C'])"  # Column 'C' does not exist
    output = execute_code(code, sample_dataframe)
    assert "An error occurred" in output
    assert "KeyError" in output
