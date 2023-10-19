from abc import ABC, abstractclassmethod

class ILingoPlugin(ABC):
    @abstractclassmethod
    def load(json):
        print("hi, iOS")