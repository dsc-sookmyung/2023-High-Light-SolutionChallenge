from google.cloud import storage
import base64
import json
import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
import tempfile
import re
import fitz
import PIL.Image  # 이거 모듈 뭐야?

BUCKET = ""
FILE_NAME = ""
USER_ID = ""
json_folder_path = ''
json_filename = ''
audio_folder_path = ''
audio_full_filename = ''
audio_one_filename = ''
image_folder_path = ''
# 프론트에서 백으로 올리는 원본 버킷이 leturn-file-bucket
# ML에서 가공한 데이터를 올리는 버킷이 cloud_storage_leturn


def download_pdf(event, context):
    """
    Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print("in CF")
    print("event", event)

    global BUCKET, FILE_NAME, USER_ID, json_folder_path, json_filename, audio_folder_path, audio_full_filename, audio_one_filename, image_folder_path

    BUCKET = event['bucket']
    FILE_NAME = event['name'].split('/')[-1]
    file_no_extension = FILE_NAME.split('.')[-2]
    USER_ID = event['name'].split('/')[0]
    if not FILE_NAME.endswith(".pdf"):
        print("Skipping request to handle", FILE_NAME)
        return

    json_folder_path = f'{USER_ID}/{file_no_extension}_json_folder'
    json_filename = f'{file_no_extension}_json'
    audio_folder_path = f'{USER_ID}/{file_no_extension}_audio_folder'
    audio_full_filename = file_no_extension + '_full_audio'
    audio_one_filename = file_no_extension + '_audio'
    image_folder_path = f'{USER_ID}/{file_no_extension}_image_folder'

    print("Extracting text from", FILE_NAME)
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)

    pdf = tempfile.NamedTemporaryFile()
    try:
        # Download blob into temporary file, extract, and uplaod.
        bucket.blob(FILE_NAME).download_to_filename(pdf.name)
        print(bucket, FILE_NAME, pdf.name)
        return get_text(pdf.name)
    except Exception as err:
        print("Exception while extracting text", err)


def upload_json(json_object, filename):
    '''
    this function will create json object in
    google cloud storage
    '''
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)

    # create a blob
    blob = bucket.blob(filename)
    # upload the blob
    blob.upload_from_string(
        data=json.dumps(json_object, ensure_ascii=False).encode('utf-8'),
        content_type='application/json'
    )
    result = filename + ' upload complete'
    print(result)
    return {'response': result}

# def init_text_audio_url(data):
#     for i in range(1, len(data) + 1):
#         count = str(i)
#         page = data[count]
#         page["full_text"]["audio_url"] = f"https://storage.googleapis.com/{BUCKET}/{audio_folder_path}/{count}/{filename}_full_audio_{count}.mp3"


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
                        {"audio_url": "", "font_size": cur_size, "text": str(text, 'utf-8')})
                full_text += text
        each_page["page_id"] = int(page_layout.pageid)
        each_page["full_text"] = {"audio_url": "",
            "full_text": str(full_text, 'utf-8')}
        each_page["text"] = info
        extract_data[str(page_layout.pageid)] = each_page
    print(extract_data)
    return upload_json(extract_data, "encode.json")


def get_detailed(data):
    # 정확도 높이기
    cur_size = 0
    text = ""
    # 줄바꿈 기준 쪼개고 글씨크기 기준으로 정확히 나누기
    for i in range(1, len(data) + 1):
        each_page_size = len(data[str(i)]["text"])
        each_page = data[str(i)]["text"]
        for j in range(each_page_size - 1):
            cur_text = each_page[j]["text"]
            next_text = each_page[j + 1]["text"]
            if cur_text == next_text:
                split_list = each_page[j]["text"].split("\n")
                for k in range(len(split_list)):
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
    return get_image(data


def get_image(data, path, image_path):
    # 이미지 추출
    pdf=fitz.open(path)
    page_id=1
    for i in range(len(pdf)):
        image_count=1
        each_page=[]
        count=str(page_id)
        page=pdf[i]  # load page
        images=page.get_images()
        for image in images:
            if not os.path.exists(f"{image_path}/{count}"):
                os.makedirs(f"{image_path}/{count}")
            base_img=pdf.extract_image(image[0])
            image_data=base_img['image']
            img=PIL.Image.open(io.BytesIO(image_data))
            extension=base_img['ext']
            img.save(
                open(f"{image_path}/{count}/{filename}_image_{image_count}.{extension}", "wb"))
            each_page.append({
                "img_idx": image_count, "img_url": f"https://storage.googleapis.com/{cloud_bucket}/{image_path}/{count}/{filename}_image_{image_count}.{extension}", "audio_url": ""})
            image_count += 1
        data[str(page_id)]["image"]=each_page
        page_id += 1
    return data

# trigger-gcs 확인해야되는 것
# 배포가 되는지 확인하기 -> 만약 된다면 upload_json이 문제
# str(text, 'utf-8')으로 수정을 하였으므로 텍스트가 한국어로 나오는지 확인해보기
