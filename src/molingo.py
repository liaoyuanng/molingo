import config_loader as Loader
import importlib
from plugins.lingo_plugin import ILingoPlugin
import os
import csv_parser as csv
    

def start():
    config = Loader.load()
    file = config.input.path
    if not os.path.isfile(file):
        raise RuntimeError(f"\"{file}\" does not exist or is not a file")
    csv_df = csv.parse(file)
    for platfrom in config.platforms:
        module = importlib.import_module(platfrom.module)
        instance = getattr(module, platfrom.plugin)
        if issubclass(instance, ILingoPlugin):
            instance.load(instance, csv_df, platfrom)
        else:
            raise RuntimeError(f"{platfrom.plugin} must be a subclass of `ILingoPlugin`")

if __name__ == "__main__":
    start()