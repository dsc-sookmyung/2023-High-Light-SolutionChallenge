import json
import json
from google.cloud import texttospeech
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./tts_api_key.json"


def text_to_speech(text, fileName):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
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


filename = 'os_4'
image_path = './' + filename + '_audio/'

with open('./' + filename + '_ver2.json', 'r', encoding="utf-8") as f:
    json_data = json.load(f)

for i in range(1, len(json_data) + 1):
    local_image_path = image_path
    local_image_path += str(i)
    full_text = json_data[str(i)]['full_text']['full_text']
    if not os.path.exists(local_image_path):
        os.makedirs(local_image_path)
    text_to_speech(full_text, local_image_path +
                   "./full_text" + str(i) + ".mp3")
    line = len(json_data[str(i)]['text'])
    for j in range(line):
        text = json_data[str(i)]['text'][j]['text']
        print(text)
        fileName = local_image_path + "./text" + str(i) + "_" + str(j) + ".mp3"
        text_to_speech(text, fileName)

print("fin")
