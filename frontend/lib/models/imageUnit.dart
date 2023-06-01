class ImageUnit{
  final String imgUrl;
  final String audioUrl;

  ImageUnit({required this.imgUrl, required this.audioUrl});

  factory ImageUnit.fromJson(Map<String, dynamic> json) => ImageUnit(
      imgUrl: json["img_url"], audioUrl: json["audio_url"]);
}