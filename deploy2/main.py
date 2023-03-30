from google.cloud import storage
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
    # client = storage.Client()
    # bucket = client.get_bucket(BUCKET)

    # pdf = tempfile.NamedTemporaryFile()
    # try:
    #     # Download blob into temporary file, extract, and uplaod.
    #     bucket.blob(file_path).download_to_filename(pdf.name)
    #     print(bucket, file_path, pdf.name)
    #     return get_image(data, pdf.name)
    # except Exception as err:
    #     print("Exception while extracting text", err)


def get_image(data, path):
    print("Success in get_image")
    # 이미지 추출
    pdf = fitz.open(path)
    print("success fitz.open")  # 여기까지 성공
    page_id = 1
    for i in range(len(pdf)):
        image_count = 1
        each_page = []
        count = str(page_id)
        page = pdf[i]  # load page
        images = page.get_images()
        print("After images = page.get_images()")
        for image in images:
            # if not os.path.exists(f"{image_folder_path}/{count}"):
            #     os.makedirs(f"{image_folder_path}/{count}")
            base_img = pdf.extract_image(image[0])
            image_data = base_img['image']
            img = PIL.Image.open(io.BytesIO(image_data))
            extension = base_img['ext']
            print("SUCCESS PIL.image")
            # #! 이미지 파일 저장 -> 수정 필요
            # img.save(
            #     open(f"{image_folder_path}/{count}/{filename}_image_{image_count}.{extension}", "wb"))
            # #! ---
            upload_image(
                img, f"{file_no_extension}_image_{image_count}.{extension}", f"{image_folder_path}/{count}/{file_no_extension}_image_{image_count}.{extension}")
            each_page.append({
                "img_idx": image_count, "img_url": f"https://storage.googleapis.com/{BUCKET}/{image_folder_path}/{count}/{file_no_extension}_image_{image_count}.{extension}"})
            image_count += 1
        data[str(page_id)]["image"] = each_page
        page_id += 1
    print("fin get_image")
    return prepare_upload_json(data, "leturn-file-bucket")
