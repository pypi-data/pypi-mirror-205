import os
import pandas as pd
import random

def excel_processing(input_file_path, output_file_path):
    # Read the input Excel file
    input_file = pd.read_excel(input_file_path)

    # Square the numbers in the input file and add a random integer
    random_int = random.randint(1, 100)
    squared_and_random = input_file['Numbers'] ** 2 + random_int

    # Create a new DataFrame with the squared and random numbers
    output_file = pd.DataFrame({'New numbers': squared_and_random})

    # Write the output DataFrame to a new Excel file
    output_file.to_excel(output_file_path, index=False)

    # Return the path to the output Excel file
    return output_file_path

