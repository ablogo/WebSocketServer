from datetime import datetime
import os, json
from dotenv import load_dotenv
from log2mongo import log2mongo

from src.user_service import save_message
from src.message_model import Message

load_dotenv()
log = log2mongo(os.environ["LOG_DB_URL"], os.environ["LOG_DATABASE_NAME"], "", os.environ["LOG_LEVEL"])

def to_message(dct) -> Message | None:
    try:
        if "sender" in dct and "receiver" in dct and "message" in dct and "created_at" in dct:
            return Message(dct["sender"], dct["receiver"], dct["message"], dct["created_at"])
    except Exception as e:
        log.logger.error(e)
        return None

def validate_message(message: str) -> Message | None:
    m = None
    try:
        m = json.loads(message, object_hook = to_message)
    except Exception as e:
        log.logger.error(e)
    return m
    
def get_current_user(users: dict, ws_id: str) -> str | None:
    try:
        for user in users:
            if users[user][2] == ws_id:
                log.logger.debug("user returned: " + user)
                return user
    except KeyError as e:
        log.logger.error(e)
    except Exception as e:
        log.logger.error(e)

def remove_connection(users: dict, ws_id: str):
    try:
        key= ""
        for k, value in users.items():
            if value[2] == ws_id:
                key = k
                log.logger.debug("connection removed: " + k)
        users.pop(key)
    except Exception as e:
        log.logger.error(e)
    
def try_to_save_message(users: dict, current_user: str, msg: Message):
    try:
        log.logger.debug("msg sended to DB: " + msg.message)
        token = users[current_user][0]
        msg.sender = current_user
        result = save_message(msg, token)
    except Exception as e:
        log.logger.error(e)