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
    
    data = None
    if (file_extension == '.xls' or file_extension == '.xlsx'):

        data = __conver_excel_to_csv(file)
    elif file_extension == '.csv':
        data = pandas.read_csv(config.input.path)
        # data.dropna(inplace=True)
    else:
        raise RuntimeError(f"not support {file_extension} file, only support `csv` or `xlsx` file")
    
    json = data.to_json()
    
    print(json)
    
    for platrom in config.platforms:
        module = importlib.import_module(platrom.module)
        instance = getattr(module, platrom.plugin)
        if issubclass(instance, ILingoPlugin):
            instance.load(data)

def __conver_excel_to_csv(excel):
   data = pandas.read_excel(excel)
   data.to_csv(index=False)
#    data.dropna(inplace=True)
   return data
    

if __name__ == "__main__":
    start()