from redis import Redis
from pydantic import BaseModel
from typing import Union
from ConfigManager import ConfigManager
from enum import Enum
import json

class Type(str, Enum):
    create = "c"
    read = "r"
    update = "u"
    delete = "d"


class Handle(BaseModel):
    key: str 
    obj: object

class Return(str, Enum):
    AlreadyExists = "Exists"
    DoesNotExist = "DNE"
    OK = "OK"

class PersistenceService:
    def __init__(self, base: ConfigManager):
        self.base = base

        redis_config = base.get('redis')
        # Connect to Redis
        self.redis = Redis(host=redis_config['host'], port=redis_config['port'], decode_responses=True)

    def create(self, library, obj) -> Handle:
        obj = json.dumps(obj)
        key = self.base.gen_key(obj)
        self.insert_key_library(library_key=library, obj=key)
        self.redis.set(key, obj)
        return Handle(key=key, obj=obj)
        

    def read(self, key) -> Handle:
        return Handle(key=key, obj=self.redis.get(key))
    
    def reads(self, key) -> Handle:
        return Handle(key=key, obj=self.redis.smembers(key))
    
    def update(self, handle: Handle) -> Union[Handle, Return]:
        if self.redis.exists(handle.key):
            self.redis.set(handle.key, handle.obj)
            return Return.OK
        else:
            return Return.DoesNotExist
        
    def delete(self, handle: Handle) -> Union[int, Return]:
        if self.redis(handle.key):
            return self.redis.delete(handle.key)
        else:
            return Return.DoesNotExist
        
    def get_set_size(self, key) -> int:
        return self.redis.scard(key)

    def insert_key_library(self, library_key, obj):
        self.redis.sadd(library_key, obj)
