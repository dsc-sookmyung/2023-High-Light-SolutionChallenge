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
from PIL import Image

# 사용자 id/폴더 id/원본 파일
# 2/21/os_3.pdf
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

    # file_path = event['name']
    # file_path += ".pdf"
    # BUCKET = event['bucket']
    # FILE_NAME = file_path.split('/')[-1]
    # file_no_extension = FILE_NAME.split('.')[0]
    # USER_ID = event['name'].split('/')[0]
    BUCKET = event['bucket']
    FILE_NAME = event['name'].split('/')[-1]
    file_path = event['name']
    file_no_extension = FILE_NAME.split('.')[0]
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
    print(BUCKET)
    print(FILE_NAME)
    print(file_no_extension)
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)

    pdf = tempfile.NamedTemporaryFile()
    try:
        # Download blob into temporary file, extract, and uplaod.
        bucket.blob(file_path).download_to_filename(pdf.name)
        print(BUCKET, file_path, pdf.name)
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
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    val = f"{file_no_extension}_thumbnail.png"
    page = pdf.load_page(0)
    pix = page.get_pixmap(matrix=mat)
    img = pix.pil_tobytes(format="PNG", optimize=True)
    client = storage.Client()
    bucket = client.get_bucket(FINAL_BUCKET)
    blob = bucket.blob(f"{USER_ID}/{file_no_extension}_thumbnail.png")
    blob.upload_from_string(img)
    # upload_image(
    #     img, f"{USER_ID}/{file_no_extension}_sumnail.png", f"{FINAL_BUCKET}")
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
            upload_image(
                img, f"{image_folder_path}/{count}/{file_no_extension}_image_{image_count}.{extension}", f"{FINAL_BUCKET}")
            each_page.append({
                "img_idx": image_count, "img_url": f"https://storage.googleapis.com/{FINAL_BUCKET}/{image_folder_path}/{count}/{file_no_extension}_image_{image_count}.{extension}"})
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

    blob.upload_from_string(json.dumps(data), content_type="application/json")
    print('File uploaded to {}.'.format(path))


def upload_image(image_data, destination_blob_name, load_bucket):
    print("SUCCESS in upload_image")
    image_name = destination_blob_name.split('/')[-1]
    extension = destination_blob_name.split('.')[-1]

    # Storage Client에 Bucket,
    storage_client = storage.Client()
    # get_bucket에 bucket_name 설정
    bucket = storage_client.get_bucket(load_bucket)
    # blob 객체 선언 및 생성 file name 설정
    blob = bucket.blob(destination_blob_name)
    print(type(image_data))
    buffer = io.BytesIO()
    image_data.save(buffer, format=extension.upper())
    print("2")
    print(type(buffer.getvalue()))  # -> bytes면 넣기,,,
    bytes_img = buffer.getvalue()
    blob.upload_from_string(bytes_img)

    print("DONE upload_image")

# json 파일 업로드 확인 content-type 확인

# 확인한다음 upload_image
