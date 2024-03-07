# transcription_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('start_transcription/', views.start_transcription, name='start_transcription'),
    path('clear_transcription/', views.clear_transcription, name='clear_transcription'),
]
