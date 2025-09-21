import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# It is assumed that the user has a .env file with the OPENAI_API_KEY.
# If the API key is not set, the code will raise an error.
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OPENAI_API_KEY environment variable not found. Please create a .env file with your API key.")

def get_relevant_column(question: str, columns: list[str]) -> str:
    """
    Identifies the most relevant column from a list of columns based on a user's question.

    Args:
        question: The user's question.
        columns: A list of column names in the DataFrame.

    Returns:
        The name of the most relevant column.
    """
    prompt = f"""
    Given the user's question: "{question}"
    And the list of available columns: {columns}

    Which column is the most relevant to answer the question?
    Please return only the name of the column, and nothing else.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that helps with data analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        # The response from the API is a Choice object.
        # The content is in response.choices[0].message.content
        relevant_column = response.choices[0].message.content.strip()

        # Basic validation to ensure the returned column is in the list
        if relevant_column in columns:
            return relevant_column
        else:
            # If the model returns something unexpected, we could fall back to a simpler matching or raise an error.
            # For now, we will raise an error.
            raise ValueError(f"The model returned a column ('{relevant_column}') that is not in the list of available columns.")

    except Exception as e:
        print(f"An error occurred while communicating with the OpenAI API: {e}")
        raise

def generate_analysis_code(question: str, df_info: dict, relevant_column: str) -> str:
    """
    Generates Python code to perform data analysis based on a user's question.

    Args:
        question: The user's question.
        df_info: A dictionary containing information about the DataFrame (e.g., columns, dtypes).
        relevant_column: The most relevant column for the analysis.

    Returns:
        A string containing the generated Python code.
    """
    prompt = f"""
    You are a data analyst. Your task is to write a Python script to answer a user's question about a dataset.
    The data is in a pandas DataFrame called `df`.

    User's question: "{question}"

    The most relevant column for this question is: "{relevant_column}"

    DataFrame Information:
    - Columns: {df_info['columns']}
    - Data types: {df_info['dtypes']}

    Please write a Python script that uses the `df` DataFrame to answer the question.
    The script should perform the analysis and print the result in a user-friendly format.

    Important:
    - The script should not include any code to load the data. The `df` DataFrame is already available.
    - The script should be self-contained and ready to execute.
    - Only return the Python code, without any explanations or markdown formatting.
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates Python code for data analysis."},
                {"role": "user", "content": prompt}
            ],
            temperature=0,
        )

        generated_code = response.choices[0].message.content.strip()

        # Sometimes the model might wrap the code in ```python ... ```.
        # We can remove that.
        if generated_code.startswith("```python"):
            generated_code = generated_code[9:]
            if generated_code.endswith("```"):
                generated_code = generated_code[:-3]

        return generated_code.strip()

    except Exception as e:
        print(f"An error occurred while communicating with the OpenAI API: {e}")
        raise
