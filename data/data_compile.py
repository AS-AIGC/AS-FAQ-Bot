import pandas as pd
import os

data_folder = 'source'  # Folder where the source CSV files are located
dataframes = []  # List to store dataframes

try:
    # Iterate through all files in the data_folder
    for filename in os.listdir(data_folder):
        # Check if the file is a CSV file
        if filename.endswith('.csv'):
            filepath = os.path.join(data_folder, filename)  # Get the full file path
            try:
                df = pd.read_csv(filepath)  # Read the CSV file into a dataframe
                dataframes.append(df)  # Append the dataframe to the list
            except pd.errors.EmptyDataError:
                print(f"Warning: {filename} is empty and has been skipped.")
            except pd.errors.ParserError:
                print(f"Error: {filename} is not a valid CSV file and has been skipped.")
            except Exception as e:
                print(f"An unexpected error occurred while reading {filename}: {e}")

    # Combine all dataframes into a single dataframe
    combined_df = pd.concat(dataframes, ignore_index=True)
    # Drop the 'group' column from the combined dataframe
    combined_df = combined_df.drop('group', axis=1)

    # Write the combined data to a text file
    with open('AS-ALL.txt', 'w') as f:
        for index, row in combined_df.iterrows():
            for column_name, cell_value in row.items():
                # Replace any newline characters in the cell value
                cell_value = str(cell_value).replace('\n', '')
                f.write(f"{column_name}: {cell_value}\n")  # Write column name and cell value to the file
            f.write("\n")  # Print a blank line
            f.write("\n")  # Print another blank line

except FileNotFoundError:
    print(f"Error: The directory '{data_folder}' does not exist.")
except PermissionError:
    print("Error: You do not have permission to read/write files in the specified directory.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")

