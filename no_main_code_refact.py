from google.cloud import storage
import tempfile
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from flask import abort
import re


BUCKET = ""
FILE_NAME = ""
USER_ID = ""
file_no_extension = ''
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

    global BUCKET, FILE_NAME, USER_ID, json_folder_path, json_filename, audio_folder_path, audio_full_filename, audio_one_filename, image_folder_path, file_no_extension

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
                # full_text = full_text.decode('utf-8')
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

    # 이미지 추출 및 저장 -> 상대 경로 문제 해결 필요
    get_image(data)

    return data

# 추가 모듈: fitz, os, PIL. io


def get_image(data, path):
    # 이미지 추출
    pdf = fitz.open(path)
    page_id = 1
    for i in range(len(pdf)):
        image_count = 1
        each_page = []
        count = str(page_id)
        page = pdf[i]  # load page
        images = page.get_images()
        for image in images:
            if not os.path.exists(f"{image_folder_path}/{count}"):
                os.makedirs(f"{image_folder_path}/{count}")
            base_img = pdf.extract_image(image[0])
            image_data = base_img['image']
            img = PIL.Image.open(io.BytesIO(image_data))
            extension = base_img['ext']
            #! 이미지 파일 저장 -> 수정 필요
            img.save(
                open(f"{image_folder_path}/{count}/{filename}_image_{image_count}.{extension}", "wb"))
            #! ---
            each_page.append({
                "img_idx": image_count, "img_url": f"https://storage.googleapis.com/{BUCKET}/{image_folder_path}/{count}/{file_no_extension}_image_{image_count}.{extension}", "audio_url": ""})
            image_count += 1
        data[str(page_id)]["image"] = each_page
        page_id += 1
    return data

# upload_json -> 진짜 경로에 따라 json 파일 하나만 추가될 수 있게끔
