from google.cloud import storage


def upload_file(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Cloud Storage bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f'File {source_file_name} uploaded to {destination_blob_name}.')


# Example usage
upload_file('my-bucket', 'audio.mp3', 'audio/audio.mp3')
