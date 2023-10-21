from abc import ABC, abstractclassmethod
from config import Platform

class ILingoPlugin(ABC):
    @abstractclassmethod
    def load(self, file, platform: Platform):
        pass
    
    @abstractclassmethod
    def pre_load(self):
        pass
    
    @abstractclassmethod
    def post_load(self):
        pass