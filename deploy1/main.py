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

# json upload


def upload_json(data, path, load_bucket):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(load_bucket)
    blob = bucket.blob(path)

    blob.upload_from_string(data, content_type="application/json")


def prepare_upload_json(data, load_bucket):
    print("SUCCESS in upload_json")
    print(len(data))
    for i in range(1, len(data) + 1):
        count = str(i)
        path = f"{json_folder_path}/{count}/{file_no_extension}_{count}.json"
        upload_json(json.dumps(data[str(i)]).encode(
            'utf-8'), path, load_bucket)
        print('File uploaded to {}.'.format(
            f"{json_folder_path}/{count}/{file_no_extension}_{count}.json"))

    print("fin prepare_upload_json")


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
    return get_detailed(extract_data)


def get_detailed(data):
    # 정확도 높이기
    print('SUCCESS in get_detailed')
    cur_size = 0
    text = ""
    # 줄바꿈 기준 쪼개고 글씨크기 기준으로 정확히 나누기
    for i in range(1, len(data) + 1):
        each_page_size = len(data[str(i)]["text"])
        each_page = data[str(i)]["text"]  # 리스트 형식
        for j in range(each_page_size - 1):
            cur_text = each_page[j]["text"]  # str인 바이트 코드
            cur_text = str.encode(cur_text)
            cur_text = cur_text.decode('utf-8')
            print("cur_text: ", cur_text)
            next_text = each_page[j + 1]["text"]
            next_text = str.encode(next_text)
            next_text = next_text.decode('utf-8')
            if cur_text == next_text:
                split_list = cur_text.split("\n")
                print('if cur_text == next_text:', split_list)
                for k in range(len(split_list)):
                    text = str.encode(text)
                    text = split_list[k] + "\n"
                    text = re.sub(r"[^\w\s]]", "", text)  # import re
                    if split_list[k] != '':
                        font_size = each_page[j + k]["font_size"]
                    if text == "\n":
                        continue
                    else:
                        each_page[j + k] = {"audio_url": "",
                                            "font_size": font_size, "text": text}

    # 글씨 크기 같은 애들은 묶기
    print("get_detailed first for fin")  # 헐,,, 여기까지 끝냄
    print(data)
    concat_text = ""
    for i in range(1, len(data) + 1):
        each_page_size = len(data[str(i)]["text"])
        each_page = data[str(i)]["text"]
        concat_text = each_page[0]["text"]
        to_del_list = []
        for j in range(each_page_size - 1):
            cur_size = each_page[j]["font_size"]
            next_size = each_page[j + 1]["font_size"]
            if cur_size == next_size:
                concat_text += each_page[j + 1]["text"]
                to_del_list.append(j)
            else:
                each_page[j]["text"] = concat_text
                concat_text = each_page[j + 1]["text"]
                j += 1
        list_len = len(to_del_list)
        for j in range(list_len - 1, -1, -1):
            del(each_page[to_del_list[j]])

    print("get_detailed second for fin")
    print(data)
    return get_text_audio_url(data)


def get_text_audio_url(data):
    # text/audio url 생성
    for i in range(1, len(data) + 1):
        count = str(i)
        page = data[count]
        page["full_text"]["audio_url"] = f"https://storage.googleapis.com/{BUCKET}/{audio_folder_path}/{count}/{file_no_extension}_full_audio_{count}.mp3"
        for j in range(len(page["text"])):
            line_count = str(j + 1)
            page["text"][j]["audio_url"] = f"https://storage.googleapis.com/{BUCKET}/{audio_folder_path}/{count}/{file_no_extension}_audio_{count}_{line_count}.mp3"

    print(data)
    print("FIN get_datailed()")

    upload_json(data, f'{USER_ID}/temp_{FILE_NAME}', "temporay")


# 2. upload_json 함수를 통해서 이미지도 올려지는지 -> 이미지는 안올라감 <PIL.PngImagePlugin.PngImageFile image mode=RGBA size=403x7 at 0x3E0809920D50> could not be converted to bytes
# 지금 배포 중인 extract-data는 안될 가능성이 높음 -> image_file 자체가 바이트가 아닌 것 같음.
