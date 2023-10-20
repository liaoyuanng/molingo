from typing import List

class Input:
    def __init__(self, path, type):
        self.path = path
        self.type = type
        

class Platform:
    def __init__(self, platform, module, plugin, output, mode="append", same_key="keep"):
        self.platform = platform
        self.module = module
        self.plugin = plugin
        self.output = output
        self.mode = mode

class Config:
    def __init__(self, input, platforms: List['Platform']):
        self.input = Input(**input)
        self.platforms = [Platform(**platform) for platform in platforms]
         