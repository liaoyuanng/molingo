import config_loader as Loader
import importlib
from plugins.lingo_plugin import ILingoPlugin
import os
import csv_parser as csv
import inspect
import utils
    
def start():
    config = Loader.load()
    file = config.input.path
    if not os.path.isfile(file):
        utils.log_err(f"\"{file}\" does not exist or is not a file")
        exit(0)
    csv_df = csv.parse(file)
    for platfrom in config.platforms:
        module = importlib.import_module(platfrom.module)
        instance = getattr(module, platfrom.plugin)
        if not inspect.isabstract(instance):
            if issubclass(instance, ILingoPlugin):
                utils.log_succ(f">>>>>>>>> {platfrom.platform} Localization Start")
                instance.load(instance(), csv_df, platfrom)
                utils.log(f"{platfrom.platform} Localization End")
            else:
                raise RuntimeError(f"{platfrom.plugin} must be a subclass of `ILingoPlugin`")
if __name__ == "__main__":
    start()