# tts 사용하기
from google.cloud import storage
from google.cloud import texttospeech
import tempfile

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


def download_pdf(event, context):
    """
    Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print("in CF")
    print("event", event)

    global BUCKET, FILE_NAME, USER_ID, json_folder_path, json_filename, audio_folder_path, audio_full_filename, audio_one_filename, image_folder_path, file_no_extension, file_path

    BUCKET = event['bucket']
    FILE_NAME = event['name'].split('/')[-1]
    file_path = event['name']
    file_no_extension = FILE_NAME.split('.')[-2]
    USER_ID = event['name'].split('/')[0]
    if not file_path.endswith(".pdf"):
        print("Skipping request to handle", file_path)
        return

    json_folder_path = f'{USER_ID}/{file_no_extension}_json_folder'
    json_filename = f'{file_no_extension}_json'
    audio_folder_path = f'{USER_ID}/{file_no_extension}_audio_folder'
    audio_full_filename = file_no_extension + '_full_audio'
    audio_one_filename = file_no_extension + '_audio'
    image_folder_path = f'{USER_ID}/{file_no_extension}_image_folder'

    print("Extracting text from", file_path)
    print("USER_ID : ", USER_ID)
    print(json_folder_path)
    print(audio_folder_path)
    print(image_folder_path)
    client = storage.Client()
    bucket = client.get_bucket(BUCKET)

    pdf = tempfile.NamedTemporaryFile()

    temp_json = '''
    {
        "1": {
            "page_id": 1,
            "full_text": {
                "audio_url": "",
                "full_text": b"러시아 당국이 일간지 ‘노바야 가제타’를 폐쇄할지라도 그곳의 편집장인 드미트리 무라토프는 여전히 침묵 당하길 거부한다.

                BBC는 모스크바에서 2021년 노벨평화상 수상자이기도 한 무라토프 편집장을 만났다.

                무라토프 편집장은 러시아 당국이 서방과의 대결에서 과연 어디까지 나아갈지 걱정했다.

                “지난 2세대가 핵전쟁의 위협 없이 살아왔다”는 무라토프 편집장은 “그러나 이제 (평화의) 시대는 끝이 났다. 푸틴은 핵 버튼을 누를 것인가, 누르지 않을 것인가? 누가 알겠는가. 그 누구도 알지 못한다. (핵전쟁이 일어나지 않으리라고) 확실하게 말할 수 있는 사람은 단 한 명도 없다”고 말했다.\nData\n1\n"
            },
            "text": [
                {
                    "audio_url": "",
                    "font_size": 40,
                    "text": " 2\n"
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
    try:
        # Download blob into temporary file, extract, and uplaod.
        bucket.blob(file_path).download_to_filename(pdf.name)
        print(bucket, file_path, pdf.name)
        return upload_blob(temp_json, "upload.json")
    except Exception as err:
        print("Exception while extracting text", err)

# json 파일 업로드


def upload_blob(blob_text, destination_file_name):
    # destination_file_name : 폴더 경로까지 다 입력해야됨
    """Uploads a file to the bucket."""
    print("SUCCESS in upload_blob")
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(BUCKET)
    blob = bucket.blob(destination_file_name)

    blob.upload_from_string(blob_text)

    print('File uploaded to {}.'.format(
        destination_file_name))


def text_to_speech(text, fileName):
    print("Success in text_to_speech()")
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="ko",
        ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    print("tts fin")
    # The response's audio_content is binary.
    # fileName = "./audio_output/sample" + str(i) + "_" + str(j) + ".mp3"
    # with open(fileName, "wb") as out:
    #     # Write the response to the output file.
    #     out.write(response.audio_content)
    #     print('Audio content written to file ' + fileName)
