
import pandas as pd


def writter(file_path: str, fileType: str, datas: list):
    """
    Writes the provided data to the specified file in either JSON or CSV format.

    Args:
        file_path (str): The path to the file to be written to.
        fileType (str): The type of file to write. Must be either "json" or "csv".
        datas (list): The data to be written to the file. Must be a list of dictionaries.

    Returns:
        int: -1 on failure, 0 on success.

    Raises:
        FileNotFoundError: If the specified file does not exist.

    """
    if fileType == 'json':

        # Load the existing JSON data into a DataFrame
        try:
            existing_df = pd.read_json(file_path, encoding='utf-8')
        except:
            print("CHECK IF THIS FILE EXIST & Have atlest []")
            return -1
        # Create a new DataFrame from the data to append
        new_data = datas
        new_df = pd.DataFrame(new_data, index=[0])

        # Append the new DataFrame to the existing one
        combined_df = pd.concat([existing_df, new_df], ignore_index=True)

        # Write the combined DataFrame back to the JSON file
        combined_df.to_json(file_path, orient='records')

        print(
            f"GulistanDB:\t\033[1;32m\n{new_df}\nINSERTED successfully!\033[0m")

    elif fileType == 'csv':
        with open(file_path, 'a') as f:
            f.write('\n')
            for i, data in enumerate(datas):
                f.write(data)
                if i == len(datas)-1:
                    break
                    # continue
                else:
                    f.write(',')
        print("INSERTED CSV")

    else:
        print("SOMETHING WRONG IN FILE TYPE")
