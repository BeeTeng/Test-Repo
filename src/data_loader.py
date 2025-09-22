import pandas as pd

def load_csv(file_path: str) -> pd.DataFrame:
    """
    Loads data from a CSV file into a pandas DataFrame.

    Args:
        file_path: The path to the CSV file.

    Returns:
        A pandas DataFrame containing the data from the CSV file.

    Raises:
        FileNotFoundError: If the file is not found at the specified path.
        Exception: For other potential errors during file reading.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file at {file_path} was not found.")
        raise
    except Exception as e:
        print(f"An error occurred while reading the CSV file: {e}")
        raise
