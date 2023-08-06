import pandas as pd
from robot.api.deco import keyword
from robot.api import logger


class FileOperations:

    ROBOT_LIBRARY_SCOPE = 'TEST CASE'
    ROBOT_LIBRARY_DOC_FORMAT = 'REST'

    def __init__(self):
        self.df = None

    @keyword(name="Create Dataframe from file")
    def create_dataframe_from_file(self, file_path: str, delimiter: str = ',', has_header: bool = True, width=None,
                                   encoding='ISO-8859-1',
                                   on_bad_lines='warn', skiprows=0, skipfooter=0):
        """
        Creates a Pandas DataFrame from a CSV, PSV, or fixed-width file.

        Parameters:
            file_path (str): The path to the input file.
            delimiter (str): The delimiter character used in the input file. Default is ','.
            has_header (bool): Whether the input file has headers. Default is True.
            width (list or tuple): A list or tuple of integers specifying the width of each fixed-width field.
                                  Required when reading a fixed-width file. Default is None.
            encoding (str): The encoding of the input file. Default is 'ISO-8859-1'.
            on_bad_lines (str): What to do with bad lines encountered in the input file.
                                Valid values are 'raise', 'warn', and 'skip'. Default is 'warn'.
            skiprows (int or list-like): Line numbers to skip (0-indexed) or number of lines to skip (int) at the start of the file. Default is 0.
            skipfooter (int): Number of lines to skip at the end of the file. Default is 0.

        Returns:
            pandas.DataFrame: The DataFrame created from the input file.

        Examples:
        | Create Dataframe from file | /path/to/file.csv |
        | Create Dataframe from file | /path/to/file.psv | delimiter='|', has_header=False |
        | Create Dataframe from file | /path/to/file.xlsx | has_header=False |
        | Create Dataframe from file | /path/to/file.fwf | width=[10, 20, 30] |
        | Create Dataframe from file | /path/to/file.csv | encoding='utf-8', on_bad_lines='raise' |

        """
        # Determine the file type based on the file extension
        file_ext = file_path.split('.')[-1].lower()
        if file_ext == 'csv':
            # Log info message
            logger.info(
                f"Step 1: Reading CSV file '{file_path}' with delimiter '{delimiter}' and encoding '{encoding}'")
            # Read CSV file into a DataFrame
            if has_header:
                df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, on_bad_lines=on_bad_lines,
                                 skiprows=skiprows, skipfooter=skipfooter)
            else:
                df = pd.read_csv(file_path, delimiter=delimiter, header=None, encoding=encoding,
                                 on_bad_lines=on_bad_lines,
                                 skiprows=skiprows, skipfooter=skipfooter)
        elif file_ext == 'psv':
            # Log info message
            logger.info(
                f"Step 1: Reading PSV file '{file_path}' with delimiter '{delimiter}' and encoding '{encoding}'")
            # Read PSV file into a DataFrame
            if has_header:
                df = pd.read_csv(file_path, delimiter='|', encoding=encoding, on_bad_lines=on_bad_lines,
                                 skiprows=skiprows, skipfooter=skipfooter)
            else:
                df = pd.read_csv(file_path, delimiter='|', header=None, encoding=encoding,
                                 on_bad_lines=on_bad_lines,
                                 skiprows=skiprows, skipfooter=skipfooter)

        elif file_ext == 'xlsx':
            # Log info message
            logger.info(f"Step 1: Reading XLSX file '{file_path}'")
            # Read XLSX file into a DataFrame
            if has_header:
                df = pd.read_excel(file_path, skiprows=skiprows, skipfooter=skipfooter)
            else:
                df = pd.read_excel(file_path, header=None, skiprows=skiprows, skipfooter=skipfooter)

        elif file_ext == 'fwf':
            # Log info message
            logger.info(f"Step 1: Reading FWF file '{file_path}' with column width {width}")
            # Read FWF file into a DataFrame
            df = pd.read_fwf(file_path, widths=width, header=None, encoding=encoding, on_bad_lines=on_bad_lines,
                             skiprows=skiprows, skipfooter=skipfooter)

        else:
            # Log error message
            logger.error(f"File type '{file_ext}' not supported. Please provide a CSV, PSV, XLSX, or FWF file.")
            # Raise exception
            raise ValueError(f"File type '{file_ext}' not supported. Please provide a CSV, PSV, XLSX, or FWF file.")

        # Log info message
        logger.info(f"Step 2: DataFrame created with {len(df)} rows and {len(df.columns)} columns")
        # Return the DataFrame
        return df
