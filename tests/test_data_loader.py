import pytest
import pandas as pd
from src.data_loader import load_csv

def test_load_csv_success(tmp_path):
    """
    Tests that load_csv successfully loads a CSV file.
    """
    # Create a temporary directory and a dummy CSV file
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "data.csv"
    p.write_text("col1,col2\n1,2\n3,4")

    # Call the function with the path to the dummy file
    df = load_csv(str(p))

    # Assert that the returned object is a DataFrame
    assert isinstance(df, pd.DataFrame)
    # Assert that the DataFrame has the correct shape
    assert df.shape == (2, 2)
    # Assert that the column names are correct
    assert df.columns.tolist() == ["col1", "col2"]

def test_load_csv_file_not_found():
    """
    Tests that load_csv raises FileNotFoundError for a non-existent file.
    """
    # Use pytest.raises to assert that a FileNotFoundError is raised
    with pytest.raises(FileNotFoundError):
        load_csv("non_existent_file.csv")
