from pathlib import Path
from agno.agent import Agent
from agno.tools.csv_toolkit import CsvTools
from config import Config
import pandas as pd
import re

config = Config()

def normalize_filename(filename):
    name, ext = filename.rsplit('.', 1)
    normalized = re.sub(r'[^A-Za-z0-9]', '_', name)
    return f"{normalized}.{ext}"

def clean_csv_file(file_path):
    """Clean CSV file by removing empty columns and handling data formatting"""
    try:
        encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
        df = None
        for encoding in encodings:
            try:
                df = pd.read_csv(file_path, encoding=encoding)
                print(f"Successfully read {file_path} with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if df is None:
            print(f"Could not read {file_path} with any encoding")
            return
        
        df = df.dropna(axis=1, how='all')
        df = df.replace('—', pd.NA)
        
        df.to_csv(file_path, index=False, encoding='utf-8')
        print(f"Cleaned CSV file: {file_path}")
        
    except Exception as e:
        print(f"Error cleaning {file_path}: {e}")

# Clean all CSV files first
data_folder = Path(config.data_folder)
for csv_file in data_folder.glob("*.csv"):
    clean_csv_file(csv_file)
    # Also normalize filenames
    normalized_name = normalize_filename(csv_file.name)
    if csv_file.name != normalized_name:
        new_path = csv_file.with_name(normalized_name)
        csv_file.rename(new_path)


data_tables = config.get_data_tables()
model = config.get_model()
db = config.db

agent_datatable = Agent(
    name="DataTableAgent",
    tools=[CsvTools(csvs=data_tables)],
    model=model,
    db=db,
    instructions=[
        "First always get the list of files",
        "Then check which file you need to use based on the file names and the question",
        "Then check the columns in the selected file. The first row is the column names.",
        "Then check the first two rows of the selected file",
        "Then change all of the values equal to '—' to nan.",
        "Then remove ',' from all of the values of the columns",
        "Then run the query to answer the question",
        "Always wrap column names with double quotes if they contain spaces or special characters",
        "Remember to escape the quotes in the JSON string (use \")",
        "Use single quotes for string values",
        "Don't return the errors or logs or intermediate results from the tool calls."
    ],
    add_history_to_context=True,
    num_history_runs=3,
    add_datetime_to_context=True, 
    markdown=True,
    exponential_backoff=True
)

if __name__ == "__main__":
    print("Please run from the main.py file.")