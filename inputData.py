import pandas as pd

# Replace 'data.xlsx' with the actual path to your Excel file
excel_file = pd.ExcelFile('data.xlsx')

# Assuming the first sheet in the Excel file contains the data
sheet_name = excel_file.sheet_names[0]

# Read the first column as a list
df = pd.read_excel(excel_file, sheet_name=sheet_name)
first_column_values = df.iloc[:, 0].tolist()

print(first_column_values)