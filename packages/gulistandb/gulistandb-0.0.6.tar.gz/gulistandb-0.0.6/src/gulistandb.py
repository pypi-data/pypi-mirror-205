import os
from editor import fileInit
from reader import reader
from writter import writter


SUPPORTED_DATA_TYPES = ['csv',   'json']


class Table:

    def __init__(self, tableName: str, *column, **fileType: str) -> None:
        """
    Initialize a new table with the specified name, columns and file type.

    Args:
        tableName: A string representing the name of the table to create.
        column: A variable-length argument list of strings representing the names of the columns to create.
        fileType: Keyword arguments specifying the file type to use and any other options. Valid options are 'csv'.

    Returns:
        None.

    Raises:
        None.

    Example usage:
        t = Table('users', 'id', 'name', 'email', fileType='csv')
    """

        self.TableName = tableName
        self.column = column
        self.__isCalled = False
        # File Type, Default File Type Csv
        self.fileType = fileType.get('fileType', 'csv').lower() if fileType.get(
            'fileType', 'csv') in SUPPORTED_DATA_TYPES else 'csv'

        self.folder_path = os.path.join(
            os.getcwd(), "Data")
        self.file_path = f'{os.path.join(os.getcwd(), "Data")}/{self.TableName}.{self.fileType}'

        print(
            f"GulistanDB:\t\033[1;32mTable initialized successfully!\n{self.file_path}\033[0m")
        if not os.path.exists(self.folder_path):
            self.__commit()
            return None
        print("ReInitilized")

    def __commit(self):
        self.file_path = f'{os.path.join(os.getcwd(), "Data")}/{self.TableName}.{self.fileType}'
        try:
            if not os.path.exists(self.folder_path):
                os.makedirs(self.folder_path)
            fileInit(self.fileType, self.file_path, self.column)
        except FileExistsError:
            print(
                f"GulistanDB:\t\033[1;31mThis file name already exists. Please try a different name.\033[0m")
            return -1

        print(
            f"GulistanDB:\t\033[1;33m{self.TableName} created successfully!\n{self.file_path}\033[0m")

    def rename(self, newName: str, **fileType: str):
        """
    Rename the table to a new name and/or a new file type.

    Args:
        newName: A string representing the new name of the table.
        fileType: Keyword arguments specifying the file type to use and any other options. Valid options are 'csv'.

    Returns:
        -1 if the new file name already exists, otherwise None.

    Raises:
        None.

    Example usage:
        t = Table('users', 'id', 'name', 'email', fileType='csv')
        t.rename('guests', fileType='json')
    """

        self.fileType = fileType.get('fileType', self.fileType)
        print(fileType)
        post_file_path = f"{self.folder_path}/{newName}.{fileType}"

        if os.path.exists(post_file_path):
            print(
                f"GulistanDB:\t\033[1;31mThis file name already exists. Please try a different name.\033[0m")
            return -1
        self.drop()
        self.TableName = newName
        # if fileType:
        #     self.fileType = fileType.get('fileType', csv)
        self.__commit()
        print(
            f"GulistanDB:\t\033[1;33mFile Name REPLACED successfully!\n{self.file_path}\033[0m")

    def drop(self):
        """
    Deletes the file containing the table data, if it exists.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.

    Example usage:
        t = Table('users', 'id', 'name', 'email', fileType='csv')
        t.drop()
    """
        if os.path.exists(self.file_path):
            try:
                os.unlink(self.file_path)
                print(
                    f"GulistanDB:\t\033[1;31m {self.file_path}\n has been deleted.\033[0m")

            except PermissionError as e:
                print(f"Failed to delete {self.file_path}: {e}")
            except Exception as e:
                print(
                    f"An error occurred while deleting {self.file_path}: {e}")
        else:
            print(
                f"GulistanDB:\t\033[1;31m The file {self.file_path} does not exist.\033[0m")

    def read(self, Oformat='default'):

        return reader(self.fileType, self.file_path, Oformat)

    def get(self):
        """
    Read the table data from the file and return it as a string.

    Args:
        None.

    Returns:
        A string containing the table data.

    Raises:
        None.

    Example usage:
        t = Table('users', 'id', 'name', 'email', fileType='csv')
        data = t.get()
    """

        with open(self.file_path, 'r') as file:
            data = file.read()
            return (data)

    def clear(self):
        fileInit(self.fileType, self.file_path, self.column)
        return 0

    def insert(self, *datas):
        """
    Inserts new data into the table file.

    Args:
        *datas: Variable-length argument list of data rows to insert. Each row should be provided as a tuple of values.

    Returns:
        A string indicating whether the insertion was successful or not.

    Raises:
        None.

    Example usage:
        t = Table('users', 'id', 'name', 'email', fileType='csv')
        t.insert(('1', 'John Doe', 'john.doe@example.com') ('2', 'Jane Smith', 'jane.smith@example.com'))
    """
        print(datas)
        if len(datas[0]) == len(self.column) and self.fileType == 'json':

            writter(self.file_path, self.fileType, datas)
            return 'SUCCESSED'
        elif len(datas) == len(self.column) and self.fileType == 'csv':
            writter(self.file_path, self.fileType, datas)

        else:
            print(
                f"GulistandDB:\t\033[1;31mPlease provide input data that is similar in quantity and order to the columns in your table.\nYour table has {len(self.column)} columns, but you provided {len(datas)} columns.\033[0m")

# NOT IMPLEMENTED YET
    def __update(self, _primary_id, content):
        """ UPDATE """
        pass

# NOT IMPLEMENTED YET
    def __delete(self, _primary_id):
        """ DELETE  """
        pass
