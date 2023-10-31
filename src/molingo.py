#!/usr/bin/env python3

import config_loader as Loader
from importlib import import_module
from plugins.lingo_plugin import ILingoPlugin
from os.path import isfile
import csv_parser as csv
from inspect import isabstract
import utils
    
def start():
    config = Loader.load()
    file = config.input.path
    if not isfile(file):
        utils.log_err(f"\"{file}\" does not exist or is not a file")
        exit(0)
    csv_df = csv.parse(file, config)
    for platfrom in config.platforms:
        module = import_module(platfrom.module)
        instance = getattr(module, platfrom.plugin)
        if not isabstract(instance):
            if issubclass(instance, ILingoPlugin):
                utils.log_succ(f">>>>>>>>> {platfrom.platform} Localization Start")
                instance.load(instance(), csv_df, platfrom)
                utils.log(f"{platfrom.platform} Localization End")
            else:
                raise RuntimeError(f"{platfrom.plugin} must be a subclass of `ILingoPlugin`")
if __name__ == "__main__":
    start()