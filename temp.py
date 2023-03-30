from google.cloud import storage
import tempfile
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
from flask import abort


def on_finalized(event, _):
    """on_finalized is the Cloud Function entry point for handling GCS object
    finalized events. It downloads the specified PDF from GCS into a temporary
    file, extracts the text from that PDF, then uploads that text to a new GCS
    object.

    event -- the received GCS event. Includes the bucket name and the name of
        the finalized object.
    """
    bucket = event['bucket']
    objectName = event['name']
    # Skip non-PDF files: this function writes to the bucket it watches.
    if not objectName.endswith(".pdf"):
        print("Skipping request to handle", objectName)
        return

    print("Extracting text from", objectName)
    # Connect to GCS bucket.
    client = storage.Client()
    bucket = client.bucket(bucket)
    # Initialize temporary file for downloaded PDF.
    pdf = tempfile.NamedTemporaryFile()
    try:
        # Download blob into temporary file, extract, and uplaod.
        bucket.blob(objectName).download_to_filename(pdf.name)
        print(bucket, objectName, pdf.name)
        print("Success: extracted {} characters")
        get_text(pdf.name)
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
        each_page["page_id"] = int(page_layout.pageid)
        each_page["full_text"] = {"audio_url": "", "full_text": full_text}
        each_page["text"] = info
        extract_data[str(page_layout.pageid)] = each_page
    print(extract_data)
    return upload_json(extract_data, "extracted.json")
