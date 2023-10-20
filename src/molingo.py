import config_loader as Loader
import importlib
from plugins.lingo_plugin import ILingoPlugin
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
            instance.load(instance, file=file, platform=platfrom)
        else:
            raise RuntimeError(f"{platfrom.plugin} must be a subclass of `ILingoPlugin`")

if __name__ == "__main__":
    start()