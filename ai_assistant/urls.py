from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_view, name='chat_view'),
    path("speech-to-text/", views.speech_to_text, name="speech_to_text"),
    path("transcribe/", views.transcribe_audio_view, name="transcribe_audio"),
    path("chat/clear/", views.clear_chat_history, name="clear_chat_history"),
]
