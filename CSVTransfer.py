import pandas as pd

def excel_to_csv(input_filepath, output_filepath, columns, start_row, end_row, sheet_name):
    """
    Converts specific columns and rows from an Excel file to a CSV file.
    
    Parameters:
    - input_filepath (str): Path to the input Excel file.
    - output_filepath (str): Path to the output CSV file.
    - columns (list): List of column names or column indices to be included in the CSV.
    - start_row (int): Row number to start reading data (0-indexed).
    - sheet_name (str): Name of the sheet to read data from.
    """
    nrows_to_read = end_row - start_row + 1
    # Read the Excel file from a specific sheet
    df = pd.read_excel(input_filepath, skiprows=lambda x: x in range(start_from_row),nrows=nrows_to_read, usecols=columns, sheet_name=sheet_name, engine='openpyxl')
    df.columns = ['Group Name','Group Email']  # <- REPLACE WITH YOUR COLUMN NAMES HERE
    print(df)

    # Save the data to a CSV file
    df.to_csv(output_filepath, index=False)

if __name__ == "__main__":
    root_path = r'INPUT YOUR ROOT PATH HERE'
    input_file = root_path + '\\inputfile.xlsx'
    output_file = root_path + "\\output.csv"
    desired_columns = [1,2]  # <- REPLACE WITH YOUR COLUMN HERE 0-STARTED INDEX
    start_from_row = 5 # <- REPLACE WITH YOUR START ROW HERE 0-STARTED INDEX
    end_at_row = 45 # <- REPLACE WITHYOUR END ROW HERE 0-STARTED INDEX
    desired_sheet_name = "INPUT YOUR SHEET NAME HERE"  
    print(output_file)

    excel_to_csv(input_file, output_file, desired_columns, start_from_row, end_at_row, desired_sheet_name)
