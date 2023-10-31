import utils
import pathlib
import pandas
import config

def check_main_lang(config, df):
    
    if not config.languages.main is None:
       if not config.languages.main in df.columns[1:]:
           utils.log_err(f"The main language {[config.languages.main]} must be included in the file")
           exit()
    else:
        if len(df.columns) > 1:
            config.languages.main = df.columns[1]
        else:
            utils.log_err("File must contain at least one language.")
            exit()

def parse(file, config):
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
    
    # check main language and set main language if needed
    check_main_lang(config, filtered_df)
        
    # replace missing language value with the main language.
    fallback_df = filtered_df.apply(lambda row: row.fillna(row[config.languages.main]), axis=1)
    return fallback_df

def conver_excel_to_csv(excel):
    df = pandas.read_excel(excel)
    df.to_csv(index=False)
    return df