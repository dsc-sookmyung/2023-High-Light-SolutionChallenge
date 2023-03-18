import fitz
import PIL.Image
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
import os
import json
import PIL.Image
import io
import re
import io
from io import BytesIO
import pandas as pd
from google.cloud import storage
from google.cloud import texttospeech

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./tts_api_key.json"
#! 다운받은 파일명을 어떻게 받지?
downloaded = 'StallingsOS8e-Chap04.pdf'
# downloaded = 'data_1.pdf'
cloud_bucket = 'cloud_storage_leturn'
split_file = list(downloaded.split('.'))
filename = split_file[0]
json_folder_path = filename + '_json_folder/'
json_filename = filename + '_json'
audio_folder_path = filename + '_audio_folder/'
audio_full_filename = filename + '_full_audio'
audio_one_filename = filename + '_audio'
image_folder_path = filename + '_image_folder/'
path = r'./' + filename + '.pdf'


def get_text(path):
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
        each_page["page_id"] = int(page_layout.pageid)
        each_page["full_text"] = {"audio_url": "", "full_text": full_text}
        each_page["text"] = info
        extract_data[str(page_layout.pageid)] = each_page
    return extract_data


# 정확도 높이기
def get_detailed(data):
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
    return data


def get_image(data, path, image_path):
    pdf = fitz.open(path)
    page_id = 1
    for i in range(len(pdf)):
        image_count = 1
        each_page = []
        local_image_path = image_path
        local_image_path += str(page_id)
        page = pdf[i]  # load page
        images = page.get_images()
        for image in images:
            if not os.path.exists(local_image_path):
                os.makedirs(local_image_path)
            base_img = pdf.extract_image(image[0])
            image_data = base_img['image']
            img = PIL.Image.open(io.BytesIO(image_data))
            extension = base_img['ext']
            img.save(
                open(local_image_path + f"/{filename}_image_{image_count}.{extension}", "wb"))
            each_page.append({
                "img_idx": image_count, "audio_url": "", "img_url": ""})
            image_count += 1
        data[str(page_id)]["image"] = each_page
        page_id += 1
    return data


# 텍스트 추출
extract_data = get_text(path)
extract_data = get_detailed(extract_data)

# text/image/audio url 생성
for i in range(1, len(extract_data) + 1):
    page = extract_data[str(i)]
    count = str(i)
    page["full_text"]["audio_url"] = f"https://storage.googleapis.com/{cloud_bucket}/{audio_folder_path}{count}/{filename}_full_audio_{count}.mp3"
    for j in range(len(page["text"])):
        line_count = str(j + 1)
        one_text_audio_url = page["text"][j]["audio_url"]
        page["text"][j]["audio_url"] = f"https://storage.googleapis.com/{cloud_bucket}/{audio_folder_path}{count}/{filename}_audio_{count}_{line_count}.mp3"
for each_page in os.listdir(image_folder_path):
    img_idx = 0
    for img in os.listdir(image_folder_path + each_page):
        # extract_data[each_page]["image"][img_idx][
        #     "img_url"] = f"https://storage.googleapis.com/{cloud_bucket}/{image_folder_path}{each_page}/{img}"
        print(extract_data[each_page])
        img_idx += 1
# 이미지 추출 및 폴더 저장
# if not os.path.exists(image_folder_path):
#     os.makedirs(image_folder_path)
# get_image(extract_data, path, image_folder_path)
get_image(extract_data, path, "image_extract/")
with open('get_url.json', 'w', encoding='utf-8') as make_file:
    json.dump(extract_data, make_file, indent="\t", ensure_ascii=False)
# print(extract_data)
