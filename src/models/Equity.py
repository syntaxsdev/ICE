from pydantic import BaseModel
from typing import Optional, Union
from enum import Enum


class Outfit(BaseModel):
    set: list[int]
    cross_set: list[list[int]]


class Type(str, Enum):
    BULL = "BULL"
    BEAR = "BEAR"
    NC = "NOTCONFIGURED"

class Signal(str, Enum):
    BUY = "BUY"
    SELL = "SELL"
    UNKNOWN = "UNK"

class SignalElapsedSet(BaseModel):
    sig_cross_above: int
    sig_cross_below: int
    elapsed_time: int
    timeframe: str


class IndexEquity(BaseModel):
    ticker: str
    leverage: Optional[float] = 1
    type: Optional[Type] = Type.BULL


class Stock(BaseModel):
    ticker: str
    is_index: Optional[bool] = False
    index_equity: Optional[IndexEquity]
    leveraged_equity: Optional[list[IndexEquity]]
    outfit_set: list[Outfit]
    signal_cross: Optional[Signal] = Signal.UNKNOWN
    signal_cross_elapsed_set: Optional[list[SignalElapsedSet]] = []

    @staticmethod
    def serial_obj(obj: 'Stock'):
        dict = obj.dict()
        if "index_equity" in dict.keys() and dict['index_equity'] is not None:
            dict['index_equity']['type'] = dict['index_equity']['type'].value
        
        if "leveraged_equity" in dict.keys() and dict['leveraged_equity'] is not None:
            for equity in dict['leveraged_equity']:
                equity['type'] = equity['type'].value

        if "signal_cross" in dict.keys() and dict['signal_cross'] is not None:
            dict['signal_cross'] = dict['signal_cross'].value
        return dict
