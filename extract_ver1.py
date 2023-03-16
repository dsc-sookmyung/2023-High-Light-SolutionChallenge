import fitz
import PIL.Image
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
import os
import json
import PIL.Image
import io
import re


# full-text -> image 순으로 페이지당으로 나옴
def get_fullText_image(path):
    extract_data = {}
    pdf = fitz.open(path)
    page_id = 1
    for i in range(len(pdf)):
        each_page = {}
        page = pdf[i]  # load page
        images = page.get_images()
        text = page.get_text('sentences')

        for image in images:
            base_img = pdf.extract_image(image[0])
            image_data = base_img['image']
            img = PIL.Image.open(io.BytesIO(image_data))
            extension = base_img['ext']
            img.save(
                open(f"temp_dataset/split_pages/image{page_id}.{extension}", "wb"))
        each_page["page_id"] = page_id
        full_text_data = {"audio_url": "", "full_text": text}
        each_page["full_text"] = full_text_data
        extract_data[str(page_id)] = each_page
        page_id += 1
    return extract_data


# line-text 페이지당으로 나옴
def get_lineText(data, path):
    for page_layout in extract_pages(path):
        each_page = {}
        info = []
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

        data[str(page_layout.pageid)]["text"] = info
    return data

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
                info = []
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
            # j = 0
            # while j != each_page_size - 1:
            cur_size = each_page[j]["font_size"]
            next_size = each_page[j + 1]["font_size"]
            if cur_size == next_size:
                concat_text += each_page[j + 1]["text"]
                to_del_list.append(j)
                # del(each_page[j + 1])
            else:
                each_page[j]["text"] = concat_text
                concat_text = each_page[j + 1]["text"]
                # to_del_list.append(j - 1)
                j += 1
        # print(to_del_list)
        # 반복문을 통해서 리스트 뒤에서부터 지우기
        # 스택이나 큐를 사용해서 제거
        list_len = len(to_del_list)
        for j in range(list_len - 1, -1, -1):
            del(each_page[to_del_list[j]])
        #     print(to_del_list[j])
        # print()


filename = "os_3"
path = r'./' + filename + '.pdf'

data = get_fullText_image(path)
extract_data = get_lineText(data, path)
get_detailed(extract_data)

with open('./' + filename + '.json', 'w', encoding='utf-8') as make_file:
    json.dump(extract_data, make_file, indent="\t", ensure_ascii=False)
print("fin")
