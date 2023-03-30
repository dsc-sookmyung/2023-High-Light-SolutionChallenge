from google.cloud import storage
import base64
import json
import os
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTLine, LAParams
import tempfile
import re

BUCKET = ""
FILE_NAME = ""
USER_ID = ""
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

    BUCKET = event['bucket']
    FILE_NAME = event['name']
    USER_ID = [event['name'].split('/')][0]
    if not FILE_NAME.endswith(".pdf"):
        print("Skipping request to handle", FILE_NAME)
        return

    json_folder_path = f'{USER_ID}/{FILE_NAME}_json_folder'
    json_filename = f'{FILE_NAME}_json'
    audio_folder_path = f'{USER_ID}/{FILE_NAME}_audio_folder'
    audio_full_filename = FILE_NAME + '_full_audio'
    audio_one_filename = FILE_NAME + '_audio'
    image_folder_path = f'{USER_ID}/{FILE_NAME}_image_folder'

    print("Extracting text from", FILE_NAME)
    print("USER_ID : ", USER_ID)
    print(json_folder_path)
    print(audio_folder_path)
    print(image_folder_path)
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)

    temp = {
        "type": "service_account",
        "project_id": "heroic-habitat-376713",
        "private_key_id": "240e39aa3e4a765e0a880033f307339b0a51958b",
        "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCdUP/ZhVCrJwcb\nL1aOe/3ac8SWcgTjMMkmCUocw1kdvv5Hw3NhJlKKURz9rhBnm2pxQjnKq4zhyO3B\n1fln5PSOSTz0iMObJ/eULjNNgASyrldq76XqxlS7n++9p2rRHn+CtpSwRgFIo4N0\nMnKbDvvvGgTdeyPEWaiFqM/ENi+NgpiT6PfGqYE/TrNABJvM5dyn1vCPZGFNH/T2\ne4l5cg0TIxzJYUIS7U2Tj8BJ6SHFjpH+vCs4PDtYT0GGIm6Zq6q9djYEsZzw7C1t\nt2wpmfO1uQlllhTzgRp6IEYTmn9ImfTcHxxAEol5Gun1OeuIJd5XumvOdSArOCnC\n+YfyoWLRAgMBAAECggEANfU21BZwXUv1GYNqllN79gYYKxvvhjdQ/t1X0LbGJbhB\nQj8NH4jD7dI1deNSmB7L6w3ygYvGthizR/VK5rI2mWkQYbVZFiomtmoESbQ7qEe5\nDyIkj/q3zGTml2/JaPGjfaN/K1jPjukaqOu2uG1yxwdvHMJkObAg57tHi/6j386e\nFrQtJv6FAcao4Mb+maQtoYccDjG8q7inOZOWghNhmu4DPoLkqv5A+ESiVLuSlB/h\nQeQUq1JcwRKV9DcNoy8uxohWDwKcGMpUOQj8rnJqUm/g2xlpUQVNIcSi/Z9r8s5P\nZ+LhmGmcb31ZT80QVFC2kl3kAEuH/SmDn2B8DhAmMwKBgQDRycW3s2DfhizTABl3\npgiLRT/MMG8J5iTphpcuXzuBlJOODpSCIxGWuC4Js8DeBOeSttBXChJGiCUwVZ7R\nhgvLm+ChHE77C3MTC/us1jLk/5N0PRg+G6FVCzkxKeJfhS4TVpXA9lRpplDseS1a\nDrtpDm/Xp+KNEfOGP/PmCAto0wKBgQC/+EadHPB423edHrR3NTAzlCJPgIR1Y5sc\n55g7rGwErupqDtRYDQaHxqc0qRkEc77ERHvSF3Rc/dz3MnkO10oXuYTm5X8QH2b+\ntAOaBeJx4USHKt5mIWXgbG2iwXp4gzntiNAu0VP46yhTICZT8suzlkjn9SyDC0+w\nK+okGvN/SwKBgDZ49t7ZM+k2VMNA/lvj/8nx5Dvnw51FZgZBDVZcIf5mjt3PCV61\nLmb9Ue7w/r5ndZ3R3E0Nb2tjBI0FXmS3Mq7evbf3usZS1cF3VhUt1S9C8Y24I2hV\nElIbxPDwGDiHQ0yAKghdrdN0/QQ5/r2on58KwZ20mQ3aQGp2hqUPJ69DAoGAOsDo\nC8oBp1u0PjhZj2qN+BtMbPyujacQoEYZh5n77WsDf7ZOMyy5ZPDd1/YxG/W42yUC\nqIhZKuTfriCagHpPyPcUv/5ZZzvVL/s0Zv2KEsSZTq1GKAfswEUvQPLqYtv27MZE\nwS97/eErFFXwpRzYT3ydj7CwEONzXj3yiV5eTAUCgYAL9JCD7zVd/aq1ImHskCti\nxf3fBGSTrr9Vmd90GNWWRDGV4acaoWvyM5MMNvIH9p0kpdaD0a0nsfIV2pQpCYOn\nkaRAE2lSaQiBru4pOzMDp89Qb4QLy+Ox3CUYdvN/t0pBTTtlZkPZko/++zcTxWYr\noAV8BzlvSOBPBXEnMGCyDg==\n-----END PRIVATE KEY-----\n",
        "client_email": "tts-api@heroic-habitat-376713.iam.gserviceaccount.com",
        "client_id": "109228275188240992905",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/tts-api%40heroic-habitat-376713.iam.gserviceaccount.com"
    }
    upload_json(temp, "author.json")
    pdf = tempfile.NamedTemporaryFile()
    try:
        # Download blob into temporary file, extract, and uplaod.
        bucket.blob(FILE_NAME).download_to_filename(pdf.name)
        print(bucket, FILE_NAME, pdf.name)
    except Exception as err:
        print("Exception while extracting text", err)


def upload_json(json_object, FILE_NAME):
    '''
    this function will create json object in
    google cloud storage
    '''
    print("SUCCESS in upload_json")
    # create a blob
    blob = BUCKET.blob(FILE_NAME)
    # upload the blob
    blob.upload_from_string(
        data=json.dumps(json_object, ensure_ascii=False).encode('utf-8'),
        content_type='application/json'
    )
    result = FILE_NAME + ' upload complete'
    print(result)
    return {'response': result}
