from typing import List
class Input:
    def __init__(self, path):
        self.path = path
class Languages:
    def __init__(self, main):
        self.main = main
        
class Platform:
    def __init__(self, platform, module, plugin, proj_root_path, mode="append", same_key="keep", pre_load="", post_load=""):
        self.platform = platform
        self.module = module
        self.plugin = plugin
        self.proj_root_path = proj_root_path
        self.mode = mode
        self.pre_load = pre_load
        self.post_load = post_load
class Config:
    def __init__(self, input, platforms: List['Platform'], languages=None):
        self.input = Input(**input)
        self.platforms = [Platform(**platform) for platform in platforms]
        if languages is None:
            self.languages = Languages(main=None)
        else:
            self.languages = Languages(**languages)
         