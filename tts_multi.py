from google.cloud import speech_v1p1beta1 as speech

client = speech.SpeechClient()

speech_file = "https://storage.googleapis.com/cloud_storage_leturn/StallingsOS8e-Chap04_audio_folder/14/StallingsOS8e-Chap04_full_audio_46.mp3"
first_lang = "ko"
second_lang = "en"

# with open(speech_file, "rb") as audio_file:
#     content = audio_file.read()
content = "프로세스와 쓰레드\n• 쓰레드의 장점: 예 (그림 4.3: RPC(Remote Procedure Call)"
audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    audio_channel_count=2,
    language_code=first_lang,
    alternative_language_codes=[second_lang],
)

print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print("-" * 20)
    print("First alternative of result {}: {}".format(i, alternative))
    print("Transcript: {}".format(alternative.transcript))
