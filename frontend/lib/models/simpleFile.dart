class SimpleFile {
  final int fileId;
  final String fileName;
  final String fileImg;

  SimpleFile({
    required this.fileId,
    required this.fileName,
    required this.fileImg
  });

  factory SimpleFile.fromJson(Map<String, dynamic> json){
    return SimpleFile(
        fileId: json["file_id"],
        fileName: json["file_name"],
        fileImg: json["file_img"]);
  }
}