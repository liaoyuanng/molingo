import os
import sys
import yaml
import json
from config import *
import utils

def loadYAML():
    script_path = os.path.realpath(sys.argv[0])
    script_dir = os.path.dirname(script_path)
    yaml_path = os.path.join(os.path.dirname(script_dir), './lingo.yml')
    if not utils.check_is_file(yaml_path):
        utils.log_err("lingo.yml file does not exist")
        exit()
    with open(yaml_path, 'r') as file:
        try:
            content = yaml.safe_load(file)
            return content
        except yaml.YAMLError as e:
            utils.log_err(f"load lingo.yml fial, {e}")
            exit()
        
def load():
    dict = loadYAML()
    plugin = json.loads(json.dumps(dict))
    config = Config(**plugin)
    return config