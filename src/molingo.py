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
    
    for platfrom in config.platforms:
        module = importlib.import_module(platfrom.module)
        instance = getattr(module, platfrom.plugin)
        if issubclass(instance, ILingoPlugin):
            instance.load(instance, file=file, platforom=platfrom)

if __name__ == "__main__":
    start()