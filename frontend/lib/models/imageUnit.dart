class ImageUnit{
  final String imgUrl;

  ImageUnit({required this.imgUrl});

  factory ImageUnit.fromJson(Map<String, dynamic> json) => ImageUnit(
      imgUrl: json["img_url"]);
}