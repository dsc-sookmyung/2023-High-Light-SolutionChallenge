class ImageUnit{
  final String imgUrl;
  final imgAudioUrl;

  ImageUnit({
    required this.imgUrl,
    required this.imgAudioUrl});

  factory ImageUnit.fromJson(Map<String, dynamic> json) => ImageUnit(
      imgUrl: json["img_url"],
      imgAudioUrl: json["img_text"]);
}