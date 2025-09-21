import io
import pandas as pd
from contextlib import redirect_stdout

def execute_code(code: str, df: pd.DataFrame) -> str:
    """
    Executes a string of Python code in a controlled environment.

    Args:
        code: The Python code to execute, as a string.
        df: The pandas DataFrame to be used in the code. The code can access it as `df`.

    Returns:
        The captured standard output from the executed code.
    """
    # Create a string buffer to capture the output
    buffer = io.StringIO()

    # The environment in which the code will be executed.
    # We pass the DataFrame 'df' to this environment.
    execution_globals = {'df': df, 'pd': pd}

    try:
        # Redirect stdout to the buffer
        with redirect_stdout(buffer):
            # Execute the code
            exec(code, execution_globals)

        # Get the content of the buffer
        output = buffer.getvalue()
        return output

    except Exception as e:
        # If there is an error in the generated code, we capture it.
        return f"An error occurred while executing the generated code:\n{type(e).__name__}: {e}"
    finally:
        # It's good practice to close the buffer, though it's not strictly necessary for StringIO.
        buffer.close()
