# Flutter App Backend

This is a minimal Django backend used for testing a Flutter application that:

- Sends and receives photo and audio messages via HTTP
- Receives and sends WebSocket events

---

## 🛠️ Requirements

- Python 3.11+
- `virtualenv`
- `pip`

## Setup Instructions

Clone the repository and start the project

```bash
git clone git@github.com:mariosgn/flask-app-backend.git
cd flutter-app-backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

## Running the Backend

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
