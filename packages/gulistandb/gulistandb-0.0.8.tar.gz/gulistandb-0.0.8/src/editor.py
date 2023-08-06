def fileInit(file_type: str, file_path: str, columns: tuple):
    """ 
        Create a new file of the specified type if it doesn't exist, and write a header row if the file is a CSV.

    Args:
        file_type: A string representing the type of file to create. Valid options are 'json' and 'csv'.
        file_path: A string representing the path to the file to create.
        columns: A list of strings representing the CSV column names to write to the file.

    Returns:
        None.

    Raises:
        None.

    Example usage:
        fileInit('csv', 'data.csv', ['Name', 'Email', 'Phone'])
    """
    if file_type == 'json':
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write('[]')

    elif file_type == 'xlsv':
        pass
    else:
        with open(file_path, 'w', encoding='utf-8') as f:
            for i, key in enumerate(columns):
                f.write(key)
                if i == len(columns)-1:
                    break

                else:
                    f.write(',')
