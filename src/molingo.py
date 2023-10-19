import loader as Loader
import pandas
import importlib
from plugins.lingo_plugin import ILingoPlugin
import pathlib
import os
    

def start():
    config = Loader.load()
    file = config.input.path
    if not os.path.isfile(file):
        raise RuntimeError(f"\"{file}\" does not exist or is not a file")
    
    file_extension = pathlib.Path(file).suffix
    
    df = None
    if (file_extension == '.xls' or file_extension == '.xlsx'):
        df = __conver_excel_to_csv(file)
    elif file_extension == '.csv':
        df = pandas.read_csv(config.input.path)
    else:
        raise RuntimeError(f"not support {file_extension} file, only support `csv` or `xlsx` file")

    df.dropna(how="all",axis=0,inplace=True)
    filtered_df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    json = filtered_df.to_json()
    
    for platrom in config.platforms:
        module = importlib.import_module(platrom.module)
        instance = getattr(module, platrom.plugin)
        if issubclass(instance, ILingoPlugin):
            instance.load(json)

def __conver_excel_to_csv(excel):
   df = pandas.read_excel(excel)
   df.to_csv(index=False)
   return df
    

if __name__ == "__main__":
    start()