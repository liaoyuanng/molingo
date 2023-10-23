import yaml
import json
from config import *
import utils

def loadYAML():
    if not utils.check_is_file("./lingo.yml"):
        utils.log_err("lingo.yml file does not exist")
        exit()
    with open('./lingo.yml', 'r') as file:
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