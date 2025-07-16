import json
import os
import threading
import time
import uuid

from django.http import JsonResponse, Http404, FileResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import random

from django.views.generic import TemplateView

UPLOAD_PATH = "store/upload/"
AUDIO_TESTS_PATH = "store/audio_tests/"
WS_MESSAGES_PATH = "store/websocket_messages/"


def send_message():
    random_number = random.randint(1, 10)
    for idx, value in enumerate(range(1, random_number + 1), 1):
        print( f"Waiting befrore sending message {idx} of {random_number}")
        time.sleep(1)

    print("Sending message")

    id = str(uuid.uuid4())
    msg = {"action": "PLAY", "value": id}

    messages_dir = os.path.join(settings.BASE_DIR, WS_MESSAGES_PATH)
    os.makedirs(messages_dir, exist_ok=True)
    message_file = os.path.join(messages_dir, f"{id}.txt")
    with open(message_file, 'w') as f:
        json.dump(msg, f)


"""
To test this function (whithout autentication):
curl -X POST http://localhost:8000/media_post/ \
  -F "file=@audio_test_1.mp3" \
  -F "param1=test1" \
  -F "param2=test2"
"""
@csrf_exempt
def media_post(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST method allowed'}, status=405)

    # Check if there is at least one file
    if 'file' not in request.FILES:
        return JsonResponse({'error': 'No file part in the request'}, status=400)

    uploaded_file = request.FILES['file']
    filename = uploaded_file.name

    dest_dir = os.path.join(settings.BASE_DIR, UPLOAD_PATH)
    os.makedirs(dest_dir, exist_ok=True)
    destination_path = os.path.join(dest_dir, filename)

    # Write file to destination_path
    with open(destination_path, 'wb+') as dest:
        for chunk in uploaded_file.chunks():
            dest.write(chunk)

    # Get other parameters, if present
    param1 = request.POST.get('param1', None)
    param2 = request.POST.get('param2', None)

    threading.Timer(1.0, send_message).start()

    return JsonResponse({
        'status': 'File saved',
        'filename': filename,
        'param1': param1,
        'param2': param2,
        'saved_to': destination_path
    })


"""
To test this function (whithout autentication):
curl http://localhost:8000/media_get/?media_id=904cb473-5d17-4885-9363-46f466a7d140 --output output.mp3
"""
@csrf_exempt
def media_get(request):
    if request.method != 'GET':
        return Http404("Only GET method is allowed.")

    media_id = request.GET.get('media_id')
    if not media_id:
        return JsonResponse({'error': 'media_id parameter is required'}, status=400)

    audios = (
        "audio_test_1.mp3",
        "audio_test_2.mp3",
        "audio_test_3.mp3",
    )
    filename = random.choice(audios)
    file_path = os.path.join(settings.BASE_DIR, AUDIO_TESTS_PATH, filename)
    # Check if file exists
    if not os.path.exists(file_path):
        raise Http404("Audio file not found.")

    # Return file as response
    return FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')


class HomeView(TemplateView):
    template_name = "home.html"