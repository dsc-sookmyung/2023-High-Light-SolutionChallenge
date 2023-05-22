from googletrans import Translator
import os
from google.cloud import texttospeech
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./vision_api_key.json"


def text_to_speech(text, path):
    print("SUCCESS in text_to_speech")
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    return response.audio_content


translator = Translator()

text = "a penguin with a white background and a black and white background"
print(text)
result = translator.translate(text, dest='ko')

print(result.text)
