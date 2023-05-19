from google.cloud import storage
from google.cloud import texttospeech
import json


FINAL_BUCKET = "cloud_storage_leturn"
BUCKET = ""
FILE_NAME = ""
USER_ID = ""
file_no_extension = ''
file_path = ''
json_folder_path = ''
json_filename = ''
audio_folder_path = ''
audio_full_filename = ''
audio_one_filename = ''
image_folder_path = ''


def download_json(event, context):
    # download json file from bucket
    global BUCKET, FILE_NAME, USER_ID, json_folder_path, json_filename, audio_folder_path, audio_full_filename, audio_one_filename, image_folder_path, file_no_extension, file_path

    BUCKET = event['bucket']
    FILE_NAME = event['name'].split('/')[-1]
    file_path = event['name']
    file_no_extension = FILE_NAME.split('.')[-2]
    USER_ID = event['name'].split('/')[0]
    if not file_path.endswith(".json"):
        print("Skipping request to handle", file_path)
        return

    json_folder_path = f'{USER_ID}/{file_no_extension}_json_folder'
    json_filename = f'{file_no_extension}_json'
    audio_folder_path = f'{USER_ID}/{file_no_extension}_audio_folder'
    audio_full_filename = file_no_extension + '_full_audio'
    audio_one_filename = file_no_extension + '_audio'
    image_folder_path = f'{USER_ID}/{file_no_extension}_image_folder'

    print("Extracting text from", file_path)

    client = storage.Client()
    bucket = client.get_bucket(BUCKET)
    file_blob = bucket.get_blob(file_path)
    download_data = file_blob.download_as_string()
    download_data = json.loads(download_data)
    print(download_data)
    get_audio(download_data)


def get_audio(data):
    # transform the audio file
    print("SUCCESS in get_audio")

    for i in range(1, len(data) + 1):
        full_text = data[str(i)]['full_text']['full_text']
        full_text = str.encode(full_text)
        full_text = full_text.decode('utf-8')
        count = str(i)
        text_to_speech(
            full_text, f"{audio_folder_path}/{count}/{audio_full_filename}_{count}.mp3")
        line = len(data[str(i)]['text'])
        for j in range(line):
            text = data[str(i)]['text'][j]['text']
            text = str.encode(text)
            text = text.decode('utf-8')
            line_count = str(j + 1)
            fileName = f"{audio_folder_path}/{count}/{audio_one_filename}_{count}_{line_count}.mp3"
            text_to_speech(text, fileName)


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

    upload_audio(response.audio_content, path, f'{FINAL_BUCKET}')


def upload_audio(mp3, path, load_bucket):
    """Uploads a file to the Cloud Storage bucket."""
    print("SUCCESS in upload_audio")
    print(type(mp3))
    source_file_name = path.split('/')[-1]
    storage_client = storage.Client()
    bucket = storage_client.bucket(load_bucket)
    blob = bucket.blob(path)
    blob.upload_from_string(mp3)
    print(f'File {source_file_name} uploaded to {path}.')
