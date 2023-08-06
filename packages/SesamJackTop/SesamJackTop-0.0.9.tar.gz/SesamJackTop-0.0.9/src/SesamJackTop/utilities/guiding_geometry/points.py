"""     This module is to say hello to the user     """

import openpyxl

def read_points(filename, sheet_name):
    # Load the Excel file
    wb = openpyxl.load_workbook(filename)

    # Select the sheet you want to read data from
    ws = wb[sheet_name]

    # Read data from the sheet
    data = []
    for row in ws.iter_rows(min_row=2, max_col=4, values_only=True):
        # Extract data from the first four columns
        col1, col2, col3, col4 = row
        # Add the data to a list
        data.append((col1, col2, col3, col4))

    return data


