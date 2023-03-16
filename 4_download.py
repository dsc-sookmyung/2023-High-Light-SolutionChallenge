import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./tts_api_key.json"

try:
    import io
    from io import BytesIO
    import pandas as pd
    from google.cloud import storage

except Exception as e:
    print("Some Modules are Missing {}".format(e))

storage_client = storage.Client.from_service_account_json(
    "./tts_api_key.json")

# GCP에서 파일 다운로드

bucket_name = 'cloud_storage_leturn'    # 서비스 계정 생성한 bucket 이름 입력
source_blob_name = 'os_5_folder/os_5_2.json'    # GCP에 저장되어 있는 파일 명
# 다운받을 파일을 저장할 경로("local/path/to/file")
local_image_path = './download'
if not os.path.exists(local_image_path):
    os.makedirs(local_image_path)

# 상대 경로에 저장되는 파일 이름
destination_file_name = './download/download_data_2.json'

storage_client = storage.Client()
bucket = storage_client.bucket(bucket_name)
blob = bucket.blob(source_blob_name)

blob.download_to_filename(destination_file_name)
print('fin')
