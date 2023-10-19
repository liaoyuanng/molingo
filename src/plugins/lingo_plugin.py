from abc import ABC, abstractclassmethod

class ILingoPlugin(ABC):
    @abstractclassmethod
    def load(csv_data):
        print("hi, iOS")