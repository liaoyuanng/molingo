import utils
import pathlib
import pandas

def parse(file):
    # using magic number is better
    file_extension = pathlib.Path(file).suffix
    df = None
    if (file_extension == '.xls' or file_extension == '.xlsx'):
        df = conver_excel_to_csv(file)
    elif file_extension == '.csv':
        df = pandas.read_csv(file)
    else:
        err_msg = f"not support {file_extension} file, only support `csv` or `xlsx` file"
        utils.log_err(err_msg)
        exit(0)
    
    # remove all n/a data
    df.dropna(how="all",axis=0,inplace=True)

    # remove all unnamed columns
    filtered_df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return filtered_df

def conver_excel_to_csv(excel):
    df = pandas.read_excel(excel)
    df.to_csv(index=False)
    return df