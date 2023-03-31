from google.cloud import storage
import tempfile
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from flask import abort
import re
import os
import fitz
import PIL.Image
from PIL import Image
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


def download_pdf(event, context):
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
    if not file_path.endswith(".pdf"):
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
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)

    pdf = tempfile.NamedTemporaryFile()
    try:
        # Download blob into temporary file, extract, and uplaod.
        bucket.blob(file_path).download_to_filename(pdf.name)
        print(bucket, file_path, pdf.name)
        return get_text(pdf.name)
    except Exception as err:
        print("Exception while extracting text", err)


def get_text(path):
    print("Success in get_text()")
    # full-text, line-text 뽑기
    extract_data = {}
    for page_layout in extract_pages(path):
        each_page = {}
        info = []
        full_text = ''
        cur_size = 0
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    for character in text_line:
                        if isinstance(character, LTChar):
                            next_size = round(character.size)
                    if (cur_size != 0) or (cur_size != next_size):
                        cur_size = next_size
                        text = ""
                    if cur_size == next_size:
                        text += element.get_text()
                    info.append(
                        {"audio_url": "", "font_size": cur_size, "text": text})
                full_text += text
                print(full_text)
        each_page["page_id"] = int(page_layout.pageid)
        each_page["full_text"] = {"audio_url": "", "full_text": full_text}
        each_page["text"] = info
        extract_data[str(page_layout.pageid)] = each_page
    print(extract_data)
    # 이미지 추출 및 저장 -> 상대 경로 문제 해결 필요
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)

    pdf = tempfile.NamedTemporaryFile()
    try:
        # Download blob into temporary file, extract, and uplaod.
        bucket.blob(file_path).download_to_filename(pdf.name)
        print(bucket, file_path, pdf.name)
        return get_image(extract_data, pdf.name)
    except Exception as err:
        print("Exception while extracting text", err)


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
            #! 이미지 업로드 다시 해야됨
            upload_image(
                img, f"{image_folder_path}/{count}/{file_no_extension}_image_{image_count}.{extension}", "cloud_storage_leturn")
            each_page.append({
                "img_idx": image_count, "img_url": f"https://storage.googleapis.com/{BUCKET}/{image_folder_path}/{count}/{file_no_extension}_image_{image_count}.{extension}"})
            image_count += 1
        data[str(page_id)]["image"] = each_page
        page_id += 1
    print(data)
    upload_json(data, f"{USER_ID}/{file_no_extension}.json",
                "middle-temporary")

# json upload


def upload_json(data, path, load_bucket):
    print("SUCCESS in upload_json")
    print(data)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(load_bucket)
    blob = bucket.blob(path)

    blob.upload_from_string(json.dumps(data)).encode(
        'utf-8', content_type="application/json")
    print('File uploaded to {}.'.format(path))


def upload_image(image_data, destination_blob_name, load_bucket):
    print("SUCCESS in upload_image")
    extension = destination_blob_name.split('.')[-1]
    # Storage Client에 Bucket,
    storage_client = storage.Client()
    # get_bucket에 bucket_name 설정
    bucket = storage_client.get_bucket(load_bucket)
    # blob 객체 선언 및 생성 file name 설정
    blob = bucket.blob(destination_blob_name)
    Image.save(image_data, extension)

    blob.upload_from_string(image_data.getvalue())
    blob.make_public()
    print("DONE upload_image")
