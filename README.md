# Flutter App Backend

This is a minimal Django-based backend designed to demonstrate a simple interaction between a web client and a WebSocket server.

Components
----------

1. Django Server
   - Exposes a single web page at the root URL.
   - Serves a static HTML page that connects to a WebSocket on load.
   - Accepts two types of HTTP requests via curl:
     - A POST request to upload a file (for debug purposes), which is saved into a local directory called "store/" at the root of the project.
     - A GET request to download one of three predefined audio files available in the repository.

2. WebSocket Daemon (Python)
   - Must be launched separately before opening the page.
   - Listens on ws://localhost:8765.
   - The frontend HTML page automatically tries to connect to this WebSocket when loaded.
   - Sends a "[ping] Server heartbeat" message every 10 seconds to all connected clients.
   - Echoes back to all clients any text file added into the "websocket_messages/" directory:
     - When a .txt file is placed in that directory, its content is read and immediately sent to all connected clients.
     - The file is deleted after being sent.

Trigger Behavior
----------------

When a file is uploaded via the POST endpoint, the server triggers a delayed message (between 1 and 10 seconds) sent via WebSocket to the connected client. This message is predefined and demonstrates asynchronous server-to-client communication.

Required Work
------------------------------------

- Both GET and POST endpoints must require Django user authentication.
  - These endpoints will only accept requests authenticated via the Django user
    created during login from the Flutter app.
  - Authentication will likely use token-based headers or session cookies.
  - Additional checks such as validating file IDs will be handled later (not required now).

- WebSocket Authentication:
  - The WebSocket server does NOT enforce authentication at this stage.
  - However, clients must send the same authentication values used in the GET and POST requests
    (e.g. token or session ID) when connecting.
  - These values will be ignored for now, but will be parsed and stored for future use.
  - The current websocket server will send same message to all connected clients, broadcast: this is fine 

- Dependencies:
  - The project must include `django-allauth` for social authentication (Google/Facebook).
  - Minimal other dependencies are expected.

Other Notes
-----------

- The WebSocket server will remain as a standalone Python script (not Django-integrated).
- Future integration of authentication or routing logic in the WebSocket server will be handled separately.
- Static file handling, admin configuration, and model extensions are outside the scope of this minimal backend.

Requirements
-----------

- Python 3.11+
- `virtualenv`
- `pip`

Setup Instructions
-----------

Clone the repository and start the project

```bash
git clone git@github.com:mariosgn/flask-app-backend.git
cd flutter-app-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

Running the Backend
-----------

Start the django debug server (in the project directory)

```bash
python manage.py runserver
```

Start the websocket server (in the project directory)

```bash
python websocket_server.py
```

## Check django and websocket connection

Open the browser to http://127.0.0.1:8000/

## Run the curl calls and send a message to the websocket

Always in the main project directory

To upload an audio file without authentication:

```bash
curl -X POST http://localhost:8000/media_post/ \
  -F "file=@store/audio_tests/audio_test_1.mp3" \
  -F "param1=test1" \
  -F "param2=test2"
```

To download an audio file without authentication:

```bash
curl http://localhost:8000/media_get/?media_id=904cb473-5d17-4885-9363-46f466a7d140 --output output.mp3
```

To send a message to the client via websocket
```bash
echo ' {"action": "PLAY", "value": "fake-uuuid"}' > store/websocket_messages/message.txt
```


