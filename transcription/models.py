# transcription/models.py
from django.db import models

class Transcription(models.Model):
    text = models.TextField()
