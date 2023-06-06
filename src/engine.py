from ConfigManager import ConfigManager
from iMessageBroker import iMessageBroker
from models.Equity import *
from services.persistence import *
import json
from pprint import pprint

base = ConfigManager("src/config.yml")
imb = iMessageBroker(base)
persistance = PersistenceService(base)

outfits = base.read_yaml("src/industry/outfits.yml")

Stocks: list[Handle] = []

library = base.get("library_keys")
EqLibrary = library["equities"]
OutfitLibrary = library["outfits"]

if persistance.get_set_size(EqLibrary) > 0:
    print("Previously saved equities found... Loading")
    equities_keys = persistance.reads(EqLibrary).obj
    for e in equities_keys:
        handle = persistance.read(e)
        handle.obj = Stock.parse_raw(handle.obj)
        Stocks.append(handle)
else:
    print("Creating equities... None found")
    equities = base.read_yaml("src/industry/equities.yml")
    for equity in equities:
        equity['outfit_set'] = [outfits[eq_set] for eq_set in equity['outfit_set']]
        stock = Stock.parse_obj(equity)
        Stocks.append(stock)  

        # Save equities to Redis
        res = persistance.create(EqLibrary, Stock.serial_obj(stock))