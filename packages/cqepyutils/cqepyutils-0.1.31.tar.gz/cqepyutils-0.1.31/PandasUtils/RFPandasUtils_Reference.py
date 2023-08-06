import pandas as pd
import numpy as np
from robot.api import logger
from robot.api.deco import keyword


import pandas as pd
import numpy as np
from robot.api import logger
from robot.api.deco import keyword


@keyword(name="Create Dataframe from file")
def create_dataframe_from_file(file_path, delimiter=',', has_header=True, width=None, encoding='ISO-8859-1', on_bad_lines='warn', skiprows=0, skipfooter=0):
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
        logger.info(f"Step 1: Reading CSV file '{file_path}' with delimiter '{delimiter}' and encoding '{encoding}'")
        # Read CSV file into a DataFrame
        if has_header:
            df = pd.read_csv(file_path, delimiter=delimiter, encoding=encoding, on_bad_lines=on_bad_lines, skiprows=skiprows, skipfooter=skipfooter)
        else:
            df = pd.read_csv(file_path, delimiter=delimiter, header=None, encoding=encoding, on_bad_lines=on_bad_lines, skiprows=skiprows, skipfooter=skipfooter)
    elif file_ext == 'psv':
        # Log info message
        logger.info(f"Step 1: Reading PSV file '{file_path}' with delimiter '|'")
        # Read PSV file into a DataFrame
        if has_header:
            df = pd.read_csv(file_path, delimiter='|', encoding=encoding, on_bad_lines=on_bad_lines, skiprows=skiprows, skipfooter=skipfooter)
        else:
            df = pd.read_csv(file_path, delimiter='|', header=None, encoding=encoding, on_bad_lines=on_bad_lines, skiprows=skiprows, skipfooter=skipfooter)
    elif file_ext == 'xlsx':
        # Log info message
        logger.info(f"Step 1: Reading Excel file '{file_path}'")
        # Read Excel file into a DataFrame
        if has_header:
            df = pd.read_excel(file_path, skiprows=skiprows, skipfooter=skipfooter)
        else:
            df = pd.read_excel(file_path, header=None, skiprows=skiprows, skipfooter=skipfooter)
    elif file_ext == 'fwf':
        # Log info message
        logger.info(f"Step 1: Reading fixed-width file '{file_path}' with width {width}")
        # Read fixed-width file into a DataFrame
        df = pd.read_fwf(file_path, widths=width, header=None, encoding=encoding, on_bad_lines=on_bad_lines,
                         skiprows=skiprows, skipfooter=skipfooter)
    else:
        # Log error message and raise exception
        logger.error(
            f"Error: Unsupported file type '{file_ext}'. Supported file types are 'csv', 'psv', 'xlsx', and 'fwf'.")
        raise Exception(f"Unsupported file type '{file_ext}'")

    # Log info message
    logger.info(f"Step 2: DataFrame created with {df.shape[0]} rows and {df.shape[1]} columns")
    # Return the DataFrame
    return df


# @keyword(name="Create Dataframe from file")
# def create_dataframe_from_file(file_path, delimiter=',', has_header=True, skiprows=None, skipfooter=0, width=None):
#     """
#     Creates a Pandas DataFrame from a CSV, PSV, FWF, or Excel file.
#
#     Parameters:
#         file_path (str): The path to the input file.
#         delimiter (str): The delimiter character used in the input file. Default is ','.
#         has_header (bool): Whether the input file has headers. Default is True.
#         skiprows (int or list-like): Line numbers to skip (0-indexed). Default is None.
#         skipfooter (int): Number of lines at bottom of file to skip. Default is None.
#         width (int or list-like): Width of each fixed-width field. No default.
#
#     Returns:
#         pandas.DataFrame: The DataFrame created from the input file.
#
#     Examples:
#     | Create Dataframe from file | /path/to/file.csv |
#     | Create Dataframe from file | /path/to/file.psv | delimiter='|', has_header=False |
#     | Create Dataframe from file | /path/to/file.xlsx | has_header=False |
#     | Create Dataframe from file | /path/to/file.fwf | has_header=False, width=None |
#     | Create Dataframe from file | /path/to/file.txt | delimiter='\\t', has_header=False, width=[10, 15, 20], skiprows=2 |
#
#     """
#     # Determine the file type based on the file extension
#     file_ext = file_path.split('.')[-1].lower()
#     if file_ext == 'csv':
#         # Log info message
#         logger.info(f"Step 1: Reading CSV file '{file_path}' with delimiter '{delimiter}'")
#         # Read CSV file into a DataFrame
#         if has_header:
#             df = pd.read_csv(file_path, delimiter=delimiter, skiprows=skiprows, skipfooter=skipfooter)
#         else:
#             df = pd.read_csv(file_path, delimiter=delimiter, header=None, skiprows=skiprows, skipfooter=skipfooter)
#     elif file_ext == 'psv':
#         # Log info message
#         logger.info(f"Step 1: Reading PSV file '{file_path}' with delimiter '|'")
#         # Read PSV file into a DataFrame
#         if has_header:
#             df = pd.read_csv(file_path, delimiter='|', skiprows=skiprows, skipfooter=skipfooter)
#         else:
#             df = pd.read_csv(file_path, delimiter='|', header=None, skiprows=skiprows, skipfooter=skipfooter)
#     elif file_ext == 'xlsx':
#         # Log info message
#         logger.info(f"Step 1: Reading Excel file '{file_path}'")
#         # Read Excel file into a DataFrame
#         if has_header:
#             df = pd.read_excel(file_path, skiprows=skiprows, skipfooter=skipfooter)
#         else:
#             df = pd.read_excel(file_path, header=None, skiprows=skiprows, skipfooter=skipfooter)
#     elif file_ext == 'fwf':
#         # Log info message
#         logger.info(f"Step 1: Reading FWF file '{file_path}'")
#         # Read FWF file into a DataFrame
#         if has_header:
#             df = pd.read_fwf(file_path, skiprows=skiprows, skipfooter=skipfooter)
#         else:
#             df = pd.read_fwf(file_path, header=None, skiprows=skiprows, skipfooter=skipfooter,widths=width)
#     else:
#         raise ValueError("Unsupported file type.")
#
#     # Log success message
#     logger.info(f"Step 2: DataFrame created with shape {df.shape}")
#
#     return df

# import pandas as pd
# import numpy as np
# from robot.api import logger
# from robot.api.deco import keyword


# import pandas as pd
# import numpy as np
# from robot.api import logger
# from robot.api.deco import keyword
#
#
# @keyword(name="Create Dataframe from file")
# def create_dataframe_from_file(file_path, delimiter=',', has_header=True):
#     """
#     Creates a Pandas DataFrame from a CSV or PSV file.
#
#     Parameters:
#         file_path (str): The path to the input file.
#         delimiter (str): The delimiter character used in the input file. Default is ','.
#         has_header (bool): Whether the input file has headers. Default is True.
#
#     Returns:
#         pandas.DataFrame: The DataFrame created from the input file.
#
#     Examples:
#     | Create Dataframe from file | /path/to/file.csv |
#     | Create Dataframe from file | /path/to/file.psv | delimiter='|', has_header=False |
#     | Create Dataframe from file | /path/to/file.xlsx | has_header=True |
#     """
#     # Determine the file type based on the file extension
#     file_ext = file_path.split('.')[-1].lower()
#     if file_ext == 'csv':
#         # Log info message
#         logger.info(f"Step 1: Reading CSV file '{file_path}' with delimiter '{delimiter}'")
#         # Read CSV file into a DataFrame
#         if has_header:
#             df = pd.read_csv(file_path, delimiter=delimiter)
#         else:
#             df = pd.read_csv(file_path, delimiter=delimiter, header=None)
#     elif file_ext == 'psv':
#         # Log info message
#         logger.info(f"Step 1: Reading PSV file '{file_path}' with delimiter '|'")
#         # Read PSV file into a DataFrame
#         if has_header:
#             df = pd.read_csv(file_path, delimiter='|')
#         else:
#             df = pd.read_csv(file_path, delimiter='|', header=None)
#     elif file_ext == 'xlsx' or file_ext == 'xls':
#         # Log info message
#         logger.info(f"Step 1: Reading Excel file '{file_path}'")
#         # Read Excel file into a DataFrame
#         if has_header:
#             df = pd.read_excel(file_path)
#         else:
#             df = pd.read_excel(file_path, header=None)
#     else:
#         raise ValueError("Unsupported file type.")
#
#     # Log success message
#     logger.info(f"Step 2: DataFrame created with shape {df.shape}")
#
#     return df

# **************
# @keyword(name="Create Dataframe from file")
# def create_dataframe_from_file(file_path, delimiter=',', widths=None, has_header=True, skiprows=None, skipfooter=None):
#     """
#     Creates a Pandas DataFrame from a CSV, PSV, or fixed width file.
#
#     Parameters:
#         file_path (str): The path to the input file.
#         delimiter (str): The delimiter character used in the input file. Default is ','.
#         widths (list of int): The field widths for each column in the input file. If None, calculate the field widths. Default is None.
#         has_header (bool): Whether the input file has headers. Default is True.
#         skiprows (list of int): Line numbers to skip at the start of the file.
#         skipfooter (int): Number of lines to skip at the end of the file.
#
#     Returns:
#         pandas.DataFrame: The DataFrame created from the input file.
#
#     Examples:
#     | Create Dataframe from file | /path/to/file.csv |
#     | Create Dataframe from file | /path/to/file.psv | delimiter='|' |
#     | Create Dataframe from file | /path/to/file.txt | widths=[10, 5, 8, 10], has_header=False, skiprows=[0, 1], skipfooter=1 |
#     | Create Dataframe from file | /path/to/file.dat | delimiter=' ' | widths=None, skipfooter=2 |
#     | Create Dataframe from file | /path/to/file.xlsx |
#
#     """
#     # Determine the file type based on the file extension
#     file_ext = file_path.split('.')[-1].lower()
#     if file_ext == 'csv':
#         # Log info message
#         logger.info(f"Step 1: Reading CSV file '{file_path}' with delimiter '{delimiter}'")
#         # Read CSV file into a DataFrame
#         if has_header:
#             df = pd.read_csv(file_path, delimiter=delimiter)
#         else:
#             df = pd.read_csv(file_path, delimiter=delimiter, header=None)
#     elif file_ext == 'psv':
#         # Log info message
#         logger.info(f"Step 1: Reading PSV file '{file_path}' with delimiter '|'")
#         # Read PSV file into a DataFrame
#         if has_header:
#             df = pd.read_csv(file_path, delimiter='|', skiprows=skiprows, skipfooter=skipfooter)
#         else:
#             df = pd.read_csv(file_path, delimiter='|', header=None, skiprows=skiprows, skipfooter=skipfooter)
#     elif file_ext == 'txt' or file_ext == 'dat':
#         if widths is None:
#             # Calculate field widths
#             logger.info(f"Step 1: Calculating field widths for fixed width file '{file_path}'")
#             with open(file_path, 'r') as f:
#                 # Read the first line of the file to determine the number of columns
#                 num_cols = len(f.readline().strip().split(delimiter))
#                 # Calculate the width of each column by dividing the width of the file by the number of columns
#                 width = int(f.tell() / num_cols)
#                 # Set the widths parameter to a list of equal width integers
#                 widths = [width] * num_cols
#                 logger.info(f"Calculated widths: {widths}")
#         else:
#             logger.info(f"Step 1: Reading fixed width file '{file_path}' with widths {widths}")
#         # Read fixed width file into a DataFrame
#         if has_header:
#             df = pd.read_fwf(file_path, widths=widths, skiprows=[0], skipfooter=1)
#         else:
#             df = pd.read_fwf(file_path, widths=widths, header=None, skiprows=[0], skipfooter=1)
#     elif file_ext == 'xlsx' or file_ext == 'xls':
#         # Log info message
#         logger.info(f"Step 1: Reading Excel file '{file_path}'")
#         # Read Excel file into a DataFrame
#         if has_header:
#             df = pd.read_excel(file_path, skiprows=skiprows, skipfooter=skipfooter)
#         else:
#             df = pd.read_excel(file_path, header=None, skiprows=skiprows, skipfooter=skipfooter)
#     else:
#         raise ValueError("Unsupported file type.")
#
#     # Log success message
#     logger.info(f"Step 2: DataFrame created with shape {df.shape}")
#
#     return df


@keyword("Write DataFrame to CSV file")
def write_df_to_csv(df_to_write: pd.DataFrame, file_path: str, file_name: str, index: bool = False):
    """
    This method is to write the df to csv file
    :param df_to_write: DataFrame to write to CSV file
    :param file_path: Path where the CSV file needs to be created
    :param file_name: Name of the CSV file to be created
    :param index: Whether to include the index in the CSV file
    :return: None
    """
    logger.info('Step 1: Writing DataFrame to CSV file...')
    try:
        df_to_write.to_csv(path_or_buf=file_path + '/' + file_name, mode='w', index=index)
        logger.info('Step 2: Writing DataFrame to CSV file completed successfully.')
    except Exception as e:
        logger.error(f'Step 2: Writing DataFrame to CSV file failed with error: {e}')


@keyword("Write DataFrame to PSV file")
def write_df_to_psv(df_to_write: pd.DataFrame, file_path: str, file_name: str):
    """
    This method is to write the df to psv file
    :param df_to_write: DataFrame to write to PSV file
    :param file_path: Path where the PSV file needs to be created
    :param file_name: Name of the PSV file to be created
    :return: None
    """
    logger.info('Step 1: Writing DataFrame to PSV file...')
    try:
        df_to_write.to_csv(path_or_buf=file_path + '/' + file_name, mode='w', sep='|', index=False)
        logger.info('Step 2: Writing DataFrame to PSV file completed successfully.')
    except Exception as e:
        logger.error(f'Step 2: Writing DataFrame to PSV file failed with error: {e}')


@keyword("Compare two DataFrames and show differences")
def df_diff(actual_file_path: str, expected_file_path: str, actual_file_name: str, expected_file_name: str,
            file_format: str, key_columns: list, ignore_columns: list):
    """
    This method is used to find the differences between two data frame
    :param actual_file_path: r'C://Desktop//Comparison//data//actual//'
    :param expected_file_path: r'C://Desktop//Comparison//data//baseline//'
    :param actual_file_name: compare_actual_file
    :param expected_file_name: compare_base_file
    :param file_format: 'psv' or 'csv' or 'DAT'
    :param key_columns: unique key columns names as list ['Key_Column1', 'Key_Column2']
    :param ignore_columns: columns to ignore ['Ignore_Column1', 'Ignore_Column2']
    :return:
    """
    logger.info('****************************************************************************************************')
    logger.info('PandasUtil Data Frame Comparison - Cell by Cell comparison with detailed mismatch report')
    logger.info('****************************************************************************************************')
    logger.info('Step-01 : Based on file format create the data frames with delimiter(sep)')
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()
    if file_format == 'psv':
        df1 = pd.read_csv(expected_file_path + expected_file_name + '.' + file_format, sep='|', dtype='str',
                          keep_default_na=False)
        df2 = pd.read_csv(actual_file_path + actual_file_name + '.' + file_format, sep='|', dtype='str',
                          keep_default_na=False)
    elif file_format == 'csv':
        df1 = pd.read_csv(expected_file_path + expected_file_name + '.' + file_format, dtype='str',
                          keep_default_na=False)
        df2 = pd.read_csv(actual_file_path + actual_file_name + '.' + file_format, dtype='str',
                          keep_default_na=False)
    elif file_format == 'DAT':
        df1 = pd.read_fwf(expected_file_path + expected_file_name + '.' + file_format, dtype='str',
                          keep_default_na=False, header=None, encodings="ISO-8859-1", on_bad_lines='skip')
        df2 = pd.read_fwf(actual_file_path + actual_file_name + '.' + file_format, dtype='str',
                          keep_default_na=False, header=None, encodings="ISO-8859-1", on_bad_lines='skip')

    # Store total records in actual and expected df
    total_expected = round(len(df1))
    total_actual = round(len(df2))
    total_mismatch = total_expected - total_actual

    logger.info('Step-02 : Remove the columns based on ignore columns list')
    # If ignore columns are specified, remove those columns from comparison
    if len(ignore_columns) > 0:
        df1.drop(columns=ignore_columns, inplace=True)
        df2.drop(columns=ignore_columns, inplace=True)

    logger.info('Step-03 : Check for duplicate rows in both actual and expected')
    df1.sort_values(by=key_columns, ascending=True, inplace=True)
    df2.sort_values(by=key_columns, ascending=True, inplace=True)
    df1_dup_df = df1[df1[key_columns].duplicated()]
    df2_dup_df = df2[df2[key_columns].duplicated()]
    logger.debug(df1_dup_df)
    logger.debug(df2_dup_df)
    logger.debug(len(df1_dup_df))
    logger.debug(len(df2_dup_df))

    total_expected_dup = round(len(df1_dup_df))
    total_actual_dup = round(len(df2_dup_df))

    logger.info('Step-04 : Remove duplicate records from actual and expected')
    # Create the duplicate detail df
    dup_expected_df = df1_dup_df.copy()
    dup_actual_df = df2_dup_df.copy()
    dup_expected_df['source'] = 'Expected'
    dup_actual_df['source'] = 'Actual'

    dup_cons_df = pd.concat([dup_expected_df, dup_actual_df], axis=0)
    dup_cons_df.reset_index(inplace=True)
    dup_cons_df.drop('index', axis=1, inplace=True)
    df1.drop_duplicates(key_columns, inplace=True)
    df2.drop_duplicates(key_columns, inplace=True)
    logger.debug(dup_expected_df)
    logger.debug(dup_actual_df)
    logger.debug(dup_cons_df)

    logger.info('Step-05 : Sort the actual and expected based on key columns and reset the index')
    # Sort df1 and df2 based on key columns and reset the index
    df1.sort_values(by=key_columns, ascending=True, inplace=True)
    df2.sort_values(by=key_columns, ascending=True, inplace=True)
    df1.reset_index(inplace=True)
    df2.reset_index(inplace=True)

    # Set the index based on key columns in df1 and df2. Remove the default index column
    df1 = df1.set_index(key_columns, drop=True, append=False, inplace=False, verify_integrity=True)
    df2 = df2.set_index(key_columns, drop=True, append=False, inplace=False, verify_integrity=True)
    df1 = df1.drop('index', axis=1)
    df2 = df2.drop('index', axis=1)

    logger.info('Step-06 : Identify the rows matching based on key in both actual and expected')
    # Identify the rows matching based on key in both df1 and df2
    merge_outer_df = pd.merge(df1, df2, how='outer', on=key_columns, indicator='source')
    # merge_outer_df = pd.merge(df1_key_columns, df2_key_columns, how='outer', on=key_columns, indicator='source')
    key_matched_df = merge_outer_df.loc[merge_outer_df['source'] == 'both'].copy()
    logger.debug(len(key_matched_df))
    key_mismatched_df = merge_outer_df.loc[merge_outer_df['source'] != 'both'].copy()
    key_mismatched_df = key_mismatched_df[['source']]
    logger.debug(key_mismatched_df)

    # Update the source column left_only to actual and right_only to expected
    # key_mismatched_df.loc[key_mismatched_df['source'] == 'left_only', 'source'] = 'Actual'

    expected_key_mismatch = len(key_mismatched_df[key_mismatched_df.source == 'left_only'])
    actual_key_mismatch = len(key_mismatched_df[key_mismatched_df.source == 'right_only'])

    logger.info('Step-07 : Create the summary report based on count diff, duplicate rows and key mismatches')

    # Create the executive summary df
    exec_summary_col = ['Summary', 'Expected', 'Actual', 'Mismatch']

    exec_summary_df = pd.DataFrame(columns=exec_summary_col)
    exec_summary_df.loc[1] = ['Total_Records', total_expected, total_actual, total_mismatch]
    exec_summary_df.loc[2] = ['Duplicates', total_expected_dup, total_actual_dup, 0]
    exec_summary_df.loc[3] = ['Key_Mismatch', expected_key_mismatch, actual_key_mismatch, 0]

    logger.debug(exec_summary_df)

    logger.info('Step-08 : Remove the mismatched key values and proceed further in validation')
    df1.drop(key_mismatched_df.loc[key_mismatched_df['source'] == 'left_only'].index, inplace=True)
    df2.drop(key_mismatched_df.loc[key_mismatched_df['source'] == 'right_only'].index, inplace=True)

    logger.info('Step-09 : Started cell by cell comparison for key values that exist in both actual and expected')
    # Verify if columns in both df1 and df2 are same
    assert (df1.columns == df2.columns).all(), logger.debug('Failed - Column mismatch determined')

    logger.info('Step-10 : Verify column data types in both the files, if not convert based on actual')
    if any(df1.dtypes != df2.dtypes):
        logger.debug('Data Types are different, trying to convert')
        df2 = df2.astype(df1.dtypes)

    logger.info('Step-11 : Verify cell by cell data in both the data frame and generate mismatch report')
    # df to hold cell by cell comparison results
    cell_comp_df = pd.DataFrame([])

    # Verify if all the cell data are identical
    if df1.equals(df2):
        logger.info('          Passed : Cell by Cell comparison')
    else:
        logger.info('          Failed : Cell by Cell comparison ..Started to extract mismatched column values')
        # create new data frame with mismatched columns
        diff_mask = (df1 != df2) & ~(df1.isnull() & df2.isnull())
        ne_stacked = diff_mask.stack()
        changed = ne_stacked[ne_stacked]
        key_columns.append('Mismatch_Column')
        changed.index.names = key_columns
        difference_locations = np.where(df1 != df2)
        changed_from = df1.values[difference_locations]
        changed_to = df2.values[difference_locations]
        cell_comp_df = pd.DataFrame({'Expected_Data': changed_from, 'Actual_Data': changed_to}, index=changed.index)
    logger.info('Step-12 : Comparison completed and generated info for reports(summary, keys mismatch, cell by cell')
    logger.info('****************************************************************************************************')
    return exec_summary_df, dup_cons_df, key_matched_df, key_mismatched_df, cell_comp_df

#
# *** Test Cases ***
# Test Write DataFrame to CSV file
#     ${df}=  Create Dataframe  1,2,3\n4,5,6\n7,8,9
#     Write DataFrame to CSV file  ${df}  ./  test.csv
#     ${written_df}=  Read CSV  ./test.csv
#     Should Be True  ${df}.equals(${written_df})
#
# Test Write DataFrame to PSV file
#     ${df}=  Create Dataframe  1,2,3\n4,5,6\n7,8,9
#     Write DataFrame to PSV file  ${df}  ./  test.psv
#     ${written_df}=  Read CSV  ./test.psv  delimiter=|
#     Should Be True  ${df}.equals(${written_df})
#
# Test Compare two DataFrames and show differences
#     ${actual_file_path}=  Set Variable  ./test_data/
#     ${expected_file_path}=  Set Variable  ./baseline_data/
#     ${actual_file_name}=  Set Variable  actual_file
#     ${expected_file_name}=  Set Variable  expected_file
#     ${file_format}=  Set Variable  csv
#     ${key_columns}=  Create List  Key_Column1  Key_Column2
#     ${ignore_columns}=  Create List  Ignore_Column1  Ignore_Column2
#     ${expected_df}=  Read CSV  ${expected_file_path}${expected_file_name}.${file_format}
#     ${actual_df}=  Read CSV  ${actual_file_path}${actual_file_name}.${file_format}
#     Compare two DataFrames and show differences  ${actual_file_path}  ${expected_file_path}  ${actual_file_name}  ${expected_file_name}  ${file_format}  ${key_columns}  ${ignore_columns}

# *** Settings ***
# Library    Pandas
# Library    OperatingSystem

# *** Test Cases ***
# Test Create DataFrame from File
#     [Documentation]    Test the 'Create Dataframe from file' keyword
#     [Tags]    create_dataframe_from_file
#
#     ${df1}    Create Dataframe from file    ${CURDIR}/data/test.csv
#     Should Be Equal As Integers    ${df1.shape[0]}    5
#     Should Be Equal As Integers    ${df1.shape[1]}    3
#
#     ${df2}    Create Dataframe from file    ${CURDIR}/data/test.psv    delimiter='|'
#     Should Be Equal As Integers    ${df2.shape[0]}    5
#     Should Be Equal As Integers    ${df2.shape[1]}    3
#
#     ${df3}    Create Dataframe from file    ${CURDIR}/data/test.txt    widths=[10, 5, 8], has_header=False, skiprows=[0, 1], skipfooter=1
#     Should Be Equal As Integers    ${df3.shape[0]}    3
#     Should Be Equal As Integers    ${df3.shape[1]}    3
#
#     ${df4}    Create Dataframe from file    ${CURDIR}/data/test.xlsx
#     Should Be Equal As Integers    ${df4.shape[0]}    5
#     Should Be Equal As Integers    ${df4.shape[1]}    3
