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
    "./backend_test.json")

# GCP에 파일 올리기
bucket = storage_client.get_bucket('cloud_storage_leturn')

# 폴더 통채로 storage에 올리기
folder = 'os_4' + '_folder'

for filename in os.listdir(folder):
    # GCP에 올릴 파일 이름
    blob = bucket.blob(folder + '/' + filename)

    with open(folder + '/' + filename, 'rb') as f:
        blob.upload_from_file(f)

# 파일 올리기
# bucket = storage_client.get_bucket('cloud_storage_leturn')
# filename = 'StallingsOS8e-Chap04.pdf'
# blob = bucket.blob(filename)

# with open(filename, 'rb') as f:
#     blob.upload_from_file(f)
# blob = bucket.blob(filename)


print("Upload complete")
