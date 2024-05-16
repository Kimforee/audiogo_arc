# transcription_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('process_transcription/', views.process_transcription, name='process_transcription'),
]

