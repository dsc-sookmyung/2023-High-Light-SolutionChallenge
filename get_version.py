def upload_file(upload_file, file_name, new_width=500):

    blob = bucket.blob(file_name)
    pil_img = Image.open(upload_file)
    new_height = int(new_width/pil_img.size[0]*pil_img.size[1])
    pil_img = pil_img.resize((new_width, new_height))
    b = io.BytesIO()
    pil_img.save(b, 'jpg')
    pil_img.close()
    blob.upload_from_string(b.getvalue(), content_type=’image/jpeg’)
    blob.make_public()
    return blob.public_url
