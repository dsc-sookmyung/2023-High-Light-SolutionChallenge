from google.cloud import storage
import json
import re

FINAL_BUCKET = "cloud_storage_leturn"
BUCKET = ""
FILE_NAME = ""
USER_ID = ""
file_no_extension = ''
file_path = ''
json_folder_path = ''
json_filename = ''
audio_folder_path = ''
audio_full_filename = ''
audio_one_filename = ''
image_folder_path = ''


def download_json(event, context):

    global BUCKET, FILE_NAME, USER_ID, json_folder_path, json_filename, audio_folder_path, audio_full_filename, audio_one_filename, image_folder_path, file_no_extension, file_path

    BUCKET = event['bucket']
    FILE_NAME = event['name'].split('/')[-1]
    file_path = event['name']
    file_no_extension = FILE_NAME.split('.')[-2]
    USER_ID = event['name'].split('/')[0]
    if not file_path.endswith(".json"):
        print("Skipping request to handle", file_path)
        return

    json_folder_path = f'{USER_ID}/{file_no_extension}_json_folder'
    json_filename = f'{file_no_extension}_json'
    audio_folder_path = f'{USER_ID}/{file_no_extension}_audio_folder'
    audio_full_filename = file_no_extension + '_full_audio'
    audio_one_filename = file_no_extension + '_audio'
    image_folder_path = f'{USER_ID}/{file_no_extension}_image_folder'

    print("Extracting text from", file_path)
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)
    file_blob = bucket.get_blob(file_path)
    download_data = file_blob.download_as_string()
    download_data = json.loads(download_data)
    print(download_data)

    get_detailed(download_data)


def get_detailed(data):
    # improve detail
    print('SUCCESS in get_detailed')
    print("downloaded json data: ", data)
    cur_size = 0
    text = ""
    # 줄바꿈 기준 쪼개고 글씨크기 기준으로 정확히 나누기
    for i in range(1, len(data) + 1):
        each_page_size = len(data[str(i)]["text"])
        each_page = data[str(i)]["text"]
        for j in range(each_page_size - 1):
            cur_text = each_page[j]["text"]
            cur_text = str.encode(cur_text)
            cur_text = cur_text.decode('utf-8')
            next_text = each_page[j + 1]["text"]
            next_text = str.encode(next_text)
            next_text = next_text.decode('utf-8')
            if cur_text == next_text:
                split_list = cur_text.split("\n")
                for k in range(len(split_list)):
                    text = str.encode(text)
                    text = split_list[k] + "\n"
                    text = re.sub(r"[^\w\s]]", "", text)
                    if split_list[k] != '':
                        font_size = each_page[j + k]["font_size"]
                    if text == "\n":
                        continue
                    else:
                        each_page[j + k] = {"audio_url": "",
                                            "font_size": font_size, "text": text}

    print("get_detailed first for fin")
    print(data)
    concat_text = ""
    for i in range(1, len(data)):
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

    print("get_detailed second for fin")
    return get_text_audio_url(data)


def get_text_audio_url(data):
    # text/audio url 생성
    for i in range(1, len(data) + 1):
        count = str(i)
        page = data[count]
        page["full_text"]["audio_url"] = f"https://storage.googleapis.com/{FINAL_BUCKET}/{audio_folder_path}/{count}/{file_no_extension}_full_audio_{count}.mp3"
        for j in range(len(page["text"])):
            line_count = str(j + 1)
            page["text"][j]["audio_url"] = f"https://storage.googleapis.com/{FINAL_BUCKET}/{audio_folder_path}/{count}/{file_no_extension}_audio_{count}_{line_count}.mp3"

    print("FIN get_datailed()")
    prepare_upload_json(data, "cloud_storage_leturn")
    upload_json(data, f"{USER_ID}/{file_no_extension}.json",
                'middle-temporary-2')


def upload_json(data, path, load_bucket):
    print("SUCCESS in upload_json")
    print(data)
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(load_bucket)
    blob = bucket.blob(path)

    blob.upload_from_string(json.dumps(data), content_type="application/json")
    print('File uploaded to {}.'.format(path))


def prepare_upload_json(data, load_bucket):
    print("SUCCESS in upload_json")
    print(len(data))
    for i in range(1, len(data) + 1):
        count = str(i)
        path = f"{json_folder_path}/{count}/{file_no_extension}_{count}.json"
        upload_json(data[str(i)], path, load_bucket)
        print('File uploaded to {}.'.format(
            f"{json_folder_path}/{count}/{file_no_extension}_{count}.json"))

    print("DONE prepare_upload_json")
    print("DONE extract-data-2")
