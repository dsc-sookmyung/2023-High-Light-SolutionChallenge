from google.cloud import storage

from flask import abort

DES_BUCKET = "cloud_storage_leturn"
TO_BUCKET = "leturn-file-bucket"


def download_pdf(event, context):
    json_file = '''
    {
        "1": {
            "page_id": 1,
            "full_text": {
                "audio_url": "",
                "full_text": "손수경 2\nData\n1\n"
            },
            "text": [
                {
                    "audio_url": "",
                    "font_size": 40,
                    "text": "Chapter 2\n"
                },
                {
                    "audio_url": "",
                    "font_size": 32,
                    "text": "Data\n"
                },
                {
                    "audio_url": "",
                    "font_size": 14,
                    "text": "1\n"
                }
            ],
            "image": {
                "img_idx": 1,
                "audio_url": "",
                "img_url": ""
            }
	    }
    }
    '''
    upload_json(json_file, 'new.json')


def upload_json(json_file, destination_file_name):
    # destination_file_name : 폴더 경로까지 다 입력해야됨
    """Uploads a file to the bucket."""
    print("SUCCESS in upload_json")

    storage_client = storage.Client()
    bucket = storage_client.get_bucket(TO_BUCKET)
    blob = bucket.blob(destination_file_name)

    blob.upload_from_string(json_file)

    print('File uploaded to {}.'.format(
        destination_file_name))
    return
