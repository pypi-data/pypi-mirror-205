import pandas as pd


def reader(fileType: str, file_path: str, Oformat: str):
    """
    Read data from a file and return a Pandas DataFrame or a dictionary of records, depending on the specified output format.

    Args:
        fileType: A string representing the type of file to read. Valid options are 'json' and 'csv'.
        file_path: A string representing the path to the file to read.
        Oformat: A string representing the output format. Valid options are 'df' (for DataFrame) and 'dict'.

    Returns:
        A Pandas DataFrame if Oformat is 'df', or a dictionary of records if Oformat is 'dict'.

    Raises:
        None.

    Example usage:
        data = reader('json', 'data.json', 'dict')
    """

    if fileType == 'json':
        df = pd.read_json(file_path, encoding='utf-8')
        if Oformat == 'dict':
            data_dict = df.to_dict('records')
            return data_dict
        return df

    elif fileType == 'csv':
        df = pd.read_csv(file_path, encoding='ISO-8859-1')
        if Oformat == 'dict':
            data_dict = df.to_dict('records')
            return data_dict
        return df

    else:
        print(
            f'You Are Redirected To Default Format\nFormat Named {fileType} Doesnot exist here, You may again Check \nDoes {fileType} spelling is correct.')
