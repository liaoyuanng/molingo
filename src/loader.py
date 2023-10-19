import yaml
import json
from config import *
from types import SimpleNamespace

def loadYAML():
    with open('./lingo.yml', 'r') as file:
        try:
            content = yaml.safe_load(file)
            return content
        except yaml.YAMLError as e:
            print(e)
            raise e
        
def load():
    dict = loadYAML()
    plugin = json.loads(json.dumps(dict))
    config = Config(**plugin)
    return config