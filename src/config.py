from typing import List

class Input:
    def __init__(self, path, type):
        self.path = path
        self.type = type
        

class Platform:
    def __init__(self, platform, module, plugin, output):
        self.platform = platform
        self.module = module
        self.plugin = plugin
        self.output = output

class Config:
    def __init__(self, input, platforms: List['Platform']):
        self.input = Input(**input)
        self.platforms = [Platform(**platform) for platform in platforms]
         