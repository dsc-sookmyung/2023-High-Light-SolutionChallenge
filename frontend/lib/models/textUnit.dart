class TextUnit {
  late final String audioUrl;
  late final int fontSize;
  late final String textLine;

  TextUnit({
    required this.audioUrl,
    required this.fontSize,
    required this.textLine
  });

  factory TextUnit.fromJson(Map<dynamic, dynamic> json){
    //logger.e("TextUnit>>> ${json["text"]}");
    //logger.e("TextUnit>>> ${json["idx"]}");
    return TextUnit(
        audioUrl: json["audio_url"],
        fontSize: json["font_size"],
        textLine: json["text_content"]);
  }
}