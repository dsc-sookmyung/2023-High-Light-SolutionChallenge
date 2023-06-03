import json
import requests
from transformers import BlipProcessor, BlipForConditionalGeneration
from google.cloud import storage
from PIL import Image
import torch
from googletrans import Translator
from google.cloud import texttospeech

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
    print('event: ', event)
    print('context: ', context)
    
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
    for_making_caption(download_data)

def gen_image_caption(img_url):
    processor = BlipProcessor.from_pretrained(
        "Salesforce/blip-image-captioning-base")
    model = BlipForConditionalGeneration.from_pretrained(
        "Salesforce/blip-image-captioning-base")

    img_url = img_url
    raw_image = Image.open(requests.get(
        img_url, stream=True).raw).convert('RGB')

    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    image_caption = processor.decode(out[0], skip_special_tokens=True)
    print(image_caption)
    return image_caption
    
def for_making_caption(data):
    print("SUCCESS in for_making_caption")
    for i in range(1, len(data) + 1):
        count = str(i)
        image = data[count]["image"]
        for j in range(len(image)):
            print("img_url: ", image[j]["img_url"])
            img_idx = image[j]["img_idx"]
            print("img_idx: ", img_idx)
            image_caption = gen_image_caption(image[j]["img_url"])
            translator = Translator()
            text = image_caption
            translated_text = ''
            try:
                translator = Translator()
                translation = translator.translate(text, dest='ko')
                translated_text = translation.text
            except Exception as e:
                print("Translation error:", e)
                translated_text = text
            text_to_speech(
                translated_text, f"{image_folder_path}/{count}/{file_no_extension}_image_audio_{img_idx}.mp3")
            image[j]["img_text"] = translated_text
            image[j]["img_audio_url"] = f"https://storage.googleapis.com/{FINAL_BUCKET}/{image_folder_path}/{count}/{file_no_extension}_image_audio_{img_idx}.mp3"

    prepare_upload_json(data, FINAL_BUCKET)

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

def upload_json(data, path, load_bucket):
    print("SUCCESS in upload_json")
    print(data)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(load_bucket)
    blob = bucket.blob(path)

    blob.upload_from_string(json.dumps(data), content_type="application/json")
    print('File uploaded to {}.'.format(path))
    
def prepare_upload_json(data, load_bucket):
    print("SUCCESS in upload_json")
    print(len(data))
    for i in range(1, len(data) + 1):
        count = str(i)
        path = f"{json_folder_path}/{count}/{file_no_extension}_{count}.json"
        upload_json(data[str(i)], path, load_bucket)
        print('File uploaded to {}.'.format(
            f"{json_folder_path}/{count}/{file_no_extension}_{count}.json"))