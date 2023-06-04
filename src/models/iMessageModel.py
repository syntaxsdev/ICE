from pydantic import BaseModel
from typing import Optional
from abc import ABC, abstractclassmethod

class iMessageInterface(ABC):
    @abstractclassmethod
    def s(self):
        pass


class BodyModel(BaseModel):
    message: str

class RecipientModel(BaseModel):
    handle: str

class IncomingMessageModel(BaseModel):
    body: BodyModel
    sendStyle: str
    attachments: list
    recipient: RecipientModel
    sender: dict
    date: str
    guid: str
    
    class Config:
        extra = "allow"

class Attachment(BaseModel):
    filePath: str


class AttachmentsModel(BaseModel):
    list[Attachment]

class OutgoingMessageModel(BaseModel):
    body: BodyModel
    recipient: RecipientModel
    attachments: Optional[list[Attachment]] = None




