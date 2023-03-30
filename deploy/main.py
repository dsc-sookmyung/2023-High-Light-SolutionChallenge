from google.cloud import storage
import base64
import json
import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
import tempfile

BUCKET = ""
FILE_NAME = ""

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

    BUCKET = event['bucket']
    FILE_NAME = event['name']
    if not FILE_NAME.endswith(".pdf"):
        print("Skipping request to handle", FILE_NAME)
        return

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
    # create a blob
    blob = BUCKET.blob(filename)
    # upload the blob
    blob.upload_from_string(
        data=json.dumps(json_object),
        content_type='application/json'
    )
    result = filename + ' upload complete'
    print(result)
    return {'response': result}


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
                        text.encode(encoding='utf-8', errors='ignore')
                    info.append(
                        {"audio_url": "", "font_size": cur_size, "text": text})
                full_text += text
        each_page["page_id"] = int(page_layout.pageid)
        each_page["full_text"] = {"audio_url": "", "full_text": full_text}
        each_page["text"] = info
        extract_data[str(page_layout.pageid)] = each_page
    print(extract_data)
    return upload_json(extract_data, "extracted.json")
