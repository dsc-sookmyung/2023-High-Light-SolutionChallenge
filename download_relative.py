import fitz
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar


def get_text(path):
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
        each_page["page_id"] = int(page_layout.pageid)
        each_page["full_text"] = {"audio_url": "", "full_text": full_text}
        each_page["text"] = info
        extract_data[str(page_layout.pageid)] = each_page
    return extract_data
