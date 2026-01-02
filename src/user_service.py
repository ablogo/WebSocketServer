import os, requests, json
from dotenv import load_dotenv

from src.message_model import Message
from src.mongo_logging import MongoLogger

load_dotenv()
log = MongoLogger(os.environ["LOG_DB_URL"], os.environ["LOG_DATABASE_NAME"], "", os.environ["LOG_LEVEL"])

def verify_token(token: str):
    result = False
    email = None
    try:
        url = os.environ["API_AUTH_URL"] + "/auth/validate-token"
        headers = {"Authorization": "Bearer " + token}
        
        response = requests.post(url, headers= headers)

        if response.ok:
            email = response.text
            result = True

    except Exception as e:
        log.logger.error(e)
    return result, email

def save_message(message: Message, token: str):
    result = False
    try:
        url = os.environ["API_CHAT_URL"] + "/chat/save-message"
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json"
            }
        myobj = json.dumps(message.__dict__)
        
        response = requests.post(url, data = myobj, headers= headers)

        if response.ok:
            result = True

    except Exception as e:
        log.logger.error(e)
    return result
    
def get_messages(user: str, token: str) -> list[Message] | None:
    result = None
    try:
        url = os.environ["API_CHAT_URL"] + "/chat/get-messages"
        headers = {"Authorization": "Bearer " + token}
        
        response = requests.get(url, headers= headers)

        if response.ok:
            result = response.json()

    except Exception as e:
        log.logger.error(e)
    return result
    
def update_status(token: str, status: bool):
    result = False
    try:
        url = str(f"{ os.environ["API_AUTH_URL"] }/user/change-status/?user_status={ status }")
        headers = {"Authorization": "Bearer " + token}

        response = requests.post(url, headers = headers)

        if response.ok:
            result = True

    except Exception as e:
        log.logger.error(e)
    return result