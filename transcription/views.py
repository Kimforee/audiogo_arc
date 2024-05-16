from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .logic import initialize_recorder
from threading import Thread
from .model_loader import get_response

recorder, source = initialize_recorder()
transcription_thread = None  # Track the transcription thread

def index(request):
    return render(request, 'html/index.html')

@csrf_exempt
def process_transcription(request):
    if request.method == 'POST' and 'transcription' in request.POST:
        transcription = request.POST['transcription']
        # Process the transcription here
        print("Transcription received:", transcription)
        # Respond with a static message for now
        response_message = get_response(transcription)
        return JsonResponse({'status': 'success', 'response': response_message})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'})