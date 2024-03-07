# transcription/logic.py
import os
import numpy as np
import whisper
import torch
import speech_recognition as sr
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

def initialize_recorder(sample_rate=16000, energy_threshold=1000, default_microphone=None):
    recorder = sr.Recognizer()
    recorder.energy_threshold = energy_threshold
    recorder.dynamic_energy_threshold = False

    if 'linux' in platform:
        mic_name = default_microphone
        if not mic_name or mic_name == 'list':
            print("Available microphone devices are: ")
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                print(f"Microphone with name \"{name}\" found")
            return None
        else:
            for index, name in enumerate(sr.Microphone.list_microphone_names()):
                if mic_name in name:
                    source = sr.Microphone(sample_rate=sample_rate, device_index=index)
                    break
    else:
        source = sr.Microphone(sample_rate=sample_rate)

    with source:
        recorder.adjust_for_ambient_noise(source)

    return recorder, source

def start_real_time_transcription(recorder, source, record_timeout=2, phrase_timeout=3, model="medium"):
    phrase_time = None
    data_queue = Queue()
    try:
     audio_model = whisper.load_model(model)
    except Exception as e:
        print(f"Error loading Whisper model: {e}")
    transcription = ['']

    def record_callback(_, audio: sr.AudioData) -> None:
        data = audio.get_raw_data()
        data_queue.put(data)

    recorder.listen_in_background(source, record_callback, phrase_time_limit=record_timeout)

    print("Model loaded.\n")

    while True:
        try:
            now = datetime.utcnow()
            if not data_queue.empty():
                phrase_complete = False
                if phrase_time and now - phrase_time > timedelta(seconds=phrase_timeout):
                    phrase_complete = True
                phrase_time = now

                audio_data = b''.join(data_queue.queue)
                data_queue.queue.clear()

                audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0

                result = audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                text = result['text'].strip()

                if phrase_complete:
                    transcription.append(text)
                else:
                    transcription[-1] = text
                print("->_>->_>->")
                print(text)
                os.system('cls' if os.name == 'nt' else 'clear')
                for line in transcription:
                    print(line)
                print('', end='', flush=True)

                sleep(0.25)
        except KeyboardInterrupt:
            break

    print("\n\nTranscription:")
    for line in transcription:
        print(line)
