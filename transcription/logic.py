# transcription_app/logic.py
import os
import numpy as np
import whisper
import torch
import speech_recognition as sr
from datetime import datetime, timedelta
from queue import Queue
from time import sleep
from sys import platform

from django.http import JsonResponse
global transcription_text
def initialize_recorder(sample_rate=16000, energy_threshold=1000, default_microphone=None):
    recorder = sr.Recognizer()
    recorder.energy_threshold = energy_threshold
    recorder.dynamic_energy_threshold = False
    print("initialize recorder ////////////////////////////////////////")
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