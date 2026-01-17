# WebSocketServer
WebSocket server created this [chat application](https://github.com/ablogo/ChatService).

This project must be used in conjunction with at least two others, one that is an authentication microservice that manage the users, and another microservice that manages chat functions.

It is necessary to develop a WebSocket client, or you can use the one found in [this repository](https://github.com/ablogo/WebSocketClient).

When connecting to the server, a token must be sent, which is obtained from this [authentication microservice](https://github.com/ablogo/AuthFastApi).

All logs are sent to a MongoDB database.

## Requirements
- Python 3.12+
- MongoDB database

## Installing
1. Create a virtual environment
```bash
python -m venv .venv
```
2. Activate it (Linux, macOS)
```bash
source .venv/bin/activate
```
   - Activate it (Windows PowerShell)
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
6. Use this [websocket client](https://github.com/ablogo/WebSocketClient) to connect and test the websocket server