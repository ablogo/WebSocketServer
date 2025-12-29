import os, http, json
from websockets.sync.server import serve
from dotenv import load_dotenv

from src.message_service import get_current_user, remove_connection, try_to_save_message, validate_message
from src.user_service import verify_token, update_status, get_messages
from src.mongo_logging import MongoLogger

users = dict()
load_dotenv()
log = MongoLogger(os.environ["LOG_DB_URL"], os.environ["LOG_DATABASE_NAME"], "", os.environ["LOG_LEVEL"])

def handler(websocket):
    try:
        token = websocket.request.headers["Authorization"]
        current_user = get_current_user(users, websocket.id)
        result = update_status(token, True)

        if current_user is not None:
            messages = get_messages(current_user, token)
            
            if messages is not None:
                for message in messages:
                    websocket.send(json.dumps(message))
        
        #if not result:
        #    remove_connection(users, websocket)
        #    return websocket.respond(http.HTTPStatus.SERVICE_UNAVAILABLE)
        
        for message in websocket:
            send_mesage(current_user, message)

    except Exception as e:
        log.logger.error(e)
    finally:
        remove_connection(users, websocket.id)
        update_status(token, False)

def send_mesage(current_user, message):
    try:
        result = False
        msg = validate_message(message)
        if msg is not None:
            log.logger.debug("\ncurrent user: " + current_user)
            msg.sender = current_user
            email_to = msg.receiver
            log.logger.debug("send to: " + email_to)
            global users
            websocket = users[email_to][1]
            websocket.send(json.dumps(msg.__dict__))
            result = True
            log.logger.debug("\nmsg sended: " + json.dumps(msg.__dict__))
    except KeyError as e:
        log.logger.error(e)
    except Exception as e:
        log.logger.error(e)
    finally:
        if not result and msg is not None:
            try_to_save_message(users, current_user, msg)
    return result
    
def process_request(connection, request):
    try:
        if request.path.startswith("/?token="):
            token = request.path.replace("/?token=", "")
            request.headers["Authorization"] = token
        else:
            token = get_header(request.headers, "Authorization")
        
        if not token:
            return connection.respond(http.HTTPStatus.UNAUTHORIZED, "Missing token\n")

        is_valid, email = verify_token(token)
        if is_valid and email is not None:
            global users
            users[email] = [token, connection, connection.id]
            log.logger.debug("user connected: " + email)
        else:
            return connection.respond(http.HTTPStatus.UNAUTHORIZED, "Invalid token\n")
    except Exception as e:
        log.logger.error(e)
        return connection.respond(http.HTTPStatus.SERVICE_UNAVAILABLE)

def get_header(headers, header_name: str):
    try:
        result = ""
        result = headers[header_name]
    except Exception as e:
        log.logger.error(e)
    return result
    
def health_check(connection, request):
    if request.path == "/healthz":
        return connection.respond(http.HTTPStatus.OK, "OK\n")


def main():
    try:
        with serve(
            handler, os.environ["WS_HOST"], int(os.environ["WS_PORT"]),
            process_request= process_request,
            ping_timeout= 30, ping_interval= 30) as server:
            server.serve_forever()

    except Exception as e:
        log.logger.error(e)


if __name__ == "__main__":
    main()