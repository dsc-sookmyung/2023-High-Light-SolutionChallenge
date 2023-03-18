downloaded = 'StallingsOS8e-Chap04.pdf'
split_file = list(downloaded.split('.'))
filename = split_file[0]
json_folder_path = filename + '_json_folder'
json_file_path = json_folder_path + '/' + filename + '_json'
audio_folder_path = filename + '_audio_folder'
audio_full_file_path = filename + '_full_audio'
audio_one_file_path = filename + 'audio'
image_folder_path = filename + '_image_folder'
image_file_path = './' + filename + '/'
path = r'./' + filename + '.pdf'

print("filename: ", filename)
print("json_folder_path: ", json_folder_path)
print("json_file_path: ", json_file_path)
print("audio_folder_path: ", audio_folder_path)
print("audio_full_file_path: ", audio_full_file_path)
print("audio_one_file_path: ", audio_one_file_path)
print("image_folder_path: ", image_folder_path)
print("image_file_path: ", image_file_path)
