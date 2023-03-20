from google.cloud import speech_v1p1beta1 as speech
from google.cloud import storage
from google.cloud import texttospeech
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./tts_api_key.json"

client = speech.SpeechClient()

# speech_file = "https://storage.googleapis.com/cloud_storage_leturn/StallingsOS8e-Chap04_audio_folder/14/StallingsOS8e-Chap04_full_audio_46.mp3"
speech_file = "./data_1_audio_folder/2/data_1_full_audio_2.mp3"
first_lang = "ko"
second_lang = "en"

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()
# content = "프로세스와 쓰레드\n• 쓰레드의 장점: 예 (그림 4.3: RPC(Remote Procedure Call)"
# audio = speech.RecognitionAudio(content=content)
# audio = speech.RecognitionAudio(
#     uri="https://storage.googleapis.com/cloud_storage_leturn/StallingsOS8e-Chap04_audio_folder/10/StallingsOS8e-Chap04_full_audio_10.mp3")

# config = speech.RecognitionConfig(
#     encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
#     sample_rate_hertz=44100,
#     audio_channel_count=2,
#     language_code=first_lang,
#     alternative_language_codes=[second_lang],
# )


def text_to_speech(text, fileName):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL,
        # alternative_language_codes=["en"]
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    # The response's audio_content is binary.
    # fileName = "./audio_output/sample" + str(i) + "_" + str(j) + ".mp3"
    with open(fileName, "wb") as out:
        # Write the response to the output file.
        out.write(response.audio_content)
        print('Audio content written to file ' + fileName)


print("Waiting for operation to complete...")
text_to_speech('프로세스와 쓰레드\n• 단일쓰레딩(Single threading) 대 멀티쓰레딩(Multi \nthreading)\n– 단일 프로세스 내에 멀티 쓰레드 실행을 지원 가능\n5\n Before the Lecture…\n▪ What is “data mining”?\n– The process of discovering hidden patterns or knowledge from large data\n– Involves methods from various fields\n• Computer science (esp. databases), statistics, machine learning, …\n5\n', "en_ko.mp3")
