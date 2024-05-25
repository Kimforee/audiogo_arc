from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .logic import initialize_recorder
from threading import Thread

recorder, source = initialize_recorder()
transcription_thread = None  # Track the transcription thread

def index(request):
    return render(request, 'html/index.html')

def process_transcription(request):
    if request.method == 'POST' and 'transcription' in request.POST:
        transcription = request.POST['transcription']
        # Process the transcription here, e.g., pass it to the model for further processing
        print("Transcription received:", transcription)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})


