from django.shortcuts import render
from django.http import JsonResponse
import openai
from django.views.decorators.csrf import csrf_exempt
import json

# transcription_app/views.py
from django.shortcuts import render
from django.http import JsonResponse
from .logic import initialize_recorder, start_real_time_transcription
from threading import Thread

@csrf_exempt
def index(request):
    return render(request, 'html/index.html')

@csrf_exempt
def start_transcription(request):
    if request.method == 'POST':
        recorder, source = initialize_recorder()
        # Start real-time transcription in a separate thread
        transcription_thread = Thread(target=start_real_time_transcription, args=(recorder, source))
        transcription_thread.daemon = True
        transcription_thread.start()

        return JsonResponse({'status': 'success'})
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def clear_transcription(request):
    # Your logic for clearing the transcription goes here
    return JsonResponse({'status': 'success'})

