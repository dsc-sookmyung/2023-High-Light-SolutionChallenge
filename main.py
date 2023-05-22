import json
import requests
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from google.cloud import storage
import json
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

    raw_image = Image.open(requests.get(
        img_url, stream=True).raw).convert('RGB')

    inputs = processor(raw_image, return_tensors="pt")

    out = model.generate(**inputs)
    image_caption = processor.decode(out[0], skip_special_tokens=True)
    return image_caption


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


def for_making_caption(data):
    print("SUCCESS in for_making_caption")
    for i in range(1, len(data) + 1):
        count = str(i)
        image = data[count]["image"]
        for j in range(len(image)):
            print(image[j]["img_url"])
            img_idx = image[j]["img_idx"]
            image_caption = gen_image_caption(image[j]["img_url"])
            print(image_caption)
            translator = Translator()
            result = translator.translate(image_caption, dest='ko')
            text_to_speech(
                result.text, f"{image_folder_path}/{count}/{file_no_extension}_image_audio_{img_idx}.mp3")
            image[j]["img_text"] = image_caption
            image[j]["img_audio_url"] = f"https://storage.googleapis.com/{FINAL_BUCKET}/{image_folder_path}/{count}/{file_no_extension}_image_audio_{img_idx}.mp3"
