# WebSocketServer
WebSocket server created for a chat application.

This project must be used in conjunction with at least two others, one that is an authentication microservice that manage the users, and another microservice that manages chat functions.

It is necessary to develop a WebSocket client, or you can use the one found in the next repository.

When connecting to the server, a token must be sent, which is obtained from the authentication microservice.

All logs are sent to a MongoDB database.

## Requirements
- Python 3.12+
- MongoDB (local server or remote server)

## Installing
1. Create a virtual environment
```bash
python -m venv .venv
```
2. Activate it (Linux, macOS)
```bash
source .venv/bin/activate
```
   Activate it (Windows PowerShell)
```bash
.venv\Scripts\Activate.ps1
```
3. Install dependencies
```bash
pip install -r requirements.txt
```
4. Set configuration file (.env)

The address and port of the websocket server, the connection string of the database and other configurations must be included

5. Run it locally
```bash
python main.py
```
6. Open the next url in a browser to see the Swagger UI
```bash
h
```