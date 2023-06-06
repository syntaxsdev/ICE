import os, json, time, requests
from ConfigManager import ConfigManager
from models.iMessageModel import Attachment, AttachmentsModel, OutgoingMessageModel, RecipientModel, BodyModel
from typing import Optional, Union


class iMessageBroker:
    def __init__(self, base: ConfigManager):
        self.base = base

        # Config specifics
        self.endpoints = base.get('endpoints')
        self.handles = base.get('test_handles')

    def send_message(self, msg: str, recip: str, attachments: Optional[Union[str, list[str]]] = None):
        att = attachments
        
        if type(attachments) == list:
            attList = [Attachment(filePath=file) for file in attachments]      
        else:
            attList = [Attachment(filePath=attachments)]

        omm: OutgoingMessageModel = OutgoingMessageModel(
            body=BodyModel(message=msg),
            recipient=RecipientModel(handle=recip),
            attachments=attList)
        
        print(omm.dict())

        requests.post(url=self.endpoints['send_message'], json=omm.dict())


    def get_rel_fp(self, file):
        current_dir = os.getcwd()
        return os.path.join(current_dir, 'imgs', file)


