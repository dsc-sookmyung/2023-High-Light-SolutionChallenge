import os
import tempfile
import uuid
from google.cloud import storage
from PIL import Image


def upload_image_to_bucket(data, context):
    # Get the file name and bucket name from the event data.
    file_name = data['name']
    bucket_name = data['bucket']

    # Create a client object for the bucket.
    client = storage.Client()

    # Create a new blob object with a random name.
    blob_name = str(uuid.uuid4())
    blob = client.bucket(bucket_name).blob(blob_name)

    # Open the PIL Image from the bytes data.
    image = Image.open(data['mediaLink'])

    # Convert the PIL Image to bytes.
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        image.save(tmp, format='JPEG')
        tmp.flush()
        blob.upload_from_filename(tmp.name)

    # Set the content type and cache control for the blob.
    blob.content_type = 'image/jpeg'
    blob.cache_control = 'max-age=31536000'

    # Set any desired metadata for the blob.
    blob.metadata = {
        'uploaded_by': 'my-function'
    }
    blob.patch()

    print(
        f"Uploaded image '{file_name}' to bucket '{bucket_name}' as '{blob_name}'")
