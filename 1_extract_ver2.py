import fitz
import PIL.Image
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
import os
import json
import PIL.Image
import io
import re

# full-text, line-text 뽑기


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
    for i in range(1, len(extract_data) + 1):
        each_page_size = len(extract_data[str(i)]["text"])
        each_page = extract_data[str(i)]["text"]
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

# 이미지 추출


def get_image(data, path, image_path):
    pdf = fitz.open(path)
    page_id = 1
    for i in range(len(pdf)):
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
                open(local_image_path + f"/image{page_id}.{extension}", "wb"))
        data[str(page_id)]["image"] = {
            "img_idx": 1, "audio_url": "", "img_url": ""}
        page_id += 1
    return data


filename = "data_2"
image_path = './' + filename + '/'
path = r'./' + filename + '.pdf'

# 텍스트 추출
extract_data = get_text(path)
extract_data = get_detailed(extract_data)
# 이미지 추출
get_image(extract_data, path, image_path)

if not os.path.exists(filename + '_folder'):
    os.makedirs(filename + '_folder')

for i in range(1, len(extract_data) + 1):
    each_page = extract_data[str(i)]
    with open(filename + '_folder' + './' + filename + '_' + str(i) + '.json', 'w', encoding='utf-8') as make_file:
        json.dump(each_page, make_file, indent="\t", ensure_ascii=False)
print("fin")