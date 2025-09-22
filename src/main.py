import argparse
import pandas as pd
from data_loader import load_csv
from llm_handler import get_relevant_column, generate_analysis_code
from code_executor import execute_code

def main():
    """
    Main function to run the data analysis application.
    """
    parser = argparse.ArgumentParser(description="Data analysis application powered by AI.")
    parser.add_argument("file_path", help="The path to the CSV file.")
    parser.add_argument("question", help="The question you want to ask about the data.")

    args = parser.parse_args()

    print(f"Loading data from: {args.file_path}")

    try:
        df = load_csv(args.file_path)
        print("Data loaded successfully.")

        print(f"\nUser question: {args.question}")

        columns = df.columns.tolist()
        print(f"Identifying the most relevant column for your question...")

        relevant_column = get_relevant_column(args.question, columns)
        print(f"Most relevant column identified: {relevant_column}")

        print("\nGenerating Python code for analysis...")

        df_info = {
            "columns": df.columns.tolist(),
            "dtypes": {col: str(df[col].dtype) for col in df.columns},
        }

        generated_code = generate_analysis_code(args.question, df_info, relevant_column)

        print("\nGenerated Python code:")
        print("-----------------------")
        print(generated_code)
        print("-----------------------")

        print("\nExecuting generated code...")

        output = execute_code(generated_code, df)

        print("\nAnalysis Result:")
        print("----------------")
        print(output)
        print("----------------")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
