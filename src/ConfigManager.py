from abc import ABC, abstractmethod
import os, shutil, yaml as yml, hashlib

class ConfigInterface(ABC):

    @abstractmethod
    def get(self):
        pass


class ConfigManager(ConfigInterface):
    def __init__(self, configFile):
        self.config = self.read_yaml(configFile)
        self.images_dir = os.path.join(os.path.expanduser("~"), "Pictures", "_imb")
        if not os.path.exists(self.images_dir):
            os.makedirs(self.images_dir)

    def get(self, key):
        return self.config[key]
    
    def read_yaml(self, file: str):
        with open(file, 'r') as ymlFile:
            return yml.safe_load(ymlFile.read())
    
    def read_yamls(self, yaml_str: str):
        return yml.safe_load(yaml_str)
    
    def to_yaml(self, obj) -> str:
        return yml.dump(obj)

    def gen_key(self, data: str) -> str:
        hash_object = hashlib.sha256(data.encode())
        hash_key = hash_object.hexdigest()
        return hash_key
    

        
    

