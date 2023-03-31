from google.cloud import storage
from google.cloud import texttospeech
import tempfile
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from flask import abort
import re
import os
import fitz
import PIL.Image
import io
import json
from google.api_core import exceptions

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
    """
    Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print("in CF")
    print("event", event)

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
    print("USER_ID : ", USER_ID)
    print(json_folder_path)
    print(audio_folder_path)
    print(image_folder_path)
    # 이미지 추출 및 저장 -> 상대 경로 문제 해결 필요
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)
    file_blob = bucket.get_blob(file_path)
    download_data = file_blob.download_as_string()
    download_data = json.loads(download_data)
    print(download_data)
    get_audio(download_data)


def get_audio(data):
    print("SUCCESS in get_audio")

    # 오디오 파일 생성 및 파일 저장
    # * 상대 경로 참조
    # if not os.path.exists(f"{audio_folder_path}"):
    #     os.makedirs(f"{audio_folder_path}")
    for i in range(1, len(data) + 1):
        full_text = data[str(i)]['full_text']['full_text']
        full_text = str.encode(full_text)
        full_text = full_text.decode('utf-8')
        count = str(i)
        # * 상대 경로 참조
        # if not os.path.exists(f"{audio_folder_path}/{count}"):
        #     os.makedirs(f"{audio_folder_path}/{count}")
        print(full_text)
        text_to_speech(
            full_text, f"{audio_folder_path}/{count}/{audio_full_filename}_{count}.mp3")
        line = len(data[str(i)]['text'])
        for j in range(line):
            text = data[str(i)]['text'][j]['text']
            text = str.encode(text)
            text = text.decode('utf-8')
            print(text)
            line_count = str(j + 1)
            fileName = f"{audio_folder_path}/{count}/{audio_one_filename}_{count}_{line_count}.mp3"
            text_to_speech(text, fileName)

    print("audio fin")


def text_to_speech(text, path):
    print("SUCCESS in text_to_speech")
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
    # with open(fileName, "wb") as out:
    #     # Write the response to the output file.
    #     out.write(response.audio_content)

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
