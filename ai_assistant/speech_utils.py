from google.cloud import speech_v1p1beta1 as speech
import io

LANGUAGE_CODES = {
    'en': 'en-IN',
    'hi': 'hi-IN',
    'mr': 'mr-IN',
}

def transcribe_audio(audio_file, lang_code="en"):
    client = speech.SpeechClient()
    language_code = LANGUAGE_CODES.get(lang_code, "en-IN")
    print("transcribe_audio")
    print(language_code)
    content = audio_file.read()
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
        sample_rate_hertz=48000,
        language_code=language_code,
        model="default"
    )


    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + " "
    return transcript.strip()
