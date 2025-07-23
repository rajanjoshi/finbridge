# ai_assistant/views.py

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import QuestionForm
from .rag_utils import ask_gemini_with_rag

from django.views.i18n import set_language
from django.utils.translation import activate
from django.http import HttpResponseRedirect
from django.urls import reverse
from users.models import UserProfile
import os
from django.core.files.storage import default_storage
from google.cloud import speech
from google.cloud.speech import RecognitionConfig, RecognitionAudio

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .speech_utils import transcribe_audio
from django.views.decorators.http import require_POST
from django.shortcuts import redirect
from google.cloud import texttospeech
import base64

def synthesize_speech(text, language_code="en-IN", voice_name=None):
    client = texttospeech.TextToSpeechClient()

    voice_params = {
        "language_code": language_code,
        "ssml_gender": texttospeech.SsmlVoiceGender.NEUTRAL
    }
    if voice_name:
        voice_params["name"] = voice_name

    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(**voice_params)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    return base64.b64encode(response.audio_content).decode("utf-8")

@require_POST
def clear_chat_history(request):
    request.session["chat_history"] = []
    return redirect("chat_view")



@csrf_exempt
def transcribe_audio_view(request):
    if request.method == 'POST' and 'audio' in request.FILES:
        audio_file = request.FILES['audio']
        lang = request.POST.get('lang', 'en')
        try:
            print("transcribe_audio_view")
            print(lang)
            transcript = transcribe_audio(audio_file, lang_code=lang)
            return JsonResponse({'success': True, 'transcript': transcript})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Invalid request'})


@csrf_exempt
@login_required
def speech_to_text(request):
    if request.method == "POST" and request.FILES.get("audio"):
        try:
            audio_file = request.FILES["audio"]
            transcript = transcribe_audio(audio_file, request.user)
            return JsonResponse({"transcript": transcript})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    return JsonResponse({"error": "Invalid request"}, status=400)

def set_language_and_update_profile(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        response = set_language(request)
        if request.user.is_authenticated and hasattr(request.user, "profile"):
            user_profile = request.user.profile
            user_profile.language = language
            user_profile.save()
        return response
    return HttpResponseRedirect("/")
    

@login_required
def chat_view(request):
    response_text = None
    error = None
    audio_base64 = None
    chat_history = request.session.get("chat_history", [])
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data["question"].strip()

            # If no typed input, try speech
            if not question and 'audio' in request.FILES:
                try:
                    audio_file = request.FILES['audio']
                    lang = request.user.profile.language or "en"
                    print("chat_view")
                    print(request.user.profile.language)
                    print(lang)
                    transcription = transcribe_audio(audio_file, lang_code=lang)
                    if transcription:
                        question = transcription
                    else:
                        error = "No speech recognized and no text input provided."
                except Exception as e:
                    error = f"Speech transcription failed: {str(e)}"

            if question:
                try:
                    response_text = ask_gemini_with_rag(question, request.user)

                    language_map = {
                        "en": "en-IN",
                        "hi": "hi-IN",
                        "mr": "mr-IN",
                    }
                    language_code = language_map.get(request.user.profile.language or 'en', 'en-IN')
                    print("chat_view:")
                    print(language_code)
                    
                    audio_base64 = synthesize_speech(response_text, language_code)
                    chat_history.append({"question": question, "answer": response_text})
                    request.session["chat_history"] = chat_history
                except Exception as e:
                    error = str(e)
            elif not error:
                error = "Please enter a question or use the mic."

    else:
        form = QuestionForm()

    return render(request, "ai_assistant/chat.html", {
        "form": form,
        "response": response_text,
        "error": error,
        "chat_history": chat_history,
        "audio_base64": audio_base64
    })