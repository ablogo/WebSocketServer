from datetime import datetime, timezone
from typing import Optional
from time import time

class Message:
    #id: Optional[int] = None
    sender: str
    receiver: str
    message: str
    created_at: int = int(time() * 1000)
    sended: Optional[bool] = False
    read: Optional[bool] = False
    #updated_at: Optional[datetime] = None

    def __init__(self, sender, receiver, message, created_at, sended = False) -> None:
        self.sender = sender
        self.receiver = receiver
        self.message = message
        self.created_at = created_at
        self.sended = sended

class MessagesSended():
    ids: list[str]