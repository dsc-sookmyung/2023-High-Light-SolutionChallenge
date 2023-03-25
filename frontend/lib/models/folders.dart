class Folders {
  final int folderId;
  final String folderName;

  Folders({
    required this.folderId,
    required this.folderName
  });

  factory Folders.fromJson(Map<String, dynamic> json){
    return Folders(folderId: json["folder_id"], folderName: json["folder_name"]);
  }

}
