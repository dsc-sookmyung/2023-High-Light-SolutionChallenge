class TextUnit {
  late final int idx;
  late final int fontSize;
  late final String text;

  TextUnit({
    required this.idx,
    required this.fontSize,
    required this.text
  });

  factory TextUnit.fromJson(Map<dynamic, dynamic> json){
    return TextUnit(
        idx: json['idx'],
        fontSize: json['font_size'],
        text: json['text']);
  }
}