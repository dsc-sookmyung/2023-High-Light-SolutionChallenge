import 'package:extended_image/extended_image.dart';
import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'dart:convert';

import 'package:just_audio/just_audio.dart';
import 'package:leturn/const/colors.dart';
import 'package:leturn/models/imageUnit.dart';
import 'package:leturn/models/textUnit.dart';
import 'package:leturn/views/home_screen.dart';
import 'package:leturn/views/pages/image_view.dart';

class ViewPage extends StatefulWidget {
  final int fileId;
  final int pageId;
  final AudioPlayer player;
  final fontBase;
  final onScaleUpdate;
  final isPlayingTrue;

  const ViewPage({Key? key, required this.fileId, required this.pageId, required this.player,
  required this.fontBase, required this.onScaleUpdate, required this.isPlayingTrue}) : super(key: key);

  @override
  _ViewPageState createState() => _ViewPageState();
}

class _ViewPageState extends State<ViewPage>
    with AutomaticKeepAliveClientMixin {
  @override
  bool get wantKeepAlive => true; // 탭 이동해도 다시 로딩X


  late Future<UnitList> unitList;
  late List<TextUnit> _allTexts;
  late List<ImageUnit> _allImages;

  final List<String> _audioUrls = [];

  Future<UnitList> getList() async {
    final response = await dio.get('/files/${widget.fileId}/page/${widget.pageId}');

    if(response.statusCode == 200) {
      var data = jsonDecode(response.data)["data"];
      final unit = UnitList.fromJson(data);
      //print("data>>> $data");

      _allTexts = unit.textList ?? <TextUnit>[];
      _allImages = unit.imgList ?? <ImageUnit>[];
      _audioUrls.addAll(_allTexts.map((e) => e.audioUrl));

      return unit;
    }else{

      print("page_view>>> error StatusCode : ${response.statusCode}");
      throw Exception('페이지 로드에 실패했습니다.');
    }
  }

  Future<void> initAudioPlayer() async {

    await widget.player.setAudioSource(
      ConcatenatingAudioSource(
          children: _audioUrls
              .map((url) => AudioSource.uri(Uri.parse(url)))
              .toList()),
      initialIndex: 0,
      initialPosition: Duration.zero,
    );
  }


  @override
  void initState() {
    super.initState();
    unitList = getList();

  }

  @override
  void dispose() {
    widget.player.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            children: [
              //_FixedTop(),
              Expanded(
                child: GestureDetector(
                  onScaleUpdate: (details) => widget.onScaleUpdate,
                  child: Container(
                      height: double.infinity,
                      color: Colors.white,
                      padding:
                          EdgeInsets.only(left: 30.w, top: 10.w, right: 10.w),
                      child: FutureBuilder(
                          future: unitList,
                          builder: (BuildContext ctx, snapshot) {
                            if (snapshot.hasData) {
                              if (_allImages.isEmpty) {
                                return textListView(_allTexts, widget.fontBase, snapshot.data!.imgExist);
                              } else {
                                return Stack(
                                  children:
                                  [
                                    textListView(_allTexts, widget.fontBase, snapshot.data!.imgExist),
                                    Positioned(bottom: 0, left: 0, right: 0, height: 120.h,
                                      child: imgWidget(_allImages)),
                                  ],
                                );}
                            } else if (snapshot.hasError){
                              return Text("snapshot error>>> ${snapshot.error}",);
                            } else{
                              return const Center(child: CircularProgressIndicator(color: MAIN_YELLOW,strokeWidth: 5,));
                            }
                          })),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget textBlock(List<TextUnit> _allTexts, num fontBase, int idx) {
    return Material(
      color: Colors.transparent,
      child: InkWell(
        highlightColor: Colors.amberAccent,
        splashColor: Colors.amberAccent,
        onTap: () async {
          widget.isPlayingTrue();
          await widget.player.setUrl(_allTexts[idx].audioUrl);
          await widget.player.play();
          //widget.isPlayingTrue();
        },
        child: Container(
          //color: Colors.orange,
          child: Text(
            _allTexts[idx].textLine,
            style: TextStyle(
                fontSize: _allTexts[idx].fontSize.toDouble() + fontBase),
          ),
        ),
      ),
    );
  }

  Widget textListView(List<TextUnit> _allTexts, num fontBase, bool spacer) {
    return Container(
      //height: double.infinity,
      child: ListView.builder(
          itemCount: _allTexts.length,
          itemBuilder: (ctx, int idx) {
            if ((idx == _allTexts.length - 1) && spacer) {
              //print(spacer);
              return Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  textBlock(_allTexts, fontBase, idx),
                  Container(
                    //color:Colors.amber,
                    height: 110.h,
                    width: 200.w,
                  ),
                ],
              );
            }
            return textBlock(_allTexts, fontBase, idx);
          }),
    );
  }

  Widget imgWidget(List<ImageUnit>? allImages) {
    return Container(
      decoration: BoxDecoration(
        borderRadius: BorderRadius.only(
            topLeft: Radius.circular(30.w), topRight: Radius.circular(30.w)),
        color: Color(0x4d666666),
      ),
      child: ListView.builder(
          scrollDirection: Axis.horizontal,
          itemCount: allImages!.length,
          itemBuilder: (ctx, int idx) {
            return GestureDetector(
              onTap: (){
                Navigator.push(context, MaterialPageRoute(
                    builder: (context) => ImageView(url: allImages![idx].imgUrl)
                  ),
                );
              },
              child: Container(
                  margin: EdgeInsets.fromLTRB(20.w, 10.h, 30.w, 10.h),
                  child: ExtendedImage.network(
                    allImages![idx].imgUrl,
                    width: 100.w,
                    height: 100.h,
                    fit: BoxFit.fill,
                  )),
            );
          }),
    );
  }
}

class UnitList {
  final List<TextUnit> textList;
  List<ImageUnit>? imgList;
  final bool imgExist;

  UnitList({required this.textList, this.imgList, required this.imgExist});

  factory UnitList.fromJson(Map<String, dynamic> json) {
    List<dynamic> jsonResponse = json["text"];
    List<dynamic> jsonResponse2 = json["image"];

    List<TextUnit> textList = <TextUnit>[];
    textList = jsonResponse.map((t) => TextUnit.fromJson(t)).toList();

    if (jsonResponse2.isNotEmpty) {
      List<ImageUnit> imgList = <ImageUnit>[];
      imgList = jsonResponse2.map((e) => ImageUnit.fromJson(e)).toList();
      return UnitList(textList: textList, imgList: imgList, imgExist: true);
    }

    return UnitList(textList: textList, imgExist: false);
  }
}
